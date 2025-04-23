<script setup>
import {saveLicense} from "@/api/sys.js";
import {ref, getCurrentInstance} from "vue";
import {useStore} from "vuex";

const store = useStore();
const licenseText = ref('');
const loading = ref(false)
const {proxy} = getCurrentInstance();
const props = defineProps({
  success: {
    type: Function,
    default: undefined
  }
});

const saveLicenseCode = () => {
  if (licenseText.value === '') {
    proxy.$toast.warn('请输入授权码');
    return;
  }
  loading.value = true;
  saveLicense(licenseText.value).then(resp => {
    resp.license = licenseText.value;
    store.commit('setLicense', resp);
    proxy.$toast.success('授权成功');
  }).catch(e => {
    if (e.response.data) {
      proxy.$toast.warn(e.response.data.detail);
    } else {
      proxy.$toast.warn(e.message);
    }
  }).finally(() => {
    loading.value = false;
  });
}
</script>

<template>
<div>
  <div class="weui-form">
    <div class="weui-form__bd">
      <div class="weui-form__control-area">
        <div class="weui-cells__group weui-cells__group_form">
          <div class="weui-cells__title">填写授权码，没有授权码？<a class="but-btn" href="https://www.cloudbak.org/buy/pro.html" target="_blank">点击够买</a></div>
          <div class="weui-cells weui-cells_form">
            <div class="weui-cell weui-cell_active">
              <div class="weui-cell__bd">
                <textarea class="weui-textarea" placeholder="请输入授权码" rows="3" v-model="licenseText"></textarea>
                <div role="option" aria-live="polite" class="weui-textarea-counter"><span>0</span>/200</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="weui-form__ft">
      <div class="weui-form__opr-area">
        <a role="button" class="weui-btn weui-btn_primary" href="javascript:" id="showTooltips" @click="saveLicenseCode">保存授权码</a>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped lang="less">
.weui-form {
  padding: 0;
}
.weui-form__opr-area {
  margin-bottom: 0;
}
.but-btn {
  color: #2aae67;
  cursor: pointer;
}
</style>