export const initMembersMap = (chatroomInfo) => {
    let chatRoomNameMap = {}
    if (chatroomInfo.members) {
        for (let i = 0; i < chatroomInfo.members.length; i++) {
            let m = chatroomInfo.members[i]
            chatRoomNameMap[m.username] = m;
        }
    }
    return chatRoomNameMap;
}