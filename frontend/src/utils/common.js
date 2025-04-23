export const getDomain = (url) => {
    let domain = url.split('/');
    if (domain[2]) {
        domain = domain[2];
    } else {
        domain = '';
    }
    return domain;
};

export const isLogin = () => {
    return !!token();
};

export const token = () => {
    return localStorage.getItem("token");
};

export const loginSuccess = (resp) => {
    let token = resp.token_type + " " + resp.access_token;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(resp));
    // 设置 cookies token 用于 home 页数据共享
    let home_host = import.meta.env.VITE_HOME_HOST;
    document.cookie = "token=" + token + ";domain=" + home_host + "; path=/;";
    document.cookie = "username=" + resp.username + ";domain=" + home_host + "; path=/;";
}

export const loginUser = () => {
    let user = localStorage.getItem("user");
    if (user) {
        return JSON.parse(user);
    }
}

export const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
};

export const lengthOfCharts = (str) => {
    let m = 0;
    let a = str.split("");
    for (let i = 0; i < a.length; i++) {
        if (a[i].charCodeAt(0) < 299) {
            m++;
        } else {
            m += 2;
        }
    }
    return m;
}

// 缩略字符串，一个中文按照两位计算，英文一位
export const shortenCharts = (str, max, suffix) => {
    if (str) {
        let m = 0, str_return = '';
        let a = str.split("");
        for (let i = 0; i < a.length; i++) {
            if (a[i].charCodeAt(0) < 299) {
                m++;
            } else {
                m += 2;
            }
            if (m > max) {
                if (suffix)
                    str_return += suffix;
                break;
            }
            str_return += a[i];
        }
        return str_return;
    } else {
        return str;
    }
}

// 根据微信号获取用户信息
export const getUserByWxId = (store, name) => {
    return store.getters.getMappedContact[name];
}

// 根据微信号获取用户备注或昵称
export const getUserNameByWxId = (store, wxId) => {
    let user = getUserByWxId(store, wxId);
    if (user) {
        if (user.Remark){
            return user.Remark;
        } else {
            return user.NickName;
        }
    } else {
        return '未知用户'
    }
}

const chatType = (wxid) => {
    if (wxid.includes('@')) {
        return 0;
    } else {
        return 1;
    }
}

export const isChatRoom = (wxid) => {
    return chatType(wxid) === 0;
}

export const parseXml = (xmlString) => {
    const parser = new DOMParser();
    return parser.parseFromString(xmlString, 'application/xml');
};

export const getReferFileName = (content) => {
    try {
        let array = content.split(':');
        let xmlStr = array[0];
        if (array.length === 2) {
            xmlStr = array[1]
        }
        let dom = parseXml(xmlStr.trim());
        let title = dom.getElementsByTagName('title')[0];
        return title.textContent;
    } catch (e) {
        console.error(e)
    }
    return 'Undefined';
}

export const getThumbFromStringContent = (content) => {
    try {
        let dom = parseXml(content);
        const emoji = dom.querySelector('emoji');
        if (emoji) {
            return emoji.getAttribute('cdnurl');
        }
        return '';
    } catch (e) {
        console.error(e)
    }
    return '';
}

export const getVoiceLength = (content) => {
    try {
        let dom = parseXml(content);
        const length = dom.querySelector('voicemsg').getAttribute('length');
        // 将毫秒转换为秒和分钟
        const seconds = Math.floor(length / 1000);
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;

        // 格式化为分钟和秒
        if (minutes > 0) {
            return `${minutes}m ${remainingSeconds}"`;
        } else {
            return `${remainingSeconds}"`;
        }
    } catch (e) {
        console.error(e)
    }
    return '';
}


export const xmlToJson = (xml) => {
    let obj = {};

    // 如果是元素节点，获取节点名称和属性
    if (xml.nodeType === 1) {
        // 获取所有属性
        if (xml.attributes.length > 0) {
            obj["@attributes"] = {};
            for (let j = 0; j < xml.attributes.length; j++) {
                const attribute = xml.attributes.item(j);
                obj["@attributes"][attribute.nodeName] = attribute.nodeValue;
            }
        }
    } else if (xml.nodeType === 3 || xml.nodeType === 4) {
        // 文本节点或CDATA节点
        obj = xml.nodeValue;
    }

    // 处理子节点
    if (xml.hasChildNodes()) {
        for (let i = 0; i < xml.childNodes.length; i++) {
            const item = xml.childNodes.item(i);
            const nodeName = item.nodeName;

            // 如果节点名称已经存在，转成数组
            if (typeof obj[nodeName] === "undefined") {
                obj[nodeName] = xmlToJson(item);
            } else {
                if (!Array.isArray(obj[nodeName])) {
                    const old = obj[nodeName];
                    obj[nodeName] = [];
                    obj[nodeName].push(old);
                }
                obj[nodeName].push(xmlToJson(item));
            }
        }
    }

    return obj;
};


export const fromXmlToJson = (strContent) => {
    let parser = new DOMParser();
    let xml = parser.parseFromString(strContent, "text/xml");
    // 创建一个对象来保存结果
    return xmlToJson(xml);
}

export const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

export const validateUsername = (username) => {
    const re = /^[a-zA-Z0-9_]+$/;
    return re.test(username);
}


export const validatePassword = (password) => {
    if (password.length < 6) {
        return false; // 密码长度不足
    }

    const hasNumber = /[0-9]/.test(password);
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    // 检查是否至少包含两种字符类型
    const typesCount = [hasNumber, hasLetter, hasSpecialChar].filter(Boolean).length;

    return typesCount >= 2;
}

export const parseImg = (data) => {
    for (let i of data) {
        // 图片信息处理
        if (i.Type === 3 && i.SubType === 0) {
            images.push({
                thumbnail: data.Thumb,
                source: data.Image
            })
            // data.StrContent
            if (i.StrContent) {
                const xmlDoc = parseXml(i.StrContent);
                const imgTag = xmlDoc.querySelector('img');
                if (imgTag) {
                    const cdnthumbheight = imgTag.getAttribute('cdnthumbheight');
                    i.cdnthumbheight = cdnthumbheight;

                    const cdnthumbwidth = imgTag.getAttribute('cdnthumbwidth');
                    i.cdnthumbwidth = cdnthumbwidth;

                    const md5 = imgTag.getAttribute('md5');
                    i.md5 = md5;
                }
            }
        }
    }
}

export const formatMsgDate = (timestamp) => {
    const date = new Date(timestamp * 1000);
    const now = new Date();

    // 获取今天的日期
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    // 获取昨天的日期
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    // 获取年、月、日、小时、分钟
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    // 根据日期判断输出格式
    if (date >= today) {
        return `${hours}:${minutes}`;
    } else if (date >= yesterday) {
        return `昨天 ${hours}:${minutes}`;
    } else {
        return `${year}年${month}月${day}日 ${hours}:${minutes}`;
    }
};

export const formatFilterMsgDate = (timestamp) => {
    const date = new Date(timestamp * 1000);
    const now = new Date();

    // 获取今天的日期
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    // 获取昨天的日期
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    // 获取年、月、日、小时、分钟
    const year = String(date.getFullYear()).slice(-2);
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    // 根据日期判断输出格式
    if (date >= today) {
        return `${hours}:${minutes}`;
    } else if (date >= yesterday) {
        return `昨天 ${hours}:${minutes}`;
    } else {
        return `${year}/${month}/${day} ${hours}:${minutes}`;
    }
};

export const filterDateFormatView = (date) => {
    const year = String(date.getFullYear());
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}/${month}/${day}`
}

export const filterDateFormatQuery = (date) => {
    const year = String(date.getFullYear());
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}${month}${day}`
}

export const fileSize = (bytes) => {
    if (bytes < 1024) {
        return bytes + ' B';
    } else if (bytes < 1024 * 1024) {
        return (bytes / 1024).toFixed(2) + ' KB';
    } else if (bytes < 1024 * 1024 * 1024) {
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    } else if (bytes < 1024 * 1024 * 1024 * 1024) {
        return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
    } else {
        return (bytes / (1024 * 1024 * 1024 * 1024)).toFixed(2) + ' TB';
    }
}

export const formatUserCreateTime = (timestamp) => {
    const date = new Date(timestamp * 1000);

    // 获取年、月、日、小时、分钟
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${year}/${month}/${day} ${hours}:${minutes}`;
};
