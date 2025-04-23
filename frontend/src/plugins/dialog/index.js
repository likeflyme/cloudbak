import { createVNode, render } from 'vue';
import Dialog from './Dialog.vue';

const createDialog = () => {
    return {
        open(options) {
            const container = document.createElement('div');
            document.body.appendChild(container);

            // 创建新的 VNode
            const dialogVNode = createVNode(Dialog, {
                ...options,
                onConfirmed: () => {
                    // 调用传入的 onConfirmed 回调
                    options.onConfirmed?.();
                    // 清理 VNode 和容器
                    this.close(container);
                },
                onCancelled: () => {
                    // 调用传入的 onCancelled 回调
                    options.onCancelled?.();
                    // 清理 VNode 和容器
                    this.close(container);
                },
            });

            // 渲染 VNode 到 DOM 中
            render(dialogVNode, container);

            // 打开对话框
            dialogVNode.component.exposed.openDialog(options.title, options.desc);
        },
        close(container) {
            // 卸载 VNode 并移除容器
            render(null, container);
            document.body.removeChild(container);
        },
    };
};

const dialogPlugin = {
    install(app) {
        app.config.globalProperties.$dialog = createDialog();
    },
};

export default dialogPlugin;
