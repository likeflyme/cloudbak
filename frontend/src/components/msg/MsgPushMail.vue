<script setup>
import {fromXmlToJson} from "@/utils/common.js";

const props = defineProps({
  msg: {
    type: Object,
    required: true
  }
});

const jsonData = fromXmlToJson(props.msg.StrContent);
const openLink = (url) => {
  window.open(url);
}
</script>

<template>
  <div class="n-container">
    <div class="n-box">
      <p class="n-box-title">{{ jsonData.msg?.pushmail?.content?.sender['#cdata-section'] }}</p>
      <p class="n-box-subject">{{ jsonData.msg?.pushmail?.content?.subject['#cdata-section'] }}</p>
      <p class="n-box-digest">{{ jsonData.msg?.pushmail?.content?.digest['#cdata-section'] }}</p>
    </div>
  </div>
</template>

<style scoped lang="less">
.n-container {
  width: 100%;
  .n-box {
    margin: 5px auto;
    background-color: #FFFFFF;
    border-radius: 3px;
    width: 350px;
    direction: ltr;
    padding: 15px;
    .n-box-title {
      font-size: 14px;
    }
    .n-box-subject {
      font-size: 13px;
      padding: 5px 0;
    }
    .n-box-digest {
      font-size: 13px;
      padding: 5px 0;
      color: gray;
    }
  }
}
</style>