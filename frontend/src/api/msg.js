import service from "../utils/request";
import {toBase64} from "js-base64";

export const session = (strUsrName) => {
    return service.get("/api/msg/session?username=" + strUsrName);
};

export const sessions = (page, size) => {
    const query = {
        page: page,
        size: size
    }
    return service.post(`/api/msg/sessions`, query);
};

export const msgBySvrId = (username, svrId, DbNo) => {
    return service.get(`/api/msg/msg_by_svr_id?svr_id=${svrId}&db_no=${DbNo}`);
};

export const singleMsg = (username, v3_msg_svr_id) => {
    return service.get(`/api/msg/single-msg?v3_msg_svr_id=${v3_msg_svr_id}&username=${username}`);
};


export const msgBySequence = (params) => {
    return service.get(`/api/msg/msgs-by-sequence?${params}`);
};

export const msgsAll = (query) => {
    return service.get(`/api/msg/msgs-all?strUsrName=${query.strUsrName}&page=${query.page}&size=${query.size}&start=${query.start}&dbNo=${query.dbNo}&filterType=${query.filterType}&filterText=${query.filterText}&filterDay=${query.filterDay}&filterUser=${query.filterUser}`);
};

export const msgs = (query) => {
    return service.post(`/api/msg/msgs`, query);
};

export const ghMsgs = (query) => {
    return service.get(`/api/msg/gh-msgs?strUsrName=${query.strUsrName}&page=${query.page}&size=${query.size}&start=${query.start}&dbNo=${query.dbNo}&filterType=${query.filterType}&filterText=${query.filterText}&filterDay=${query.filterDay}&filterUser=${query.filterUser}`);
};

export const msgsFilter = (query) => {
    return service.get(`/api/msg/msgs-filter?strUsrName=${query.strUsrName}&page=${query.page}&size=${query.size}&start=${query.start}&dbNo=${query.dbNo}&filterType=${query.filterType}&filterText=${query.filterText}&filterDay=${query.filterDay}&filterUser=${query.filterUser}&filterMode=${query.filterMode}`);
};

export const msgsByLocalId = (query) => {
    return service.get(`/api/msg/msgs-by-local-id?strUsrName=${query.strUsrName}&page=${query.page}&size=${query.size}&start=${query.start}&dbNo=${query.dbNo}&localId=${query.localId}&CreateTime=${query.CreateTime}&Sequence=${query.Sequence}&filterMode=${query.filterMode}`);
};

export const contact = () => {
    return service.get('/api/msg/contact');
};

export const contactSplit = (page, size, search, ChatRoomType=0) => {
    return service.get(`/api/msg/contact-split?page=${page}&size=${size}&ChatRoomType=${ChatRoomType}&search=${search}`);
};

export const contactSearch = (search) => {
    return service.get(`/api/msg/contact-search?search=${search}`);
};

export const chatroom = (chatroomName) => {
    return service.get(`/api/msg/chatroom?username=${chatroomName}`);
};

export const chatroomInfo = (chatroomName) => {
    return service.get(`/api/msg/chatroom-info?username=${chatroomName}`);
};

export const headImage = (usrName) => {
    return service.get("/api/resources/head-image?usrName=" + usrName);
};

export const contactPage = (query) => {
    return service.post('/api/msg/contact-page',query);
};
