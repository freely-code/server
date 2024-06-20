import redis,time


r=redis.Redis()
while True:
    r.set('b', 'bar')
    print(r.get('b'))
    time.sleep(0.5)
# class Cache:
#     def __init__(self, host='localhost', port=6379, db=0, password=None,ssl=False):
#         # 初始化连接池时没有传递 ssl 参数
#         self.pool = redis.ConnectionPool(
#             host=host, port=port, db=db, password=password)
#         self.client = redis.Redis(connection_pool=self.pool)

#     def set(self, key, value):
#         return self.client.set(key, value)

#     def get(self, key):
#         return self.client.get(key)

#     def get_pool_status(self):
#         # 获取连接池状态信息
#         print("连接池大小: ", self.pool._created_connections)
#         print("连接池使用中的连接数: ", len(self.pool._available_connections))
#         print("连接池等待连接数: ", len(self.pool._in_use_connections))


# # 创建 Cache 实例
# cache = Cache()

# # 设置值
# cache.set("a", "1")

# # 获取值
# value = cache.get("a")
# print(value)

# # 打印连接池状态
# cache.get_pool_status()
