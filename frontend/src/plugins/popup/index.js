// src/plugins/popup-plugin.js
import {createVNode, reactive, render} from 'vue';
import Popup from "./Popup.vue";

let popupCount = 0; // 记录打开过的窗口数量
let lastTop = 0;
let lastLeft = 0;

const popupState = reactive({
    windows: []
});
let prev = null;

export default {
    install(app) {

        app.config.globalProperties.$popup = {
            open(Component, props, options = {}) {
                popupCount++;
                let slotVNode;
                if (props) {
                    slotVNode = createVNode(Component, props);
                } else {
                    slotVNode = createVNode(Component);
                }

                // 设置窗口的默认配置
                const { width = '400px', height = '300px' } = options;

                if (lastTop === 0) {
                    lastTop = (window.innerHeight - parseInt(height)) / 2;
                    lastLeft = (window.innerWidth - parseInt(width)) / 2;
                } else {
                    lastTop += 20;
                    lastLeft += 20;
                }
                options['top'] = lastTop + 'px';
                options['left'] = lastLeft + 'px';
                options['id'] = `popup-${popupCount}`;
                options['zIndex'] = 800 + popupCount;


                const windowVNode = createVNode(Popup, {
                    ...options, // 传递options中的所有参数
                    close: () => {
                        this.closeOnPopup(options['id']); // 调用插件中的关闭函数
                    }
                }, {
                    default: () => slotVNode  // 将 slotVNode 传递给默认插槽
                });
                // 注入 app context
                windowVNode.appContext = app._context;
                windowVNode['id'] = options['id'];
                prev = windowVNode;

                const container = document.createElement('div');
                container['id'] = options['id'];
                popupState.windows.push(container);
                document.body.appendChild(container);
                render(windowVNode, container);
            },
            closeOnPopup(id) {
                const index = popupState.windows.findIndex(win => win.id === id);
                if (index !== -1) {
                    const containers = popupState.windows.splice(index, 1);
                    if (containers.length === 0) {
                        console.warn(`No popup found with id: ${id}`);
                        return;
                    }
                    if (containers.length !== 1) {
                        console.warn(`Multiple popups found with id: ${id}`);
                        return;
                    }
                    lastTop -= 20;
                    lastLeft -= 20;
                    const container = containers[0];
                    render(null, container);

                    // 从 DOM 中移除容器
                    if (container.parentNode) {
                        container.parentNode.removeChild(container);
                    }
                } else {
                    console.warn(`No popup found with id: ${id}`);
                }
            }
        };



    }
};