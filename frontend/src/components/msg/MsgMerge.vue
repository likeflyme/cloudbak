<script setup>
import MsgMergeDetail from "./MsgMergeDetail.vue";
import {getCurrentInstance} from "vue";

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  desc: {
    type: String,
    required: true
  },
  recorditem: {
    type: Object,
    required: true
  }
});


const { proxy } = getCurrentInstance();

const replaceBreak = (str) => {
  if (str) {
    return str.replaceAll("\n", "<br>");
  }
  return str;
}

const openTransferDetail = () => {
  proxy.$popup.open(MsgMergeDetail,
      {
        recorditem: props.recorditem
      },
      { title: props.title, width: '650px', height: '800px' });
}
</script>

<template>
<div class="transfer" @click="openTransferDetail()">
  <div class="transfer-title">
    {{ props.title }}
  </div>
  <div class="transfer-desc" v-html="replaceBreak(props.desc)">

  </div>
  <div class="transfer-footer">
    聊天记录
  </div>
</div>
</template>

<style scoped lang="less">
.transfer {
  background-color: #FFFFFF;
  border-radius: 3px;
  padding: 10px;
  direction: ltr;
  min-width: 250px;
  .transfer-title {

  }
  .transfer-desc {
    font-size: 11px;
    color: #797979;
    height: 55px;
    overflow-y: hidden;
    width: 200px;
    white-space: nowrap;        /* 防止文字换行 */
    overflow-x: hidden;         /* 隐藏超出容器宽度的文字 */
    text-overflow: ellipsis;    /* 超出部分用省略号代替 */
  }
  .transfer-footer {
    padding-top: 5px;
    font-size: 11px;
    color: #797979;
  }
}
.transfer:hover {
  background-color: #ebebeb;
  cursor: pointer;
}
</style>