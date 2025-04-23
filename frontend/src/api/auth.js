import service from "../utils/request";

export const token = (data) => {
    return service.post("/api/auth/token", data, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
};
export const userinfo = () => {
    return service.get("/api/auth/me")
};

export const getTwoStepQrcode = () => {
    return service.get("/api/auth/get-two-step-qrcode")
};
