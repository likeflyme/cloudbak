<script setup>
import {getCurrentInstance, ref} from "vue";
import {useStore} from "vuex";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import SysInfoLicense from "./SysInfoLicense.vue";
import SysInfoLicenseShow from "./SysInfoLicenseShow.vue";

const store = useStore();
const loading = ref(false);

const { proxy } = getCurrentInstance();

const writeSuccess = () => {
  console.log("写入成功");
}

const openWriteLicense = () => {
  proxy.$popup.open(SysInfoLicense,{success: writeSuccess},{ title: '填写授权码', width: '400px', height: '400px' });
}

const showLicense = (license) => {
  proxy.$popup.open(SysInfoLicenseShow,{license: license},{ title: '授权码', width: '400px', height: '400px' });
}
</script>

<template>
  <div class="s-page">
    <div class="page-body">
      <div class="conf-group">
        <div class="conf-title">系统信息</div>
        <div class="conf-row">
          <div class="conf-label">系统版本</div>
          <div class="conf-right">
            <p>{{store.getters.getSysInfo?.sys_version}}</p>
          </div>
        </div>
        <div class="conf-row">
          <div class="conf-label">系统唯一标识</div>
          <div class="conf-right">
            {{ store.getters.getSysInfo.client_id }}
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped lang="less">
@import "/src/style/components/tools/tab.less";

.sys-info-write-license {
  color: #418fde;
  cursor: pointer;
}
.show-license {
  color: #418fde;
  cursor: pointer;
}
</style>