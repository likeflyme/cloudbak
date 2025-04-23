import service from "../utils/request.js";

export const sysInfo = () => {
    return service.get(`/api/sys/sys-info`);
};


export const saveLicense = (license) => {
    const data = {
        'license_text': license
    }
    return service.post(`/api/sys/save-license`, data);
};

