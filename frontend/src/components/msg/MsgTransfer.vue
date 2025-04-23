<script setup>
import {useStore} from "vuex";

const store = useStore();

const props = defineProps({
  msg: {
    type: Object,
    required: true
  }
});

const payInfo = props.msg.compress_content.msg.appmsg.wcpayinfo;

const getMsgWxId = () => {
  if ('WxId' in props.msg && props.msg.WxId !== '' && props.msg.WxId !== null && props.msg.WxId !== undefined) {
    return props.msg.WxId;
  } else if (props.msg.IsSender === 1) {
    return store.getters.getCurrentWxId;
  } else {
    return props.msg.StrTalker;
  }
}

// 消息发送者微信id
const msgWxId = getMsgWxId();



</script>

<template>
  <div class="t-container">
    <div class="t-box">
      <div class="t-content">
        <p v-if="payInfo.paysubtype === '1' && payInfo.pay_memo !== null"> {{payInfo.pay_memo}} </p>
        <p v-else-if="payInfo.paysubtype === '1'"> 点击收款 </p>
        <p v-else>已收款</p>
        <p>{{ payInfo.feedesc }}</p>
      </div>
      <div class="t-footer">
        微信转账
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.t-container {
  .t-box {
    width: 200px;
    .t-content {
      border-top-left-radius: 5px;
      border-top-right-radius: 5px;
      background-color: #fa9c3e;
      color: #FFFFFF;
      font-size: 14px;
      padding: 10px;
    }
    .t-footer {
      background-color: #FFFFFF;
      font-size: 11px;
      padding:5px 8px;
      color: #c8c8c8;
      border-bottom-left-radius: 5px;
      border-bottom-right-radius: 5px;
    }
  }
}
</style>