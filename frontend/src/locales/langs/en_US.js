export default {
    login: {
        title: 'NavKeeper Sign In',
        loginBtn: 'Sign In',
        username: {
            placeholder: 'email',
            rule: {
                required: 'please input email'
            }
        },
        password: {
            placeholder: 'password',
            rule: {
                required: 'please input password'
            }
        },
        keepLogin: 'keep alive in this computer',
        forgetPassword: 'forget password',
        noAcct: 'Have no Account? Sign Up',
        doLogin: {
            notification: {
                title: 'Notification'
            }
        }
    },
    // 注册页面
    register: {
        title: 'NavKeeper Sign Up',
        placeholder: {
            username: 'Nickname',
            email: 'Email',
            password: 'Password',
            repeatPassword: 'Repeat Password'
        },
        rule: {
            username: {
                required: 'Please enter your nickname',
                repeat: 'Username already exists',
                formatError: 'Nickname must consist of letters, numbers, and underscores',
                lengthWrong: 'Nickname length should be at least 5 and at most 15 characters',
            },
            password: {
                required: 'Please enter your password',
                lengthWrong: 'Password length should be at least 8 and at most 32 characters',
                formatError: 'Password should contain at least two of the following: letters, numbers, or special characters'
            },
            repeatPassword: {
                required: 'Please repeat your password',
                notMatch: 'The two passwords you entered do not match'
            },
            email: {
                required: 'Please enter your email',
                formatError: 'Invalid email format',
                registed: 'Email already registered'
            }
        },
        signUpBtn: 'Sign Up',
        goLogin: 'Already have an account? Click here to login',
        notification: {
            title: 'Notification',
            successMsg: '<strong>Registration successful, You have been redirected to the login page. Please proceed to log in and enjoy the experience. </strong>'
        }
    },
    home: {
        title: 'NavKeeper, a Simple Tag Management Program',
        header: {
            search: {
                placeholder: 'Search shortcuts'
            },
            menu: {
                sysConfig: 'System Settings',
                logOut: 'Log Out'
            }
        },
        tools: {
            add: {
                tip: 'Add Directory'
            },
            import: {
                tip: 'Import Bookmarks'
            },
            settings: {
                tip: 'Settings'
            },
            clear: {
                confirm: 'Confirm',
                cancel: 'Cancel',
                title: 'Are you sure you want to clear all data? You will lose all data.'
            }
        },
        content: {
            group: {
                star: 'Frequently Used'
            }
        },
        dialogMenu: {
            addTitleBtn: 'Add Menu',
            editTitleBtn: 'Edit Menu',
            formInputTitle: 'Title',
            cancelBtn: 'Cancel',
            ruleTitleRequired: 'Please enter a title'
        },
        dialogImport: {
            title: 'Import',
            confirmBtn: 'Confirm',
            cancelBtn: 'Cancel',
            radioToolbar: 'Bookmarks Toolbar',
            radioAll: 'All',
            toolbarDesc: 'When importing only the bookmarks toolbar, the directories in the toolbar will become menu items, and individual shortcuts will be imported into a directory named "Bookmarks Toolbar".',
            allDesc: 'Import all bookmarks, including those on mobile devices.',
            desc: "To import bookmarks from another browser's bookmark file, if you are unsure how to export the bookmark file from the other browser, you can refer to the ",
            descHelpCenter: "Help Center",
            fileLabel: 'Select File',
            fileDesc: 'Existing data will not be overwritten.',
            fileSizeLimit: 'The file size limit for uploading is 2MB.',
            outLimit: 'The file size exceeds the limit(2M).'
        },
        dialogShare: {
            titleShare: 'Share',
            titleEdit: 'Edit',
            btnCancel: 'Cancel',
            label: {
                title: 'Title',
                password: 'Password',
                expire: 'Expiration Date',
                nodes: 'Select Bookmarks'
            },
            expireRadio: {
                day: '1 Day',
                week: '1 Week',
                month: '1 Month',
                year: '1 Year',
                forever: 'Never Expires',
                custom: 'Custom Date',
            },
            placeholder: {
                expire: 'Select an expiration date'
            },
            dialog: {
                title: 'Share Link',
                copy: 'Click to Copy',
                password: 'Password'
            },
            rules: {
                titleRequired: 'Please enter a title',
                nodesRequired: 'Please select the nodes to share'
            },
            addSucccess: {
                title: 'Share Successful',
                content: 'All shared links can be managed in the Settings'
            },
            addFail: {
                title: "Attention",
                noChecked: 'Please select the bookmarks you would like to share.'
            },
            copy: {
                title: 'Copy Successful',
                content: 'Your shared links Copy Successful'
            },
            updateSuccess: 'Update Successful',
            allBookmarks: 'All Bookmarks'
        },
        itemDyn: {
            updateBtn: 'Edit Shortcut',
            removeBtn: 'Remove'
        },
        itemFolder: {
            updateBtn: 'Edit Folder Name',
            removeBtn: 'Remove'
        },
        sidebar: {
            updateBtn: 'Edit',
            removeBtn: 'Remove'
        },
        itemAdd: {
            addBtn: 'Add'
        },
        dialogAdd: {
            title: {
                add: 'Add',
                edit: 'Edit',
                typeItem: 'Shortcut',
                typeFolder: 'Folder'
            },
            label: {
                type: 'Type',
                title: 'Title',
                link: 'Link',
                icon: 'Icon',
                upload: 'Upload'
            },
            recognize: {
                custom: 'Set Manually',
                customDesc: 'Manually set the link, or',
                auto: 'Automatically Recognize',
                autoDesc: 'Automatically recognize the link, or',
                fail: 'Auto-recognition failed. Please set manually.',
                extension: 'Suggest use browser extension'
            },
            chooseFile: 'Select Icon File',
            cancel: 'Cancel',
            rules: {
                required: {
                    link: 'Please enter the link',
                    title: 'Please enter the title',
                },
                linkFormat: 'must be a correct http link, such as https://www.xxx.com'
            },
            upload: {
                limitTitle: 'The uploaded file size exceeds the limit.',
                limitDesc: 'Maximum 100kb'
            }
        },
        settingsUser: {
            title: 'Settings',
            pane: {
                password: 'Change Password',
                users: 'User Management',
                shares: 'Share Management',
                lang: 'Language'
            }
        },
        updatePassword: {
            label: {
                oldPassword: 'Old Password',
                newPassword: 'New Password',
                repeatPassword: 'Confirm New Password'
            },
            btn: {
                confirm: 'Confirm'
            },
            rules: {
                oldPassword: {
                    required: 'Please enter the old password',
                },
                newPassword: {
                    required: 'Please enter a new password',
                    sameToOld: 'New password cannot be the same as the old password',
                },
                repeat: {
                    required: 'Please enter the new password again',
                    error: 'The repeated password is incorrect',
                }
            },
            updateSuccess: 'Password changed successfully'
        },
        users: {
            label: {
                username: 'Username',
                email: 'Email'
            },
            btn: {
                edit: 'Edit',
                enable: 'Enable',
                disable: 'Disable',
                add: 'Add User',
            },
            disabled: 'Disabled',
            dialog: {
                title: {
                    add: 'Add User',
                    edit: 'Edit User',
                },
                label: {
                    role: 'Role',
                    username: 'Username',
                    email: 'Email',
                    password: 'Password'
                },
                rules: {
                    username: 'Please enter the username',
                    email: 'Please enter the email',
                    password: 'Please enter the password'
                },
                roles: {
                    normal: 'Normal User'
                },
                cancel: 'Cancel'
            }
        },
        shares: {
            label: {
                title: 'Title',
                expire: 'Expiration Time',
                password: 'Password',
            }
        }
    },
    emailActive: {
        msg: {
            activing: 'Activating, please wait...',
            activeSuccess: {
                msg: 'Activation success! Now, go to manage all your tags',
                notificationTitle: 'Notification',
                notificationMsg: '<strong>Activation success: </strong>, you can now <a href="/home">click here to manage your tags</a>'
            },
            activeFail: 'Activation failed'
        }
    },
    index: {
        title: 'NavKeeper A simple yet powerful bookmark management tool.',
        login: 'Login',
        bannerContent: {
            desc: "Easy, Simple, and User-friendly",
            signUp: "Sign Up"
        },
        content1: {
            title: "Cross-platform Tag Management Software",
            desc: "NavKeeper combines the ease of use of a browser's built-in bookmark manager with additional features that a browser bookmark manager lacks. It is a simple tool for managing bookmarks, and you will definitely love it."
        },
        content2: {
            title: "Easy Management",
            desc: "Managing bookmarks is no longer a hassle",
            drag1Title: "Drag and Drop",
            drag1Content1: "You can simply drag and drop to change the position and directory, just like using a browser's tab manager. There is no additional learning cost, and it is intuitive to use.",
            drag1Content2: "Maybe you want to move Instagram from 'Social Media' to 'Media.' All you need to do is drag it. It's that simple.",
            drag2Title: "Free Dragging",
            drag2Content: "You can even directly drag a sidebar directory to any other directory, and it will become a directory. The organizational structure is similar to that of a browser's bookmark manager. Then, you can interact with it like opening a folder.",
            favoriteTitle: "Favorite Bookmarks",
            favoriteContent: "You can always have the bookmarks you want to see first displayed at the top. This feature is very convenient, just click the star."
        },
        search: {
            title: "Instant Retrieval",
            desc: "Simply enter a few keywords to quickly find your bookmarks."
        },
        other: {
            title: "Other Convenient Features",
            desc1: "Share links, automatic link detection, import browser bookmarks.",
            desc2: "In the future, we will also support browser plugins to make bookmark management even more convenient."
        }
    },
    share: {
        msg: {
            invalid: 'The shared link has expired.',
            expired: 'The shared link has expired.'
        }
    }
}
