from config.log_config import logger
import zstandard as zstd


class ZstandardUtils(object):
    @staticmethod
    def convert_zstandard(data):
        if data is None:
            return None
        if isinstance(data, str):
            return data
        elif isinstance(data, bytes):
            dctx = zstd.ZstdDecompressor()
            b_data = dctx.decompress(data)
            return b_data.decode('utf-8')
        else:
            logger.warn(f"zstandard data no support: {data}")
            return data
