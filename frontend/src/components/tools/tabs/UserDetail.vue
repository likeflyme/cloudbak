<script setup>
import {formatUserCreateTime} from "@/utils/common.js";
import {UserState} from "@/enums/TaskState.js";
import {getCurrentInstance, ref} from "vue";
import {userBan, userActive} from "@/api/user.js";

const { proxy } = getCurrentInstance();

const props = defineProps({
  user: Object
});

const getUserState = (user) => {
  if (user.state !== undefined && user.state !== null && user.state !== '') {
    return user.state;
  } else {
    return 1;
  }
};

const userState = ref(1);

userState.value = getUserState(props.user);


const banUser = () => {
  userBan(props.user.id).then(resp => {
    proxy.$toast.success('禁用成功');
    props.user.state = 0;
    userState.value = 0;
  }).catch(e => {
    proxy.$toast.warn('禁用失败：' + e);
  })
}

const activeUser = () => {
  userActive(props.user.id).then(resp => {
    proxy.$toast.success('启用成功');
    props.user.state = 1;
    userState.value = 1;
  }).catch(e => {
    proxy.$toast.warn('启用失败：' + e);
  })
}


const banUserAsk = () => {
  proxy.$dialog.open({
    title: '禁用用户',
    desc: '确定禁用该用户吗？',
    onConfirmed: () => {
      banUser();
    },
    onCancelled: () => {
      console.log('用户取消禁用');
    }
  });
}

const activeUserAsk = () => {
  proxy.$dialog.open({
    title: '启用用户',
    desc: '确定启用该用户吗？',
    onConfirmed: () => {
      activeUser();
    },
    onCancelled: () => {
      console.log('用户取消启用');
    }
  });
}
</script>

<template>
  <div class="user-detail-container">
    <div class="user-detail-box">
      <p class="user-detail-box-item">用户名：{{ props.user.username }}</p>
      <p class="user-detail-box-item">用户昵称：{{ props.user.nickname }}</p>
      <p class="user-detail-box-item">邮箱：{{ props.user.email }}</p>
      <p class="user-detail-box-item">创建时间：{{ formatUserCreateTime(props.user.create_time) }}</p>
      <p class="user-detail-box-item">状态：{{ UserState[getUserState(props.user)].desc }}</p>
      <p class="user-detail-box-item" v-if="userState === 1">
        <a data-v-9c259c1f="" class="weui-btn weui-btn_mini weui-btn_warn weui-wa-hotarea" @click="banUserAsk"> 禁用该用户</a>
      </p>
      <p class="user-detail-box-item" v-else>
        <a data-v-9c259c1f="" class="weui-btn weui-btn_mini weui-btn_primary weui-wa-hotarea" @click="activeUserAsk"> 启用该用户</a>
      </p>
    </div>
  </div>
</template>

<style scoped lang="less">
.user-detail-container {
  background-color: #f2f2f2;
  width: 100%;
  height: 100%;
  .user-detail-box {
    width: 300px;
    margin: 0 auto;
    .user-detail-box-item {
      padding: 5px;
      font-size: 12px;
    }
  }
}
</style>