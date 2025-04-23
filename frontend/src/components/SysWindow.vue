<script setup>
import {useStore} from "vuex";
import {ref} from "@vue/reactivity";

const store = useStore();
const isShow = ref(false);
defineProps({
  title: {
    type: String,
    required: false,
    default: ''
  }
});

const show = () => {
  isShow.value = true;
}

const hide = () => {
  isShow.value = false;
}

defineExpose({
  show, hide
});

</script>

<template>
  <div class="window" v-if="isShow">
    <div class="window-head">
      <div class="window-title">{{ $props.title }}</div>
      <div class="window-grow"></div>
      <div class="window-close">
        <font-awesome-icon :icon="['fas', 'xmark']" @click="hide"/>
      </div>
    </div>
    <div class="window-body">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="less">
.window {
  width: 600px;
  height: 650px;
  border: 1px solid lightgray;
  background-color: #FFFFFF;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  .window-head {
    display: flex;
    font-size: 14px;
    color: #999999;
    .window-title {
      padding-left: 10px;
      padding-top: 5px;

    }
    .window-grow {
      flex-grow: 1;
    }
    .window-close {
      padding-right: 5px;
      cursor: pointer;
    }
  }
  .window-body {
    font-size: 14px;
    height: 470px;
    padding: 10px;
  }
}
</style>