<script setup>
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {computed, onUnmounted, reactive, ref, watch} from "vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {msgsSearch, msgsSplit} from "@/api/fts.js";
import {getContactById, getContactHeadById, getContactName} from "@/utils/contact.js";
import {shortenCharts} from "@/utils/common.js";
import defaultImage from '@/assets/default-head.svg';
import SysLoading from "../tools/SysLoading.vue";
import MsgsUpAndDown from "../msg/MsgsUpAndDown.vue";
import {chatroomInfo} from "../../api/msg.js";

const props = defineProps({
  match: {
    type: String,
    default: ''
  },
  contact: {
    type: Object,
    default: null
  }
});

const store = useStore();
const router = useRouter();

const search = ref(props.match);
const loading = ref(false); // 左侧结果加载中
const msgs = reactive([]); // 左侧结果数据列表
const contentLoading = ref(false); // 右侧内容加载中
const contentMsgs = reactive([]); // 右侧内容数据列表
const selectedContact = ref(''); // 选中的联系人，默认为空，调用方可传 clientSelected 默认选中
const startIndex = ref(0);
const startDb = ref('');
const contentMsgCount = ref(0);
const scrollContainer = ref(null);
// 群聊用户名
const chatRoomNameMap = reactive({});
const pageQuery = reactive({
  username: '',
  text: '',
  page: 1,
  size: 30,
  start: 0,
  start_db: '',
  is_end: false
});

const clear = () => {
  search.value = '';
  msgs.length = 0;
  contentMsgs.length = 0;
}

// 输入停止1秒后执行的函数
const handleInputEnd = () => {
  msgs.length = 0;
  selectedContact.value = '';
  if (search.value) {
    loading.value = true;
    // 聊天记录搜索
    msgsSearch(search.value).then(resp => {
      msgs.push(...resp);
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
      loading.value = false;
    });
  }
};

let timeout = null;

// 监听输入框值的变化
watch(search, () => {
  // 清除之前的计时器
  if (timeout) clearTimeout(timeout);

  // 设置一个新的计时器
  timeout = setTimeout(() => {
    handleInputEnd();
  }, 1000); // 1秒后触发
});

// enter 事件搜索
const inputEnter = () => {
  if (timeout) clearTimeout(timeout);
  handleInputEnd();
}

// 清除计时器以防内存泄漏
onUnmounted(() => {
  if (timeout) clearTimeout(timeout);
});

/**
 * 设置默认图片
 * @param event
 */
const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}

// 打开时执行搜索
handleInputEnd();

// 以下为右侧消息查询

const loadMsgs = () => {
  // 避免重复执行
  if (contentLoading.value) {
    return;
  }
  // 消息末尾
  if (pageQuery.is_end) {
    return;
  }
  if (selectedContact.value === '') {
    return;
  }
  contentLoading.value = true;
  pageQuery.username = selectedContact.value;
  pageQuery.text = search.value;
  msgsSplit(pageQuery).then(resp => {
    pageQuery.start = resp.start;
    pageQuery.start_db = resp.start_db;
    contentMsgs.push(...resp.msgs);
    if (resp.msgs.length < pageQuery.size) {
      pageQuery.is_end = true;
    }
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
    contentLoading.value = false;
  });
}

// 选中的消息，查看上下文
// 被选中的联系人信息
const selectedContactInfo = reactive({});
const selectedMsg = ref(null); // 被选中的消息
// const selectedHead = ref('');
const selectedHead = computed(() => {
  if (selectedContactInfo.value) {
    return getContactHeadById(selectedContactInfo.value.username);
  } else {
    return '';
  }
});
const selectedContactName = computed(() => {
  if (selectedContactInfo.value) {
    return getContactName(selectedContactInfo.value.username);
  } else {
    return '';
  }
});

// 选择
const selectContact = (contact) => {
  const username = contact.username;
  startIndex.value = 0;
  startDb.value = '';
  selectedContact.value = username;
  contentMsgs.length = 0;
  contentMsgCount.value = contact.count;
  selectedMsg.value = null;
  selectedContactInfo.value = getContactById(username);
  selectedHead.value = getContactHeadById(username);

  pageQuery.username = '';
  pageQuery.text = '';
  pageQuery.page = 1;
  pageQuery.start = 0;
  pageQuery.start_db = ''
  pageQuery.is_end = false;

  // 聊天室需要加载成员信息

  let loadMembers = new Promise((resolve, reject) => {
    if (contact.username.includes('@chatroom')) {
      let roomInfo = chatRoomNameMap[contact.username];
      if (roomInfo === undefined) {
        let allInfo = store.getters.getAllChatroomInfo;
        roomInfo = allInfo[username];
        if (roomInfo === undefined) {
          chatroomInfo(contact.username).then(data => {
            if(data) {
              store.commit("setChatroomInfo", data);
              if (data.members) {
                roomInfo = {}
                for (let i = 0; i < data.members.length; i++) {
                  let m = data.members[i]
                  roomInfo[m.username] = m;
                }
                chatRoomNameMap[contact.username] = roomInfo;
              }
            }
            resolve();
          }).catch(e => {
            reject(e);
          });
        } else {
          let members = roomInfo.members;
          if (members) {
            for (let i = 0; i < members.length; i++) {
              let m = members[i]
              chatRoomNameMap[m.username] = m;
            }
          }
          resolve();
        }
      } else {
        resolve();
      }
    } else {
      resolve();
    }
  });

  loadMembers.then(resp => {
    loadMsgs();
  })
}



const displayName = (username) => {
  let name = displayNameReal(username);
  return name;
}

const displayNameReal = (username) => {
  let contact = getContactById(username);
  if (contact) {
    return getContactName(username);
  }
  const members = chatRoomNameMap[selectedContact.value]
  if (members) {
    let member = members[username];
    if (member) {
      if (member.remark) {
        return member.remark;
      } else {
        return member.nickname;
      }
    }
  }
  return '';
}

const deSelectContact = () => {
  selectedContact.value = '';
  contentMsgs.length = 0;
}

// 默认选中
if (props.contact) {
  selectContact(props.contact);
}

// 其他
const formatUserCreateTime = (timestamp) => {
  const date = new Date(timestamp);

  // 获取年、月、日、小时、分钟
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${year}/${month}/${day}`;
};

// 格式化内容
// 1. 匹配的值设置为绿色
// 2. 换行符替换为 <br>
const formatContent = (content) => {
  content = content.replace(new RegExp(search.value, 'g'), `<span style="color: green">${search.value}</span>`).replace(/\n/g, '<br>');
  return content;
}


// 上下文相关
// 消息选中
const choseMsg = (msg) => {
  selectedMsg.value = msg;
}
// 消息选中返回
const unChoseMsg = () => {
  selectedMsg.value = null;
}
// 打开聊天
const openSession = () => {
  selectedMsg.value = {
    userName: selectedContact.value,
    sequence: Date.now()
  };
}

// 反向滚动
const onWheel = (event) => {
  // 阻止默认滚动行为，以便完全自定义滚动效果
  event.preventDefault();

  // 根据滚轮事件的 deltaY 属性调整滚动条位置
  const delta = event.deltaY;

  // 根据滚轮方向调整滚动条位置，注意方向是反的
  scrollContainer.value.scrollTop -= delta;
};

// 滚动加载
const onScroll = () => {
  const clientHeight = scrollContainer.value.clientHeight;
  const scrollHeight = scrollContainer.value.scrollHeight;
  const scrollTop = scrollContainer.value.scrollTop;
  // 到底部加载数据
  if (scrollTop + clientHeight === scrollHeight) {
    loadMsgs();
  }
};

const comment = () => {
  router.push({
    name: 'chat',
    params: {
      sessionId: store.getters.getCurrentSessionId,
      id: selectedContact.value
    },
    query: {
      userName: selectedContact.value
    }
  });
}

</script>

<template>
  <div class="fts">
    <div class="fts-head">
      <div class="fts-search">
        <div class="weui-search-bar weui-search-bar_filled-grey weui-search-bar_focusing" id="searchBar">
          <div id="searchForm" role="combobox" aria-haspopup="true" aria-expanded="false" aria-owns="searchResult" class="weui-search-bar__form">
            <div aria-hidden="false" id="searchBox" class="weui-search-bar__box">
              <i class="weui-icon-search"></i>
              <input type="search" v-model="search" @keyup.enter="inputEnter" aria-controls="searchResult" class="weui-search-bar__input" id="searchInput" placeholder="搜索聊天记录" required/>
              <div class="weui-search-bar__mask"></div>
              <a href="javascript:" role="button" title="清除" class="weui-icon-clear" id="searchClear" @click="clear"></a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="fts-body" v-if="msgs.length > 0">
      <div class="fts-contact-container">
        <div class="fts-contact"
             v-for="msg in msgs"
             @click="selectContact(msg)"
             :class="{'selected': selectedContact === msg.username}">
          <div class="fts-contact-head">
            <img alt="head" :src="getContactHeadById(msg.username)" @error="setDefaultImage"/>
          </div>
          <div class="fts-contact-content">
            <p class="fts-contact-title">{{ getContactName(msg.username) }}</p>
            <p class="fts-contact-desc" v-if="msg.count === 1">{{shortenCharts(msg.content, 40, '...')}}</p>
            <p class="fts-contact-desc" v-else>{{msg.count}}条相关聊天记录</p>
          </div>
        </div>
      </div>
      <div class="fts-msgs" v-if="selectedContact" :class="{'open': selectedContact}">
        <div class="fts-msgs-content">
          <div class="fts-msgs-head">
            <div class="fts-msg-title">{{ contentMsgCount }}条与“{{ search }}”有关的聊天记录</div>
            <div class="fts-msg-tools" @click="comment">
              <font-awesome-icon class="audio-icon" :icon="['fas', 'comment']" title="进入聊天"/> 进入聊天</div>
          </div>
          <div class="fts-msgs-head-mobile">
            <div class="fts-msg-head-mobile-top-bar">
              <p class="fts-msg-head-mobile-top-bar-back" @click="deSelectContact">取消</p>
            </div>
            <div class="fts-msg-head-mobile-session" @click="openSession">
              <img class="fts-msg-head-mobile-session-img" alt="sessionHead" :src="selectedHead"/>
              <p class="fts-msg-head-mobile-session-title">{{selectedContactName}}</p>
              <p class="fts-msg-head-mobile-session-toolbar">
                <font-awesome-icon :icon="['fas', 'arrow-right']"/>
              </p>
            </div>
          </div>
          <div class="fts-msgs-roller" ref="scrollContainer" @wheel="onWheel" @scroll="onScroll">
            <div class="fts-msg" v-for="msg in contentMsgs">
              <div class="fts-msg-left">
                <img alt="head" :src="getContactHeadById(msg.sender)" @error="setDefaultImage"/>
              </div>
              <div class="fts-msg-center">
                <div class="fts-msg-center-nickname">{{ displayName(msg.sender) }}</div>
                <div class="fts-msg-center-content" v-html="formatContent(msg.content)"></div>
              </div>
              <div class="fts-msg-right">
                <p class="fts-msg-right-time">{{ formatUserCreateTime(msg.sequence) }}</p>
                <p class="fts-msg-right-show-content" @click="choseMsg(msg)">查看上下文</p>
              </div>
            </div>
            <div class="fts-msg-loading" v-if="contentMsgs.length < contentMsgCount">
              <sys-loading v-if="contentLoading"/>
              <p class="fts-msg-loading-btn" v-if="!contentLoading && !pageQuery.is_end" @click="loadMsgs">加载更多</p>
            </div>
          </div>
        </div>
        <div class="fts-chose" :class="{'open': selectedMsg}">
          <div class="fts-chose-back-bar">
            <font-awesome-icon class="fts-chose-back" :icon="['fas', 'chevron-left']" @click="unChoseMsg"/>
          </div>
          <msgs-up-and-down class="fts-chose-msg-up-and-down" v-if="selectedMsg" :username="selectedContact" :msg="selectedMsg" :session-id="store.getters.getCurrentSessionId" />
        </div>
      </div>
    </div>
    <div class="fts-body" v-else>
      <div v-if="loading" class="fts-loading">
        <sys-loading/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.fts {
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  .fts-head {
    .fts-search {
      margin: 0 auto;
      .weui-search-bar {
        height: 4.5rem;
        background-color: #f5f5f5;
        .weui-search-bar__form {
          height: 1.786rem;
          top: 0.714rem;
        }
        .weui-search-bar__mask {
          height: 1.786rem;
        }
      }
      .weui-search-bar__input {
        font-size: 0.929rem;
      }
    }
  }
  .fts-body {
    width: 100%;
    height: 504px;
    display: flex;
    .fts-contact-container {
      .fts-contact {
        .fts-contact-head {
          width: 40px;
          height: 40px;
          img {
            width: 40px;
            height: 40px;
          }
        }
        .fts-contact-content {
          padding-left: 10px;
          .fts-contact-title {
            font-size: 13px;
          }
          .fts-contact-desc {
            color: #999999;
            font-size: 12px;
          }
        }
      }
      .fts-contact:hover {
        background-color: #ececec;
      }
      .fts-contact.selected {
        background-color: #d4d4d4;
      }
    }
    .fts-msgs {
      flex-grow: 1;
      .fts-msgs-content {
        height: 100%;
        .fts-msgs-head {
          display: flex;
          padding: 10px 0;
          border-bottom: 1px solid #ececec;
          z-index: 100;
          background-color: #f5f5f5;
          .fts-msg-title {
            flex-grow: 1;
            padding-left: 20px;
            color: #999999;
          }
          .fts-msg-tools {
            width: 200px;
            text-align: center;
            cursor: pointer;
          }
        }
        .fts-msgs-roller {
          width: 100%;
          overflow-y: scroll;
          transform: rotate(180deg) translateZ(0);
          direction: rtl;
          .fts-msg {
            display: flex;
            padding: 10px 20px;
            transform: rotate(180deg) translateZ(0);
            direction: ltr;
            .fts-msg-left {
              width: 40px;
              padding: 10px 0;
              flex-shrink: 0;
              img {
                width: 40px;
                height: 40px;
              }
            }
            .fts-msg-center {
              flex-grow: 1;
              border-bottom: 1px solid #ececec;
              padding: 10px;
              .fts-msg-center-nickname {
                color: #999999;
              }
              .fts-msg-center-content {
                padding: 10px 0;
                word-break: break-word;
              }
            }
            .fts-msg-right {
              width: 100px;
              border-bottom: 1px solid #ececec;
              padding: 10px 0;
              flex-shrink: 0;
              .fts-msg-right-time {
                color: #999999;
              }
              .fts-msg-right-show-content {
                color: #576b95;
                cursor: pointer;
                visibility: hidden;
              }
            }
          }
          .fts-msg:hover {
            .fts-msg-right-show-content {
              visibility: visible;
            }
          }
          .fts-msg-loading {
            text-align: center;
            transform: rotate(180deg) translateZ(0);
            .fts-msg-loading-btn {
              padding: 10px 0;
              cursor: pointer;
              font-size: 13px;
              color: #576b95;
            }
          }
        }
      }
    }
    .fts-loading {
      height: 20px;
      width: 100%;
      text-align: center;
    }
  }
}


@media (max-width: 1024px) {
  .fts {
    display: flex;
    flex-direction: column;
    .fts-head {
      .fts-search {
        width: 100%;
      }
    }
    .fts-body {
      .fts-contact-container {
        width: 100%;
        height: 100%;
        overflow-y: scroll;
        overflow-x: hidden;
        .fts-contact {
          display: flex;
          padding: 15px;
          border-bottom: 1px solid #e7e7e7;
        }

      }
      .fts-msgs {
        position: absolute;
        height: 100%;
        overflow-x: hidden;
        top: 0;
        left: 100%;
        width: 100%;
        transition: transform 0.3s ease-in-out;
        background-color: #f5f5f5;
        z-index: 200;
        .fts-msgs-content {
          display: flex;
          flex-direction: column;
          .fts-msgs-head {
            display: none;
          }
          .fts-msgs-head-mobile {
            background-color: #e0e0e0;
            padding: 10px 0;
            text-align: right;
            .fts-msg-head-mobile-top-bar {
              padding: 0 10px;
            }
            .fts-msg-head-mobile-session {
              display: flex;
              text-align: left;
              padding: 10px;
              background-color: #f5f5f5;
              align-items: center;
              .fts-msg-head-mobile-session-img {
                width: 40px;
                height: 40px;
              }
              .fts-msg-head-mobile-session-title {
                padding-left: 10px;
                flex-grow: 1;
                overflow-x: hidden;
              }
              .fts-msg-head-mobile-session-toolbar {
                width: 40px;
                font-size: 18px;
              }
            }
          }
          .fts-msgs-roller {
            flex-grow: 1;
          }
        }
        .fts-chose {
          position: absolute;
          top: 0;
          left: 100%;
          width: 100%;
          height: 100%;
          transition: transform 0.3s ease-in-out;
          background-color: #f5f5f5;
          display: flex;
          flex-direction: column;
          .fts-chose-back-bar {
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #ececec;
            z-index: 100;
            .fts-chose-back {
              margin-left: 10px;
              cursor: pointer;
              color: dimgray;
            }
          }
          .fts-chose-msg-up-and-down {
            flex-grow: 1;
          }
        }
        .fts-chose.open {
          transform: translateX(-100%);
        }
      }
      .fts-msgs.open {
        transform: translateX(-100%);
      }
    }
  }
}

@media (min-width: 1025px) {
  .fts-msgs-head-mobile {
    display: none;
  }
  .fts-msgs-roller {
    height: 460px;
  }
  .fts {
    .fts-head {
      .fts-search {
        width: 500px;
      }
    }
    .fts-body {
      border-top: 1px solid #e7e7e7;
      .fts-contact-container {
        width: 220px;
        height: 100%;
        border-right: 1px solid #e7e7e7;
        overflow-y: scroll;
        overflow-x: hidden;
        flex-shrink: 0;
        .fts-contact {
          display: flex;
          padding: 15px;
          cursor: pointer;
          border-bottom: 1px solid #e7e7e7;
        }
      }
      .fts-msgs {
        flex-grow: 1;
        height: 100%;
        position: relative;
        overflow-x: hidden;
        .fts-msgs-content {

        }
        .fts-chose {
          position: absolute;
          top: 0;
          left: 100%;
          width: 100%;
          height: 100%;
          transition: transform 0.3s ease-in-out;
          background-color: #f5f5f5;
          .fts-chose-back-bar {
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #ececec;
            z-index: 100;
            .fts-chose-back {
              margin-left: 10px;
              cursor: pointer;
              color: dimgray;
            }
          }
          .fts-chose-msg-up-and-down {
            height: 460px;
          }
        }
        .fts-chose.open {
          transform: translateX(-100%);
        }
      }
    }
  }
  // 以下是滚动条样式
  /* 隐藏默认的滚动条轨道和拇指 */
  /* 隐藏默认的滚动条轨道和拇指 */
  .fts-msgs-roller::-webkit-scrollbar,
  .fts-contact-container::-webkit-scrollbar {
    width: 0.429rem;
    background: transparent; /* 使滚动条轨道背景透明 */
  }

  /* 鼠标悬停时显示滚动条轨道 */
  .fts-msgs-roller:hover::-webkit-scrollbar,
  .fts-contact-container:hover::-webkit-scrollbar {
    width: 0.429rem; /* 设置滚动条宽度 */
  }

  /* 滚动条轨道样式 */
  .fts-msgs-roller:hover::-webkit-scrollbar-track-piece,
  .fts-contact-container:hover::-webkit-scrollbar-track-piece {
    border-radius: 0.571rem; /* 设置滚动条轨道圆角 */
  }

  /* 滚动条拇指样式 */
  .fts-msgs-roller:hover::-webkit-scrollbar-thumb,
  .fts-contact-container:hover::-webkit-scrollbar-thumb {
    background-color: #c8c9cc; /* 设置滚动条拇指背景颜色 */
    border-radius: 0.571rem; /* 设置滚动条拇指圆角 */
  }

  /* 鼠标悬停在滚动条拇指上时的样式 */
  .fts-msgs-roller:hover::-webkit-scrollbar-thumb:hover,
  .fts-contact-container:hover::-webkit-scrollbar-thumb:hover {
    background-color: #b0b0b0; /* 鼠标悬停时滚动条拇指背景颜色 */
  }
}

</style>