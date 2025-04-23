from cachetools import TTLCache

# 三十分钟缓存
cache_half_hour = TTLCache(maxsize=100, ttl=30*60)
