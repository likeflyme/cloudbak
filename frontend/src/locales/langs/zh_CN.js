export default {
    // 登录页面
    login: {
        title: 'NavKeeper 登录',
        loginBtn: '登录',
        username: {
            placeholder: '邮箱',
            rule: {
                required: '请输入邮箱'
            }
        },
        password: {
            placeholder: '密码',
            rule: {
                required: '请输入密码'
            }
        },
        keepLogin: '保持登录',
        forgetPassword: '忘记密码',
        noAcct: '没有账户，点击这里注册',
        doLogin: {
            notification: {
                title: '通知'
            }
        }
    },
    // 注册页面
    register: {
        title: 'NavKeeper 注册',
        placeholder: {
            username: '昵称',
            email: '邮箱',
            password: '密码',
            repeatPassword: '重复输入密码'
        },
        rule: {
            username: {
                required: '请输入用户名',
                repeat: '用户名已被使用',
                formatError: '用户名必须为字母、数字、下划线组成',
                lengthWrong: '用户名长度需要至少5位最多15位',
            },
            password: {
                required: '请输入密码',
                lengthWrong: '密码长度至少8位最多32位',
                formatError: '密码至少包含：字母、数字、特殊符号之中的其中两种'
            },
            repeatPassword: {
                required: '请重复输入密码',
                notMatch: '两次输入的密码不匹配'
            },
            email: {
                required: '请输入邮箱',
                formatError: '邮箱格式错误',
                registed: '邮箱已被注册'
            }
        },
        signUpBtn: '注册',
        goLogin: '已经有账户了？点击这里登录',
        notification: {
            title: '通知',
            successMsg: '<strong>注册成功，<a href="/login">点这里去登录</a></strong>'
        }
    },
    // 主页，
    home: {
        title: 'NavKeeper 一个简单的标签管理程序',
        header: {
            search: {
                placeholder: '搜索快捷方式'
            },
            menu: {
                sysConfig: '系统设置',
                logOut: '退出登录'
            }
        },
        tools: {
            add: {
                tip: '添加目录'
            },
            import: {
                tip: '导入书签'
            },
            settings: {
                tip: '设置'
            },
            clear: {
                confirm: '确定',
                cancel: '取消',
                title: '你会丢失所有数据，确定要清除所有数据吗？'
            }
        },
        content: {
            group: {
                star: '常用'
            }
        },
        dialogMenu: {
            addTitleBtn: '添加菜单',
            editTitleBtn: '修改菜单',
            formInputTitle: '标题',
            cancelBtn: '取消',
            ruleTitleRequired: '请输入标题'
        },
        dialogImport: {
            title: '导入',
            confirmBtn: '确定',
            cancelBtn: '取消',
            radioToolbar: '书签栏',
            radioAll: '全部',
            toolbarDesc: '只导入书签栏时，书签栏中的目录将作为菜单栏，单独的快捷方式将导入同一个名为“书签栏”的目录。',
            allDesc: '全部导入将导入包括移动端的书签。',
            desc: '从其他浏览器的书签文件导入，如果你不知道如何从其他浏览器导出书签文件，可以参考',
            descHelpCenter: '帮助中心',
            fileLabel: '选择文件',
            fileDesc: '不会覆盖原有的数据',
            fileSizeLimit: '上传文件大小限制为 2MB.',
            outLimit: '超过文件大小限制 (2M).'
        },
        dialogShare: {
            titleShare: '分享',
            titleEdit: '修改',
            btnCancel: '取消',
            label: {
                title: '标题',
                password: '访问密码',
                expire: '过期时间',
                nodes: '选择书签'
            },
            expireRadio: {
                day: '一天',
                week: '一周',
                month: '一月',
                year: '一年',
                forever: '永不过期',
                custom: '其他日期',
            },
            placeholder: {
                expire: '选择一个过期日'
            },
            dialog: {
                title: '分享链接',
                copy: '点击复制',
                password: '密码'
            },
            rules: {
                titleRequired: '请输入标题',
                nodesRequired: '请选择要分享的节点'
            },
            addSucccess: {
                title: '分享成功',
                content: '可在设置中管理所有分享链接'
            },
            addFail: {
                title: '注意',
                noChecked: '请选择需要分享的书签'
            },
            copy: {
                title: '拷贝成功',
                content: '分享链接拷贝成功'
            },
            updateSuccess: '修改成功',
            allBookmarks: '所有书签'
        },
        itemDyn: {
            updateBtn: '修改快捷方式',
            removeBtn: '移除'
        },
        itemFolder: {
            updateBtn: '修改目录名',
            removeBtn: '移除'
        },
        sidebar: {
            updateBtn: '修改',
            removeBtn: '移除'
        },
        itemAdd: {
            addBtn: '添加'
        },
        dialogAdd: {
            title: {
                add: '添加',
                edit: '修改',
                typeItem: '快捷方式',
                typeFolder: '目录'
            },
            label: {
                type: '类型',
                title: '标题',
                link: '链接',
                icon: '图标',
                upload: '上传'
            },
            recognize: {
                custom: '手动设置',
                customDesc: '手动设置链接，也可以',
                auto: '自动识别',
                autoDesc: '自动识别链接，也可以',
                fail: '自动识别失败，请手动设置',
                extension: '推荐使用浏览器插件'
            },
            chooseFile: '选择图标文件',
            cancel: '取消',
            rules: {
                required: {
                    link: '请输入链接',
                    title: '请输入标题',
                },
                linkFormat: '必须为正确的http链接，例如 https://www.xxx.com'
            },
            upload: {
                limitTitle: '上传文件大小超过限制',
                limitDesc: '最大 100kb'
            }
        },
        // 用户设置
        settingsUser: {
            title: '设置',
            pane: {
                password: '修改密码',
                users: '用户管理',
                shares: '分享管理',
                lang: '语言'
            }
        },
        updatePassword: {
            label: {
                oldPassword: '原密码',
                newPassword: '旧密码',
                repeatPassword: '确认新密码'
            },
            btn: {
                confirm: '确定'
            },
            rules: {
                oldPassword: {
                    required: '请输入原密码',
                },
                newPassword: {
                    required: '请输入新密码',
                    sameToOld: '新密码与原密码禁止相同',
                },
                repeat: {
                    required: '请输入再次输入新密码',
                    error: '重复密码错误',
                }
            },
            updateSuccess: '修改成功'
        },
        users: {
            label: {
                username: '登录名',
                email: '邮箱'
            },
            btn: {
                edit: '修改',
                enable: '启用',
                disable: '注销',
                add: '添加用户',
            },
            disabled: '失效',
            dialog: {
                title: {
                    add: '添加用户',
                    edit: '修改用户',
                },
                label: {
                    role: '角色',
                    username: '登录名',
                    email: '邮箱',
                    password: '密码'
                },
                rules: {
                    username: '请输入登录名',
                    email: '请输入邮箱',
                    password: '请输入密码'
                },
                roles: {
                    normal: '普通用户'
                },
                cancel: '取消'
            }
        },
        shares: {
            label: {
                title: '标题',
                expire: '过期时间',
                password: '密码',
            }
        }
    },
    // email 激活页面
    emailActive: {
        msg: {
            activing: '正在激活，请稍后...',
            activeSuccess: {
                msg: '激活成功！现在，去管理您的所有标签',
                notificationTitle: '通知',
                notificationMsg: '<strong>激活成功: </strong>，现在可以<a href="/home">点击这里管理您的标签</a>'
            },
            activeFail: '激活失败'
        }
    },
    // 首页
    index: {
        title: 'NavKeeper 简单又强大的书签管理工具',
        login: '登录',
        bannerContent: {
            desc: '轻松，简单，又好用',
            signUp: '注册'
        },
        content1: {
            title: '跨平台的标签管理软件',
            desc: 'NavKeeper 具有浏览器自带书签管理器的易用性，也具备浏览器书签管理器所不具备的其他特性，且使用简单，是管理书签非常好的工具，你一定会爱上他'
        },
        content2: {
            title: '管理简单',
            desc: '管理书签不再是一件麻烦事儿',
            drag1Title: '拖拽换位',
            drag1Content1: '像使用浏览器标签管理器一样拖拽即可更换位置和目录，没有额外的学习成本，符合使用直觉。',
            drag1Content2: '也许你想将 Instgram 从 Social Medea 更改到 Media，你只需要拖动它；看，就是这么简单。',
            drag2Title: '自由拖拽',
            drag2Content: '你甚至可以直接将侧边栏目录拖动到任意一个其他目录下，它就会变成一个目录，组织结构与浏览器的书签管理没有差别。然后，你可以像打开文件夹一样操作它。',
            favoriteTitle: '最爱的书签',
            favoriteContent: '总有你想要第一时间就想看到的书签展示在最顶部，这个功能非常方便，只需要点击 star'
        },
        search: {
            title: '随时检索',
            desc: '简单输入几个关键字，就能快速查找你的书签'
        },
        other: {
            title: '还有其他方便的特性',
            desc1: '分享链接，链接添加自动识别，导入浏览器书签',
            desc2: '未来，我们还将支持浏览器插件，使书签的管理更加方便'
        }
    },
    share: {
        invalid: {
            invalidMsg: '分享链接已失效。',
            expiredMsg: '分享链接已过期。'
        }
    }
}
