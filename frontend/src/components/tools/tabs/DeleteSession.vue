<script setup>
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import {getCurrentInstance, ref} from "vue";
import {deleteSession, updateCurrentSession as updateCurrentSessionOnServer} from "@/api/user.js";

const store = useStore();
const router = useRouter();

const { proxy } = getCurrentInstance();

const showDeleteDialog = ref(false);
const isOnDelete = ref(false);


const sessionDelete = (id) => {
  if (isOnDelete.value) {
    console.log("正在删除，无效的重复点击");
    return;
  }
  isOnDelete.value = true;
  deleteSession(id).then(resp => {
    let sessions = store.getters.getSysSessions;
    if (sessions && sessions.length > 0) {
      let first = sessions[0];
      proxy.$toast.success('删除会话成功');
      showDeleteDialog.value = false;
      updateCurrentSessionOnServer(first.id).then((data) => {
        store.commit("dropSession", id);
        isOnDelete.value = false;
        router.push({ name: 'home'});
      }).catch(e => {
        isOnDelete.value = false;
        if ("response" in e) {
          store.commit("showErrorToastMsg", {
            msg: e.response.data
          })
        } else {
          store.commit("showErrorToastMsg", {
            msg: e
          })
        }
      });
    }
  }).catch(e => {
    isOnDelete.value = false;
    if ("response" in e) {
      store.commit("showErrorToastMsg", {
        msg: e.response.data
      })
    } else {
      store.commit("showErrorToastMsg", {
        msg: e
      })
    }
  });
}
</script>

<template>
  <div class="s-page">
    <div class="page-body">
      <div class="conf-group">
        <div class="conf-row">
          注意：此操作不可取消，删除后将无法恢复。
        </div>
        <div class="conf-row">
          <div class="conf-right">
            <a class="weui-btn weui-btn_mini weui-btn_warn weui-wa-hotarea"
               @click="showDeleteDialog?showDeleteDialog=false:showDeleteDialog=true">删除会话</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div role="dialog" aria-hidden="true" aria-modal="true" aria-labelledby="js_title1" id="iosDialog1" v-if="showDeleteDialog">
    <div class="weui-mask"></div>
    <div class="weui-dialog">
      <div class="weui-dialog__hd"><strong class="weui-dialog__title" id="js_title1">删除会话</strong></div>
      <div class="weui-dialog__bd">
        <p>确定要删除会话吗？</p>
        <p>确定删除后，该会话的数据文件将在后台静默删除！</p>
        <p>会话名称：{{ store.getters.getCurrentSession.name }}</p>
        <p>会话备注：{{ store.getters.getCurrentSession.desc }}</p>
        <p>微信账号：{{ store.getters.getCurrentSession.wx_acct_name }}</p>
        <p>微信昵称：{{ store.getters.getCurrentSession.wx_name }}</p>
      </div>
      <div class="weui-dialog__ft">
        <a role="button" href="javascript:" class="weui-dialog__btn weui-dialog__btn_default" @click="showDeleteDialog=false">取消</a>
        <a role="button" href="javascript:" class="weui-dialog__btn weui-dialog__btn_primary" @click="sessionDelete(store.getters.getCurrentSession.id)">确定删除</a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
@import "/src/style/components/tools/tab.less";
</style>