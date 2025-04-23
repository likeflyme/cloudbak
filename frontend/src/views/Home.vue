<template>
  <div role="alert" class="weui-information-bar weui-information-bar_warn-weak" v-if="showDownload">
    <div class="weui-information-bar__hd">
      <i class="weui-icon-outlined-warn"></i>
    </div>
    <div class="weui-information-bar__bd">
      您还没有同步任何数据到服务器，<a class="downloadClient" target="_blank" href="https://www.cloudbak.org/download-desktop.html">下载 Windows 同步客户端</a>。
    </div>
    <div class="weui-information-bar__ft">
      <button class="weui-btn_icon" @click="closeError">关闭<i class="weui-icon-close-thin"></i></button>
    </div>
  </div>
  <div class="page-home">
    <div class="sidebar">
      <div class="open-close-container">
        <!--      <img class="open-close" src="../images/icon_nav_form.png" alt=" 展开" role="button">-->
      </div>
      <ul class="sidebar-ul">
        <li class="sidebar-li" v-for="session in store.getters.getSysSessions">
          <div class="name-container"
               :class="{'active': store.getters.getUserInfo.current_session_id === session.id}"
               :title="session.wx_name"
               @click="updateCurrentSession(session)">
            {{ session.wx_name[0] }}
          </div>
        </li>
        <li class="sidebar-li">
          <div class="name-container" title="添加会话" @click="sessionAddRef.show()">
            <font-awesome-icon :icon="['fas', 'plus']" />
          </div>
        </li>
      </ul>
    </div>
    <router-view :key="routerKey" v-if="showMain"/>
    <Toolbar class="toolbar"></Toolbar>
    <Toast></Toast>
    <SysWindow class="sys-window-add-session" ref="sessionAddRef" title="添加会话">
      <SessionAdd></SessionAdd>
    </SysWindow>
  </div>

</template>

<script setup lang="ts">
import {ref} from "vue";
import {sysInfo} from "@/api/sys.js";
import {userinfo} from "@/api/auth.js";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {sysSessions, updateCurrentSession as updateCurrentSessionOnServer, sessionCheck} from "@/api/user.js";
import Toolbar from "./toolbar/Toolbar.vue";
import packageJson from '../../package.json';
import Toast from "../components/Toast.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import SysWindow from "../components/SysWindow.vue";
import SessionAdd from "../components/home/SessionAdd.vue";
const store = useStore();
const router = useRouter();

const routerKey = ref(0);

const showMain = ref(false);
const showDownload = ref(false);
const sessionAddRef = ref(null);

// 加载系统信息
sysInfo().then(resp => {
  store.commit("setSysInfo", resp);
});
// 加载用户信息
userinfo().then(resp => {
  store.commit("setUserInfo", resp);
  if (resp.current_session ) {
    showMain.value = true;
  }
  // 初始化配置
  // if ("configs" in resp) {
  //   for (let i = 0; i < resp.configs.length; i++) {
  //     const conf = resp.configs[i];
  //     if ("sys_conf" === conf.key) {
  //       store.commit("setSysConf", conf)
  //     } else if ("user_conf" === conf.key) {
  //       store.commit("setUserConf", conf);
  //     } else {
  //       store.commit("addSessionConf", conf);
  //     }
  //   }
  // }

  // 加载所有 session
  sysSessions().then(data => {
    store.commit("setSysSessions", data);
    // 跳转上次选择的 session
    if (resp.current_session) {
      const currentSession = resp.current_session;
      routerKey.value = currentSession.id;
      router.push({ name: "session", params: { sessionId: currentSession.id } });
    }
    // if (data.length > 0) {
    //   updateCurrentSession(data[0]);
    // } else {
    //   showDownload.value = true;
    // }
  });
});


const updateCurrentSession = (session) => {
  // 切换 session
  updateCurrentSessionOnServer(session.id).then((data) => {
    // 设置当前会话
    store.commit("setCurrentSession", data);
    routerKey.value = session.id;
    // 路由跳转
    router.push({ name: "session", params: { sessionId: session.id } });
  });
}

const getStateDesc = (session) => {
  if (session.analyze_state === 1) {
    return '数据解析中'
  } else if (session.analyze_state === 2) {
    return '数据未初始化';
  } else {
    return ''
  }
}


</script>

<style scoped lang="less">
@import "/src/style/home.less";
</style>