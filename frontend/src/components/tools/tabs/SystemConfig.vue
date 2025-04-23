<script setup>
import {getCurrentInstance, reactive, ref, toRaw} from "vue";
import {updateConf, sysConf} from "@/api/conf.js";
import {useStore} from "vuex";

const store = useStore();
const { proxy } = getCurrentInstance();
const loading = ref(false);
const error = ref('');

const form = reactive({});


const loadConf = () => {
  sysConf().then(resp => {
    form.value = resp;
    store.commit('setSysConf', resp);
  });
}

loadConf();

const setError = (err) => {
  error.value = err;
}

const validForm = () => {
  let count = form.value.auth.login_error_count_day
  if (count === '' || count === null || count === undefined) {
    setError('请输入错误次数');
    return false;
  }
  if (form.value.auth.login_error_count_day < 1) {
    setError('错误次数必须大于0');
    return false;
  }
  return true;
}

const save = () => {
  setError('');
  if (validForm()) {
    loading.value = true;
    updateConf("sys_conf", JSON.stringify(toRaw(form.value))).then(resp => {
      // 修改store中的数据
      store.commit('setSysConf', form.value);
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
</script>

<template>
  <div class="s-page" v-if="form.value">
    <div class="page-body">
      <div class="conf-group">
        <div class="conf-title">登录安全</div>
        <div class="conf-row">
          <div class="conf-label">24小时错误次数限制：</div>
          <div class="conf-right">
            <input class="weui-input" type="number" placeholder="错误次数" v-model="form.value.auth.login_error_count_day" />
          </div>
        </div>
      </div>
      <div class="conf-group">
        <div class="conf-title">图片代理</div>
        <div class="conf-row">
          <div class="conf-label">微信图片代理：</div>
          <div class="conf-right">
            <input aria-labelledby="cb_txt" class="weui-switch" type="checkbox" v-model="form.value.picture.use_proxy"/>
          </div>
        </div>
      </div>
    </div>
    <div class="page-footer">
      <div class="error">
        {{ error }}
      </div>
      <a href="javascript:" role="button" class="weui-btn weui-btn_mini weui-btn_primary weui-wa-hotarea weui-btn_loading" @click="save" >
        <i v-if="loading" class="weui-mask-loading weui-mask-loading_only"></i>
        保存
      </a>
    </div>
  </div>

</template>

<style scoped lang="less">
@import "/src/style/components/tools/tab.less";
</style>