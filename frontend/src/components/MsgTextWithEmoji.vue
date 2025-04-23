<script setup>
import { ref, watchEffect } from 'vue';
import {getEmoji} from "../utils/emoji.js";
const props = defineProps({
  content: {
    type: String,
    required: true
  }
});

const data = ref(''); // 存储替换后的 HTML

const replaceBracketsWithImages = async (text) => {
  if (!text) return '';

  const matches = text.match(/\[([^\[\]]+)\]/g);
  if (!matches) return text;

  const replacements = await Promise.all(
      matches.map(async (match) => {
        const title = match.slice(1, -1);
        const emojiSrc = await getEmoji(title);
        return emojiSrc ? `<img class="emoji-chat-img" alt="${title}" src="${emojiSrc}" />` : match;
      })
  );

  let newText = text;
  replacements.forEach((replacement, index) => {
    newText = newText.replace(matches[index], replacement);
  });

  return newText;
};

// 监听 `props.content` 变化，异步更新 `data`
watchEffect(async () => {
  data.value = await replaceBracketsWithImages(props.content);
});
</script>

<template>
  <p class="emoji-chat" v-html="data"></p>
</template>

<style lang="less">
.emoji-chat {
  //display: flex;
  //align-items: center;  /* 让文字和图片在行内垂直居中 */
  word-wrap: break-word;
}

.emoji-chat-img {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin: -3px 0 0 0;
  //margin: 0 4px;  /* 给表情和文字留点间距 */
  //vertical-align: text-bottom;
}
</style>