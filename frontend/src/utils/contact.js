import store from '../store/index.js'
import defaultImage from '@/assets/default-head.svg';
import notifymessage from '@/assets/wechat/notifymessage.png'
export const getContactById = (wxid) => {
    return store.getters.getContactMap[wxid];
}
export const getContactHeadById = (wxid) => {
    if (wxid === 'notifymessage') {
        return notifymessage;
    }
    const contact = getContactById(wxid);
    if (contact && contact.small_head_url) {
        return contact.small_head_url;
    } else {
        return `/api/resources/member-head/${store.getters.getCurrentSessionId}/${wxid}`
    }
}
export const getContactNickName = (wxid) => {
    const contact = getContactById(wxid);
    if (contact) {
        return contact.NickName;
    }
    return '';
}
export const getContactName = (wxid) => {
    const contact = getContactById(wxid);
    if (contact) {
        if (contact.remark && contact.remark !== '') {
            return contact.remark;
        } else {
            return contact.nickname;
        }
    }
    return '';
}