<script setup>
import {useStore} from "vuex";
import {ref} from "vue";

const store = useStore();

const props = defineProps({
  username: {
    type: String,
    required: true
  }
})
// 获取联系人姓名
const name = ref('');
const getContactName = () => {
  const contact = store.getters.getContactMap[props.username];
  if (contact) {
    if (contact.remark && contact.remark !== '') {
      return contact.remark;
    } else {
      return contact.nickname;
    }
  }
  // 不在联系人中，从数据库中获取

};

</script>

<template>
<p>

</p>
</template>

<style scoped lang="less">

</style>