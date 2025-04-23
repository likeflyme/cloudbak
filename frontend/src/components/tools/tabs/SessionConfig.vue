<script setup>
import {useStore} from "vuex";
import {getCurrentInstance, reactive, ref, toRaw} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {updateConf, sessionConf} from "@/api/conf.js";
import {isValidCron} from "cron-validator";

const { proxy } = getCurrentInstance();
const loading = ref(false);
const error = ref('');

const form = reactive({});

const loadConf = () => {
  sessionConf().then(resp => {
    form.value = resp;
  });
}

loadConf();

const setError = (err) => {
  error.value = err;
}

const validForm = () => {
  if (form.value.analyze.analyze_open) {
    if (!isValidCron(form.value.analyze.analyze_cron)) {
      setError('cron 表达式错误');
      return false;
    }
  }
  return true;
}

const save = () => {
  setError('');
  if (validForm()) {
    loading.value = true;
    updateConf("session_conf", JSON.stringify(toRaw(form.value))).then(resp => {
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
        <div class="conf-title">定时解析
          <a class="conf-title-help" title="帮助文档" href="https://www.cloudbak.org/advanced/timing-analysis.html" target="_blank">
            <font-awesome-icon :icon="['fas', 'fa-arrow-up-right-from-square']" />
          </a>
        </div>
        <div class="conf-row">
          <input aria-labelledby="cb_txt" class="weui-switch" type="checkbox" v-model="form.value.analyze.analyze_open"/>
        </div>
        <div class="conf-row" v-if="form.value.analyze.analyze_open">
          <div class="conf-label" style="width: 100px;">cron 表达式：</div>
          <div class="conf-right">
            <input class="weui-input" type="text" placeholder="请输入 cron 表达式" v-model="form.value.analyze.analyze_cron" />
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