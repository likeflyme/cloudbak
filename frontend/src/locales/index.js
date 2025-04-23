import { createI18n } from 'vue-i18n'
import zh_CN from './langs/zh_CN'
import en_US from './langs/en_US'
import { getUserLanguage } from '../utils/language'

// 创建 i18n
const i18n = createI18n({
  legacy: false,
  globalInjection: true, // 全局模式，可以直接使用 $t
  locale: getUserLanguage(),
  messages: {
    zh_CN,
    en_US
  }
})

export default i18n