<script setup>
import {reactive, ref, getCurrentInstance} from "vue";
import {validateEmail, validatePassword, validateUsername} from "@/utils/common.js";
import {createUser} from "@/api/user.js";

const { proxy } = getCurrentInstance();

const props = defineProps({
  success: {
    type: Function
  }
});

const form = reactive({
  username: '',
  email: '',
  password: ''
});

const is_loading = ref(false);
const error_msg = ref('');

const create = () => {
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
  createUser(form).then(() => {
    // 通知调用组件
    callParent();
    proxy.$toast.success('添加用户成功');
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

const callParent = () => {
  if (props.success) {
    props.success();
  }
}
</script>

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
  <div class="weui-form">
    <div class="weui-form__bd">
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
           @click="create"
           :class="{'weui-btn_primary': !is_loading, 'weui-btn_default': is_loading, 'weui-btn_loading': is_loading}">
          <i v-if="is_loading" class="weui-mask-loading"></i>
          添加用户
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">

</style>