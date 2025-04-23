<script setup>
import defaultImage from '@/assets/default-head.svg';
import AudioPlayer from "../AudioPlayer.vue";
import unknownFile from '@/assets/filetypeicon/unknown.svg';
import cleanedImage from '@/assets/img-cleaned.png';
import {getThumbFromStringContent, fileSize, getReferFileName, fromXmlToJson} from "@/utils/common.js";
import {getContactHeadById, getContactById} from "@/utils/contact.js";
import {get_msg_desc} from "@/utils/msgtp.js";
import {msgBySvrId, singleMsg} from "@/api/msg.js"
import {toBase64} from "js-base64";

import {useStore} from "vuex";
import {reactive} from "vue";
import MsgMerge from "./MsgMerge.vue";
import MsgTransfer from "./MsgTransfer.vue";
import ChatFile from "../ChatFile.vue";
import {getContactName} from "../../utils/contact.js";
import MsgTextWithEmoji from "../MsgTextWithEmoji.vue";

const store = useStore();

const props = defineProps({
  roomId: {
    type: String
  },
  msg: {
    type: Object,
    required: true
  },
  chatRoomNameMap: {
    type: Object
  },
  isChatRoom: {
    type: Boolean,
    default: false
  }
});

const chatMapBySvrId = reactive({});

/**
 * 设置默认图片
 * @param event
 */
const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}
/**
 * 有备注先用备注，其次群备注，最后昵称
 * @param m
 * @returns {*}
 */
const displayName = (m) => {
  if (m.Remark) {
    return m.Remark;
  }
  const contact = getContactById(m.sender)
  if (contact) {
    return getContactName(m.sender)
  }
  let member = props.chatRoomNameMap[m.sender];
  if (member) {
    if (member.remark) {
      return member.remark;
    } else {
      return member.nickname;
    }
  }
}

const download = (path) => {
  if (path) {
    path = path.replace('\\', '/');
    const fileName = path.split('/').pop();
    let sessionId = store.getters.getCurrentSessionId;
    let url = `/api/resources/?path=${encodeURIComponent(path)}&session_id=${sessionId}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    // 将<a>元素添加到DOM
    document.body.appendChild(link);
    // 触发点击事件
    link.click();
    // 移除<a>元素
    document.body.removeChild(link);
  }
}

const getOriMsgBySvrId = (svrId, DbNo) => {
  let msg = chatMapBySvrId[svrId];
  // 本地不存在，则到服务端查找
  if (!msg) {
    singleMsg(props.roomId, svrId).then(data => {
      chatMapBySvrId[svrId] = data;
    });
  }
};

if (props.msg.Type === 49 && props.msg.SubType === 19) {
  console.log(props.msg);
}

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
  return defaultImage;
}

</script>

<template>
  <div class="chat" :class="{'right': props.msg.IsSender === 1, 'left': props.msg.IsSender === 0}">
    <div class="chat-header">
      <img :src="getContactHeadById(props.msg.sender)" @error="setDefaultImage" alt="" class="exclude"/>
    </div>
    <div class="chat-info">
      <div class="chat-nickname" v-if="props.isChatRoom">
        <p v-if="props.isChatRoom && props.msg.IsSender === 0"> {{ displayName(props.msg) }} </p>
      </div>
      <!-- 文本消息 -->
      <div class="chat-text" v-if="props.msg.Type === 1">
        {{props.msg.StrContent}}
      </div>
      <!-- 图片消息 -->
      <div v-else-if="props.msg.Type === 3" class="chat-img">
        <img
            :src="'/api/resources/relative-resource?relative_path=' + props.msg.thumb + '&session_id=' + store.getters.getCurrentSessionId"
            :data-original="props.msg.source ? '/api/resources/relative-resource?relative_path=' + props.msg.source + '&session_id=' + store.getters.getCurrentSessionId : cleanedImage"
            alt=""/>
      </div>
      <!-- 语音消息 -->
      <div v-else-if="props.msg.Type === 34" class="chat-media">
        <AudioPlayer
            :src="`/api/resources/media?strUsrName=${props.roomId}&MsgSvrID=${props.msg.MsgSvrIDStr}&session_id=${store.getters.getCurrentSessionId}`"
            :text="props.msg.StrContent"
            :right="props.msg.IsSender === 1"/>
      </div>
      <!-- 视频消息 -->
      <div v-else-if="props.msg.Type === 43" class="chat-img exclude">
        <video controls width="250" :poster="`/api/resources/relative-resource?relative_path=${props.msg.thumb}&session_id=${store.getters.getCurrentSessionId}`">
          <source v-if="props.msg.source" :src="`/api/resources/relative-resource?relative_path=${props.msg.source}&session_id=${store.getters.getCurrentSessionId}&resource_type=video`" type="video/mp4" />
        </video>
      </div>
      <!-- 用户图片表情 -->
      <div v-else-if="props.msg.Type === 47 && props.msg.SubType === 0" class="chat-img">
        <img class="exclude"
             :src="getImageUrl(getThumbFromStringContent(props.msg.StrContent))"
             alt=""/>
      </div>
      <!-- 49.5 通知消息 -->
      <div v-else-if="props.msg.Type === 49 && props.msg.SubType === 5" class="refer-msg">
        <p class="refer-text">
          暂不支持的消息类型：{{ get_msg_desc(props.msg.Type, props.msg.SubType) }}
        </p>
      </div>
      <!-- 引用消息 -->
      <div v-else-if="props.msg.Type === 49 && props.msg.SubType === 57" class="chat-text">
        <p>
          {{ props.msg.compress_content.msg.appmsg.title }}
        </p>
      </div>
      <!-- 文件消息 -->
      <div v-else-if="props.msg.Type === 49 && props.msg.SubType === 6" >
        <chat-file :msg="props.msg"/>
      </div>
      <!-- 通话消息 -->
      <div class="chat-phone" v-else-if="props.msg.Type === 50 && props.msg.SubType === 0">
        <font-awesome-icon class="icon-file" :icon="['fas', 'phone']" title="文件"/> {{ props.msg.DisplayContent }}
      </div>
      <div v-else class="refer-msg">
        <p class="refer-text">
          暂不支持的消息类型：{{ get_msg_desc(props.msg.Type, props.msg.SubType) }}
        </p>
      </div>
      <!-- 引用消息 -->
      <div class="refer-msg" v-if="props.msg.Type === 49 && props.msg.SubType === 57">
        <!-- 引用文本消息 -->
        <p class="refer-text" v-if="props.msg.compress_content.msg.appmsg.refermsg.type === '1'">
          {{ props.msg.compress_content.msg.appmsg.refermsg.displayname }}: {{ props.msg.compress_content.msg.appmsg.refermsg.content }}
        </p>
        <!-- 引用文件消息 -->
        <p class="refer-text" v-else-if="props.msg.compress_content.msg.appmsg.refermsg.type === '49'">
          {{ props.msg.compress_content.msg.appmsg.refermsg.displayname }}: {{ getReferFileName(props.msg.compress_content.msg.appmsg.refermsg.content) }}
          <font-awesome-icon class="icon-file" :icon="['fas', 'file']" title="文件"/>
        </p>
        <!-- 引用图片消息 -->
        <div class="refer-img" v-else-if="props.msg.compress_content.msg.appmsg.refermsg.type === '3'">
          <p v-if="chatMapBySvrId[props.msg.compress_content.msg.appmsg.refermsg.svrid]" class="refer-img-title">{{ props.msg.compress_content.msg.appmsg.refermsg.displayname }}: </p>
          <img v-if="chatMapBySvrId[props.msg.compress_content.msg.appmsg.refermsg.svrid]"
               :src="`/api/resources/resource-from-source-id/${store.getters.getCurrentSessionId}/${props.msg.compress_content.msg.appmsg.refermsg.svrid}`"
               :data-original="`/api/resources/resource-from-source-id/${store.getters.getCurrentSessionId}/${props.msg.compress_content.msg.appmsg.refermsg.svrid}?file_type=Image`"
               alt=""/>
        </div>
        <!-- 引用其他消息 -->
<!--        <p class="refer-text" v-else>-->
<!--          暂不支持的引用消息类型 refermsg.type = {{ props.msg.compress_content.msg.appmsg.refermsg.type }}-->
<!--        </p>-->
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.chat {
  margin-top: 0.714rem;
  display: flex;
  .chat-header {
    width: 2.5rem;
    height: 2.5rem;
    img {
      width: 2.5rem;
      height: 2.5rem;
      border-radius: 0.214rem;
    }
  }
  .chat-info {
    padding-left: 0.714rem;
    padding-right: 0.714rem;
    .chat-nickname {
      font-size: 0.857rem;
      color: #BEBEBE;
      text-align: left;
    }
    .chat-text {
      direction: ltr;
      font-size: 1rem;
      margin-top: 0.214rem;
      padding: 0.357rem 0.714rem;
      border-radius: 0.357rem;
      display: inline-block;
      color: #232323;
      word-wrap: break-word;
      max-width: 28.571rem;
    }
    .chat-text:hover {
      background-color: #EBEBEB;
    }
    .chat-img {
      border-radius: 0.286rem;
      img {
        max-width: 14.286rem;
      }
    }
    .chat-img:hover {
      cursor: pointer;
    }
    .chat-media {

    }
    .refer-msg {
      margin-top: 0.357rem;
      direction: ltr;
      .refer-text {
        direction: ltr;
        font-size: 0.857rem;
        background-color: #E8E8E8;
        color: #797979;
        padding: 0.357rem;
        border-radius: 0.214rem;
        display: inline-block;
        max-width: 28.571rem;
        // 长文本换行
        word-wrap: break-word;
        word-break: break-all;
        .icon-file {
          color: #207346;
        }
      }
      .refer-img {
        font-size: 0.857rem;
        background-color: #E8E8E8;
        color: #797979;
        padding: 0.357rem 0.714rem;
        border-radius: 0.214rem;
        display: inline-block;
        word-break: break-word;
      }
    }
    .chat-file {
      height: 8.343rem;
      background-color: #FFFFFF;
      border-radius: 0.357rem;
      .chat-file-top {
        height: 5.357rem;
        border-bottom: 0.071rem solid #f0f0f0;
        display: flex;
        padding: 0.714rem;
        .chat-file-left {
          width: 16.429rem;
          height: 100%;
          .chat-file-title {
            font-size: 1rem;
          }
          .chat-file-content {
            font-size: 0.857rem;
            color: #797979;
            align-items: center;
          }
        }
        .chat-file-icon {
          width: 3.571rem;
          height: 100%;
          font-size: 2.143rem;
          text-align: center;
          color: #207346;
          .item-icon {
            width: 2.857rem;
          }
        }
      }
      .chat-file-bottom {
        .chat-file-app-info {
          font-size: 0.786rem;
          color: #797979;
          padding-left: 0.714rem;
          line-height: 1.786rem;
        }
      }
    }
    .chat-file:hover {
      cursor: pointer;
    }
    .chat-phone {
      background-color: #FFFFFF;
      border-radius: 3px;
      padding:5px 10px;
    }
  }
}
.chat:last-child {
  margin-bottom: 1.429rem;
}
.chat.right {
  .chat-info {
    .chat-nickname {
      text-align: right;
    }
    .chat-text {
      text-align: left;
      background-color: #95ec69;
    }
    .chat-phone {
      background-color: #95ec69;
    }
  }
}
.chat.left {
  flex-direction: row-reverse;
  .chat-info {
    text-align: left;
    .chat-nickname {
      text-align: left;
    }
    .chat-text {
      text-align: left;
      background-color: #FFFFFF;
    }
    .chat-media {
      direction: ltr;
    }
    .chat-phone {
      direction: ltr;
    }
  }
}
.chat.right .chat-info:hover {
  .chat-text {
    background-color: #89D961;
  }
}
.chat.left .chat-info:hover {
  .chat-text {
    background-color: #ebebeb;
  }
}
</style>