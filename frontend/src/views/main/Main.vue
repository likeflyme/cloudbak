<template>
  <div class="main-container">
    <div class="main-sidebar">
      <ul class="item-container">
        <li class="item" @click="openSessionTools">
          <img class="u-header" :src="store.getters.getCurrentSession.smallHeadImgUrl" alt="" v-if="store.getters.getClientVersion === 'win.v3'"/>
          <img class="u-header" :src="`/api/resources/relative-resource?relative_path=${store.getters.getCurrentSession.smallHeadImgUrl}&session_id=${store.getters.getCurrentSessionId}`" alt="" v-else/>
        </li>
        <li class="item" v-for="m in menu">
          <font-awesome-icon class="item-icon"
                             :class="{'item-icon-active': selectedItem === m.id }"
                             :icon="m.icon"
                             :title="m.title"
                             @click="selectItem(m.id)"/>
        </li>
      </ul>
      <ul class="sidebar-bottom">
        <li class="item-icon" @click="openSessionTools()" ref="toggleButton">
          <font-awesome-icon :icon="['fas', 'bars']" />
        </li>
      </ul>
    </div>
    <div class="main-right" v-if="checked">
      <router-view :key="routerKey"/>
    </div>
    <div class="weui-tab">
      <div role="tablist" aria-label="选项卡标题" class="weui-tabbar">
        <div id="tab1"
             @click="selectItem('comment')"
             :class="{'weui-bar__item_on': selectedItem === 'comment'}"
             role="tab" aria-labelledby="t1_title" aria-describedby="t1_tips" aria-selected="true" aria-controls="panel1" class="weui-tabbar__item">
          <div id="t1_tips" aria-hidden="true" style="display: inline-block; position: relative;">
            <font-awesome-icon class="weui-tabbar__icon" :icon="['fas', 'comment']" />
          </div>
          <p id="t1_title" aria-hidden="true" class="weui-tabbar__label">聊天</p>
        </div>
        <div id="tab2"
             @click="selectItem('address-book')"
             :class="{'weui-bar__item_on': selectedItem === 'address-book'}"
             role="tab" aria-labelledby="t2_title" aria-selected="false" aria-controls="panel2" class="weui-tabbar__item">
          <font-awesome-icon class="weui-tabbar__icon" :icon="['fas', 'address-book']" />
          <p aria-hidden="true" id="t2_title" class="weui-tabbar__label">通讯录</p>
        </div>
        <div id="tab4"
             @click="selectItem('user')"
             :class="{'weui-bar__item_on': selectedItem === 'user'}"
             role="tab" aria-labelledby="t4_title" aria-selected="false" aria-controls="panel4" class="weui-tabbar__item">
          <font-awesome-icon class="weui-tabbar__icon" :icon="['fas', 'user']" />
          <p class="weui-tabbar__label" aria-hidden="true" id="t4_title">我</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useRoute, useRouter} from "vue-router";
import {contact} from "../../api/msg.js";
import {sessionCheck} from "../../api/user.js";
import {useStore} from "vuex";
import {getCurrentInstance, onMounted, onUnmounted, reactive, ref} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import SessionTools from "../../components/tools/SessionTools.vue";

const { proxy } = getCurrentInstance();
const store = useStore();
const router = useRouter();
const route = useRoute();
const selectedItem = ref('comment');
const sessionId = route.params.sessionId;
const routerKey = ref('');
const showSettings = ref(false);
// 获取按钮和设置窗口的引用
const settingsDiv = ref(null);
const toggleButton = ref(null);
const checked = ref(false);


const defaultMenu = 'comment';
const menu = reactive([
  {
    id: 'comment',
    title: '聊天',
    icon: ['far', 'comment'],
    path: 'comment'
  },
  {
    id: 'address-book',
    title: '通讯录',
    icon: ['far', 'user'],
    path: 'address-book'
  }
  // ,
  // {
  //   id: 'collect',
  //   title: '收藏',
  //   icon: ['fas', 'cube'],
  //   path: '/collect'
  // },
  // {
  //   id: 'files',
  //   title: '聊天文件',
  //   icon: ['far', 'folder'],
  //   path: '/files'
  // },
  // {
  //   id: 'community',
  //   title: '朋友圈',
  //   icon: ['fas', 'camera'],
  //   path: '/community'
  // }
])

const selectItem = (itemId) => {
  console.log('selectItem');
  selectedItem.value = itemId;
  routerKey.value = itemId;
  router.push({ name: itemId, params: { sessionId: sessionId } });
}

// 监听点击事件，判断是否点击到页面其他位置
const handleClickOutside = (event) => {
  if (
      showSettings.value &&
      settingsDiv.value &&
      toggleButton.value &&
      !settingsDiv.value.contains(event.target) &&
      !toggleButton.value.contains(event.target)
  ) {
    showSettings.value = false;
  }
};

// 在组件挂载时添加事件监听
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

// 在组件卸载时移除事件监听
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

const openSessionTools = () => {
  proxy.$popup.open(SessionTools, undefined, { title: '会话设置', width: '650px', height: '700px' });
}


const loadData = () => {
  // 检查 session
  sessionCheck(store.getters.getCurrentSessionId).then(() => {
    checked.value = true;
    console.log("是否加载过联系人：" + store.getters.isContactsLoaded)
    // 已经加载过联系人
    if (store.getters.isContactsLoaded) {
      routerKey.value = defaultMenu;
      router.push({ name: defaultMenu, params: { sessionId: sessionId } });
    } else {
      proxy.$toast.loading('初始化数据...');
      contact().then(resp => {
        // 默认加载comment
        store.commit("loadContact", resp);
        routerKey.value = defaultMenu;
        router.push({ name: defaultMenu, params: { sessionId: sessionId } });
      }).finally(() => {
        proxy.$toast.close();
      });
    }
  }).catch(e => {
    if ("response" in e) {
      store.commit("showErrorToastMsg", {
        msg: e.response.data.detail
      })
    } else {
      store.commit("showErrorToastMsg", {
        msg: e
      })
    }
  });
}

loadData();

</script>
<style scoped lang="less">
@import "/src/style/main/main.less";
</style>