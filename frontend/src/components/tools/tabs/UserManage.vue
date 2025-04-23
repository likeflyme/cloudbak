<script setup>

import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {ref} from "@vue/reactivity";
import {users as loadUsersRemote} from "@/api/user"
import {reactive, getCurrentInstance, toRaw} from "vue";
import {UserState} from "@/enums/TaskState.js";
import {formatUserCreateTime} from "@/utils/common.js";
import {useStore} from "vuex";
import UserCreate from "./UserCreate.vue";
import UserDetail from "./UserDetail.vue";

const { proxy } = getCurrentInstance();
const store = useStore();
const users = reactive([]);
const isLoading = ref(false);
const taskContent = ref();

const loadUsers = () => {
  isLoading.value = true;
  loadUsersRemote().then(data => {
    users.push(...data);
  }).catch(e => {
    if ("response" in e) {
      store.commit("showErrorToastMsg", {
        msg: e.response.data
      })
    } else {
      store.commit("showErrorToastMsg", {
        msg: e
      })
    }
  }).finally(() => {
    isLoading.value = false;
  });
}

const reloadUsers = () => {
  users.splice(0, users.length);
  loadUsers();
}
const openUserCreate = () => {
  proxy.$popup.open(UserCreate, {
    success: reloadUsers
  }, { title: '添加用户', width: '650px', height: '650px' });
}

const showDetail = (user) => {
  proxy.$popup.open(UserDetail,{user: user},{ title: '用户详情', width: '400px', height: '400px' });
}

const getUserState = (user) => {
  if (user.state !== undefined && user.state !== null && user.state !== '') {
    return user.state;
  } else {
    return 1;
  }
};

loadUsers();
</script>

<template>
  <div class="tasks" ref="taskContent">
    <div class="task-tools">
      <a class="sys-btn" @click="openUserCreate">添加用户</a>
    </div>
    <ul class="tasks-ul">
      <li class="tasks-li">
        <p class="tb-base tb-text">用户名</p>
        <p class="tb-base tb-text">昵称</p>
<!--        <p class="tb-base tb-text">邮箱</p>-->
        <p class="tb-base tb-text">创建时间</p>
        <p class="tb-base tb-grow"></p>
        <p class="tb-base tb-text">状态</p>
        <p class="tb-base"></p>
      </li>
      <li class="tasks-li" v-for="u in users">
        <p class="tb-base tb-text">{{ u.username }}</p>
        <p class="tb-base tb-text">{{ u.nickname }}</p>
<!--        <p class="tb-base tb-text">{{ u.email }}</p>-->
        <p class="tb-base tb-text">{{ formatUserCreateTime(u.create_time) }}</p>
        <p class="tb-base tb-grow"></p>
        <p class="tb-base tb-text">{{ UserState[getUserState(u)].desc }}</p>
        <p class="tb-base">
          <font-awesome-icon class="tb-btn" :icon="['fas', 'eye']" title="查看详情" @click="showDetail(u)"/>
        </p>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="less">
.sys-btn {
  color: #2C90FF;
  cursor: pointer;
}
.tasks {
  height: 100%;
  flex-grow: 1;
  padding: 0 10px;
  overflow-y: scroll;
  .task-tools {
    font-size: 12px;
    display: flex;
    //text-align: right;
    align-items: center;
    .sys-btn {
      margin-right: 10px;
    }
  }
  .tasks-ul {
    .tasks-li {
      font-size: 12px;
      display: flex;
      align-items: center;
      padding: 8px 10px;
      .tb-base {
        min-width: 60px;
        .tb-btn {
          cursor: pointer;
          margin-right: 5px;
        }
      }
      .tb-grow {
        flex-grow: 1;
      }
      .tb-time {
        font-size: 11px;
        color: #797979;
        padding: 0 10px;
      }
      .tb-success {
        color: #2ba245
      }
      .tb-failed {
        color: #ed1e45;
      }
      .tb-running {
        color: #797979;
      }
      .tb-checkout{
        padding-left: 5px;
        cursor: pointer;
        visibility: hidden;
      }
    }
    .tasks-li:hover {
      background-color: #ededed;
      .tb-checkout {
        visibility: visible;
      }
    }
  }
  .load-more {
    text-align: center;
    font-size: 12px;
    color: #2C90FF;
    .no-more-msg {
      font-size: 12px;
      color: dimgray;
    }
    .loading-icon {
      color: gray;
    }
  }
}
// 以下是滚动条样式
/* 隐藏默认的滚动条轨道和拇指 */
.tasks::-webkit-scrollbar {
  width: 6px; /* 隐藏滚动条 */
  background: transparent; /* 使滚动条轨道背景透明 */
}

/* 鼠标悬停时显示滚动条轨道 */
.tasks:hover::-webkit-scrollbar {
  width: 6px; /* 设置滚动条宽度 */
  background: #f0f0f0; /* 滚动条轨道背景颜色 */
}

/* 滚动条轨道样式 */
.tasks:hover::-webkit-scrollbar-track-piece {
  background: #f0f0f0; /* 设置滚动条轨道背景颜色 */
  border-radius: 8px; /* 设置滚动条轨道圆角 */
}

/* 滚动条拇指样式 */
.tasks:hover::-webkit-scrollbar-thumb {
  background-color: #c8c9cc; /* 设置滚动条拇指背景颜色 */
  border-radius: 8px; /* 设置滚动条拇指圆角 */
}

/* 鼠标悬停在滚动条拇指上时的样式 */
.tasks:hover::-webkit-scrollbar-thumb:hover {
  background-color: #b0b0b0; /* 鼠标悬停时滚动条拇指背景颜色 */
}
</style>