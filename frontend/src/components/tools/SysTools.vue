<script setup>
import {ref} from "@vue/reactivity";
import {useStore} from "vuex";
import Tasks from "./tabs/Tasks.vue";
import UserConfig from "./tabs/UserConfig.vue";
import UpdatePassword from "./tabs/UpdatePassword.vue";
import SystemConfig from "./tabs/SystemConfig.vue";
import UserManage from "./tabs/UserManage.vue";
import SystemInfo from "./tabs/SystemInfo.vue";

const store = useStore();

const activeMenu = ref('systemConfig');


const menus = [
  {
    name: 'systemConfig',
    title: '系统设置',
    admin: true,
    component: SystemConfig
  },
  {
    name: 'updatePassword',
    title: '修改密码',
    admin: false,
    component: UpdatePassword
  },
  {
    name: 'systemInfo',
    title: '系统信息',
    admin: true,
    component: SystemInfo
  }
]

const getCurrentComponent = () => {
  const menuItem = menus.find(m => m.name === activeMenu.value);
  return menuItem ? menuItem.component : null;
};

</script>

<template>
<div class="sys-tools">
  <div class="tools-body">
    <div class="tools-menu">
      <ul class="menu-ul">
        <li v-for="m in menus"
            class="menu-item"
            :class="{'menu-item-active': activeMenu === m.name, 'menu-item-hidden': m.admin && !store.getters.isAdmin}"
            @click="activeMenu = m.name">{{ m.title }}</li>
      </ul>
    </div>
    <div class="tools-content">
      <component :is="getCurrentComponent()" :key="activeMenu"/>
    </div>
  </div>
</div>

</template>

<style scoped lang="less">
@import "/src/style/components/tools/tools.less";
</style>