<script setup>
const props = defineProps({
  msg: {
    type: Object,
    required: true
  }
});

// 通知消息编码
const convertSysMsg = (strContent) => {
  return strContent.replace(/<\/?revokemsg>/g, '');
}

</script>

<template>
  <div class="tips">
    <p class="tips-content" v-html="convertSysMsg(props.msg.StrContent)"></p>
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
  }
}
</style>