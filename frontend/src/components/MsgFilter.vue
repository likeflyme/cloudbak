<script setup>
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {nextTick, reactive, ref} from "vue";
import {parseXml, getReferFileName, getThumbFromStringContent, getVoiceLength, parseImg, formatFilterMsgDate} from "@/utils/common.js";
import {useStore} from "vuex";
import defaultImage from '@/assets/default-head.svg';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';
import {filterDateFormatQuery, filterDateFormatView} from "../utils/common.js";
import {get_msg_desc} from "../utils/msgtp.js";
import {chatroomInfo, msgsFilter, msgsByLocalId, msgs as queryMsgs} from "../api/msg.js";
import cleanedImage from '@/assets/cleaned.jpeg';
import AudioPlayer from "./AudioPlayer.vue";
import ChatFile from "./ChatFile.vue";
import {getContactById, getContactHeadById, getContactName} from "../utils/contact.js";

dayjs.locale('zh-cn');

const store = useStore();
const props = defineProps({
  strUsrName: String,
  title: String
})
const selected = ref(false);
const selectedType = reactive({});
const msg_list = reactive([]);
const isLoading = ref(false);
const wxVersion = store.getters.getClientVersion;
// 滚动条反向滚动以及数据加载相关变量
const chatContainer = ref(null);
const isTop = ref(false);
const isBottom = ref(false);
// 展示上下文按钮
const isShowContext = ref(false);
// 日期选择相关变量
const date = ref();
const datepicker = ref();
const queryDayData = {
  type: 7,
  title: '日期',
  width: '120px',
  icon: ['fas', 'calendar-days']
}
// 是否为通过id定位查询
const isQueryByLocalId = ref(false);
// 普通查询
const query = reactive({
  username: props.strUsrName,
  page: 1,
  size: 20,
  start: 0,
  start_db: '',
  filter_mode: 0,
  filter_text: '',
  filter_day: '',
  filter_media: false,
  noMoreMsg: false,
  isLoading: false,
  isTop: false
});

// 反向查询
const queryReverse = reactive({
  username: props.strUsrName,
  page: 0,
  size: 20,
  start: 0,
  start_db: '',
  filter_mode: 0,
  filter_text: '',
  filter_day: '',
  filter_media: false,
  noMoreMsg: false,
  isLoading: false,
  isBottom: false
});

// 消息定位查询
const querySequence = reactive({
  username: props.strUsrName,
  filter_sequence: 0,
  page: 0,
  size: 20,
  start: 0,
  start_db: '',
  filter_mode: 0,
  noMoreMsg: false,
  isLoading: false,
  isTop: false
});

// 消息定位查询反向查询
const querySequenceReverse = reactive({
  username: props.strUsrName,
  filter_sequence: 0,
  page: 1,
  size: 20,
  start: 0,
  start_db: '',
  filter_mode: 1,
  noMoreMsg: false,
  isLoading: false,
  isBottom: false
});

const filterTypes = [
  {
    type: 1,
    title: '文件',
    width: '90px',
    icon: ['fas', 'file']
  },{
    type: 2,
    title: '图片视频',
    width: '170px',
    icon: ['fas', 'image']
  }
  // ,{
  //   type: 3,
  //   title: '链接',
  //   width: '100px',
  //   icon: ['fas', 'link']
  // }
  // ,{
  //   type: 4,
  //   title: '音乐与音频',
  //   width: '170px',
  //   icon: ['fas', 'volume-high']
  // }
  // ,{
  //   type: 5,
  //   title: '小程序',
  //   width: '120px',
  //   icon: ['fas', 'globe']
  // }
  // ,{
  //   type: 6,
  //   title: '视频号',
  //   width: '120px',
  //   icon: ['fas', 'video']
  // }
  // ,{
  //   type: '8',
  //   title: '群成员',
  //   width: '120px',
  //   icon: ['fas', 'users']
  // },
];

// 图片查看器配置
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

const setDefaultImage = (event) => {
  event.target.src = defaultImage;
}
const selectFilterType = (t) => {
  console.log(t);
  Object.assign(selectedType, t);
  clearQuery();
  selected.value = true;
  query.filterType = t.type;
  if (t.type === 1) {
    query.filter_file = true;
  } else if (t.type === 2) {
    query.filter_media = true;
  }
  console.log("选择后：", query);
  loadData();
}
const clear = () => {
  selected.value = false;
  query.filterText = '';
  query.filter_file = false;
  query.filter_media = false;
  query.filter_day = '';
  clearAndSearch();
}
const clearSelectType = () => {
  console.log("clearSelectType");
  selected.value = false;
  query.filterType = 0;
  clearAndSearch();
}

const clearQuery = () => {
  query.noMoreMsg = false;
  query.start = 0;
  query.start_db = '';
  query.page = 1;
  query.filter_text = '';
  query.filter_media = false;
  query.filter_file = false;
  query.filter_day = '';
  queryReverse.noMoreMsg = false;
  queryReverse.start = 0;
  queryReverse.start_db = '';
  queryReverse.page = 0;
  queryReverse.filter_media = false;
  queryReverse.filter_file = false;
  queryReverse.filter_day = '';
  querySequence.start = 0;
  querySequence.start_db = '';
  querySequence.page = 0;
  querySequence.noMoreMsg = false;
  querySequenceReverse.start = 0;
  querySequenceReverse.start_db = '';
  querySequenceReverse.page = 0;
  querySequenceReverse.noMoreMsg = false;
  isQueryByLocalId.value = false;
  msg_list.length = 0;
  isTop.value = false;
}

// 回归初始化查询条件并加载数据函数
const clearAndSearch = (showContext = false) => {
  isShowContext.value = showContext;
  clearQuery();
  loadData();
}

const enterText = () => {
  isShowContext.value = true;
  clearQuery();
  query.filter_text = query.filterText;
  loadData();
}

// 单纯的加载数据函数
const loadData = () => {
  if (!query.noMoreMsg && query.isLoading === false) {
    query.isLoading = true;
    console.log("查询前: ", query);
    queryMsgs(query).then(resp => {
      query.isLoading = false;
      query.start = resp.start;
      query.start_db = resp.start_db;
      if (resp.messages.length < query.size) {
        query.noMoreMsg = true;
      }
      if (resp.messages.length > 0) {
        if (wxVersion === 'win.v3') {
          msg_list.push(...resp.messages.map(m => m.windows_v3_properties));
        } else if (wxVersion === 'win.v4') {
          msg_list.push(...resp.messages.map(m => m.windows_v4_properties));
        }
      }
    }).catch(e => {
      query.isLoading = false;
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

// 反向加载数据函数
const loadDataReverse = () => {
  if (!queryReverse.noMoreMsg && queryReverse.isLoading === false) {
    queryReverse.isLoading = true;
    queryMsgs(queryReverse).then(resp => {
      queryReverse.isLoading = false;
      if (resp.messages.length < queryReverse.size) {
        queryReverse.noMoreMsg = true;
      }
      queryReverse.start = resp.start;
      queryReverse.start_db = resp.start_db;
      if (resp.messages.length > 0) {
        // 添加数据前，记录当前页面高度
        const previousScrollHeight = chatContainer.value.scrollHeight;
        const previousScrollTop = chatContainer.value.scrollTop;
        // 添加到数据列表头部
        // resp.messages.reverse()
        if (wxVersion === 'win.v3') {
          msg_list.unshift(...resp.messages.reverse().map(m => m.windows_v3_properties));
        } else if (wxVersion === 'win.v4') {
          msg_list.unshift(...resp.messages.reverse().map(m => m.windows_v4_properties));
        }
        nextTick(() => {
          const newScrollHeight = chatContainer.value.scrollHeight;
          chatContainer.value.scrollTop = newScrollHeight - previousScrollHeight + previousScrollTop;
        })
      }
    }).catch(e => {
      queryReverse.isLoading = false;
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

// 消息定位查询
const loadDataBySequence = () => {
  if (!querySequence.noMoreMsg && querySequence.isLoading === false) {
    console.log("loadDataByLocalId");
    querySequence.isLoading = true;
    isQueryByLocalId.value = true;
    querySequence.page = querySequence.page + 1;
    queryMsgs(querySequence).then(resp => {
      querySequence.isLoading = false;
      if (resp.messages.length < querySequence.size) {
        querySequence.noMoreMsg = true;
      }
      if (resp.messages.length > 0) {
        querySequence.start = resp.start;
        querySequence.start_db = resp.start_db;
        // 添加到数据列表
        if (wxVersion === 'win.v3') {
          msg_list.push(...resp.messages.map(m => m.windows_v3_properties));
        } else if (wxVersion === 'win.v4') {
          msg_list.push(...resp.messages.map(m => m.windows_v4_properties));
        }
      }
    }).catch(e => {
      querySequence.isLoading = false;
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

// 消息定位反向查询
const loadDataBySequenceReverse = () => {
  if (!querySequenceReverse.noMoreMsg && querySequenceReverse.isLoading === false) {
    console.log("loadDataByLocalIdReverse");
    querySequenceReverse.isLoading = true;
    isQueryByLocalId.value = true;
    querySequenceReverse.page = querySequenceReverse.page + 1;
    queryMsgs(querySequenceReverse).then(resp => {
      querySequenceReverse.isLoading = false;
      if (resp.messages.length < querySequenceReverse.size) {
        querySequenceReverse.noMoreMsg = true;
      }
      if (resp.messages.length > 0) {
        querySequenceReverse.start = resp.start;
        querySequenceReverse.start_db = resp.start_db;
        // 添加数据前，记录当前页面高度
        const previousScrollHeight = chatContainer.value.scrollHeight;
        const previousScrollTop = chatContainer.value.scrollTop;
        // 添加到数据列表
        if (wxVersion === 'win.v3') {
          msg_list.unshift(...resp.messages.reverse().map(m => m.windows_v3_properties));
        } else if (wxVersion === 'win.v4') {
          msg_list.unshift(...resp.messages.reverse().map(m => m.windows_v4_properties));
        }
        nextTick(() => {
          const newScrollHeight = chatContainer.value.scrollHeight;
          chatContainer.value.scrollTop = newScrollHeight - previousScrollHeight + previousScrollTop;
        })
      }
    }).catch(e => {
      querySequenceReverse.isLoading = false;
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

// 页面初始化加载数据
clearAndSearch();

// 加载更多数据
const loadMore = () => {
  if (isQueryByLocalId.value) {
    loadDataBySequence();
  } else {
    query.page = query.page + 1;
    query.filterMode = 1;
    loadData();
  }
};

// 反向加载更多数据
const loadReverse = () => {
  if (isQueryByLocalId.value) {
    loadDataBySequenceReverse();
  } else {
    queryReverse.page = queryReverse.page + 1;
    loadDataReverse();
  }
};

// 消息定位查询
const loadLocation = (m) => {
  querySequence.start_db = m.db_name;
  querySequence.filter_sequence = m.Sequence;
  querySequenceReverse.filter_sequence = m.Sequence;
  msg_list.length = 0;
  // 关闭查看上下文的按钮
  isShowContext.value = false;
  loadDataBySequence()
}

// 滚动条反向滚动以及数据加载相关函数
// 滚动加载
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

// 反向滚动
const onWheel = (event) => {

  // 阻止默认滚动行为，以便完全自定义滚动效果
  event.preventDefault();

  // 根据滚轮事件的 deltaY 属性调整滚动条位置
  const delta = event.deltaY;

  // 根据滚轮方向调整滚动条位置，注意方向是反的
  chatContainer.value.scrollTop -= delta;
  if (chatContainer.value.scrollTop + chatContainer.value.clientHeight === chatContainer.value.scrollHeight) {
    loadMore();
  }
  if (chatContainer.value.scrollTop === 0) {
    if (query.filterType === 7 || isQueryByLocalId.value) {
      loadReverse();
    }
  }
};

const onMove = () => {
  // 避免手机端误差
  const sub  = chatContainer.value.scrollHeight - chatContainer.value.scrollTop - chatContainer.value.clientHeight;
  if (Math.abs(sub) < 2) {
    // window.alert('loadMore');
    loadMore();
  }
  if (chatContainer.value.scrollTop === 0) {
    if (query.filterType === 7 || isQueryByLocalId.value) {
      console.log('loadReverse')
      loadReverse();
    }
  }
}

// 日期选择
const datePicked = (modelData) => {
  let view = filterDateFormatView(modelData);
  let queryValue = filterDateFormatQuery(modelData);
  clearQuery();
  query.filter_day = queryValue;
  query.filterType = 7;
  queryReverse.filter_day = queryValue;
  queryDayData.title = view;
  loadData();
}

// 群聊用户名
const chatRoomNameMap = reactive({});
const isChatRoom = props.strUsrName.includes('@chatroom');
// 群聊，加载群聊信息（人数）
if (isChatRoom) {
  chatroomInfo(props.strUsrName).then(data => {
    if(data) {
      if (data.members) {
        for (let i = 0; i < data.members.length; i++) {
          let m = data.members[i]
          chatRoomNameMap[m.username] = m;
        }
      }
    }
  });
}

/**
 * 有备注先用备注，其次群备注，最后昵称
 * @param m
 * @returns {*}
 */
const displayName = (m) => {
  let contact = getContactById(m.sender);
  if (contact) {
    return getContactName(m.sender);
  }
  let member = chatRoomNameMap[m.sender];
  if (member) {
    if (member.remark) {
      return member.remark;
    } else {
      return member.nickname;
    }
  }
  return '';
}

</script>

<template>
  <div class="filter-container">
    <div class="filter-head">
      <div class="head-title">
        <p class="head-title-title">
          {{ title }}
        </p>
        <p class="head-title-fill"></p>
        <p class="head-title-tools" @click="$emit('close-filter')">
          <font-awesome-icon :icon="['fas', 'xmark']"/>
        </p>
      </div>
      <div class="head-search">
        <div class="weui-search-bar weui-search-bar_outlined" id="searchBar">
          <div id="searchForm" role="combobox" aria-haspopup="true" aria-expanded="false" aria-owns="searchResult" class="weui-search-bar__form">
            <div class="weui-search-bar__box">
              <div class="select-type" v-if="selected" @click="clearSelectType">
                <font-awesome-icon class="select-type-clear select-icon" :icon="selectedType.icon"/>
                <p>{{ selectedType.title }}</p>
                <font-awesome-icon class="select-type-clear" :icon="['fas', 'xmark']"/>
              </div>
              <i v-else class="weui-icon-search"></i>
              <input type="search" aria-controls="searchResult" v-model="query.filterText" class="weui-search-bar__input" id="searchInput" @keydown.enter="enterText"/>
              <a v-if="selected || query.filterText" href="javascript:" role="button" title="清除" class="weui-icon-clear" @click="clear"></a>
            </div>
          </div>
        </div>
      </div>
      <div class="head-filter">
        <ul class="filter-ul">
          <li class="filter-item" v-for="t in filterTypes" @click="selectFilterType(t)">{{ t.title }}</li>
          <li class="filter-item">
            <VueDatePicker v-model="date"
                           @update:model-value="datePicked"
                           ref="datepicker"
                           :enable-time-picker="false"
                           locale="zh-cn"
                           style="z-index: 1000">
              <template #trigger>
                <p>日期</p>
              </template>
            </VueDatePicker>
          </li>
        </ul>
      </div>
    </div>
    <div class="msg-body"
         ref="chatContainer"
         @wheel="onWheel"
         @scroll="onScroll"
         @touchmove="onMove"
         v-viewer="imageOptions">
      <div class="load-more" v-if="!isQueryByLocalId && query.filterType === 7 && !queryReverse.noMoreMsg">
        <a href="javascript:void(0)" @click="loadReverse">
          <font-awesome-icon class="loading-icon" v-if="queryReverse.isLoading" :icon="['fas', 'spinner']"/>
          <p v-else>查看更多消息</p>
        </a>
      </div>
      <div class="load-more" v-else-if="isQueryByLocalId && !querySequenceReverse.noMoreMsg">
        <a href="javascript:void(0)" @click="loadReverse">
          <font-awesome-icon class="loading-icon" v-if="querySequenceReverse.isLoading" :icon="['fas', 'spinner']"/>
          <p v-else>查看更多消息</p>
        </a>
      </div>
      <div class="chat-grow"></div>
      <ul class="msg-ul" v-if="msg_list.length > 0">
        <li v-for="m in msg_list" class="msg-li">
          <div class="msg-head">
            <img alt="" :src="getContactHeadById(m.sender)" @error="setDefaultImage" class="exclude"/>
          </div>
          <div class="msg-right">
            <div class="msg-title">
              <p class="msg-nickname">{{ displayName(m)}}</p>
              <p class="msg-grow"></p>
              <p class="msg-time">{{ formatFilterMsgDate(m.CreateTime) }}</p>
            </div>
            <div class="msg-content">
              <!-- 文本 -->
              <div v-if="m.Type === 1 && m.SubType === 0" class="msg-base msg-text">
                {{ m.StrContent }}
              </div>
              <!-- 图片 -->
              <div v-else-if="m.Type === 3 && m.SubType === 0" class="msg-base msg-images">
                <img
                    :src="'/api/resources/relative-resource?relative_path=' + m.thumb + '&session_id=' + store.getters.getCurrentSessionId"
                    :data-original="m.source ? '/api/resources/relative-resource?relative_path=' + m.source + '&session_id=' + store.getters.getCurrentSessionId : cleanedImage"
                    alt=""/>
              </div>
              <!-- 语音 -->
              <div v-else-if="m.Type === 34 && m.SubType === 0" class="msg-base msg-media">
                <AudioPlayer class="audio-player"
                    :src="`/api/resources/media?MsgSvrID=${m.MsgSvrIDStr}&session_id=${store.getters.getCurrentSessionId}&db_no=${m.DbNo}`"
                    :text="getVoiceLength(m.StrContent)"/>
              </div>
              <!-- 视频 -->
              <div v-else-if="m.Type === 43 && m.SubType === 0" class="msg-base msg-video">
                <video controls width="150" :poster="`/api/resources/relative-resource?relative_path=${m.thumb}&session_id=${store.getters.getCurrentSessionId}`">
                  <source v-if="m.source" :src="`/api/resources/relative-resource?relative_path=${m.source}&session_id=${store.getters.getCurrentSessionId}&source_type=video`" type="video/mp4" />
                </video>
              </div>
              <div class="msg-base msg-chat-file" v-else-if="m.Type === 49 && m.SubType === 6" >
                <ChatFile :msg="m"></ChatFile>
              </div>
              <div v-else class="msg-base msg-no-support">
                不支持的类型：{{ get_msg_desc(m.Type, m.SubType) }}
              </div>
              <div class="msg-ref" v-if="isShowContext">
                <p class="msg-checkout" @click="loadLocation(m)">查看上下文</p>
              </div>
            </div>
          </div>
        </li>
      </ul>
      <p class="no-msg" v-else-if="msg_list.length === 0 && !isLoading"> 无内容 </p>
      <!-- 非定位查询，加载更多 -->
      <div class="load-more" v-if="!isQueryByLocalId && !query.noMoreMsg">
        <a href="javascript:void(0)" @click="loadMore">
          <font-awesome-icon class="loading-icon" v-if="query.isLoading" :icon="['fas', 'spinner']"/>
          <p v-else>查看更多消息</p>
        </a>
      </div>
      <!-- 定位查询，加载更多 -->
      <div class="load-more" v-else-if="isQueryByLocalId && !querySequence.noMoreMsg">
        <a href="javascript:void(0)" @click="loadMore">
          <font-awesome-icon class="loading-icon" v-if="querySequence.isLoading" :icon="['fas', 'spinner']"/>
          <p v-else>查看更多消息</p>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
@import "/src/style/components/msg-filter.less";
</style>