import service from "../utils/request";


export const taskList = (page, size) => {
    return service.get("/api/task/?page=" + page + "&size=" + size);
};

export const taskLog = (taskId) => {
    return service.get("/api/task/log?task_id=" + taskId);
};

export const singleDecrypt = (sessionId, deep = false) => {
    return service.post(`/api/task/single-decrypt/${sessionId}/${deep}`);
}

export const updateConf = (sessionId) => {
    return service.post(`/api/task/single-decrypt/${sessionId}`);
}


