<script setup>
import defaultImage from '@/assets/default-head.svg';
import AudioPlayer from "../AudioPlayer.vue";
import unknownFile from '@/assets/filetypeicon/unknown.svg';
import cleanedImage from '@/assets/img-cleaned.png';
import {getThumbFromStringContent, fileSize, getReferFileName, fromXmlToJson} from "@/utils/common.js";
import {getContactHeadById} from "@/utils/contact.js";
import {parseMsg} from "@/utils/message_parser_v4.js";
import {get_msg_desc} from "@/utils/msgtp_v4.js";
import {msgBySvrId, singleMsg} from "@/api/msg.js"
import {toBase64} from "js-base64";

import {useStore} from "vuex";
import {reactive} from "vue";
import {getContactById, getContactName} from "../../utils/contact.js";
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
 * @param username
 * @returns {*}
 */
const displayName = (username) => {
  const contact = getContactById(username);
  if (contact) {
    return contact.remark ? contact.remark : contact.nickname;
  }
  let member = props.chatRoomNameMap[username];
  if (member) {
    return member.remark ? member.remark : member.nickname;
  }
  return '未知用户';
}

const headImage = (username) => {
  const contact = getContactById(username);
  if (contact) {
    return contact.small_head_url;
  }
  const member = props.chatRoomNameMap[username]
  if (member) {
    return member.small_head_img;
  }
  return defaultImage;
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

// 解析数据
parseMsg(props.msg)

const isSender = props.msg.sender === store.getters.getCurrentWxId;

</script>

<template>
  <div class="chat" :class="{'right': isSender, 'left': isSender === false}">
    <div class="chat-header">
      <img :src="headImage(props.msg.sender)" @error="setDefaultImage" alt="" class="exclude"/>
    </div>
    <div class="chat-info">
      <div class="chat-nickname" v-if="props.isChatRoom">
        <p v-if="props.isChatRoom"> {{ displayName(props.msg.sender) }} </p>
      </div>
      <!-- 文本消息 -->
      <div class="chat-text" v-if="props.msg.local_type === 1">
        <msg-text-with-emoji :content="props.msg.data.content"/>
      </div>
      <!-- 图片消息 -->
<!--      <div class="chat-img" v-else-if="props.msg.local_type === 3">-->
<!--        <p>-->
<!--          {{ props.msg.data.content }}-->
<!--        </p>-->
<!--      </div>-->
      <!-- 视频消息 -->
<!--      <div v-else-if="props.msg.local_type === 43" class="chat-img exclude">-->
<!--        <video controls width="250" :poster="`/api/resources-v4/video-poster/${store.getters.getCurrentSessionId}/${props.msg._video?.msg.videomsg['@attributes']?.md5}`">-->
<!--          <source :src="`/api/resources-v4/video/${store.getters.getCurrentSessionId}/${props.msg._video?.msg.videomsg['@attributes']?.md5}`" type="video/mp4" />-->
<!--        </video>-->
<!--      </div>-->
      <div class="chat-text" v-else>
        <p>
          [不支持的消息类型: {{get_msg_desc(props.msg.local_type)}}]
        </p>
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
      direction: ltr;
      word-break: break-word;
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