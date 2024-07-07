"""缓存类
参数标准为redis
"""
import redis
import aioredis
import asyncio
from typing import Optional,Callable,Any

class Redis:
    def __init__(self, **kwargs: dict) -> None:
        """初始化
        """
        self.pipe = None
        self.kwargs = kwargs
        #检查密码是否为整数
        password = self.kwargs.get("password", None)
        if isinstance(password, int):
            self.kwargs["password"] = str(password)

        del self.kwargs["single_connection_client"]
        if not self.kwargs.get("ssl", None):
            del self.kwargs["ssl"]
            del self.kwargs["ssl_keyfile"]
            del self.kwargs["ssl_certfile"]
            del self.kwargs["ssl_cert_reqs"]
            del self.kwargs["ssl_ca_certs"]

        # # 判断是否使用连接池
        # self.pool = self.kwargs.pop("pool", None)
        # if self.pool:
            # 创建连接池
        self.loop = self.kwargs.get("loop", asyncio.get_event_loop())
        self.connect()

        # if self.loop.is_running():
        #     self.connect()
        #         # self.connect_async()
        #     else:
        #         self.loop.run_until_complete(self.connect_async())
        # else:
        #     self.connect()

    # 同步

    def connect(self) -> None:
        """连接redis_同步"""
        if self.loop.is_running():
            url = f"redis://{self.kwargs.get('host')}:{self.kwargs.get('port')}/{self.kwargs.get('db')}"
            self.redis = aioredis.from_url(url=url, **self.kwargs)
        else:
            pool = redis.ConnectionPool(**self.kwargs)
            self.redis = redis.Redis(connection_pool=pool)

    def transaction_begin(self, watch_key: Optional[str| list] = None):
        """事务开始_同步
            watch_key: 监视的键，在事务执行期间如果监视的键被修改，事务会被打断并返回一个错误
        """
        self.transaction_end()
        self.pipe = self.redis.pipeline()
        if watch_key:
            self.pipe.watch(watch_key)
        return self.pipe.multi()

    def transaction_end(self, success: bool = False):
        """事务结束_同步"""
        if not self.pipe:
            return
        if success:
            self.pipe.execute()
        else:
            self.pipe.discard()

    def set(self, key: str, value: str = "", expire: int = -1) -> bool:
        """设置键值对_同步
            expire:过期时间(秒)
            返回是否成功
        """
        try:
            if self.pipe:
                self.pipe.set(key, value, ex=expire)
                return True
            return self.redis.set(key, value, ex=expire)  # ex秒 px毫秒
        except Exception as e:
            if self.pipe:
                self.transaction_end(success=False)
            return False

    def get(self, key:str| tuple) -> str:
        """获取键值对_同步
            返回值
        """
        if isinstance(key, tuple):
            return self.redis.mget(key)
        return self.redis.get(key)

    def delete(self, *key: str|list) -> int:
        """删除键值对_同步
            返回删除个数
        """
        return self.redis.delete(*key)

    def append(self, key: str, value: str = "") -> int:
        """追加值_同步
            返回追加后的长度
        """
        return self.redis.append(key, value)

    def add(self, key: str, value: int = 1) -> int:
        """累加_同步
            返回追加后的值
        """
        return self.redis.incrby(key, value)

    def sub(self, key: str, value: int = 1) -> int:
        """累减1_同步
            返回追加后的值
        """
        return self.redis.decrby(key, value)

    def list_push(self, key: str, value: str = "", expire: int = -1, end: bool = False) -> bool:
        """添加列表_同步
            expire:过期时间(秒)
            end:是否在列表尾部追加
            返回是否成功
        """
        try:
            if end:
                self.redis.rpush(key, value)
            else:
                self.redis.lpush(key, value)
            if expire:
                self.redis.expire(key, expire)
            return True
        except Exception as e:
            return False

    def list_pop(self, key: str|list,  end: bool = False, timeout: int = 0) -> str:
        """弹出列表_同步
            key:如果为字符串,则立即弹出 如果为列表,则循环这个列表进行弹出,直到某个列表有值能弹出了,就返回,否则一直循环等待,如果等待的时间超过了超时时间则返回None
                例如:key为['a','b','c'] 先查看a是否能弹出值,能就返回,不能就看b,一直看到最后一个,又返回到a看是否能弹出
            end:是否从尾部弹出
            timeout:超时时间,当key为列表时可用
            返回值
        """
        try:
            if isinstance(key, list):
                if end:
                    return self.redis.brpop(key, timeout)
                else:
                    return self.redis.blpop(key, timeout)
                    self.redis.move(key, 0, 1)

            if end:
                return self.redis.rpop(key)
            else:
                return self.redis.lpop(key)
        except Exception as e:
            return ""

    def list_range(self, key: str, start: int = 0,  end: int = -1) -> list:
        """获取列表_同步
            正数是从前往后数0表示第一个值 负数是从后往前数-1表示最后一个值
            start:开始索引
            end:结束索引(包含自身)
            返回列表
        """
        return self.redis.lrange(key, start, end)

    def list_len(self, key: str) -> int:
        """获取列表长度_同步
            返回长度
        """
        return self.redis.llen(key)

    def list_delete(self, key: str, value: str = "", count: int = 0) -> int:
        """删除列表_同步
            key:列表的键
            value:要删除的值
            count:删除的个数
            返回长度
        """
        return self.redis.lrem(key, count, value)

    def key_move(self, key: str,  db: int = 0) -> bool:
        """移动键_同步
            将当前库的key移动到指定的库
            db:库索引
            返回是否成功
        """
        try:
            return self.redis.move(key, db) > 0
        except Exception as e:
            return False

    def set_add(self, key: str, value: Optional[str| list] = None, expire: int = -1) -> bool:
        """添加集合_同步
            expire:过期时间(秒)
            返回是否成功
        """
        try:
            self.redis.sadd(key, *value)
            if expire:
                self.redis.expire(key, expire)
            return True
        except Exception as e:
            return False

    def set_delete(self, key: str, value: str = "") -> bool:
        """删除集合_同步
            返回是否成功
        """
        try:
            return self.redis.srem(key, value) > 0
        except Exception as e:
            return False

    def set_len(self, key: str) -> int:
        """获取集合长度_同步
            返回长度
        """
        try:
            return self.redis.scard(key)
        except Exception as e:
            return 0

    def set_in(self, key: str, value: str) -> bool:
        """集合是否包含某值_同步
            返回是否包含
        """
        try:
            return self.redis.sismember(key, value) > 0
        except Exception as e:
            return False

    def set_all(self, key: str) -> dict:
        """集合取所有_同步
            返回是否包含
        """
        try:
            return self.redis.smembers(key)
            self.pipe = self.redis.pipeline(transaction=False)
            self.pipe.watch(key)
        except Exception as e:
            return {}

    def subscriber(self, channel: str|list, callback: Callable[[Any], None] = None) -> None:
        """订阅者_同步
            返回是否包含
        """
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        if callback:
            callback(pubsub)
        else:
            for message in pubsub.listen():
                if message['type'] == 'message':
                    print(f'Received message: {message["data"]}')

    def publisher(self, channel: str|list, message: str = "") -> int:
        """发布者_同步
            返回订阅数
        """
        if isinstance(channel, list):
            count = 0
            for i in channel:
                count += self.redis.publish(i, message)
        else:
            count = self.redis.publish(channel, message)
        return count

    # 异步

    async def connect_async(self):
        """连接redis_异步"""
        url = f"redis://{self.kwargs.get('host')}:{self.kwargs.get('port')}/{self.kwargs.get('db')}"
        self.redis = aioredis.from_url(url=url, **self.kwargs)

    async def set_async(self, key: str, value: str = "", expire: int = -1) -> bool:
        """设置键值对_同步
            expire:过期时间(秒)
            返回是否成功
        """
        return await self.redis.set(key, value, ex=expire)  # ex秒 px毫秒

    async def get_async(self, key: str|tuple) -> str:
        """获取键值对_同步
            返回值
        """
        if isinstance(key, tuple):
            return await self.redis.mget(key)
        return await self.redis.get(key)

    async def delete_async(self, *key: str|list) -> int:
        """删除键值对_同步
            返回删除个数
        """
        return await self.redis.delete(*key)

    async def append_async(self, key: str, value: str = "") -> int:
        """追加值_同步
            返回追加后的长度
        """
        return await self.redis.append(key, value)

    async def add_async(self, key: str, value: int = 1) -> int:
        """累加_同步
            返回追加后的值
        """
        return await self.redis.incrby(key, value)

    async def sub_async(self, key: str, value: int = 1) -> int:
        """累减1_同步
            返回追加后的值
        """
        return await self.redis.decrby(key, value)

    async def list_push_async(self, key: str, value: str = "", expire: int = -1, end: bool = False) -> bool:
        """添加列表_同步
            expire:过期时间(秒)
            end:是否在列表尾部追加
            返回是否成功
        """
        try:
            if end:
                self.redis.rpush(key, value)
            else:
                self.redis.lpush(key, value)
            if expire:
                self.redis.expire(key, expire)
            return True
        except Exception as e:
            return False

    async def list_pop_async(self, key: str| list,  end: bool = False, timeout: int = 0) -> str:
        """弹出列表_同步
            key:如果为字符串,则立即弹出 如果为列表,则循环这个列表进行弹出,直到某个列表有值能弹出了,就返回,否则一直循环等待,如果等待的时间超过了超时时间则返回None
                例如:key为['a','b','c'] 先查看a是否能弹出值,能就返回,不能就看b,一直看到最后一个,又返回到a看是否能弹出
            end:是否从尾部弹出
            timeout:超时时间,当key为列表时可用
            返回值
        """
        try:
            if isinstance(key, list):
                if end:
                    return await self.redis.brpop(key, timeout)
                else:
                    return await self.redis.blpop(key, timeout)
                    self.redis.move(key, 0, 1)

            if end:
                return await self.redis.rpop(key)
            else:
                return await self.redis.lpop(key)
        except Exception as e:
            return None

    async def list_range_async(self, key: str, start: int = 0,  end: int = -1) -> list:
        """获取列表_同步
            正数是从前往后数0表示第一个值 负数是从后往前数-1表示最后一个值
            start:开始索引
            end:结束索引(包含自身)
            返回列表
        """
        return await self.redis.lrange(key, start, end)

    async def list_len_async(self, key: str) -> int:
        """获取列表长度_同步
            返回长度
        """
        return await self.redis.llen(key)

    async def list_delete_async(self, key: str, value: str = "", count: int = 0) -> int:
        """删除列表_同步
            key:列表的键
            value:要删除的值
            count:删除的个数
            返回长度
        """
        return await self.redis.lrem(key, count, value)

    async def key_move_async(self, key: str,  db: int = 0) -> bool:
        """移动键_同步
            将当前库的key移动到指定的库
            db:库索引
            返回是否成功
        """
        try:
            return await self.redis.move(key, db) > 0
        except Exception as e:
            return False

    async def set_add_async(self, key: str, value: str| list = "", expire: int = -1) -> bool:
        """添加集合_同步
            expire:过期时间(秒)
            返回是否成功
        """
        try:
            self.redis.sadd(key, *value)
            if expire:
                self.redis.expire(key, expire)
            return True
        except Exception as e:
            return False

    async def set_delete_async(self, key: str, value: str = "") -> bool:
        """删除集合_同步
            返回是否成功
        """
        try:
            return await self.redis.srem(key, value) > 0
        except Exception as e:
            return False

    async def set_len_async(self, key: str) -> int:
        """获取集合长度_同步
            返回长度
        """
        try:
            return await self.redis.scard(key)
        except Exception as e:
            return 0

    async def set_in_async(self, key: str, value: str) -> bool:
        """集合是否包含某值_同步
            返回是否包含
        """
        try:
            return await self.redis.sismember(key, value) > 0
        except Exception as e:
            return False

    async def set_all_async(self, key: str) -> dict:
        """集合取所有_同步
            返回是否包含
        """
        try:
            return self.redis.smembers(key)
        except Exception as e:
            return {}

    async def subscriber_async(self, channel: str|list, callback: Callable[[Any], None] = None) -> None:
        """订阅者_同步
            返回是否包含
        # """
        # self.redis.pubsub
        pubsub =  self.redis.pubsub()
        await pubsub.subscribe("nihao")
        if callback:
            await callback(pubsub)
        else:
            async for  message in pubsub.listen():
                if message['type'] == 'message':
                    print(f'Received message: {message["data"]}')

    async def publisher_async(self, channel: str|list, message: str = "") -> int:
        """发布者_同步
            返回订阅数
        """
        if isinstance(channel, list):
            count = 0
            for i in channel:
                count += await self.redis.publish(i, message)
        else:
            count = await self.redis.publish(channel, message)
        return count

async def aaa(**k):
    # pass

    a = Cache(**k)
    # print(await a.publisher_async(["nihao", "wohao"], "我来了"))
    print(await a.subscriber_async(["nihao", "wohao"],test))

    # await a.transaction_begin_async()
    # print(await a.set_async("b","90"))
    # await a.transaction_end_async(False)
    # print(await a.get_async("a"))


async def test(a)->None:
    async for message in a.listen():
        if message['type'] == 'message':
            print(f'收到: {message["data"]}')
    print(a)


if __name__ == '__main__':
    # a = {"host": 'localhost', "port": 6379, "db": 0, "ssl": False, }
    a = {
        "host": "localhost",
        "port": 6379,
        "password": None,
        "db": 0,
        "max_connections": 10,
        "socket_timeout": None,
        "socket_connect_timeout": None,
        "retry_on_timeout": False,
        "encoding": "utf-8",
        "encoding_errors": "strict",
        "decode_responses": True,
        "ssl": None,
        "ssl_keyfile": None,
        "ssl_certfile": None,
        "ssl_cert_reqs": None,
        "ssl_ca_certs": None,
        "single_connection_client": False
    }

    asyncio.run(aaa(**a))
    # a = Cache(**a)
    # print(a.publisher(["nihao","wohao"], "adsadasdas"))
    # a.subscriber(["nihao.*", "wohao"], test)
    # a.transaction_begin()
    # print(a.set("b", "901"))
    # print(a.get("b"))
    # print(a.set("e", "64"))
    # a.transaction_end(False)
    # print(await a.get_async("b"))

    # print(a.push("d","dsa"))
    # print(a.push("d","d"))
    # print(a.push("d","sa"))
    # print(a.push("d","a"))
    # print(a.set("b"))
    # print(a.set("c"))
    # print(a.set_all("sett"))
