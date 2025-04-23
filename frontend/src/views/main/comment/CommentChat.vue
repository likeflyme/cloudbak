<script setup>
import {reactive, ref} from "vue";
import {useRoute} from "vue-router";
import {msgs, session as getSession, chatroomInfo} from "@/api/msg.js"
import {useStore} from "vuex";
import {parseXml, formatMsgDate} from "@/utils/common.js";
import {getContactName} from "@/utils/contact.js";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import MsgFilter from "@/components/MsgFilter.vue";
import {shortenCharts} from "@/utils/common.js";
import MsgSysMsg from "@/components/msg/MsgSysMsg.vue";
import MsgSysMsgV4 from "@/components/msg4/MsgSysMsg.vue";
import MsgHeadTemplate from "@/components/msg/MsgHeadTemplate.vue";
import MsgHeadTemplateV4 from "@/components/msg4/MsgHeadTemplate.vue";
import MsgNotice from "@/components/msg/MsgNotice.vue";
import MsgPushMail from "../../../components/msg/MsgPushMail.vue";
import {initMembersMap} from "../../../utils/chatroom.js";

const store = useStore();
const route = useRoute();

const id = route.params.id
const isChatRoom = id.includes('@chatroom');
const userLength = ref(0);
const chatMapBySvrId = reactive({});
const chatRoomNameMap = reactive({});
const showTool = ref(false);
const showFilter = ref(false);
const selfDisplayName = ref('');

const initChatroomInfo = (info) => {
  selfDisplayName.value = info.self_display_name;
  if (info.members) {
    for (let i = 0; i < info.members.length; i++) {
      let m = info.members[i]
      chatRoomNameMap[m.username] = m;
    }
    userLength.value = info.members.length;
  }
}

// 群聊，加载群聊信息（人数）
if (isChatRoom) {
  let allInfo = store.getters.getAllChatroomInfo;
  let roomInfo = allInfo[id];
  if (roomInfo === undefined || roomInfo === null) {
    chatroomInfo(id).then(data => {
      if(data) {
        store.commit("setChatroomInfo", data);
        initChatroomInfo(data)
      }
    });
  } else {
    initChatroomInfo(roomInfo)
  }
}

const noMoreMsg = ref(false);
const isLoading = ref(false);

const query = reactive({
  username: id,
  page: 1,
  size: 30,
  start: 0,
  start_db: ''
});
const session = reactive({})

const isTop = ref(false);
const msg_list = reactive([])

const imageOptions = reactive({
  // 配置选项
  toolbar: true,
      title: true,
      tooltip: true,
      movable: true,
      zoomable: true,
      rotatable: true,
      scalable: true,
      transition: false,
      url: 'data-original',
      filter(image) {
        // 排除带有 exclude 类的 img 元素
        return !image.classList.contains('exclude');
      },
});

const loadSession = () => {
  getSession(id).then(resp => {
    Object.assign(session, resp);
  })
}
loadSession();

const loadData = () => {
  if (!noMoreMsg.value) {
    isLoading.value = true;
    // 其他按照对话处理
    msgs(query).then(resp => {
      isLoading.value = false;
      if (resp.messages.length < query.size) {
        noMoreMsg.value = true;
      }
      if (resp.messages.length > 0) {
        query.start = resp.start;
        // 设置起始数据库名
        query.start_db = resp.start_db;
        for (let c of resp.messages) {
          msg_list.push(c);
          // // 图片类型存一份到映射中方便引用类型查找
          // if (c.Type === 3 && c.SubType === 0) {
          //   chatMapBySvrId[c.MsgSvrIDStr] = c;
          // }
        }
      }
    }).catch(e => {
      isLoading.value = false;
      console.log("load msg error:", e)
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


// 加载数据
loadData();

const chatContainer = ref(null);

// 反向滚动
const onWheel = (event) => {
  // 阻止默认滚动行为，以便完全自定义滚动效果
  event.preventDefault();

  // 根据滚轮事件的 deltaY 属性调整滚动条位置
  const delta = event.deltaY;

  // 根据滚轮方向调整滚动条位置，注意方向是反的
  chatContainer.value.scrollTop -= delta;
  if (isTop.value === true) {
    // 只有在到达顶部的标记为 true 时才加载数据，加载完后将标记修改为 false;
    loadMore();
    isTop.value = false;
  }
};

const onScroll = () => {
  // 翻转计算，为避免滚动到底部时有一点误差，允许误差在2以内
  let top = chatContainer.value.scrollHeight - chatContainer.value.clientHeight;
  if (Math.abs(chatContainer.value.scrollTop - top) < 2) {
    // 避免过快加载数据，这里只标记到达顶部
    if (!isTop.value) {
      isTop.value = true;
    }
  }
};

const handleTouchMove = () => {
  let top = chatContainer.value.scrollHeight - chatContainer.value.clientHeight;
  if (Math.abs(chatContainer.value.scrollTop - top) < 2) {
    // 避免过快加载数据，这里只标记到达顶部
    if (!isTop.value) {
      isTop.value = true;
    } else {
      loadMore();
      isTop.value = false;
    }
  }
}
const loadMore = () => {
  query.page = query.page + 1;
  loadData();
};

const shouldDisplayTimestampV3 = (currentTimestamp, index) => {
  let nextIndex = index + 1;
  // 最后一条消息输出时间
  if (msg_list.length < nextIndex + 1) {
    return true;
  }
  let last = msg_list[index + 1]
  return (currentTimestamp - last.windows_v3_properties.CreateTime) > 600;
}

const shouldDisplayTimestampV4 = (currentTimestamp, index) => {
  let nextIndex = index + 1;
  // 最后一条消息输出时间
  if (msg_list.length < nextIndex + 1) {
    return true;
  }
  let last = msg_list[index + 1]
  return (currentTimestamp - last.windows_v4_properties.create_time) > 600;
}

const closeFilter = () => {
  showFilter.value = false;
}
// 移动端返回
const emit = defineEmits(['goBack']);

const titleShorten = (title) => {
  const width = window.innerWidth;
  if (width > 768) {
    return title;
  } else {
    return shortenCharts(title, 26, '...');
  }
}
</script>
<template>
  <div class="main-content">
    <div class="main-content-top">
      <p class="main-content-title" @click="emit('goBack');"><font-awesome-icon class="main-back" :icon="['fas', 'chevron-left']"/></p>
      <p class="main-content-title">{{ getContactName(id) }}</p>
      <p class="main-content-title" v-if="isChatRoom"> ({{userLength}})</p>
      <p style="flex-grow: 1"></p>
      <p class="main-content-toolbar" @click="showTool?showTool=false:showTool=true">...</p>
    </div>
    <div class="main-content-info"
         @wheel="onWheel"
         @scroll="onScroll"
         @touchmove="handleTouchMove"
         ref="chatContainer"
         v-viewer="imageOptions">
      <div class="chat-grow">
      </div>
      <!-- win.v3-->
      <div v-if="store.getters.getClientVersion === 'win.v3'" class="chat-container" v-for="(m, index) in msg_list" :key="m">
        <div class="tips" v-if="shouldDisplayTimestampV3(m.windows_v3_properties.CreateTime, index)">
          <p class="tips-content">
            {{ formatMsgDate(m.windows_v3_properties.CreateTime) }}
          </p>
        </div>
        <!-- 系统消息 -->
        <MsgSysMsg
            v-if="m.windows_v3_properties.Type === 10000"
            :msg="m.windows_v3_properties"></MsgSysMsg>
        <!-- 特殊的简单通知类型，已知为QQ邮箱 -->
        <MsgPushMail
            v-else-if="m.windows_v3_properties.Type === 35 && m.windows_v3_properties.SubType === 0"
            :msg="m.windows_v3_properties"></MsgPushMail>
        <!-- 通知类消息，主要为公众号，服务号通知等 -->
        <MsgNotice
            v-else-if="m.windows_v3_properties.Type === 49 && m.windows_v3_properties.SubType === 5 && !id.startsWith('wxid_') && !id.endsWith('@chatroom')"
            :msg="m.windows_v3_properties"></MsgNotice>
        <MsgHeadTemplate
            v-else
            :roomId="route.params.id"
            :msg="m.windows_v3_properties"
            :chatRoomNameMap="chatRoomNameMap"
            :isChatRoom="isChatRoom"
        ></MsgHeadTemplate>
      </div>
      <div v-if="store.getters.getClientVersion === 'win.v4'" class="chat-container" v-for="(m, index) in msg_list" :key="m">
        <div class="tips" v-if="shouldDisplayTimestampV4(m.windows_v4_properties.create_time, index)">
          <p class="tips-content">
            {{ formatMsgDate(m.windows_v4_properties.create_time) }}
          </p>
        </div>
        <!-- 系统消息 -->
        <MsgSysMsgV4
            v-if="m.windows_v4_properties.local_type === 10000"
            :msg="m.windows_v4_properties"></MsgSysMsgV4>
        <MsgHeadTemplateV4
            v-else
            :roomId="route.params.id"
            :msg="m.windows_v4_properties"
            :chatRoomNameMap="chatRoomNameMap"
            :isChatRoom="isChatRoom"
        ></MsgHeadTemplateV4>
      </div>
      <div class="load-more">
        <a v-if="!noMoreMsg" href="javascript:void(0)" @click="loadMore">
          <font-awesome-icon class="loading-icon" v-if="isLoading" :icon="['fas', 'spinner']"/>
          <p v-else>查看更多消息</p>
        </a>
      </div>
    </div>
    <div class="main-tools" v-if="showTool">
      <ul class="main-tools-ul">
        <li class="main-tools-li" v-if="isChatRoom">
          <div class="chatroom-item">
            <p>群聊名称</p>
            <p class="chatroom-value"> {{ getContactName(id) }} </p>
          </div>
          <div class="chatroom-item">
            <p>群聊公告</p>
            <p class="chatroom-value"> 暂不支持 </p>
          </div>
          <div class="chatroom-item">
            <p>群聊备注</p>
            <p class="chatroom-value"> {{ session.Remark?session.Remark:'未设置' }} </p>
          </div>
          <div class="chatroom-item">
            <p>我在本群的昵称</p>
            <p class="chatroom-value" v-if="selfDisplayName"> {{selfDisplayName}} </p>
            <p class="chatroom-value" v-else> 未设置 </p>
          </div>
        </li>
        <li class="main-tools-li flex tool-chat" @click="showFilter?showFilter = false: showFilter = true">
          <p>聊天记录</p>
          <p style="flex-grow: 1"></p>
          <p class="tool-chevron-right"><font-awesome-icon :icon="['fas', 'chevron-right']"/></p>
        </li>
      </ul>
    </div>
  </div>
  <div class="msg-filter" :class="{'open': showFilter}" v-if="showFilter" >
    <MsgFilter @close-filter="closeFilter" :str-usr-name="id" :title="session.Remark?session.Remark:session.strNickName"></MsgFilter>
  </div>
</template>
<style scoped lang="less">
@import "/src/style/main/comment/comment-chat.less";
</style>