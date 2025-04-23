import { createApp, createVNode, render } from 'vue';
import Toast from './Toast.vue';

let toastApp = null;
let toastVNode = null;

const createToast = () => {
    const container = document.createElement('div');
    document.body.appendChild(container);

    return {
        success(options) {
            if (typeof options === 'string') {
                options = { message: options, type: 'success', duration: 2000 };
            }
            options.type = 'success';
            this.open(options);
        },
        warn(options) {
            if (typeof options === 'string') {
                options = { message: options, type: 'warn', duration: 2000 };
            }
            options.type = 'warn';
            this.open(options);
        },
        loading(options) {
            if (typeof options === 'string') {
                options = { message: options, type: 'loading', duration: 2000 };
            }
            options.type = 'loading';
            this.open(options, false);
        },
        open(options, autoClose = true) {
            if (typeof options === 'string') {
                options = { message: options, type: 'success', duration: 2000 };
            }
            if (toastVNode === null) {
                // 创建 Dialog 组件的 VNode
                toastVNode = createVNode(Toast);
                // 将 VNode 渲染到 DOM 中
                render(toastVNode, container);
            }

            // 打开对话框
            toastVNode.component.exposed.open({
                message: options.message,
                type: options.type,
            });

            // 定时关闭
            if (autoClose) {
                setTimeout(() => {
                    toastVNode.component.exposed.close();
                }, options.duration);
            }
        },
        close() {
            if (toastVNode !== null) {
                toastVNode.component.exposed.close();
            }
        }
    };
};

const toastPlugin = {
    install(app) {
        toastApp = createToast();
        app.config.globalProperties.$toast = toastApp;
    },
};

export default toastPlugin;