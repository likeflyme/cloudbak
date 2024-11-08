# 前端代码构建环境
FROM node:20-alpine as frontend

COPY ./frontend/ /app

WORKDIR /app

RUN npm install -g cnpm --registry=https://registry.npmmirror.com \
    && cnpm install \
    && npm run build \
    && npm cache clean --force

# python 代码编译环境
FROM python:3.11-slim-bullseye as builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./backend/ /app/backend

WORKDIR /app/backend

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
RUN pyinstaller --onefile main.py
RUN pyinstaller --onefile user_create.py
RUN pyinstaller --onefile user_password_reset.py
RUN pyinstaller --onefile decrypt_db.py

FROM python:3.11-slim-bullseye as backend

COPY --from=frontend /app/dist /app/frontend

RUN apt-get update \
    && apt-get install -y nginx gcc build-essential ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 将编译环境的可执行文件放到工作目录
COPY --from=builder /app/backend/dist/main /app/backend/main
COPY --from=builder /app/backend/dist/user_create /app/backend/user_create
COPY --from=builder /app/backend/dist/user_password_reset /app/backend/user_password_reset
COPY --from=builder /app/backend/dist/decrypt_db /app/backend/decrypt_db

# 查看启动命令是否存在
RUN ls /app/backend/main

COPY ./.env /app/backend

COPY nginx.conf /etc/nginx/nginx.conf

COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 80

WORKDIR /app/backend

CMD service nginx start ;  ./main


