<script setup>
import {onUnmounted, reactive, ref, watch, getCurrentInstance} from 'vue'
import {sessions as getSessions, contactSearch} from "@/api/msg.js";
import {msgsSearchTop5} from "@/api/fts.js";
import {useStore} from "vuex";
import {useRouter, useRoute} from "vue-router";
import defaultImage from '@/assets/default-head.svg';
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {getContactHeadById, getContactName, getContactById} from "@/utils/contact.js";
import UserDetail from "@/components/tools/tabs/UserDetail.vue";
import FTSMsgs from "@/components/fts/FTSMsgs.vue";
import {toBase64} from "js-base64";

const store = useStore();
const router = useRouter();
const route = useRoute();
const {proxy} = getCurrentInstance();

const page = ref(1);
const size = ref(20);
const loading = ref(false);
const noMore = ref(false);

const sessions = reactive([]);

const contactContainer = ref(null);

const sysSessionId = route.params.sessionId;
const userName = route.query.userName;

const selectedItem = ref(null)

const selectItem = (wxId) => {
  selectedItem.value = wxId;
  // const targetPath = '/comment/' + session.strUsrName;

  router.push({ name: 'chat', params: { sessionId: sysSessionId, id: wxId} });
  // router.push(targetPath);
}

// 移动端自动打开
if (userName) {
  selectItem(userName);
}

const deSelectItem = () => {
  selectedItem.value = null;
}

const formatDate = (timestamp) => {
  const date = new Date(timestamp * 1000);
  const now = new Date();

  // 获取今天的日期
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  // 获取昨天的日期
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  // 获取年、月、日、小时、分钟
  // const year = date.getFullYear();
  const year = String(date.getFullYear()).slice(-2); // 只取年份的后两位
  const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  // 根据日期判断输出格式
  if (date >= today) {
    return `${hours}:${minutes}`;
  } else if (date >= yesterday) {
    return `昨天 ${hours}:${minutes}`;
  } else {
    return `${year}/${month}/${day}`;
  }
};

const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}

const load = () => {
  // 没有更多数据不再获取了
  if (noMore.value) {
    return;
  }
  loading.value = true;
  // 加载用户聊天会话数据
  getSessions(page.value, size.value).then(resp => {
    sessions.push(...resp);
    page.value = page.value + 1;
    if (resp.length < size.value) {
      noMore.value = true;
    }
    loading.value = false;
  }).catch(e => {
    loading.value = false;
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

const onScroll = () => {
  let sub = contactContainer.value.scrollHeight - contactContainer.value.clientHeight - contactContainer.value.scrollTop;
  if (Math.abs(sub) <= 1) {
    load();
  }
}

// 加载session数据
load();


// 搜索
const search = ref('');
const contacts = reactive([]);
const chatRooms = reactive([]);
const chatSearchContact = reactive([]);
const chatSearchContactCount = ref(0);
const sLoading = ref(false);

const clear = () => {
  search.value = '';
}
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


// 输入停止1秒后执行的函数
const handleInputEnd = () => {
  sLoading.value = true;
  if (search.value) {
    // 联系人搜索
    contactSearch(search.value).then(resp => {
      if ('contacts' in resp) {
        contacts.push(...resp.contacts);
      }
      if ('chatrooms' in resp) {
        chatRooms.push(...resp.chatrooms);
      }
      sLoading.value = false;
    }).catch(e => {
      sLoading.value = false;
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
  } else {
    contacts.length = 0;
    chatRooms.length = 0;
    chatSearchContact.length = 0;
    chatSearchContact.length = 0;
  }
};

// 清除计时器以防内存泄漏
onUnmounted(() => {
  if (timeout) clearTimeout(timeout);
});

// enter 事件搜索
const inputEnter = () => {
  if (timeout) clearTimeout(timeout);
  handleInputEnd();
}

// 全文搜索
const openFtsPopup = (contact) => {
  console.log("外部选中 contact", contact);
  proxy.$popup.open(FTSMsgs,{ match: search.value, contact: contact },{ title: '搜聊天记录', width: '800px', height: '600px' });
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
  <div class="main-comment">
    <div class="main-session">
      <div class="session-search-container">
        <div class="weui-search-bar weui-search-bar_filled-grey weui-search-bar_focusing" id="searchBar">
          <div id="searchForm" role="combobox" aria-haspopup="true" aria-expanded="false" aria-owns="searchResult" class="weui-search-bar__form">
            <div aria-hidden="false" id="searchBox" class="weui-search-bar__box">
              <i class="weui-icon-search"></i>
              <input v-model="search" @keyup.enter="inputEnter" type="search" aria-controls="searchResult" class="weui-search-bar__input" id="searchInput" placeholder="搜索" required/>
              <div class="weui-search-bar__mask"></div>
              <a href="javascript:" role="button" title="清除" class="weui-icon-clear" id="searchClear" @click="clear"></a>
            </div>
          </div>
        </div>
      </div>
      <div class="session-items-container" v-if="search">
        <div class="session-items-fix-roller">
          <div class="loading" v-if="sLoading" >
            <font-awesome-icon class="loading-icon" :icon="['fas', 'spinner']"/>
          </div>
          <div v-else>
            <div class="session-group" v-if="contacts.length > 0">
              <div class="session-items-title">联系人</div>
              <ul class="items-ul">
                <li class="item" v-for="contact in contacts" @click="selectItem(contact.username)">
                  <div class="item-header">
                    <img :src="getContactHeadById(contact.username)" @error="setDefaultImage" alt="header">
                  </div>
                  <div class="item-msg no-wrap-text">
                    <p class="item-msg-title">{{getContactById(contact.username).nickname}}</p>
                    <p class="item-msg-desc" v-if="getContactById(contact.username).remark" >{{getContactById(contact.username).remark}}</p>
                  </div>
                </li>
              </ul>
            </div>
            <div class="session-group" v-if="chatRooms.length > 0">
              <div class="session-items-title">群聊</div>
              <ul class="items-ul">
                <li class="item" v-for="chatroom in chatRooms" @click="selectItem(chatroom.username)">
                  <div class="item-header">
                    <img :src="getContactHeadById(chatroom.username)" @error="setDefaultImage" alt="header">
                  </div>
                  <div class="item-msg no-wrap-text">
                    <p class="item-msg-title">{{getContactById(chatroom.username).nickname}}</p>
                    <p class="item-msg-desc" v-if="getContactById(chatroom.username).remark" >{{getContactById(chatroom.username).remark}}</p>
                  </div>
                </li>
              </ul>
            </div>
            <div class="session-group" v-if="chatSearchContactCount > 0">
              <div class="session-items-title">聊天记录</div>
              <ul class="items-ul">
                <li class="item" v-for="c in chatSearchContact" @click="openFtsPopup(c)">
                  <div class="item-header">
                    <img :src="getContactHeadById(c.username)" @error="setDefaultImage" alt="header">
                  </div>
                  <div class="item-msg no-wrap-text">
                    <p class="item-msg-title">{{ getContactName(c.username) }}</p>
                    <p class="item-msg-desc" v-if="c.count === 1">
                      {{ c.content }}
                    </p>
                    <p class="item-msg-desc" v-else>
                      {{ c.count }}条聊天记录
                    </p>
                  </div>
                </li>
                <li class="item" v-if="chatSearchContactCount > 5">
                  <p class="item-btn" @click="openFtsPopup(undefined)">显示全部({{ chatSearchContactCount }})</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="session-items-container" v-else ref="contactContainer" @scroll="onScroll">
        <div class="session-items-fix-roller">
          <ul class="items-ul">
            <li class="item"
                v-for="(session, idx) in sessions" :key="session.username"
                :class="{ 'item-active': selectedItem === session.username }"
                @click="selectItem(session.username)">
              <div class="item-header">
                <img :src="getContactHeadById(session.username)" @error="setDefaultImage" alt="header">
              </div>
              <div class="item-msg no-wrap-text">
                <p class="item-msg-title">{{ getContactName(session.username) }}</p>
                <p class="item-msg-desc">{{ session.summary }}</p>
              </div>
              <div class="item-info">
                <p class="item-info-time">{{ formatDate(session.modify_timestamp) }}</p>
              </div>
            </li>
          </ul>
        </div>
        <p class="load-more" v-if="!noMore" :class="{'load-more-hide': noMore}" @click="load">
          <font-awesome-icon class="loading-icon" v-if="loading" :icon="['fas', 'spinner']"/>
          <p v-else>加载更多</p>
        </p>
      </div>
    </div>
    <div class="main-msg" :class="{'open': selectedItem}">
      <router-view :key="$route.fullPath" @goBack="deSelectItem"/>
    </div>
  </div>
</template>

<style scoped lang="less">
@import "/src/style/main/comment/comment.less";
</style>