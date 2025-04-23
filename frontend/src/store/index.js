import {createStore} from 'vuex'

const state = {
    sysInfo: {},
    sessions: [],
    mapSessions: {},
    userInfo: {
        current_session: {}
    },
    mappedContact: {},
    // 联系人页面用户详情
    addrShowUser: {},
    sysSessions: [],
    error: {
        show: false,
        msg: '错误消息',
        delay: 10000,
        tm: null
    },
    sysTool: {
        show: false
    },
    sysConf: {

    },
    userConf: {

    },
    sessionConf: {

    },
    contactArray: {},
    contactMap: {},
    chatroomInfo: {}
}

const mutations = {
    setSysInfo(state, sysInfo) {
        state.sysInfo = sysInfo;
        state.sysConf = sysInfo.sys_conf
    },
    setLicense(state, license) {
        state.sysInfo.license = license.license;
        state.sysInfo.license_info = license
    },
    setSessions (state, sessions) {
        state.sessions = sessions
    },
    setUserInfo (state, userInfo) {
        state.userInfo = userInfo;
    },
    setContact(state, contact) {
        for (let c of contact) {
            state.mappedContact[c.UserName] = c;
        }
    },
    setAddrShowUser (state, addrShowUser) {
        state.addrShowUser = addrShowUser;
    },
    setSysSessions (state, sysSessions) {
        state.sysSessions = sysSessions
    },
    addSysSessions(state, session) {
        state.sysSessions.push(session);
    },
    setCurrentSession(state, sysSession) {
        state.userInfo.current_session_id = sysSession.id;
        state.userInfo.current_session = sysSession;
    },
    dropSession(state, sysSessionId) {
        state.sysSessions = state.sysSessions.filter(session => session.id !== sysSessionId);
    },
    showErrorToastMsg(state, err) {
        state.error.msg = err.msg;
        state.error.show = true;
        let delay = state.error.delay;
        if (err.delay) {
            delay = err.delay;
        }
        // 先清除前一个延时处理任务
        if (state.error.tm) {
            clearTimeout(state.error.tm);
        }
        state.error.tm = setTimeout(function () {
            state.error.show = false;
        }, delay);
    },
    closeErrorToastMsg(state) {
        if (state.error.tm) {
            state.error.show = false;
            clearTimeout(state.error.tm);
            state.error.tm = null;
        }
    },
    openSysTool (state) {
        state.sysTool.show = true;
    },
    closeSysTool (state) {
        state.sysTool.show = false;
    },
    setUserConf(state, userConf) {
        try {
            state.userConf = JSON.parse(userConf.conf_value);
        } catch (e) {
            console.log(e);
        }
    },
    addSessionConf(state, sessionConf) {
        try {
            state.sessionConf[sessionConf.session_id] = JSON.parse(sessionConf.conf_value);
        } catch (e) {
            console.log(e);
        }
    },
    loadContact(state, array) {
        let current_session_id = state.userInfo.current_session.id;
        state.contactArray[current_session_id] = array;
        const sessionContactMap = {}
        for (let i of array) {
            sessionContactMap[i.username] = i;
        }
        state.contactMap[current_session_id] = sessionContactMap;

    },
    clearContact(state) {
        state.contactMap = {};
        state.contactArray = [];
    },
    setSysConf(state, sysConf) {
        state.sysConf = sysConf;
    },
    resetState(state) {
        state.sessions.length = 0;
    },
    setChatroomInfo(state, info) {
        let current_session_id = state.userInfo.current_session.id;
        let sessionChatroomInfo = state.chatroomInfo[current_session_id];
        if (sessionChatroomInfo) {
            sessionChatroomInfo[info.username] = info;
        } else {
            sessionChatroomInfo = {}
            sessionChatroomInfo[info.username] = info
            state.chatroomInfo[current_session_id] = sessionChatroomInfo
        }
    }
}

const getters = {
    getSysInfo(state) {
        return state.sysInfo;
    },
    getSessions (state) {
        return state.sessions;
    },
    getUserInfo (state) {
        return state.userInfo;
    },
    getHeadImgPath(state) {
        return '/head/' + state.userInfo.current_session.id + '/';
    },
    getCurrentWxId(state) {
        return state.userInfo.current_session.wx_id;
    },
    getCurrentSessionName(state) {
        return state.userInfo.current_session.name;
    },
    getCurrentSessionId(state) {
        return state.userInfo.current_session_id;
    },
    getCurrentSession(state) {
        return state.userInfo.current_session;
    },
    getCurrentWxHeadImgPath(state) {
        return getters.getHeadImgPath(state) + getters.getCurrentWxId(state) + '.jpg'
    },
    getMappedContact(state) {
        return state.mappedContact;
    },
    getAddrShowUser(state) {
        return state.addrShowUser;
    },
    getSysSessions(state) {
        return state.sysSessions;
    },
    isShowToastMsg(state) {
        return state.error.show;
    },
    getToastMsg(state) {
        return state.error.msg;
    },
    isShowSysTools(state) {
        return state.sysTool.show;
    },
    getUserConf(state) {
        return state.userConf;
    },
    getSysConf(state) {
        return state.sysConf;
    },
    getSessionConf(state) {
        return state.sessionConf;
    },
    getCurrentSessionConf() {
        return state.sessionConf[state.userInfo.current_session_id];
    },
    getContactMap(state) {
        const currentSessionId = state.userInfo.current_session.id;
        if (currentSessionId in state.contactMap) {
            return state.contactMap[currentSessionId];
        } else {
            return {};
        }
    },
    getContactArray(state) {
        const currentSessionId = state.userInfo.current_session.id;
        if (currentSessionId in state.contactArray) {
            return state.contactArray[currentSessionId];
        } else {
            return [];
        }
    },
    isContactsLoaded(state) {
        const currentSessionId = state.userInfo.current_session.id;
        return currentSessionId in state.contactMap;
    },
    isAdmin(state) {
        return state.userInfo.id === 1;
    },
    isPictureProxy(state) {
        return state.sysConf.picture.use_proxy;
    },
    getClientVersion(state) {
        return state.userInfo.current_session.client_type + '.' + state.userInfo.current_session.client_version;
    },
    getAllChatroomInfo(state) {
        let current_session_id = state.userInfo.current_session.id;
        let info = state.chatroomInfo[current_session_id]
        if (info === undefined) {
            return {};
        } else {
            return info;
        }
    }
}

// 创建一个新的 store 实例
const store = createStore({
    state,
    mutations,
    getters
});
export default store;
