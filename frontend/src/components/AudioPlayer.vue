<script setup>
import {reactive, ref, onBeforeUnmount} from "vue";
import {fromXmlToJson} from "@/utils/common.js";
import {parseXml} from "../utils/common.js";

const props = defineProps({
  src: String,
  text: String,
  right: {
    type: Boolean,
    default: false
  }
})
const isPlaying = ref(false);
const currentIcon = ref('volume-high');
let updateInterval; // 用于保存定时器的引用,
const icons = reactive(['volume-off', 'volume-low', 'volume-high']);
const currentIndex = ref(0);
const maxIndex = ref(2);
const isEnable = ref(true);
const tips = ref('');
const audio = ref(null);
const audioProps = fromXmlToJson(props.text);
const voiceTrans = ref('');

const getVoiceTransText = () => {
  try {
    if ('msg' in audioProps && 'voicetrans' in audioProps.msg) {
      const attr = audioProps.msg.voicetrans['@attributes'];
      if (attr && 'transtext' in attr) {
        voiceTrans.value = attr.transtext;
      }
    }
  } catch (e) {
    console.error(e);
  }
}

getVoiceTransText();

const toggleAudio = () => {
  if (!isEnable.value) {
    return;
  }
  if (isPlaying.value) {
    audio.value.pause();
    resetIcon();
  } else {
    audio.value.play();
    // 每500毫秒更新一次图标
    updateInterval = setInterval(updateIcon, 500);
  }

  isPlaying.value = !isPlaying.value;
}

const updateIcon = () => {
  currentIndex.value = currentIndex.value + 1;
  if (currentIndex.value > maxIndex.value) {
    currentIndex.value = 0;
  }
  currentIcon.value = icons[currentIndex.value];
}

const resetIcon = () => {
  clearInterval(updateInterval);
  currentIcon.value = 'volume-high';
}

const onAudioEnded = () => {
  resetIcon();
  isPlaying.value = false; // 重置播放状态
}
const onError = (e) => {
  console.log("语音获取失败，修改为不可用", e)
  isEnable.value = false;
  tips.value = '未同步的语音';
}

const getVoiceLength = () => {
  try {
    const length = audioProps.msg.voicemsg['@attributes'].voicelength
    // 将毫秒转换为秒和分钟
    const seconds = Math.floor(length / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    // 格式化为分钟和秒
    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}"`;
    } else {
      return `${remainingSeconds}"`;
    }
  } catch (e) {
    console.error(e)
  }
  return '';
}

const calculateDivWidth = () => {
  try {
    if (voiceTrans.value) {
      return 300;
    }
    if (!isEnable.value) {
      return 180;
    }
    let voiceLength = audioProps.msg.voicemsg['@attributes'].voicelength
    const maxWidth = 300; // 最大宽度
    const minLength = 0; // 最小长度
    const maxLength = 30000; // 假设最大长度为3分钟（180000毫秒）
    if (voiceLength > maxLength) {
      voiceLength = maxLength;
    }

    const width = Math.min(maxWidth, (voiceLength / maxLength) * maxWidth);

    return width;
  } catch (e) {
    console.error(e);
  }
  return 100;
};

const playerBottomPadding = () => {
  if (voiceTrans.value) {
    return '5px';
  } else {
    return '0px';
  }
}


onBeforeUnmount(() => {
  // 组件销毁前清除定时器
  clearInterval(updateInterval);
});

</script>

<template>
  <div class="audio-container">
    <div class="audio-player" :style="{'width': calculateDivWidth() + 'px', 'padding-bottom': playerBottomPadding()}" :class="{'player-disable': !isEnable, 'player-right': props.right}" @click="toggleAudio">
      <p class="audio-player-icon">
        <font-awesome-icon class="audio-icon" :icon="['fas', currentIcon]" title="语音"/>
      </p>
      <p class="audio-player-text"> {{ getVoiceLength()}} {{}}</p>
      <p class="audio-player-text"> {{ tips }}</p>
      <audio ref="audio" :src="props.src" @ended="onAudioEnded" @error="onError"></audio>
    </div>
    <div class="trans" v-if="voiceTrans">
      <div class="trans-text">
        {{ voiceTrans }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.audio-container {
  padding: 10px 10px;
  min-width: 100px;
  max-width: 300px;
  font-size: 12px;
  background-color: #FFFFFF;
  border-radius: 4px;
}
.audio-container:hover {
  background-color: #EBEBEB;
}
.audio-player {
  display: flex;
  direction: ltr;
  min-width: 50px;
  .audio-player-icon {
    width: 20px;
    text-align: left;
  }
}
.audio-player:hover {
  cursor: pointer;
}
.audio-player-text {
  margin-right: 5px;
}
.audio-player.player-disable {
  color: gray;
}
.player-right.player-right {
  direction: rtl;
  .audio-player-icon {
    transform: rotate(180deg) translateZ(0);
  }
  .audio-player-text {
    direction: ltr;
  }
}
.trans {
  border-top: 1px solid #EBEBEB;
  padding-top: 5px;
}
</style>
