import os

if __name__ == '__main__':
    path = 'E:\\projects\\wechat-emoji\\web.wechat.com\\compressed-cwebp\\lossy-q50'
    for file in os.listdir(path):
        file_name = file.split('.')[0]
        title = file_name.split('_')[1]

        print(f"loadEmoji('{title}', '{file_name}');")
