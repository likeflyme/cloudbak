<script setup>
import {useStore} from "vuex";
import {onUnmounted, reactive, ref, watch} from "vue";
import {contactPage} from "../../../api/msg.js";
import {useRoute, useRouter} from "vue-router";
import defaultImage from '@/assets/default-head.svg';
import {getContactHeadById, getContactName} from "../../../utils/contact.js";

const store = useStore();
const router = useRouter();
const route = useRoute();

const sessionId = route.params.sessionId;

const queryChatroom = reactive({
  search: '',
  page: 1,
  size: 20,
  contact_type: 3,
  noMore: false,
  loading: false
});

const queryContact = reactive({
  search: '',
  page: 1,
  size: 20,
  noMore: false,
  loading: false
});



const page = ref(1);
const size = ref(20);
const input = ref('');
// 联系人
const contact = reactive([]);
// 群聊
const chatRoom = reactive([]);
// 公众号
const gh_contact = reactive([]);
// 企业联系人
const openim_contact = reactive([]);
const selectedItem = ref('');
const search = ref('');
const noMore = ref(false);

const clear = () => {
  search.value = '';
  load();
  loadChatroom();
}

const load = () => {
  if (queryContact.noMore) return;
  queryContact.loading = true;
  queryContact.search = search.value;
  contactPage(queryContact).then(data => {
    if (data) {
      if (data.length > 0) {
        contact.push(...data);
      } else {
        queryContact.noMore = true;
      }
      queryContact.page = queryContact.page + 1;
    }
  }).finally(() => {
    queryContact.loading = false;
  });
}

const loadChatroom = () => {
  if (queryChatroom.noMore) return;
  queryChatroom.loading = true;
  queryChatroom.search = search.value;
  contactPage(queryChatroom).then(data => {
    if (data) {
      console.log(data.length);
      if (data.length > 0) {
        chatRoom.push(...data);
      } else {
        queryChatroom.noMore = true;
      }
      queryChatroom.page = queryChatroom.page + 1;
    }
  }).finally(() => {
    queryChatroom.loading = false;
  });
}

// 加载数据
load();
loadChatroom();

const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}

const contactContainer = ref(null);

const onScroll = () => {
  let sub = contactContainer.value.scrollHeight - contactContainer.value.clientHeight - contactContainer.value.scrollTop;
  if (Math.abs(sub) <= 1) {
    load();
  }
}

const goChatRoomInfo = (contact) => {
  selectedItem.value = contact.username;
  router.push({ name: 'chat-room-info', params: {id: contact.username} });
}

const goUserInfo = (contact) => {
  selectedItem.value = contact.username;
  store.commit('setAddrShowUser', contact);
  router.push({ name: 'user-info', params: { sessionId: sessionId, id: contact.username} });
}

// 搜索
let timeout = null;
const sLoading = ref(false);


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
  noMore.value = false;
  sLoading.value = true;
  console.log('用户停止输入，执行函数');
  console.log(search.value);
  contact.length = 0;
  chatRoom.length = 0;
  queryContact.page = 1;
  queryChatroom.page = 1;
  load();
  loadChatroom();
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

const closeInfo = () => {
  selectedItem.value = null;
}
</script>

<template>
  <div class="main-addr">
    <div class="addr-left">
      <div class="addr-search-container">
        <div class="weui-search-bar weui-search-bar_filled-grey weui-search-bar_focusing" id="searchBar">
          <div id="searchForm" role="combobox" aria-haspopup="true" aria-expanded="false" aria-owns="searchResult" class="weui-search-bar__form">
            <div aria-hidden="false" id="searchBox" class="weui-search-bar__box">
              <i class="weui-icon-search"></i>
              <!--              <span class="weui-search-bar__words">微信</span>-->
              <input v-model="search" @keyup.enter="inputEnter" type="search" aria-controls="searchResult" class="weui-search-bar__input" id="searchInput" placeholder="搜索" required/>
              <div class="weui-search-bar__mask"></div>
              <a href="javascript:" role="button" title="清除" class="weui-icon-clear" id="searchClear" @click="clear"></a>
            </div>
          </div>
        </div>
      </div>
      <div class="addr-items-container" ref="contactContainer" @scroll="onScroll">
        <ul class="addr-group" v-if="chatRoom.length > 0">
          <li class="group-title">群聊</li>
          <li class="group-item"
              :class="{'item-active': selectedItem === c.username}"
              v-for="c in chatRoom"
              @click="goChatRoomInfo(c)">
            <img class="item-img"
                 :src="getContactHeadById(c.username)"
                 @error="setDefaultImage"
                 alt="">
            <p class="item-title">{{ getContactName(c.username) }}</p>
          </li>
          <li class="load-more" v-if="!queryChatroom.noMore" @click="loadChatroom">
            加载更多
          </li>
        </ul>
        <ul class="addr-group" v-if="contact.length > 0">
          <li class="group-title">联系人</li>
          <li class="group-item"
              v-for="(c,index) in contact"
              :class="{'item-active': selectedItem === c.username}"
              @click="goUserInfo(c)">
            <img class="item-img"
                 :src="getContactHeadById(c.username)"
                 @error="setDefaultImage"
                 alt="">
            <p class="item-title">{{ getContactName(c.username) }}</p>
          </li>
        </ul>
        <p class="load-more"> 加载更多 </p>
      </div>
    </div>
    <div class="addr-right" :class="{'open': selectedItem}">
      <router-view :key="$route.fullPath" @goBack="closeInfo"/>
    </div>
  </div>
</template>

<style scoped lang="less">
@import "/src/style/main/addressbook/address-book.less";
</style>