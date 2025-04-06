import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://:Test123@localhost:6379/0")
REDIS_CACHE_EXPIRE = 3600  # 1 hour

try:
    r = redis.Redis.from_url(REDIS_URL)
    
    response = r.ping()
    print("Redis connection successful! Response:", response)
    
    test_key = "test_key"
    test_value = "test_value"
    
    r.set(test_key, test_value, ex=REDIS_CACHE_EXPIRE)
    retrieved_value = r.get(test_key)
    
    print(f"Set key '{test_key}' with value '{test_value}' (expires in {REDIS_CACHE_EXPIRE} seconds)")
    print(f"Retrieved value for '{test_key}':", retrieved_value.decode())
    
except Exception as e:
    print("Redis connection failed! Error:", e)