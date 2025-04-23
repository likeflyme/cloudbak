import service from "../utils/request.js";

export const msgsSearchTop5 = (match) => {
    return service.get(`/api/fts/msgs-match-top5?match=${match}`);
};

export const msgsSearch = (match) => {
    return service.get(`/api/fts/msgs-match?match=${match}`);
};

export const msgsSplit = (query) => {
    return service.post(`/api/fts/msgs-split`, query);
};

