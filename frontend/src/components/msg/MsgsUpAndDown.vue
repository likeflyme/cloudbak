<script setup>
import SysLoading from "../tools/SysLoading.vue";
import {nextTick, reactive, ref} from "vue";
import {useStore} from "vuex";
import {getContactById, getContactHeadById, getContactName} from "../../utils/contact.js";
import {formatUserCreateTime, getThumbFromStringContent} from "../../utils/common.js";
import {get_msg_desc} from "@/utils/msgtp.js";
import {msgs as queryMsgs} from "@/api/msg.js";
import cleanedImage from '@/assets/cleaned.jpeg';
import defaultImage from '@/assets/default-head.svg';
import MsgSysMsg from "./MsgSysMsg.vue";
import {toBase64} from "js-base64";
import AudioPlayer from "../AudioPlayer.vue";
import ChatFile from "../ChatFile.vue";
import MsgTransfer from "./MsgTransfer.vue";

const props = defineProps({
  username: {
    type: String,
    required: true
  },
  msg: {
    type: Object
  },
  sessionId: {
    type: Number
  }
});
const store = useStore();
const loadUp = ref(false);
const loadDown = ref(false);
const hasMoreUpData = ref(true);
const hasMoreDownData = ref(true);
const chatContainer = ref(null); // 消息容器
const msgs = reactive([]); // 消息列表
const wxVersion = store.getters.getClientVersion;
// 群聊用户名
const chatRoomNameMap = reactive({});
const queryUp = reactive({
  username: props.msg.username,
  filter_sequence: props.msg.sequence,
  size: 20,
  start: 0,
  start_db: '',
  filter_mode: 0 // DESC
});
const queryDown = reactive({
  username: props.msg.username,
  filter_sequence: props.msg.sequence,
  size: 20,
  start: 0,
  start_db: '',
  filter_mode: 1 // ASC
});
const queryFromServerUp = () => {
  console.log("up");
  loadUp.value = true;
  queryMsgs(queryUp).then(data => {
    queryUp.start = data.start;
    queryUp.start_db = data.start_db;
    if (data.messages && data.messages.length > 0) {
      if (wxVersion === 'win.v3') {
        msgs.push(...data.messages.map(m => m.windows_v3_properties));
      } else if (wxVersion === 'win.v4') {
        msgs.push(...data.messages.map(m => m.windows_v4_properties));
      }
    } else {
      hasMoreUpData.value = false;
    }
  }).finally(() => {
    loadUp.value = false;
  });
}

const queryFromServerDown = (keepScreen = true) => {
  console.log("down");
  loadDown.value = true;
  queryMsgs(queryDown).then(data => {
    queryDown.start = data.start;
    queryDown.start_db = data.start_db;
    if (data.messages && data.messages.length > 0) {
      // 添加数据前，记录当前页面高度
      const previousScrollHeight = chatContainer.value.scrollHeight;
      const previousScrollTop = chatContainer.value.scrollTop;
      if (wxVersion === 'win.v3') {
        msgs.unshift(...data.messages.reverse().map(m => m.windows_v3_properties));
      } else if (wxVersion === 'win.v4') {
        msgs.unshift(...data.messages.reverse().map(m => m.windows_v4_properties));
      }
      if (keepScreen) {
        nextTick(() => {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight - previousScrollHeight + previousScrollTop;
        });
      }
    } else {
      hasMoreDownData.value = false;
    }
  }).finally(() => {
    loadDown.value = false;
  });
}

// 反向滚动
const onWheel = (event) => {
  // 阻止默认滚动行为，以便完全自定义滚动效果
  event.preventDefault();

  // 根据滚轮事件的 deltaY 属性调整滚动条位置
  const delta = event.deltaY;

  // 根据滚轮方向调整滚动条位置，注意方向是反的
  chatContainer.value.scrollTop -= delta;
};

// 滚动加载
const onScroll = () => {
  const clientHeight = chatContainer.value.clientHeight;
  const scrollHeight = chatContainer.value.scrollHeight;
  const scrollTop = chatContainer.value.scrollTop;
  if (scrollTop === 0) {
    queryFromServerDown();
  } else if (scrollTop + clientHeight === scrollHeight) {
    queryFromServerUp();
  }
};

// 图片查看器
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

// 换行符替换为 <br>
const formatContent = (content) => {
  if (content) {
    return content.replace(/\n/g, '<br>');
  } else {
    return content;
  }
}

const displayName = (username) => {
  let contact = getContactById(username);
  if (contact) {
    return getContactName(username);
  }
  const member = chatRoomNameMap[username]
  if (member) {
    if (member.remark) {
      return member.remark;
    } else {
      return member.nickname;
    }
  }
  return '';
}

const initMembers = () => {
  console.log("初始化成员")
  if (props.username.includes('@chatroom')) {
    console.log("聊天室")
    let allInfo = store.getters.getAllChatroomInfo;
    let roomInfo = allInfo[props.username];
    if (roomInfo) {
      let members = roomInfo.members;
      if (members) {
        for (let i = 0; i < members.length; i++) {
          let m = members[i]
          chatRoomNameMap[m.username] = m;
        }
      }
    }
  }
}
// 初始化成员信息
initMembers();
// 执行一次查询
queryFromServerUp();

// 图片代理判断
const getImageUrl = (url) => {
  if (url) {
    if (url.startsWith("/")) {
      return url;
    }
    if (store.getters.isPictureProxy) {
      return `/api/resources/image-proxy?encoded_url=${toBase64(url)}`;
    } else {
      return url;
    }
  }
  return '';
}

/**
 * 设置默认图片
 * @param event
 */
const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}

</script>

<template>
  <div class="msg-up-down"
       ref="chatContainer"
       v-viewer="imageOptions"
       @wheel="onWheel"
       @scroll="onScroll">
    <div class="msg-load" v-if="hasMoreDownData">
      <sys-loading v-if="loadUp"/>
      <p v-else @click="queryFromServerDown">加载更多</p>
    </div>
    <div class="msg-up-down-msg" v-for="msg in msgs" v-if="store.getters.getClientVersion === 'win.v3'">
      <!-- 系统消息不展示-->
      <div v-if="msg.Type === 10000"> </div>
      <div class="msg-up-down-with-head" v-else>
        <div class="msg-up-down-msg-left">
          <img alt="head" :src="getContactHeadById(msg.sender)" @error="setDefaultImage"/>
        </div>
        <div class="msg-up-down-msg-center">
          <div class="msg-up-down-msg-center-nickname">
            <p class="msg-up-down-msg-center-nickname-left">{{ displayName(msg.sender) }}</p>
            <p class="msg-up-down-msg-center-nickname-datetime">{{ formatUserCreateTime(msg.Sequence/1000) }}</p>
          </div>
          <div class="msg-up-down-msg-center-content">
            <div v-if="msg.Type === 1 && msg.SubType === 0" v-html="formatContent(msg.StrContent)"></div>
            <!-- 图片消息 -->
            <div v-else-if="msg.Type === 3 && msg.SubType === 0">
              <img
                  :src="'/api/resources/relative-resource?relative_path=' + msg.thumb + '&session_id=' + store.getters.getCurrentSessionId"
                  :data-original="msg.Image ? '/api/resources/relative-resource?relative_path=' + msg.source + '&session_id=' + store.getters.getCurrentSessionId : cleanedImage"
                  alt=""/>
            </div>
            <!-- 语音消息 -->
            <div v-else-if="msg.Type === 34" class="chat-media">
              <AudioPlayer
                  :src="`/api/resources/media?strUsrName=${msg.sender}&MsgSvrID=${msg.MsgSvrIDStr}&session_id=${props.sessionId}`"
                  :text="msg.StrContent"/>
            </div>
            <!-- 视频消息 -->
            <div v-else-if="msg.Type === 43" class="chat-img exclude">
              <video controls width="250" :poster="`/api/resources/relative-resource?relative_path=${msg.thumb}&session_id=${props.sessionId}`">
                <source v-if="msg.source" :src="`/api/resources/relative-resource?relative_path=${msg.source}&session_id=${props.sessionId}&source_type=video`" type="video/mp4" />
              </video>
            </div>
            <!-- 用户图片表情 -->
            <div v-else-if="msg.Type === 47 && msg.SubType === 0" class="chat-img">
              <img class="exclude"
                   :src="getImageUrl(getThumbFromStringContent(msg.StrContent))"
                   alt=""/>
            </div>
            <!-- 文件消息 -->
            <div v-else-if="msg.Type === 49 && msg.SubType === 6">
              <chat-file :msg="msg"></chat-file>
            </div>
            <!-- 引用消息 -->
            <div v-else-if="msg.Type === 49 && msg.SubType === 57" class="chat-text">
              <p>
                {{ msg.compress_content.msg.appmsg.title }}
              </p>
            </div>
            <!-- 转账消息 -->
            <div class="chat-transfer" v-else-if="msg.Type === 49 && msg.SubType === 2000">
              <MsgTransfer :msg="msg"/>
            </div>
            <div v-else>不支持的消息类型：{{get_msg_desc(msg.Type, msg.SubType)}}({{msg.Type }}.{{msg.SubType}})</div>
          </div>
        </div>
        <div class="msg-up-down-msg-right">
          <p class="msg-up-down-msg-right-time">{{ formatUserCreateTime(msg.Sequence/1000) }}</p>
        </div>
      </div>
    </div>
    <div class="msg-load" v-if="hasMoreUpData">
      <p @click="queryFromServerUp">加载更多</p>
    </div>
  </div>
</template>

<style scoped lang="less">
.msg-up-down {
  height: 100%;
  overflow-y: scroll;
  direction: rtl;
  transform: rotate(180deg) translateZ(0);
  .msg-load {
    transform: rotate(180deg) translateZ(0);
    direction: ltr;
    text-align: center;
    cursor: pointer;
    font-size: 13px;
    color: #576b95;
  }
  .msg-up-down-msg {
    transform: rotate(180deg) translateZ(0);
    direction: ltr;
    display: flex;
    padding: 10px 20px;
    .msg-up-down-with-head {
      display: flex;
      width: 100%;
      .msg-up-down-msg-left {
        width: 40px;
        padding: 10px 0;
        flex-shrink: 0;
        img {
          width: 40px;
          height: 40px;
        }
      }
      .msg-up-down-msg-center {
        flex-grow: 1;
        border-bottom: 1px solid #ececec;
        padding: 10px;
        .msg-up-down-msg-center-nickname {
          display: flex;
          color: #999999;
          .msg-up-down-msg-center-nickname-left {
            font-size: 14px;
            flex-grow: 1;
          }
          .msg-up-down-msg-center-nickname-datetime {
            width: 150px;
            font-size: 12px;
            text-align: right;
          }
        }
        .msg-up-down-msg-center-content {
          padding: 10px 0;
          word-break: break-word;
          .chat-img {
            img {
              max-width: 150px;
            }
          }
        }
      }
      .msg-up-down-msg-right {
        width: 100px;
        border-bottom: 1px solid #ececec;
        padding: 10px 0;
        flex-shrink: 0;
        .msg-up-down-msg-right-time {
          color: #999999;
        }
        .msg-up-down-msg-right-show-content {
          color: #576b95;
          cursor: pointer;
          visibility: hidden;
        }
      }
    }
  }
}
// 以下是滚动条样式
/* 隐藏默认的滚动条轨道和拇指 */
.msg-up-down::-webkit-scrollbar {
  width: 0.429rem; /* 隐藏滚动条 */
  background: transparent; /* 使滚动条轨道背景透明 */
}

/* 鼠标悬停时显示滚动条轨道 */
.msg-up-down:hover::-webkit-scrollbar {
  width: 0.429rem; /* 设置滚动条宽度 */
  background: #f0f0f0; /* 滚动条轨道背景颜色 */
}

/* 滚动条轨道样式 */
.msg-up-down:hover::-webkit-scrollbar-track-piece {
  background: #f0f0f0; /* 设置滚动条轨道背景颜色 */
  border-radius: 0.571rem; /* 设置滚动条轨道圆角 */
}

/* 滚动条拇指样式 */
.msg-up-down:hover::-webkit-scrollbar-thumb {
  background-color: #c8c9cc; /* 设置滚动条拇指背景颜色 */
  border-radius: 0.571rem; /* 设置滚动条拇指圆角 */
}

/* 鼠标悬停在滚动条拇指上时的样式 */
.msg-up-down:hover::-webkit-scrollbar-thumb:hover {
  background-color: #b0b0b0; /* 鼠标悬停时滚动条拇指背景颜色 */
}

@media (max-width: 1024px) {
  .msg-up-down-msg-right {
    display: none;
  }
}
@media (min-width: 1025px) {
  .msg-up-down-msg-center-nickname-datetime {
    display: none;
  }
}
</style>