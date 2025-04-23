<script setup>
import {useStore} from "vuex";
import {updateSysSession} from "@/api/user.js";
import {reactive, ref, nextTick, getCurrentInstance, watch} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {getContactHeadById} from "../../../utils/contact.js";
import EditAbleText from "../../EditAbleText.vue";
const store = useStore();
const session = store.getters.getCurrentSession;
const {proxy} = getCurrentInstance();

const sessionData = reactive({
  name: session.name,
  desc: session.desc,
  wx_name: session.wx_name,
  wx_acct_name: session.wx_acct_name,
  wx_key: session.wx_key,
  wx_mobile: session.wx_mobile,
  wx_dir: session.wx_dir
});

// 遍历 sessionData 的每个字段并添加 watch
Object.keys(sessionData).forEach((key) => {
  watch(
      () => sessionData[key],
      (newVal, oldVal) => {
        console.log(`${key} 变了: ${oldVal} -> ${newVal}`);
        updateSysSession(sessionData).then((resp) => {
          console.log("修改会话成功，resp=", resp)
          // 设置当前会话
          store.commit("setCurrentSession", resp);
        }).catch(e => {
          if ("response" in e) {
            store.commit("showErrorToastMsg", {
              msg: e.response.data
            })
          } else {
            store.commit("showErrorToastMsg", {
              msg: e
            })
          }
        });;
      }
  );
});

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000);
  // 获取年、月、日、小时、分钟
  const year = String(date.getFullYear()).slice(-2);
  const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  // 根据日期判断输出格式
  return `${year}/${month}/${day} ${hours}:${minutes}`;
};

</script>

<template>
  <div class="info">
    <div class="info-base">
      <div class="info-head">
        <img :src="store.getters.getCurrentSession.smallHeadImgUrl" alt="" v-if="store.getters.getClientVersion === 'win.v3'"/>
        <img :src="`/api/resources/relative-resource?relative_path=${store.getters.getCurrentSession.smallHeadImgUrl}&session_id=${store.getters.getCurrentSessionId}`" alt="" v-else/>
<!--        <img :src="getContactHeadById(store.getters.getCurrentSession.username)" alt=""/>-->
      </div>
      <div class="info-wx">
        <div class="info-wx-item info-wx-item-nickname">
          <p class="item-value">
            <edit-able-text v-model="sessionData.wx_name"/>
          </p>
        </div>
        <div class="info-wx-item">
          微信号：<p class="item-value"><edit-able-text v-model="sessionData.wx_acct_name"/></p>
        </div>
        <div class="info-wx-item">
          微信id：{{store.getters.getCurrentSession.wx_id}}
        </div>
        <div class="info-wx-item">手机号：<edit-able-text v-model="sessionData.wx_mobile"/>
        </div>
      </div>
    </div>
    <div class="info-row">
      <div class="info-row-item">
        会话名称：<edit-able-text v-model="sessionData.name"/>
      </div>
      <div class="info-row-item">
        会话描述：<edit-able-text v-model="sessionData.desc"/>
      </div>
      <div class="info-row-item">
        客户端系统类型：
        <span v-if="store.getters.getCurrentSession.client_type === 'win'">
          Windows
        </span>
        <span v-else-if="store.getters.getCurrentSession.client_type === 'mac'">
          MacOS
        </span>
        <span v-else>其他</span>
      </div>
      <div class="info-row-item">
        客户端微信版本：
        {{store.getters.getCurrentSession.client_version}}
      </div>
      <div class="info-row-item">
        KEY：<edit-able-text v-model="sessionData.wx_key" :mark="true"/>
      </div>
      <div class="info-row-item">
        客户端微信目录：<edit-able-text v-model="sessionData.wx_dir"/>
      </div>
      <div class="info-row-item">
        服务端数据目录：{{store.getters.getCurrentSession.data_path}}
      </div>
      <div class="info-row-item">
        创建时间：{{formatTimestamp(store.getters.getCurrentSession.create_time)}}
      </div>
      <div class="info-row-item">
        修改时间：{{formatTimestamp(store.getters.getCurrentSession.update_time)}}  （记录上次同步时间，从未同步过与创建时间相同）
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.info {
  padding: 0 10px;
  background-color: #FFFFFF;
  .info-base {
    display: flex;
    padding: 10px 0;
    border-bottom: 1px solid #f3f3f3;
    .info-head {
      width: 80px;
      height: 80px;
      img {
        width: 100%;
        height: 100%;
        border-radius: 3px;
      }
    }
    .info-wx {
      font-size: 12px;
      padding-left: 20px;
      .info-wx-item {
        color: #a7a7a7;
        display: flex;
        align-items: center;
        .item-edit {
          font-size: 12px;
          visibility: hidden;
        }
      }
      .info-wx-item:hover {
        .item-edit {
          visibility: visible;
          cursor: pointer;
        }
      }
      .info-wx-item-nickname {
        color: #4b4b4b;
        font-size: 16px;
      }
    }
  }
  .info-row {
    padding: 10px 0;
    //border-bottom: 1px solid #f3f3f3;
    .info-row-item {
      font-size: 12px;
      padding: 8px 0;
      color: #4b4b4b;
    }
  }
}
</style>