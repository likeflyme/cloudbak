<script setup>
import {useStore} from "vuex";
import {useRouter, useRoute} from "vue-router";
import {getUserNameByWxId, shortenCharts} from "@/utils/common.js";
import defaultImage from '@/assets/default-head.svg';
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {getContactById, getContactHeadById} from "../../../../utils/contact.js";

const store = useStore();
const router = useRouter();
const route = useRoute();
const user = store.getters.getAddrShowUser;
const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}
const comment = () => {
  router.push({
    name: 'chat',
    params: {
      sessionId: route.params.sessionId,
      id: user.username
    },
    query: {
      userName: user.username
    }
  });
}

// 移动端返回
const emit = defineEmits(['goBack']);
</script>

<template>
  <div class="info">
    <div class="info-head">
      <p class="info-title" @click="emit('goBack');"><font-awesome-icon class="main-back" :icon="['fas', 'chevron-left']"/></p>
    </div>
    <div class="info-container">
      <div class="info-head bottom-border">
        <img class="info-img" :src="user.small_head_url" @error="setDefaultImage" alt=""/>
        <div class="info-desc-container">
          <p class="info-title">{{ user.remark?user.remark:user.nickname }}</p>
          <p class="info-area">昵称：{{ user.nickname }}</p>
          <p class="info-wxid">微信号：{{ user.username }}</p>
        </div>
      </div>
      <div class="info-other bottom-border">
        <div class="info-other-item">
          <p class="info-key">备注</p>
          <p class="info-value">{{ user.remark }}</p>
        </div>
        <div class="info-other-item">
          <p class="info-key">个性签名</p>
          <p class="info-value"></p>
        </div>
        <div class="info-other-item">
          <p class="info-value">
            <a class="weui-btn weui-btn_primary weui-btn_mini" @click="comment">查看消息</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
@import "/src/style/main/addressbook/info/user-info.less";
</style>