<script setup>
import {useRoute, useRouter} from "vue-router";
import {chatroomInfo} from "@/api/msg.js";
import {reactive} from "vue";
import {getUserNameByWxId, shortenCharts} from "@/utils/common.js";
import {useStore} from "vuex";
import defaultImage from '@/assets/default-head.svg';
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {getContactHeadById, getContactName} from "../../../../utils/contact.js";

const store = useStore();
const router = useRouter();
const route = useRoute();
const chatroom = reactive({});
const members = reactive([]);
const chatRoomNameMap = reactive({})

const id = route.params.id;

chatroomInfo(id).then(data => {
  if (data) {
    Object.assign(chatroom, data);
    if (data.members) {
      members.push(...data.members);
    }
  }
});


const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}

// const comment = () => {
//   router.push({ name: 'chat', params: { sessionId: route.params.sessionId, id: id} });
// }

const comment = () => {
  router.push({
    name: 'chat',
    params: {
      sessionId: route.params.sessionId,
      id: id
    },
    query: {
      userName: id
    }
  });
}

/**
 * 有备注先用备注，其次群备注，最后昵称
 * @param m
 * @returns {*}
 */
const displayName = (m) => {
  if (m.remark && m.remark !== '') {
    return m.remark;
  }
  return getContactName(m.username);
}

// 移动端返回
const emit = defineEmits(['goBack']);

</script>

<template>
  <div class="info-container">
    <div class="info-top">
      <p class="info-title main-back" @click="emit('goBack');"><font-awesome-icon class="main-back" :icon="['fas', 'chevron-left']"/></p>
      <p class="info-title">{{ getContactName(id) }}  </p>
    </div>
    <div class="info-msg" >
      <div class="comment-btn">
        <a class="weui-btn weui-btn_primary weui-btn_mini" @click="comment">查看消息</a>
      </div>
      <ul class="users-container">
        <li class="user" v-for="contact in members">
          <img class="user-img" :src="getContactHeadById(contact.username)" @error="setDefaultImage" alt=""/>
          <p class="user-name"> {{ displayName(contact) }} </p>
        </li>
      </ul>

    </div>
  </div>
</template>

<style scoped lang="less">
@import "/src/style/main/addressbook/info/chatroom-info.less";
</style>