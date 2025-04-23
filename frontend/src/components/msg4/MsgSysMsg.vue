<script setup>
import {parseMsg} from "@/utils/message_parser_v4.js";

const props = defineProps({
  msg: {
    type: Object,
    required: true
  }
});

// 解析数据
parseMsg(props.msg)


</script>

<template>
  <div class="tips">
    <p class="tips-content" v-html="props.msg.data.content"></p>
  </div>
</template>

<style scoped lang="less">
.tips {
  font-size: 0.857rem;
  color: gray;
  text-align: center;
  padding: 0.714rem;
  .tips-content {
    direction: ltr;
    max-width: 21.429rem;
    margin: 0 auto;
    word-break: break-word;
  }
}
</style>