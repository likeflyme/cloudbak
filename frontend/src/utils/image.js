import {useStore} from "vuex";
import {toBase64} from "js-base64";

const store = useStore();

// 图片代理判断
export const getImageUrl = (url) => {
    if (url) {
        if (url.startsWith("/")) {
            return url;
        }
        if (store.getters.isPictureProxy) {
            return `/api/resources/image-proxy?encoded_url=${toBase64(url)}`;
        } else {
            return url;
        }
    }
    return defaultImage;
}
