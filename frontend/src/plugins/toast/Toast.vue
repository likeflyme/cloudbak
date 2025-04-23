<script setup>
import {ref} from "vue";

const message = ref('');
const type = ref('success');
const visible = ref(false);

const open = (options) => {
  message.value = options.message;
  type.value = options.type || 'success';
  visible.value = true;
}
const close = () => {
  visible.value = false;
}
defineExpose({
  open,
  close
});
</script>

<template>
  <div role="alert" v-if="visible">
    <div class="weui-mask_transparent"></div>
    <div class="weui-toast" v-if="type === 'warn'">
      <i class="weui-icon-warn weui-icon_toast"></i>
      <p class="weui-toast__content">{{ message }}</p>
    </div>
    <div class="weui-toast" v-else-if="type === 'loading'">
            <span class="weui-primary-loading weui-icon_toast">
              <span class="weui-primary-loading__dot"></span>
            </span>
      <p class="weui-toast__content">{{ message }}</p>
    </div>
    <div class="weui-toast" v-else>
      <i class="weui-icon-success-no-circle weui-icon_toast"></i>
      <p class="weui-toast__content">{{ message }}</p>
    </div>
  </div>
</template>

<style scoped lang="less">
</style>