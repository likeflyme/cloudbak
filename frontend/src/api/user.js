import service from "../utils/request";

export const sysSessions = () => {
    return service.get("/api/user/sys-sessions")
};

export const sessionCheck = (sessionId) => {
    return service.get(`/api/user/session-check/${sessionId}`)
}

export const updateCurrentSession = (sessionId) => {
    return service.put(`/api/user/set-current-session-id?sys_session_id=${sessionId}`)
}

export const addSysSession = (data) => {
    return service.post("/api/user/sys-session", data)
};

export const updateSysSession = (data) => {
    return service.put(`/api/user/sys-session`, data)
};

export const checkInstall = () => {
    return service.get("/api/user/check-install")
};

export const createUser = (data) => {
    return service.post("/api/user/create-user", data)
};
export const deleteSession = (sys_session_id) => {
    return service.delete(`/api/user/sys-session/${sys_session_id}`)
};

export const updatePassword = (data) => {
    return service.put("/api/user/update-password", data)
};

export const users = () => {
    return service.get("/api/user/users")
}

export const userBan = (userId) => {
    return service.put("/api/user/ban/" + userId)
}

export const userActive = (userId) => {
    return service.put("/api/user/active/" + userId)
}
