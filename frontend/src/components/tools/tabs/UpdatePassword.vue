<script setup>
import {getCurrentInstance} from "vue";
import {updatePassword} from "@/api/user";

import {reactive, ref} from "vue";

const {proxy} = getCurrentInstance();

const loading = ref(false);

const form = reactive({
  old_password: '',
  new_password: '',
  new_password2: ''
});
const error = ref('');

const validForm = () => {
  if (form.old_password === '') {
    setError('请输入修改前密码');
    return false;
  }
  if (form.new_password === '') {
    setError('请输入新密码');
    return false;
  }
  if (form.new_password2 === '') {
    setError('请重复新密码');
    return false;
  }
  if (form.new_password !== form.new_password2) {
    setError('两次输入的新密码不一致');
    return false;
  }
  if (form.new_password === form.old_password) {
    setError('新密码不能和旧密码相同');
    return false;
  }
  return true;
}

const save = () => {
  if (!validForm()) {
    return;
  }
  loading.value = true;
  updatePassword(form).then(resp => {
    proxy.$toast.success('修改密码成功');
  }).catch(e => {
    setError(e.response.data.detail);
  }).finally(() => {
    loading.value = false;
  });
}

const setError = (err) => {
  error.value = err;
}

</script>

<template>
  <div class="s-page">
    <div class="page-body">
      <div class="conf-group">
        <div class="conf-row">
          <div class="conf-label">修改前密码：</div>
          <div class="conf-right">
            <input class="weui-input" type="password" placeholder="" v-model="form.old_password"/>
          </div>
        </div>
        <div class="conf-row">
          <div class="conf-label">新密码：</div>
          <div class="conf-right">
            <input class="weui-input" type="password" placeholder="" v-model="form.new_password"/>
          </div>
        </div>
        <div class="conf-row">
          <div class="conf-label">重复新密码：</div>
          <div class="conf-right">
            <input class="weui-input" type="password" placeholder="" v-model="form.new_password2"/>
          </div>
        </div>
        <div class="conf-row">
          注意：请使用复杂的密码策略，以保证账户安全。
        </div>
      </div>
    </div>
    <div class="page-footer">
      <div class="error">
        {{ error }}
      </div>
      <a href="javascript:"
         role="button"
         class="weui-btn weui-btn_mini weui-btn_primary weui-wa-hotarea weui-btn_loading"
         @click="save">
        <i v-if="loading" class="weui-mask-loading weui-mask-loading_only"></i>
        保存
      </a>
    </div>
  </div>

</template>

<style scoped lang="less">
@import "/src/style/components/tools/tab.less";
</style>