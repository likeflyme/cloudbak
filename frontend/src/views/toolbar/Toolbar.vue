<script setup>
import { getCurrentInstance} from "vue";
import {logout} from "@/utils/common.js";
import {useRouter} from "vue-router";
import SysTools from "@/components/tools/SysTools.vue";
import {useStore} from "vuex";

const store = useStore();
const router = useRouter();

const { proxy } = getCurrentInstance()

const clickLogout = () => {
  logout();
  store.commit('resetState');
  router.push("/login")
}

const openSysTools = () => {
  proxy.$popup.open(SysTools, undefined, { title: '设置', width: '650px', height: '700px' });
}
</script>

<template>
<div class="toolbar">
  <font-awesome-icon class="t-icon" :icon="['fas', 'gear']" title="系统设置" @click="openSysTools"/>
  <font-awesome-icon class="t-icon icon-sign-out" :icon="['fas', 'right-from-bracket']" title="登出" @click="clickLogout"/>
</div>
</template>

<style scoped lang="less">
.toolbar {
  position: absolute;
  width: 50px;
  right: 30px;
  top: 30px;
  display: flex;
  z-index: 6000;
  .t-icon {
    cursor: pointer;
    margin-left: 10px;
  }
  .icon-sign-out {
    color: #990C15
  }
}
</style>