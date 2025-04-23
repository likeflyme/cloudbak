import {createRouter, createWebHistory} from "vue-router";
import {isLogin} from '../utils/common';

const routes = [
    {
        path: '/',
        name: 'home',
        meta: {
            title: '云朵备份',
            loginRequire: true
        },
        component: () => import("../views/Home.vue"),
        children:[
            {
                name: 'session',
                path: 'session/:sessionId',
                // component: () => import("../views/main/Main.vue"),
                components: {
                    default: () => import("../views/main/Main.vue"),
                    toolsView: () => import("../components/tools/SysTools.vue"),
                },
                children: [
                    {
                        name: 'address-book',
                        path: 'address-book',
                        component: () => import("../views/main/addressbook/AddressBook.vue"),
                        children: [
                            {
                                name: 'chat-room-info',
                                path: 'chat-room-info/:id',
                                component: () => import("../views/main/addressbook/info/ChatRoomInfo.vue"),
                            },
                            {
                                name: 'user-info',
                                path: 'user-info/:id',
                                component: () => import("../views/main/addressbook/info/UserInfo.vue"),
                            }
                        ]
                    },
                    {
                        name: 'comment',
                        path: 'comment',
                        component: () => import("../views/main/comment/Comment.vue"),
                        children: [
                            {
                                name: "chat",
                                path: ':id',
                                component: () => import("../views/main/comment/CommentChat.vue"),
                            }
                        ]
                    },
                    {
                        name: 'collect',
                        path: 'collect',
                        component: () => import("../views/main/collect/Collect.vue"),
                    },
                    {
                        name: 'files',
                        path: 'files',
                        component: () => import("../views/main/files/Files.vue"),
                    },
                    {
                        name: 'community',
                        path: 'community',
                        component: () => import("../views/main/community/Community.vue"),
                    },
                    {
                        name: 'user',
                        path: 'user',
                        component: () => import("../views/main/user/user.vue"),
                    }
                ]
            }
        ]
    },
    {
        path: '/login',
        name: 'login',
        meta: {
            title: '云朵备份-登录',
            loginRequire: false
        },
        component: () => import("../views/Login.vue"),
    },
    {
        path: '/install',
        name: 'install',
        meta: {
            title: '云朵备份-安装',
            loginRequire: false
        },
        component: () => import("../views/Install.vue"),
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title;
    // 需要登录且未登录，则重定向到 login 页
    if (to.matched.some(record => record.meta.loginRequire) && !isLogin()) {
        next({
            path: '/login',
        })
    } else {
        next();
    }
});

export default router
