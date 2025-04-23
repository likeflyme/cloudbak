<script setup>
import unknownFile from '@/assets/filetypeicon/unknown.svg';
import excelFile from '@/assets/filetypeicon/excel.svg';
import exeFile from '@/assets/filetypeicon/exe.svg';
import pdfFile from '@/assets/filetypeicon/pdf.svg';
import mediaFile from '@/assets/filetypeicon/media.svg';
import pptFile from '@/assets/filetypeicon/ppt.svg';
import txtFile from '@/assets/filetypeicon/txt.svg';
import videoFile from '@/assets/filetypeicon/video.svg';
import wordFile from '@/assets/filetypeicon/word.svg';
import wpsFile from '@/assets/filetypeicon/wps.svg';
import {fileSize} from "@/utils/common.js";
import {useStore} from "vuex";

const store = useStore();
const props = defineProps({
  msg: {
    type: Object,
    required: true,
    default: () => ({
      name: 'Unknown',
      age: 0
    })
  }
})
const download = (path) => {
  if (path) {
    path = path.replace('\\', '/');
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
}

const getFileExt = (filename) => {
  if (!filename) {
    return '';
  }
  return filename.split('.').pop();
}
const fileExt = getFileExt(props.msg.compress_content.msg.appmsg.title)

const fileType = {
  'doc': wordFile,
  'docx': wordFile,
  'xls': excelFile,
  'xlsx': excelFile,
  'ppt': pptFile,
  'pptx': pptFile,
  'pdf': pdfFile,
  'txt': txtFile,
  'wps': wpsFile,
  'exe': exeFile,
  'mp4': videoFile,
  'mp3': mediaFile,
  'wav': mediaFile,
  'avi': mediaFile,
  'flv': mediaFile,
  'rmvb': mediaFile,
  'rm': mediaFile,
  'wmv': mediaFile
}

const imageType = fileType[fileExt] || unknownFile;
</script>

<template>
  <div class="chat-file" @click="download($props.msg.source)">
    <div class="chat-file-top">
      <div class="chat-file-left">
        <p class="chat-file-title">{{ $props.msg.compress_content.msg.appmsg.title }}</p>
        <p class="chat-file-content">{{ fileSize($props.msg.compress_content.msg.appmsg.appattach.totallen)}}</p>
      </div>
      <div class="chat-file-icon">
        <img class="item-icon" :src="imageType" alt=""/>
      </div>
    </div>
    <div class="chat-file-bottom">
      <p v-if="$props.msg.source" class="chat-file-app-info">
        <p v-if="$props.msg.compress_content.msg.appinfo" class="chat-file-app-info">{{ $props.msg.compress_content.msg.appinfo.appname }}</p>
      </p>
      <p v-else class="chat-file-app-info">
        未下载的文件
      </p>
    </div>
  </div>
</template>

<style scoped lang="less">
.chat-file {
  border: 1px solid #EDEDED;
  direction: ltr;
  width: 21.429rem;
  background-color: #FFFFFF;
  border-radius: 0.357rem;
  .chat-file-top {
    height: 5.357rem;
    border-bottom: 0.071rem solid #f0f0f0;
    display: flex;
    padding: 0.714rem;
    .chat-file-left {
      width: 16.429rem;
      height: 100%;
      .chat-file-title {
        font-size: 1rem;
        word-break: break-word;
      }
      .chat-file-content {
        font-size: 0.857rem;
        color: #797979;
        align-items: center;
      }
    }
    .chat-file-icon {
      width: 3.571rem;
      height: 100%;
      font-size: 2.143rem;
      text-align: center;
      color: #207346;
      .item-icon {
        width: 2.857rem;
      }
    }
  }
  .chat-file-bottom {
    .chat-file-app-info {
      font-size: 0.786rem;
      color: #797979;
      padding-left: 0.714rem;
      line-height: 1.786rem;
    }
  }
}
.chat-file:hover {
  cursor: pointer;
}
</style>