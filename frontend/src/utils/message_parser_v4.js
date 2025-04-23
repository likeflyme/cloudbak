import {fromXmlToJson} from "@/utils/common.js";

const parseText = (msg, wx_id) => {
    let data = msg.message_content_data;
    if (data.indexOf(":\n") !== -1) {
        let array = data.split(":\n");
        return {
            sender: array[0],
            content: array[1]
        }
    } else {
        return {
            sender: wx_id,
            content: data
        }
    }
}

export const parseMsg = (msg, wx_id) => {
    msg['data'] = parseText(msg, wx_id)
    if (msg.local_type === 43) {
        if (msg.data.content) {
            msg['_video'] = fromXmlToJson(msg.data.content)
        }
    }

}

