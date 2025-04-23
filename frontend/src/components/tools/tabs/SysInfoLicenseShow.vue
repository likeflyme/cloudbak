<script setup>
const props = defineProps({
  license: {
    type: String,
    default: ""
  }
});
</script>

<template>
<div class="show-license">
  {{ license }}
</div>
</template>

<style scoped lang="less">
.show-license {
  width: 350px;
  word-break: break-word;
  margin: 10px auto;
}
</style>