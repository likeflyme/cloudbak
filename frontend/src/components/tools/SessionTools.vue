<script setup>
import {ref} from "@vue/reactivity";
import {useStore} from "vuex";
import Tasks from "./tabs/Tasks.vue";
import Info from "./tabs/Info.vue";
import SessionConfig from "./tabs/SessionConfig.vue";
import UserConfig from "./tabs/UserConfig.vue";
import UpdatePassword from "./tabs/UpdatePassword.vue";
import DeleteSession from "./tabs/DeleteSession.vue";

const store = useStore();

const activeMenu = ref('info');


const menus = [
  {
    name: 'info',
    title: '会话信息',
    component: Info,
  },
  {
    name: 'sessionConfig',
    title: '会话配置',
    component: SessionConfig
  },
  {
    name: 'tasks',
    title: '解析任务',
    component: Tasks
  },
  {
    name: 'deleteSession',
    title: '删除会话',
    component: DeleteSession
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
            :class="{'menu-item-active': activeMenu === m.name}"
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