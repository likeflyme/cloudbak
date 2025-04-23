<script setup>
import {ref} from "vue";

const emit = defineEmits(['confirmed', 'cancelled']);
const title = ref('');
const desc = ref('');

const isVisible = ref(false);

const closeDialog = () => {
  isVisible.value = false;
}

const openDialog = (dialogTitle, dialogDesc) => {
  title.value = dialogTitle;
  desc.value = dialogDesc;
  isVisible.value = true;
}

const confirm = () => {
  emit('confirmed');
  closeDialog();
}

const cancel = () => {
  emit('cancelled');
  closeDialog();
}

defineExpose({
  openDialog,
  closeDialog
});
</script>

<template>
  <div role="dialog" aria-modal="true" aria-labelledby="js_title1" v-if="isVisible">
    <div class="weui-mask"></div>
    <div class="weui-dialog">
      <div class="weui-dialog__hd"><strong class="weui-dialog__title" id="js_title1">{{title}}</strong></div>
      <div class="weui-dialog__bd">
        {{desc}}
      </div>
      <div class="weui-dialog__ft">
        <a role="button" href="javascript:" class="weui-dialog__btn weui-dialog__btn_default" @click="cancel">取消</a>
        <a role="button" href="javascript:" class="weui-dialog__btn weui-dialog__btn_primary" @click="confirm">确定</a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">

</style>