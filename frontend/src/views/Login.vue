<template>
  <div role="alert" class="weui-information-bar weui-information-bar_warn-weak" v-if="error_msg">
    <div class="weui-information-bar__hd">
      <i class="weui-icon-outlined-warn"></i>
    </div>
    <div class="weui-information-bar__bd">
      {{ error_msg }}
    </div>
    <div class="weui-information-bar__ft">
      <button class="weui-btn_icon" @click="closeError">关闭<i class="weui-icon-close-thin"></i></button>
    </div>
  </div>
  <div class="page">
    <div class="weui-form">
      <div class="weui-form__bd">
        <div class="weui-form__text-area">
          <h2 class="weui-form__title">云朵备份 - 登录</h2>
<!--          <div class="weui-form__desc">展示表单页面的信息结构样式,-->
<!--            分别由头部区域/控件区域/提示区域/操作区域和底部信息区域组成。-->
<!--          </div>-->
        </div>
        <div class="weui-form__control-area">
          <div class="weui-cells__group weui-cells__group_form">
<!--            <div class="weui-cells__title">表单组标题</div>-->
            <div class="weui-cells">
              <label for="js_input1" class="weui-cell weui-cell_active">
                <div class="weui-cell__hd"><span class="weui-label">账号</span></div>
                <div class="weui-cell__bd">
                  <input id="js_input1" class="weui-input" v-model="form.username" placeholder="用户名或邮箱"/>
                </div>
              </label>
              <label for="js_input2" class="weui-cell weui-cell_active">
                <div class="weui-cell__hd"><span class="weui-label">密码</span></div>
                <div class="weui-cell__bd">
                  <input id="js_input2" class="weui-input" type="password" v-model="form.password" @keydown.enter="login" placeholder="填写密码"/>
                </div>
              </label>
              <label for="js_input2" class="weui-cell weui-cell_active" v-if="open_two_step_auth">
                <div class="weui-cell__hd"><span class="weui-label">验证码</span></div>
                <div class="weui-cell__bd">
                  <input id="js_input2" class="weui-input" v-model="form.captcha" @keydown.enter="login" placeholder="填写验证码"/>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>
      <div class="weui-form__ft">
        <div class="weui-form__opr-area">
          <a href="javascript:"
             role="button"
             class="weui-btn"
             :class="{'weui-btn_primary': !is_loading, 'weui-btn_default': is_loading, 'weui-btn_loading': is_loading}"
             @click="login">
            <i v-if="is_loading" class="weui-mask-loading"></i>
            {{ login_btn_title }}
          </a>
        </div>
<!--        <div class="weui-form__tips-area">-->
<!--          <p class="weui-form__tips">-->
<!--            表单页提示，居中对齐-->
<!--          </p>-->
<!--        </div>-->
        <div class="weui-form__extra-area">
          <div class="weui-footer">
            <p class="weui-footer__links">
              <a href="javascript:" class="weui-footer__link">云朵备份</a>
            </p>
            <p class="weui-footer__text">Copyright © 2024-2025 cloudbak.org</p>
          </div>
        </div>
      </div>
    </div>
    <div role="alert" id="js_toast" style="display: none;">
      <div class="weui-mask_transparent"></div>
      <div class="weui-toast">
        <i class="weui-icon-success-no-circle weui-icon_toast"></i>
        <p class="weui-toast__content">已完成</p>
      </div>
    </div>
  </div>

</template>

<script setup>
import {ref, reactive} from 'vue';
import {token} from "../api/auth.js";
import {loginSuccess, isLogin} from '../utils/common';
import router from "../router/index.js";
import {checkInstall} from "../api/user.js";

const error_msg = ref('');
const is_loading = ref(false);
const login_btn_title = ref('登 录');
const open_two_step_auth = ref(false);
const form = reactive({
  username: '',
  password: '',
  captcha: ''
});

checkInstall().then(response => {
  if (response.count === 0) {
    router.push("/install")
  }
});

const login = () => {
  // openError("登录失败");
  if (!form.username) {
    openError('必须输入登录用户名或邮箱');
    return;
  }
  if (!form.password) {
    openError('必须输入登录密码');
    return;
  }
  let formData = new FormData();
  formData.append('username', form.username);
  formData.append('password', form.password);
  formData.append('captcha', form.captcha);

  token(formData).then((resp) => {
    console.log(resp);
    loginSuccess(resp);
    router.push('/')
  }).catch(e => {
    if (e.response.status === 461 && open_two_step_auth.value === false) {
      open_two_step_auth.value = true;
    } else {
      if (e.response.data) {
        openError(e.response.data.detail);
      } else {
        openError(e.message);
      }
    }
  });
};

const openError = (msg) => {
  error_msg.value = msg;
}

const closeError = () => {
  error_msg.value = '';
}

</script>

<style scoped lang="less">

.weui-form__bd {
  max-width: 35.714rem;
  margin: 7.14rem auto;
}
</style>