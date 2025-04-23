<script setup>
import {fromXmlToJson} from "@/utils/common.js";
import {reactive} from "vue";
import {useStore} from "vuex";
import cleanedImage from '@/assets/cleaned.jpeg';
import MsgMerge from "./MsgMerge.vue";
import {msgBySvrId, singleMsg} from "@/api/msg.js";

const store = useStore();

const props = defineProps({
  recorditem: {
    type: Object,
    required: true
  }
});

const getRecordInfo = (recorditem) => {
  if ('recordxml' in recorditem) {
    return recorditem.recordxml.recordinfo;
  } else {
    return recorditem.recordinfo;
  }
}

const data = getRecordInfo(props.recorditem);

const imageOptions = reactive({
  // 配置选项
  toolbar: true,
  title: true,
  tooltip: true,
  movable: true,
  zoomable: true,
  rotatable: true,
  scalable: true,
  transition: false,
  url: 'data-original',
  filter(image) {
    // 排除带有 exclude 类的 img 元素
    return !image.classList.contains('exclude');
  },
});

// datasourceid 格式: wxid#MsgSrvId$number
const getDataSourceId = (item) => {
  const attr = item['@attributes'];
  if ('datasourceid' in attr) {
    const datasourceid = item['@attributes'].datasourceid
    if (datasourceid.search('#') !== -1) {
      let msgidSeq = datasourceid.split('#')[1];
      if (msgidSeq.search('$')) {
        return msgidSeq.split('$')[0];
      } else {
        return msgidSeq;
      }
    } else {
      return datasourceid;
    }
  } else {
    return attr.dataid;
  }
}

const downloadFile = (datasourceid) => {
  singleMsg('', datasourceid).then(resp => {
    if (resp && resp.windows_v3_properties && resp.windows_v3_properties.source) {
      const source = resp.windows_v3_properties.source;
      const path = source.replace('\\', '/');
      const fileName = path.split('/').pop();
      let sessionId = store.getters.getCurrentSessionId;
      let url = `/api/resources/relative-resource?relative_path=${encodeURIComponent(path)}&session_id=${sessionId}&resource_type=file`;
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      // 将<a>元素添加到DOM
      document.body.appendChild(link);
      // 触发点击事件
      link.click();
      // 移除<a>元素
      document.body.removeChild(link);
    }
  }).catch(e => {
    console.log(e);
  })
}

// 格式化内容
// 1. 匹配的值设置为绿色
// 2. 换行符替换为 <br>
const formatContent = (content) => {
  return content.replace(/\n/g, '<br>');
}
</script>

<template>
  <!--
    合并转发消息模板
    props.msg.Type 表示类型：
      1: 文本消息
      2：图片消息
      3：语音消息
      4：视频消息
      17：合并转发消息
  -->
  <div class="td" v-viewer="imageOptions">
    <!-- 文本类型 -->
    <div class="td-row" v-for="item in data.datalist.dataitem">
      <div class="td-left">
        <div class="td-head"><img class="head-img exclude" alt="head" :src="item.sourceheadurl['#text']"/></div>
      </div>
      <div class="td-right">
        <div class="td-right-head">
          <div class="td-right-head-title">{{ item.sourcename['#text'] }}</div>
          <div class="td-right-head-time">{{ item.sourcetime['#text'] }}</div>
        </div>
        <div class="td-right-content">
          <div class="td-right-text" v-if="item['@attributes'].datatype === '1'" v-html="formatContent(item.datadesc['#text'])">
          </div>
          <div class="td-right-content-image" v-else-if="item['@attributes'].datatype === '2'">
            <!-- datasourceid 格式为 微信id#数据id$序号 是转发未知对话的消息，根据fullmd5查询图片表，否则根据 datasourceid 查询原交易图片数据 -->
            <img v-if="item['@attributes'].datasourceid && item['@attributes'].datasourceid.search('#') === -1" alt=""
                 v-lazy="`/api/resources/resource-from-source-id/${store.getters.getCurrentSessionId}/${item['@attributes'].datasourceid}`"
                 :data-original="`/api/resources/resource-from-source-id/${store.getters.getCurrentSessionId}/${item['@attributes'].datasourceid}?file_type=Image`"/>
            <img v-else alt=""
                 v-lazy="`/api/resources/image-from-full-md5/${store.getters.getCurrentSessionId}/${item.fullmd5['#text']}`"
                 :data-original="`/api/resources/image-from-full-md5/${store.getters.getCurrentSessionId}/${item.fullmd5['#text']}?file_type=Image`"/>
          </div>
          <div class="td-right-content-video" v-else-if="item['@attributes'].datatype === '4'">
            <video controls width="250" :poster="`/api/resources/resource-from-source-id/${store.getters.getCurrentSessionId}/${getDataSourceId(item)}`">
              <source :src="`/api/resources/resource-from-source-id/${store.getters.getCurrentSessionId}/${getDataSourceId(item)}?file_type=Video`" type="video/mp4" />
            </video>
          </div>
          <!-- 文件 -->
          <div class="td-right-content-file" v-else-if="item['@attributes'].datatype === '8'">
            <u class="file-btn" @click="downloadFile(item['@attributes'].datasourceid)">{{ item.datatitle['#text'] }}</u>
          </div>
          <div class="td-right-content-transfer" v-else-if="item['@attributes'].datatype === '17'">
            <MsgMerge
                class="msg-transfer"
                :title="item.datatitle['#text']"
                :desc="item.datadesc['#text']"
                :recorditem="item"/>
          </div>
          <div v-else>
            不支持的合并消息类型：{{ item['@attributes'].datatype }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.td {
  padding: 10px 0;
  width: 500px;
  margin: 0 auto;
  word-break: break-word;

  .td-row {
    display: flex;
    padding-bottom: 10px;

    .td-left {
      width: 50px;

      .head-img {
        width: 35px;
        height: 35px;
      }
    }

    .td-right {
      flex-grow: 1;
      border-bottom: 1px solid #f2f2f2;
      padding-bottom: 10px;

      .td-right-head {
        display: flex;
        color: #aeaeae;
        justify-content: space-between;

        .td-right-head-title {
          font-size: 14px;
        }

        .td-right-head-time {
          font-size: 12px;
        }
      }

      .td-right-content {
        color: #3f3f3f;

        .td-right-content-image {
          max-width: 350px;

          img {
            max-width: 100%;
          }
        }

        .td-right-text {
          max-width: 400px;
        }
        .td-right-content-transfer {
          .msg-transfer {
            background-color: #ebebeb;
          }
        }
        .td-right-content-file {
          .file-btn {
            cursor: pointer;
            color: #0b6bb7;
          }
        }
      }
    }
  }
}
</style>