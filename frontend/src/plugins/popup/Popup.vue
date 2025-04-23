<script setup>
import {ref} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const emit = defineEmits(['close']);

const visible = ref(true);

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: 'Popup Window'
  },
  width: {
    type: String,
    default: '28.571rem'
  },
  height: {
    type: String,
    default: '21.429rem'
  },
  top: {
    type: String,
    default: '3.571rem'
  },
  left: {
    type: String,
    default: '3.571rem'
  },
  zIndex: {
    type: Number,
    default: 800
  },
  close: {
    type: Function,
    required: true
  },
  titleStyle: {
    type: Object,
    default: () => {
      return {
        backgroundColor: '#f2f2f2'
      }
    }
  }
});

const closeWindow = () => {
  visible.value = false;
  props.close();
}

const computeStyle = () => {
  if (window.matchMedia("(min-width: 1025px)").matches) {
    // 视口宽度大于或等于 1025px
    console.log("Min-width matched");
    return {
      width: props.width,
      height: props.height,
      top: props.top,
      left: props.left,
      zIndex: props.zIndex
    }
  } else {
    return {
      zIndex: props.zIndex
    }
  }
}

</script>

<template>
  <div v-if="visible" class="popup-window" :style="computeStyle()">
    <div class="popup-top" :style="titleStyle">
      <div class="popup-title">
        <p>{{ props.title }}</p>
      </div>
      <div class="popup-top-grow"></div>
      <div class="popup-btns">
        <div class="popup-btn" @click="closeWindow">
          <font-awesome-icon :icon="['fas', 'xmark']" />
        </div>
      </div>
    </div>
    <!-- 动态组件 -->
    <div class="popup-slot">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="less">
.popup-window {
  overflow: auto;
  position: absolute;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  border-radius: 0.214rem;
  box-shadow: 0 0 0.714rem rgba(0, 0, 0, 0.1);
  border: 0.071rem solid lightgray;
  .popup-top {
    width: 100%;
    display: flex;
    border-bottom: 0.071rem solid #f2f2f2;
    .popup-title {
      font-size: 0.929rem;
      color: gray;
      p {
        padding: 0.357rem;
      }
    }
    .popup-top-grow {
      flex-grow: 1;
    }
    .popup-btns {
      display: flex;
      .popup-btn {
        display: flex;
        justify-content: center;  /* 水平居中 */
        align-items: center;      /* 垂直居中 */
        width: 2.143rem;
        height: 2.143rem;
        cursor: pointer;
        color: #515151;
        font-size: 0.929rem;
      }
      .popup-btn:hover {
        background-color: #fb7373;
        color: #FFFFFF;
      }
    }
  }
  .popup-slot {
    width: 100%;
    height: 52.857rem;
    overflow-y: scroll;
  }
  // 以下是滚动条样式
  /* 隐藏默认的滚动条轨道和拇指 */
  .popup-slot::-webkit-scrollbar {
    width: 0.429rem; /* 隐藏滚动条 */
    background: #f5f5f5; /* 使滚动条轨道背景透明 */

  }

  /* 鼠标悬停时显示滚动条轨道 */
  .popup-slot:hover::-webkit-scrollbar {
    width: 0.429rem; /* 设置滚动条宽度 */
    background: #f5f5f5; /* 滚动条轨道背景颜色 */
  }

  /* 滚动条轨道样式 */
  .popup-slot:hover::-webkit-scrollbar-track-piece {
    background: #f5f5f5; /* 设置滚动条轨道背景颜色 */
    border-radius: 0.571rem; /* 设置滚动条轨道圆角 */
  }

  /* 滚动条拇指样式 */
  .popup-slot:hover::-webkit-scrollbar-thumb {
    background-color: #c8c9cc; /* 设置滚动条拇指背景颜色 */
    border-radius: 0.571rem; /* 设置滚动条拇指圆角 */
  }

  /* 鼠标悬停在滚动条拇指上时的样式 */
  .popup-slot:hover::-webkit-scrollbar-thumb:hover {
    background-color: #b0b0b0; /* 鼠标悬停时滚动条拇指背景颜色 */
  }
}

@media (max-width: 768px) {
  .popup-window {
    overflow: auto;
    position: absolute;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .popup-window {
    overflow: auto;
    position: absolute;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
}

@media (min-width: 1025px) {
  .popup-window {
    overflow: auto;
    position: absolute;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    border-radius: 0.214rem;
    box-shadow: 0 0 0.714rem rgba(0, 0, 0, 0.1);
    border: 0.071rem solid lightgray;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
}
</style>