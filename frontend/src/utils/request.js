import axios from 'axios'
import { token } from "./common";
import store from "../store";
import router from "../router";

/**
 * axios的传参方式：
 * 1.url 传参 一般用于Get和Delete 实现方式：config.params={JSON}
 * 2.body传参 实现方式：config.data = {JSON}，且请求头为：headers: { 'Content-Type': 'application/json;charset=UTF-8' }
 */
// axios实例
const service = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
    timeout: 5 * 60 * 1000,
    headers: { 'Content-Type': 'application/json;charset=UTF-8' }
})

// 请求拦截器
service.interceptors.request.use(
    (config) => {
        // 追加时间戳，防止GET请求缓存
        if (config.method?.toUpperCase() === 'GET') {
            config.params = { ...config.params, t: new Date().getTime() }
        }
        let authorization = token();
        if (authorization) {
            config.headers.Authorization = authorization;
        }

        return config;
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
        if (response.status !== 200) {
            return Promise.reject(new Error(response.statusText || 'Error'))
        }

        return response.data
    }
    ,
    error => {
        if (error && error.response && error.response.status === 403) {
            // 退出时清除数据
            store.commit('clear');
            router.push('/login');
        } else {
            return Promise.reject(error)
        }
    }
)

// 导出 axios 实例
export default service
