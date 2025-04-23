<script setup>
import {toBase64} from "js-base64";
import {useStore} from "vuex";

const store = useStore();
const props = defineProps({
  msg: {
    type: Object,
    required: true
  }
});
const noticeType = props.msg.compress_content?.msg?.appmsg?.mmreader?.category['@type'];
const count = props.msg.compress_content?.msg?.appmsg?.mmreader?.category['@count'];
const appmsg = props.msg.compress_content?.msg?.appmsg;

const openLink = (url) => {
  window.open(url);
}

// 图片代理判断
const getImageUrl = (url) => {
  if (url) {
    if (url.startsWith("/")) {
      return url;
    }
    if (store.getters.isPictureProxy) {
      return `/api/resources/image-proxy?encoded_url=${toBase64(url)}`;
    } else {
      return url;
    }
  }
  return '';
}
</script>

<template>
  <div class="n-container">
    <!-- 简单通知类消息 -->
    <div class="n-box" v-if="noticeType === '0'">
      <div class="n-row n-header" v-if="props.msg.compress_content?.msg?.appmsg?.mmreader?.template_header?.display_name">
        <img class="n-header-img" width="20" height="20" :src="props.msg.compress_content?.msg?.appmsg?.mmreader?.template_header?.icon_url" alt="商户图标"/>
        <p class="n-header-name">{{ props.msg.compress_content?.msg?.appmsg?.mmreader?.template_header?.display_name }}</p>
      </div>
      <div class="n-row n-body">
        <div class="n-body-trans-type">
          {{ appmsg?.mmreader?.template_header?.title }}
        </div>
        <div class="n-body-trans">
          <p class="n-body-trans-title">{{ appmsg?.mmreader?.template_detail?.line_content?.topline?.key?.word }}</p>
          <p class="n-body-trans-amt">{{ appmsg?.mmreader?.template_detail?.line_content?.topline?.value?.word }}</p>
        </div>
        <div class="n-body-trans-desc" v-for="line in props.msg.compress_content?.msg?.appmsg?.mmreader?.template_detail?.line_content.lines.line">
          <p class="n-body-trans-desc-label">{{ line.key?.word }}</p>
          <p class="n-body-trans-desc-value">{{ line.value?.word }}</p>
        </div>
      </div>
    </div>
    <div class="n-box" v-else-if="noticeType === '20'">
      <div class="n-card n-card-single" v-if="count === '1'" @click="openLink(appmsg?.mmreader?.category?.item?.url)">
        <div class="n-card-img-container n-card-single-img">
          <img class="n-img exclude" :alt="appmsg?.mmreader?.category?.item?.cover" :src="getImageUrl(appmsg?.mmreader?.category?.item?.cover)"/>
          <div class="n-card-img-title" v-html="appmsg?.mmreader?.category?.item?.title">
          </div>
        </div>
        <div class="n-card-single-desc">
          <p class="n-card-single-desc-title" v-html="props.msg.compress_content?.msg?.appmsg?.mmreader?.category?.item?.title"></p>
        </div>
      </div>

      <div class="n-card-multi" v-else>
        <div v-for="(item, index) in appmsg.mmreader.category.item">
          <div class="n-card-img-container n-card-multi-img" v-if="index === 0" @click="openLink(item.url)">
            <img class="n-img exclude" :alt="item.cover" :src="getImageUrl(item.cover)"/>
            <div class="n-card-img-title">
              {{ item.title }}
            </div>
          </div>
          <div class="n-card-multi-item" @click="openLink(item.url)" v-else>
            {{ item.title }}
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <!-- 不支持的消息类型：{{ noticeType }} -->
    </div>
  </div>
</template>

<style scoped lang="less">
.n-container {
  width: 100%;
  .n-box {
    margin: 5px auto;
    background-color: #FFFFFF;
    border-radius: 3px;
    width: 350px;
    direction: ltr;
    .n-row {
      padding: 10px;
    }
    .n-header {
      display: flex;
      .n-header-img {
        width: 20px;
        height: 20px;
      }
      .n-header-name {
        margin-left: 20px;
      }
    }
    .n-body {
      .n-body-trans-type {
        padding: 10px 0;
      }
      .n-body-trans {
        padding: 10px 0;
        .n-body-trans-title {
          text-align: center;
          color: #888888;
        }
        .n-body-trans-amt {
          text-align: center;
          font-size: 30px;
        }
      }
      .n-body-trans-desc {
        display: flex;
        padding: 5px 0;
        .n-body-trans-desc-label {
          color: #888888;
          width: 70px;
        }
        .n-body-trans-desc-value {
          flex-grow: 1;
        }
      }
    }
  }
  .n-box .n-row {
    position: relative;
  }
  .n-box .n-row:not(:first-child)::before {
    content: "";                    /* 创建伪元素 */
    position: absolute;             /* 绝对定位 */
    top: 0;                         /* 定位到顶部 */
    left: 0;                        /* 从左边开始 */
    width: 100%;                    /* 横向填满 */
    height: 1px;                    /* 设置初始高度为1px */
    background-color: #e7e7e7;         /* 边框颜色 */
    transform: scaleY(0.7);         /* 缩小宽度为70% */
    transform-origin: left;         /* 缩放起点为左侧 */
  }
  .no-support {
    padding: 10px;
    color: #888888
  }

  .n-box .n-card-single {
    .n-card-single-desc {
      padding: 15px;
      .n-card-single-desc-title {
        color: gray;
        padding-bottom: 10px;
      }
      .n-card-single-desc-detail {
        padding-top: 10px;
      }
    }
  }
  .n-box .n-card-single:hover {
    cursor: pointer;
  }

  .n-box  {
    .n-card-multi {
      .n-card-multi-img:hover {
        cursor: pointer;
      }
      .n-card-multi-item {
        padding: 15px;
      }
      .n-card-multi-item:hover {
        cursor: pointer;
      }
    }
  }
  .n-box {
    .n-card-img-container {
      position: relative;
      width: 100%;
      .n-card-img-title {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 5px 0;
        text-indent: 10px;
      }
    }
  }
  .n-card-multi .n-card-multi-item:not(:first-child) {
    border-top: 1px solid #ccc; /* 你可以根据需要调整边框的颜色和样式 */
  }
  .n-img {
    width: 100%;
  }
}
</style>