/**
 * 有备注先用备注，其次群备注，最后昵称
 * @param m
 * @returns {*}
 */
const displayName = (m) => {
    if (m.Remark) {
        return m.Remark;
    }
    let chatName = chatRoomNameMap[m.WxId];
    if (chatName) {
        return chatName;
    } else {
        return m.NickName;
    }
}
