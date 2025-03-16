import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

try:
    redis_client.ping()
    print("Подключение к Redis успешно")
except redis.ConnectionError as e:
    print(f"Ошибка подключения к Redis: {e}")
