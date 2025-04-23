# 前端代码构建环境
FROM node:20-alpine as frontend

WORKDIR /app

# 先复制 package.json 并执行安装，利用 Docker 缓存
COPY ./frontend/package.json ./frontend/package-lock.json /app/

RUN npm install -g cnpm --registry=https://registry.npmmirror.com \
    && cnpm install \
    && npm cache clean --force

COPY ./frontend/ /app

RUN npm run build

# Python 代码编译环境
FROM python:3.11-slim-bullseye as builder

WORKDIR /app/backend

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先复制 requirements.txt 并执行安装，利用 Docker 缓存
COPY ./backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制剩余代码
COPY ./backend/ /app/backend

# 编译 Python 可执行文件
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
RUN pyinstaller --onefile main.py
RUN pyinstaller --onefile user_password_reset.py
RUN pyinstaller --onefile decrypt_db.py

FROM python:3.11-slim-bullseye as backend

COPY --from=frontend /app/dist /app/frontend

RUN apt-get update \
    && apt-get install -y nginx gcc build-essential ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 将编译环境的可执行文件放到工作目录
COPY --from=builder /app/backend/dist/main /app/backend/main
COPY --from=builder /app/backend/dist/user_password_reset /app/backend/user_password_reset
COPY --from=builder /app/backend/dist/decrypt_db /app/backend/decrypt_db

COPY ./.env /app/backend

# 注入版本号
ARG SYSTEM_VERSION
ENV SYSTEM_VERSION=${SYSTEM_VERSION}
RUN echo "SYSTEM_VERSION=${SYSTEM_VERSION}" >> /app/backend/.env

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 9527

WORKDIR /app/backend

CMD service nginx start ;  ./main