import service from "../utils/request";


export const allConf = () => {
    return service.get("/api/conf/all-conf");
};

export const updateConf = (conf_key, conf_value) => {
    let data = {
        "conf_key": conf_key,
        "conf_value": conf_value
    }
    return service.post("/api/conf/update-conf", data);
};

export const sysConf = () => {
    return service.get("/api/conf/load-sys-conf");
};

export const sessionConf = () => {
    return service.get("/api/conf/load-session-conf");
};

export const userConf = () => {
    return service.get("/api/conf/load-user-conf");
};
