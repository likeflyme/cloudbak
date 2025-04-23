import os
import pilk
from config.log_config import logger


class MediaUtils:
    @staticmethod
    def decode_media(media_folder: str, filename: str, data):
        logger.info(f"media_folder: {media_folder}")
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)
        silk_mame = f"{media_folder}/{filename}.silk"
        pcm_name = f"{media_folder}/{filename}.pcm"
        mp3_name = f"{media_folder}/{filename}.mp3"
        with open(silk_mame, 'wb') as file:
            # 将字节数组写入文件
            file.write(data)
        # silk 转 pcm
        pilk.decode(silk_mame, pcm_name, 44100)
        # pcm 转 mp3
        os.system(f"ffmpeg -y -f s16le -i {pcm_name} -ar 44100 -ac 1 {mp3_name}")
        os.remove(silk_mame)
        os.remove(pcm_name)
        return mp3_name
