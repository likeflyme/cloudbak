<script setup>
import {useStore} from "vuex";
import {logout} from "@/utils/common.js";
import {useRouter} from "vue-router";
import {getCurrentInstance, ref, toRaw} from "vue";
import {updateCurrentSession as updateCurrentSessionOnServer} from "@/api/user.js";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const { proxy } = getCurrentInstance();

const store = useStore();

const router = useRouter();

const selectAcct = ref(false);

const clickLogout = () => {

  proxy.$dialog.open({
    title: '退出账号',
    desc: '确定退出吗？',
    onConfirmed: () => {
      logout();
      router.push("/login")
    },
    onCancelled: () => {

    }
  });
}

const updateCurrentSession = (s) => {
  if (s.id === store.getters.getCurrentSession.id) {
    return;
  }
  updateCurrentSessionOnServer(s.id).then((data) => {
    store.commit("setCurrentSession", data);
    router.push({ name: "user", params: { sessionId: s.id } });
  });
}

</script>

<template>
  <div class="weui-panel weui-panel_access">
    <div class="weui-panel__bd">
      <a aria-labelledby="js_p1m1_bd" href="javascript:" class="weui-media-box weui-media-box_appmsg">
        <div aria-hidden="true" class="weui-media-box__hd">
          <img class="weui-media-box__thumb" :src="store.getters.getCurrentSession.smallHeadImgUrl" alt="">
        </div>
        <div aria-hidden="true" id="js_p1m1_bd" class="weui-media-box__bd">
          <strong class="weui-media-box__title">{{ store.getters.getCurrentSession.wx_name }}</strong>
          <p class="weui-media-box__desc">微信号：{{store.getters.getCurrentSession.wx_acct_name}}</p>
        </div>
      </a>
    </div>
    <div class="weui-panel__ft">
      <a href="javascript:" class="weui-cell weui-cell_active weui-cell_access weui-cell_link">
        <span class="weui-cell__bd" @click="selectAcct = true">切换微信</span>
        <span class="weui-cell__ft"></span>
      </a>
    </div>
    <div class="weui-panel__ft">
      <a href="javascript:" class="weui-cell weui-cell_active weui-cell_access weui-cell_link" @click="clickLogout">
        <span class="weui-cell__bd">退出</span>
        <span class="weui-cell__ft"></span>
      </a>
    </div>
  </div>
  <div class="sessions" :class="{'open': selectAcct}">
    <div class="weui-panel__hd" @click="selectAcct = false"><font-awesome-icon class="main-back" :icon="['fas', 'chevron-left']"/> 返回</div>
    <div class="weui-panel weui-panel_access"
         v-for="s in store.getters.getSysSessions"
         @click="updateCurrentSession(s)">
      <div class="weui-panel__bd">
        <a aria-labelledby="js_p1m1_bd" href="javascript:" class="weui-media-box weui-media-box_appmsg">
          <div aria-hidden="true" class="weui-media-box__hd">
            <img class="weui-media-box__thumb" :src="s.smallHeadImgUrl" alt="">
          </div>
          <div aria-hidden="true" id="js_p1m1_bd" class="weui-media-box__bd">
            <strong class="weui-media-box__title">{{ s.wx_name }}
              <font-awesome-icon v-if="s.id === store.getters.getCurrentSession.id" class="user-active" :icon="['fas', 'sun']"/>
            </strong>
            <p class="weui-media-box__desc">微信号：{{s.wx_acct_name}}</p>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.sessions {
  position: fixed;
  top: 0;
  left: 100%;
  width: 100%;
  height: 100%;
  z-index: 11;
  background-color: #ededed;
  transition: transform 0.3s ease-in-out;
  .session-item {
    background-color: #FFFFFF;
  }
}
.sessions.open {
  transform: translateX(-100%);
}
.user-active {
  color: #51c332
}
</style>