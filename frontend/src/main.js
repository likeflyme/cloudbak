import { createApp } from 'vue'
import './style/main.less'
import 'weui/dist/style/weui.min.css'
import '@fortawesome/fontawesome-svg-core/styles.css';
import App from './App.vue'
import router from './router'
import store from "./store";
import VueCookies from 'vue-cookies'
// fontawesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// v-viewer
import 'viewerjs/dist/viewer.css'
import VueViewer from 'v-viewer'
// dialog
import DialogPlugin from './plugins/dialog/index.js';
// toast
import ToastPlugin from './plugins/toast/toast.js';
// popup
import PopupPlugin from './plugins/popup/index.js';
import lazyPlugin from 'vue3-lazy';
import loadingImage from '@/assets/img-loading.png';
import errorImage from '@/assets/img-error.png';

// 将所需图标添加到库中
library.add(fas, far)

const app = createApp(App);

// 全局注册 FontAwesomeIcon 组件
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router)
    .use(store)
    .use(VueCookies)
    .use(VueViewer)
    .use(DialogPlugin)
    .use(ToastPlugin)
    .use(PopupPlugin)
    .use(lazyPlugin, {
        loading: loadingImage,
        error: errorImage
    });

app.provide('globalPopup', app.config.globalProperties.$popup);
app.mount('#app');
