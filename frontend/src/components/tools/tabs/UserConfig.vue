<script setup>
import {getCurrentInstance, reactive, ref, toRaw} from "vue";
import {updateConf, userConf} from "@/api/conf.js";
import {getTwoStepQrcode} from "@/api/auth.js";
import QRCode from 'qrcode'

const { proxy } = getCurrentInstance();
const loading = ref(false);
const error = ref('');

const form = reactive({});

const qrcodeImageUrl = ref('');

const loadConf = () => {
  userConf().then(resp => {
    form.value = resp;
  });
}

loadConf();

const setError = (err) => {
  error.value = err;
}

const validForm = () => {
  return true;
}

const save = () => {
  setError('');
  if (validForm()) {
    loading.value = true;
    updateConf("user_conf", JSON.stringify(toRaw(form.value))).then(resp => {
      proxy.$toast.success('修改配置成功');
    }).catch(e => {
      if (e.response.data) {
        setError(e.response.data.detail);
      } else {
        setError(e.message);
      }
    }).finally(() => {
      loading.value = false;
    });
  }

}

const loadQrcodeUri = () => {
  getTwoStepQrcode().then(resp => {
    QRCode.toDataURL(resp.qr_code_uri)
        .then(url => {
          qrcodeImageUrl.value = url;
        })
        .catch(err => {
          setError(err);
        })
  }).catch(e => {
    if (e.response.data) {
      setError(e.response.data.detail);
    } else {
      setError(e.message);
    }
  });
}
</script>

<template>
  <div class="s-page" v-if="form.value">
    <div class="page-body">
      <div class="conf-group">
        <div class="conf-title">两步验证</div>
        <div class="conf-row">
          <div class="conf-label">开启两步验证</div>
          <div class="conf-right">
            <input aria-labelledby="cb_txt" class="weui-switch" type="checkbox" v-model="form.value.two_step_auth.two_step_auth_open"/>
          </div>
        </div>
        <div class="conf-row">
          <div class="conf-label">获取两步验证二维码</div>
          <div class="conf-right">
            <a class="weui-btn weui-btn_mini weui-btn_primary weui-wa-hotarea weui-btn_loading"
               @click="loadQrcodeUri">
              获取</a>
          </div>
        </div>
        <div class="conf-row" v-if="qrcodeImageUrl">
          <img alt="qrcode" :src="qrcodeImageUrl"/>
        </div>
      </div>
    </div>
    <div class="page-footer">
      <div class="error">
        {{ error }}
      </div>
      <a href="javascript:" role="button" class="weui-btn weui-btn_medium weui-btn_primary weui-wa-hotarea weui-btn_loading" @click="save" >
        <i v-if="loading" class="weui-mask-loading weui-mask-loading_only"></i>
        保存
      </a>
    </div>
  </div>

</template>

<style scoped lang="less">
@import "/src/style/components/tools/tab.less";
</style>