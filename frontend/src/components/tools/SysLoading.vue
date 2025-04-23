<script setup>

import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
</script>

<template>
<div class="s-loading">
  <a href="javascript:void(0)">
    <font-awesome-icon class="loading-icon spin" :icon="['fas', 'spinner']"/>
  </a>
</div>
</template>

<style scoped lang="less">
.s-loading {
  text-align: center;
  font-size: 0.857rem;
  transform: rotate(180deg) translateZ(0);
  color: #2C90FF;
  .no-more-msg {
    font-size: 0.857rem;
    color: dimgray;
  }
  .loading-icon {
    color: gray;
  }
  .spin {
    display: inline-block;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>