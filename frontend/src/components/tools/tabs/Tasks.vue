<script setup>

import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {ref} from "@vue/reactivity";
import {taskList, singleDecrypt} from "@/api/task.js"
import {reactive, getCurrentInstance} from "vue";
import {TaskState} from "@/enums/TaskState.js";
import {formatFilterMsgDate} from "@/utils/common.js";
import {useStore} from "vuex";

const { proxy } = getCurrentInstance();
const store = useStore();
const page = ref(1);
const size = ref(30);
const tasks = reactive([]);
const noMoreMsg = ref(false);
const isLoading = ref(false);
const taskContent = ref();
const dialogConfirm = ref(false);
const dialogShow = ref(false);

const formatTimestamp = (timestamp) => {
  if (timestamp < 60) {
    // 小于 60 秒，保留两位小数
    return `${timestamp.toFixed(2)} 秒`;
  } else if (timestamp < 3600) {
    // 小于 1 小时，返回 xx 分 xx.xx 秒
    const minutes = Math.floor(timestamp / 60);
    const seconds = (timestamp % 60).toFixed(2);
    return `${minutes} 分 ${seconds} 秒`;
  } else if (timestamp < 86400) {
    // 小于 1 天，返回 xx 小时 xx 分 xx.xx 秒
    const hours = Math.floor(timestamp / 3600);
    const minutes = Math.floor((timestamp % 3600) / 60);
    const seconds = (timestamp % 60).toFixed(2);
    return `${hours} 小时 ${minutes} 分 ${seconds} 秒`;
  } else {
    // 大于等于 1 天
    return "大于1天";
  }
}


const loadTasks = () => {
  if (!noMoreMsg.value) {
    taskList(page.value, size.value).then(data => {
      if (data.length < size.value) {
        noMoreMsg.value = true;
      }
      tasks.push(...data);
      page.value = page.value + 1;
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
    });
  }
}

const refreshTasks = () => {
  tasks.length = 0;
  page.value = 1;
  noMoreMsg.value = false;
  loadTasks();
}

// 滚动
const onWheel = (event) => {
  const scrollTop = taskContent.value.scrollTop;
  const clientHeight = taskContent.value.clientHeight;
  const scrollHeight = taskContent.value.scrollHeight;
  if (scrollTop + clientHeight === scrollHeight) {
    loadTasks();
  }
};

const exeAnalyze = (deep = false) => {
  proxy.$dialog.open({
    title: '创建数据解析任务',
    desc: `确定要创建数据解析任务吗？系统将重新解析当前会话的数据库文件，这需要些时间。尽量不要在这期间查询该会话数据，避免造成库文件写入失败。`,
    onConfirmed: () => {
      singleDecrypt(store.getters.getCurrentSessionId, deep).then((data) => {
        proxy.$toast.success('创建任务成功');
        // 刷新数据
        refreshTasks();
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
      });
    },
    onCancelled: () => {}
  });
}

const openLog = (taskId) => {
  window.open("/api/task/log?task_id=" + taskId);
}

loadTasks()
</script>

<template>
<div class="tasks" ref="taskContent" @wheel="onWheel">
  <div class="task-tools">
    <a class="sys-btn" @click="exeAnalyze(false)">执行数据解析任务</a>
    <a class="sys-btn" @click="exeAnalyze(true)">全量解析</a>
    <font-awesome-icon class="sys-btn" :icon="['fas', 'rotate-right']" title="刷新" @click="refreshTasks"/>
  </div>
  <ul class="tasks-ul">
    <li class="tasks-li" v-for="t in tasks">
      <p class="tb-base tb-text">{{ t.name }}</p>
      <p class="tb-base tb-time">{{ formatFilterMsgDate(t.create_time) }}</p>
      <p class="tb-base tb-grow"></p>
      <p class="tb-base tb-time">执行：{{ formatTimestamp(t.update_time - t.create_time) }}</p>
      <p class="tb-base tb-text"
         :class="{
              'tb-success': t.state === TaskState.SUCCESS.value,
              'tb-failed': t.state === TaskState.FAILED.value
            }">{{ TaskState[t.state].desc }}</p>
      <p class="tb-base tb-checkout">
        <font-awesome-icon v-if="t.detail" :icon="['fas', 'eye']" title="查看日志" @click="openLog(t.id)"/>
      </p>
    </li>
  </ul>
  <div class="load-more">
    <a v-if="!noMoreMsg" href="javascript:void(0)" @click="loadTasks">
      <font-awesome-icon class="loading-icon" v-if="isLoading" :icon="['fas', 'spinner']"/>
      <p v-else>查看更多任务</p>
    </a>
  </div>
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