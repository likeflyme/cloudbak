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
          <h2 class="weui-form__title">云朵备份 - 安装</h2>
        </div>
        <div class="weui-form__control-area">
          <div class="weui-cells__group weui-cells__group_form">
            <!--            <div class="weui-cells__title">表单组标题</div>-->
            <div class="weui-cells">
              <label for="js_input1" class="weui-cell weui-cell_active">
                <div class="weui-cell__hd"><span class="weui-label">用户名</span></div>
                <div class="weui-cell__bd">
                  <input id="js_input1" class="weui-input" v-model="form.username" placeholder="数字字母下划线"/>
                </div>
              </label>
              <label for="js_input1" class="weui-cell weui-cell_active">
                <div class="weui-cell__hd"><span class="weui-label">邮箱</span></div>
                <div class="weui-cell__bd">
                  <input id="js_input1" class="weui-input" v-model="form.email" placeholder="邮箱"/>
                </div>
              </label>
              <label for="js_input2" class="weui-cell weui-cell_active">
                <div class="weui-cell__hd"><span class="weui-label">密码</span></div>
                <div class="weui-cell__bd">
                  <input id="js_input2" class="weui-input" type="password" v-model="form.password" placeholder="密码"/>
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
             @click="start">
            <i v-if="is_loading" class="weui-mask-loading"></i>
            {{ start_btn_title }}
          </a>
        </div>
        <div class="weui-form__extra-area">
          <div class="weui-footer">
            <p class="weui-footer__links">
              <a href="javascript:" class="weui-footer__link">云朵备份</a>
            </p>
            <p class="weui-footer__text">Copyright © 2024-2025 cloudbak.io</p>
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
import {ref, reactive, toRaw} from 'vue';
import router from "../router/index.js";
import {createUser} from "../api/user.js";
import {validateEmail, validatePassword, validateUsername} from "../utils/common.js";

const error_msg = ref('');
const is_loading = ref(false);
const start_btn_title = ref('开 始');
const form = reactive({
  username: '',
  password: '',
  email: ''
});

const start = () => {
  if (!form.username) {
    openError('必须输入用户名');
    return;
  }
  if (!validateUsername(form.username)) {
    openError('用户名必须为数字字母下划线');
    return;
  }
  if (!form.password) {
    openError('必须输入密码');
    return;
  }
  if (!validatePassword(form.password)) {
    openError('密码至少6位，且必须包含字母数字特殊字符中的至少两种');
    return;
  }
  if (!form.email) {
    openError('必须输入email');
    return;
  }
  if (!validateEmail(form.email)) {
    openError('无效的邮箱');
    return;
  }
  let jsonString = JSON.stringify(toRaw(form));
  createUser(jsonString).then(() => {
    router.push('/login')
  }).catch(e => {
    if (e.response.data) {
      openError(e.response.data.detail);
    } else {
      openError(e.message);
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
  max-width: 500px;
  margin: 100px auto;
}
</style>