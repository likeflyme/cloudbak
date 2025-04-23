<template>
  <div class="edit-container">
    <span v-if="!editing">
      <span v-if="hidden">
        {{ hiddenText }}
      </span>
      <span v-else>
        {{ newText }}
      </span>
    </span>
    <input v-else v-model="newText" ref="inputRef" @blur="cancel" @keyup.enter="saveText" @keydown.esc="cancel"/>
    <font-awesome-icon class="edit" :icon="['fas', 'eye']" v-if="props.mark && hidden" @click="hidden = false"/>
    <font-awesome-icon class="edit" :icon="['fas', 'eye-slash']" v-if="props.mark && !hidden" @click="hidden = true"/>
    <font-awesome-icon class="edit" :icon="['fas', 'edit']" @click="editText"/>
  </div>
</template>

<script setup>
import {ref, defineProps, defineEmits, nextTick, watch} from 'vue';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

const props = defineProps({
  modelValue: String,
  mark: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['update:modelValue']);

// 临时存储输入的值
const newText = ref(props.modelValue);
const hiddenText = ref(props.modelValue);
const editing = ref(false);
const inputRef = ref(null);
const hidden = ref(props.mark);

const maskString = (str) => {
  if (str.length <= 8) {
    return str; // 如果字符串长度小于等于8，返回原字符串
  }
  const start = str.slice(0, 4); // 获取前四个字符
  const end = str.slice(-4); // 获取后四个字符
  const maskedLength = str.length - 8; // 计算需要替换的字符数量
  const maskedPart = '*'.repeat(maskedLength); // 生成星号字符串

  return start + maskedPart + end; // 拼接结果
}

if (props.mark) {
  hiddenText.value = maskString(newText.value);
}

// 当 modelValue 更新时同步 newText
watch(() => props.modelValue, (newVal) => {
  newText.value = newVal;
  if (props.mark) {
    hiddenText.value = maskString(newVal);
  }
});


const editText = () => {
  editing.value = true;
  nextTick(() => {
    inputRef.value?.focus();  // 聚焦输入框
  });
};

const saveText = () => {
  emit('update:modelValue', newText.value);  // 保存输入的值
  editing.value = false;
};

const cancel = () => {
  editing.value = false;
  newText.value = props.modelValue;  // 恢复为原始值
};
</script>

<style scoped lang="less">
.edit-container {
  display: inline-block;
  .edit {
    margin-left: 5px;
    color: #07c160;
    visibility: hidden;
  }
}
.edit-container:hover {
  .edit {
    visibility: visible;
  }
}
</style>
