<script setup>
import {useStore} from "vuex";
const store = useStore();
const closeToast = () => {
  store.commit("closeErrorToastMsg");
}
</script>

<template>
  <div role="alert" class="weui-information-bar weui-information-bar_warn-no-color" v-if="store.getters.isShowToastMsg">
    <div class="weui-information-bar__hd">
      <i class="weui-icon-outlined-warn"></i>
    </div>
    <div class="weui-information-bar__bd">
      {{ store.getters.getToastMsg }}
    </div>
    <div class="weui-information-bar__ft">
      <button class="weui-btn_icon" @click="closeToast">关闭<i class="weui-icon-close-thin"></i></button>
    </div>
  </div>
</template>

<style scoped lang="less">
.weui-toast-frame {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, 0);
}
</style>