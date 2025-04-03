# CloudBak-云朵备份
云朵备份是一个微信云备份程序，使用云朵备份可以将微信数据备份到服务器，通过浏览器访问数据，你可以像正常使用微信一样浏览数据和搜索数据（参考微信网页版）。

## 为什么产生这个工具
微信占用空间数十G已是家常便饭，解决方法可以是清空聊天记录，也可以是部分聊天记录，也可以同步到PC端微信后删除手机上的聊天记录，也有一些云端备份手段，通常是直接将手机的微信的数据直接同步到云盘；还有一些个人制作的备份工具可以备份PC端的数据，将数据导出为CSV，HTML等等备份文件，八仙过海各显神通。

经过我调研后发现这样一种备份的可能，将手机上的数据备份到PC端微信后，用一个备份程序备份到服务器，通过WEB或APP方式访问备份的数据，访问数据还原微信界面和操作逻辑易于使用。所以我花了些时间（其实挺长的）写了这样一个程序，云朵备份。

## 有哪些优势
1. 无需微信登录：即便微信被封号也不影响历史消息查看；
2. 备份的数据访问更方便：如果备份的数据在手机上已经删除，就不能方便的远程访问PC上微信客户端的数据，有了云朵备份您可以随时随地访问您的备份数据；
3. 多微信查询：当需要切换微信查询备份消息时不方便，云朵备份可以简洁的在多个微信间切换；
4. 数据脱离设备，更安全：将数据备份到服务器或NAS有助于长久保存，若规划合理将有利于长久备份；
5. 定制功能

## 使用效果
[查看演示图](https://www.cloudbak.org/use-case.html)

## Docker 安装

执行以下命令安装
```shell
docker run --name=cloudbak --restart=always -d \
    -p 9527:9527 \
    -v /app/data:/app/data \
    likeflyme/cloudbak
```

## 源码安装

源码安装查看：[https://www.cloudbak.org/install/install-source.html](https://www.cloudbak.org/install/install-source.html)

## 开始使用

查看：[https://www.cloudbak.org/use/create-session.html](https://www.cloudbak.org/use/create-session.html)

## 免责声明

本项目仅供学习、研究使用，严禁商业使用，用于网络安全用途的，请确保在国家法律法规下使用，您使用本软件导致的后果，包含但不限于数据损坏，记录丢失等问题，作者不承担相关责任。因软件特殊性质，请在使用时获得微信账号所有人授权，你当确保不侵犯他人个人隐私权，后果自行承担。

## 隐私政策

客户端与服务端完全支持离线运行，不会上传任何数据到第三方系统。

## 交流与提问

精力有限，遇到问题需要优先自己处理，顺序：
1. 详细阅读文档
2. 搜索引擎/AI 搜索
3. 交流群寻求帮助（群主大部分时间不保证答复）
4. 提ISSUE

社区: [https://forum.cloudbak.org](http://forum.cloudbak.org.cn)

交流群：993046283

微信群：添加微信 `MMXC2024` 后邀请进群

## 参考

* https://github.com/xaoyaoo/PyWxDump
* https://github.com/SuxueCode/WechatBakTool
* https://github.com/AdminTest0/SharpWxDump
* [ffmpeg](https://www.ffmpeg.org/) : 语音转mp3
* DAT 转图片：记不得看的哪个了，网上挺多的
* 无源 protobuf 反序列化


