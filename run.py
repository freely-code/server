# 启动文件
import os  # 文件操作
import sys  # 系统操作
import yaml  # 配置文件
import json  # 数据处理
import signal  # 信号处理
import logging  # 日志
from init import init  # 初始化
from routes import *  # 路由  # noqa: F403
from tornado import web, ioloop, routing
from tools.str import arguments_format
from tools.database import Database
from tools.system import log, port_check
from tools.ende import token_handle, guid
from tools.redis import Redis
from tools.apifox import Apifox
from typing import Optional

logging.getLogger("tornado.access").disabled = True
db = None
redis = None
# 配置模板
config_model = {
    "debug": False,
    "server": {
        "port": 80,
    },
    "redis": {
        "host": "localhost",
        "port": 6379,
        "password": None,
        "db": 0,
        "max_connections": 0,
        "socket_timeout": None,
        "socket_connect_timeout": None,
        "retry_on_timeout": False,
        "encoding": "utf-8",
        "encoding_errors": "strict",
        "decode_responses": True,
        "ssl": False,
        "ssl_keyfile": None,
        "ssl_certfile": None,
        "ssl_cert_reqs": None,
        "ssl_ca_certs": None,
        "single_connection_client": False,
    },
    "database": {
        "type": "pgsql",
        "pool": True,
        "pgsql": {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "password": "123456",
            "database": "postgres",
        },
        "mysql": {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "db": "mysql",
            "password": "root",
        },
    },
    "routes": [{"url": "/.*", "name": "MainHandler", "class": "MainHandler"}],
}
# web.URLSpec(r'/api/member/([^/]*)', MemberRoute, name='member'),
# (r'/static/(.*)', web.StaticFileHandler, {'path': static_path} )


def config(path: str = "") -> dict:
    # 初始化配置文件
    # path默认为当前目录下的config.yaml
    if not path:
        # 如果不存在path，则获取当前目录下的config.yaml
        path = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])), "config.yml"
        )

    if not os.path.exists(path):
        # 如果不存在配置文件，则创建配置文件
        yaml_data = yaml.dump(config_model, default_flow_style=False)
        with open(path, "w") as f:
            f.write(yaml_data)
            log("config.yml文件不存在,创建并使用默认文件", "警告")
    else:
        modify = False
        # 如果存在配置文件，则读取配置文件
        with open(path, "r", encoding="utf-8") as f:
            # config_dict = yaml.load(f, Loader=yaml.FullLoader)
            config_dict = yaml.safe_load(f)
            try:
                if config_dict["debug"]:
                    config_model["debug"] = config_dict["debug"]
            except Exception:
                modify = True
                log("debug未设置,使用默认值False", "警告")

            try:
                if config_dict["server"]["port"]:
                    config_model["server"]["port"] = config_dict["server"]["port"]
            except Exception:
                modify = True
                log("server>port未设置,使用默认值80", "警告")
            try:
                if config_dict["database"]["type"]:
                    config_model["database"]["type"] = config_dict["database"]["type"]
            except Exception:
                modify = True
                log("database>type,使用默认值pgsql", "警告")
            try:
                if config_dict["database"]["pool"]:
                    config_model["database"]["pool"] = config_dict["database"]["pool"]
            except Exception:
                modify = True
                log("database>pool,使用默认值True", "警告")
            try:
                if config_dict["database"]["pgsql"]["host"]:
                    config_model["database"]["pgsql"]["host"] = config_dict["database"][
                        "pgsql"
                    ]["host"]
            except Exception:
                modify = True
                log("database>pgsql>host,使用默认值localhost", "警告")
            try:
                if config_dict["database"]["pgsql"]["port"]:
                    config_model["database"]["pgsql"]["port"] = config_dict["database"][
                        "pgsql"
                    ]["port"]
            except Exception:
                modify = True
                log("database>pgsql>port,使用默认值5432", "警告")
            try:
                if config_dict["database"]["pgsql"]["user"]:
                    config_model["database"]["pgsql"]["user"] = config_dict["database"][
                        "pgsql"
                    ]["user"]
            except Exception:
                modify = True
                log("database>pgsql>user,使用默认值postgres", "警告")
            try:
                if config_dict["database"]["pgsql"]["password"]:
                    config_model["database"]["pgsql"]["password"] = config_dict[
                        "database"
                    ]["pgsql"]["password"]
            except Exception:
                modify = True
                log("database>pgsql>password,使用默认值postgres", "警告")
            try:
                if config_dict["database"]["pgsql"]["database"]:
                    config_model["database"]["pgsql"]["database"] = config_dict[
                        "database"
                    ]["pgsql"]["database"]
            except Exception:
                modify = True
                log("database>pgsql>database,使用默认值postgres", "警告")
            try:
                if config_dict["database"]["mysql"]["host"]:
                    config_model["database"]["mysql"]["host"] = config_dict["database"][
                        "mysql"
                    ]["host"]
            except Exception:
                modify = True
                log("database>mysql>host,使用默认值localhost", "警告")
            try:
                if config_dict["database"]["mysql"]["port"]:
                    config_model["database"]["mysql"]["port"] = config_dict["database"][
                        "mysql"
                    ]["port"]
            except Exception:
                modify = True
                log("database>mysql>port,使用默认值3306", "警告")
            try:
                if config_dict["database"]["mysql"]["user"]:
                    config_model["database"]["mysql"]["user"] = config_dict["database"][
                        "mysql"
                    ]["user"]
            except Exception:
                modify = True
                log("database>mysql>user,使用默认值root", "警告")
            try:
                if config_dict["database"]["mysql"]["password"]:
                    config_model["database"]["mysql"]["password"] = config_dict[
                        "database"
                    ]["mysql"]["password"]
            except Exception:
                modify = True
                log("database>mysql>password,使用默认值root", "警告")
            try:
                if config_dict["routes"]:
                    config_model["routes"] = config_dict["routes"]
            except Exception:
                modify = True
                log("routes,使用默认值/", "警告")
            try:
                if config_dict["database"]["mysql"]["db"]:
                    config_model["database"]["mysql"]["db"] = config_dict["database"][
                        "mysql"
                    ]["db"]
            except Exception:
                modify = True
                log("database>mysql>db,使用默认值mysql", "警告")
            try:
                if config_dict["redis"]["host"]:
                    config_model["redis"]["host"] = config_dict["redis"]["host"]
            except Exception:
                modify = True
                log("redis>host,服务器的主机名或 IP 地址,使用默认值localhost", "警告")
            try:
                if config_dict["redis"]["port"]:
                    config_model["redis"]["port"] = config_dict["redis"]["port"]
            except Exception:
                modify = True
                log("redis>port,服务器的端口号,使用默认值6379", "警告")
            try:
                if config_dict["redis"]["password"]:
                    config_model["redis"]["password"] = config_dict["redis"]["password"]
            except Exception:
                modify = True
                log("redis>password,服务器的密码,默认无密码,使用默认值None", "警告")
            try:
                if config_dict["redis"]["db"]:
                    config_model["redis"]["db"] = config_dict["redis"]["db"]
            except Exception:
                modify = True
                log("redis>db,数据库索引,使用默认值0", "警告")
            try:
                if config_dict["redis"]["max_connections"]:
                    config_model["redis"]["max_connections"] = config_dict["redis"][
                        "max_connections"
                    ]
            except Exception:
                modify = True
                log("redis>max_connections,最大连接数,默认无限制,使用默认值0", "警告")
            try:
                if config_dict["redis"]["socket_timeout"]:
                    config_model["redis"]["socket_timeout"] = config_dict["redis"][
                        "socket_timeout"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>socket_timeout,连接超时时间（以秒为单位）,使用默认值None",
                    "警告",
                )
            try:
                if config_dict["redis"]["socket_connect_timeout"]:
                    config_model["redis"]["socket_connect_timeout"] = config_dict[
                        "redis"
                    ]["socket_connect_timeout"]
            except Exception:
                modify = True
                log(
                    "redis>socket_connect_timeout,连接建立超时时间（以秒为单位）,使用默认值None",
                    "警告",
                )
            try:
                if config_dict["redis"]["retry_on_timeout"]:
                    config_model["redis"]["retry_on_timeout"] = config_dict["redis"][
                        "retry_on_timeout"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>retry_on_timeout,是否在超时后重试连接,使用默认值False",
                    "警告",
                )
            try:
                if config_dict["redis"]["encoding"]:
                    config_model["redis"]["encoding"] = config_dict["redis"]["encoding"]
            except Exception:
                modify = True
                log("redis>encoding,数据的编码方式,使用默认值utf-8", "警告")
            try:
                if config_dict["redis"]["encoding_errors"]:
                    config_model["redis"]["encoding_errors"] = config_dict["redis"][
                        "encoding_errors"
                    ]
            except Exception:
                modify = True
                log("redis>encoding_errors,编码错误处理方式,使用默认值strict", "警告")
            try:
                if config_dict["redis"]["decode_responses"]:
                    config_model["redis"]["decode_responses"] = config_dict["redis"][
                        "decode_responses"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>decode_responses,是否自动解码 Redis 返回的数据,使用默认值True",
                    "警告",
                )
            try:
                if config_dict["redis"]["ssl"]:
                    config_model["redis"]["ssl"] = config_dict["redis"]["ssl"]
            except Exception:
                modify = True
                log("redis>ssl,是否使用 SSL 加密连接,使用默认值False", "警告")
            try:
                if config_dict["redis"]["ssl_keyfile"]:
                    config_model["redis"]["ssl_keyfile"] = config_dict["redis"][
                        "ssl_keyfile"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>ssl_keyfile,SSL 密钥文件的路径,如果使用 SSL 加密则需要提供,使用默认值None",
                    "警告",
                )
            try:
                if config_dict["redis"]["ssl_certfile"]:
                    config_model["redis"]["ssl_certfile"] = config_dict["redis"][
                        "ssl_certfile"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>ssl_certfile,SSL 证书文件的路径,如果使用 SSL 加密则需要提供,使用默认值None",
                    "警告",
                )
            try:
                if config_dict["redis"]["ssl_cert_reqs"]:
                    config_model["redis"]["ssl_cert_reqs"] = config_dict["redis"][
                        "ssl_cert_reqs"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>ssl_cert_reqs,SSL 证书验证要求,默认为 None,表示不进行验证,使用默认值None",
                    "警告",
                )
            try:
                if config_dict["redis"]["ssl_ca_certs"]:
                    config_model["redis"]["ssl_ca_certs"] = config_dict["redis"][
                        "ssl_ca_certs"
                    ]
            except Exception:
                modify = True
                log(
                    "redis>ssl_ca_certs,SSL 根证书文件的路径,如果使用 SSL 加密则需要提供,使用默认值None",
                    "警告",
                )
            try:
                if config_dict["redis"]["single_connection_client"]:
                    config_model["redis"]["single_connection_client"] = config_dict[
                        "redis"
                    ]["single_connection_client"]
            except Exception:
                modify = True
                log(
                    "redis>single_connection_client,是否使用单个连接,使用默认值False",
                    "警告",
                )

            if modify:
                yaml_data = yaml.dump(config_model, default_flow_style=False)
                with open(path, "w") as f:
                    f.write(yaml_data)
                    log("更新配置文件", "警告")
    return config_model


def signal_handler(signum, frame):
    # 处理信号,当按下Ctrl+C时,停止事件循环
    io_loop = ioloop.IOLoop.current()
    io_loop.add_callback(io_loop.stop)


# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)


class MainHandler(web.RequestHandler):
    def set_default_headers(self) -> None:
        # 设置跨域
        # self.set_header("Access-Control-Allow-Method","POST, DELETE, PUT, GET, OPTIONS")
        # self.set_header("Access-Control-Allow-Headers", "DNT,web-token,app-token,Authorization,Accept,Origin,Keep-Alive,User-Agent,X-Mx-ReqToken,X-Data-Type,X-Auth-Token,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range")
        self.set_header("Access-Control-Allow-Method", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Expose-Headers", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Max-Age", "3600")

    # 初始化
    def initialize(self, **kwargs) -> None:
        # 用户进入
        self.db = kwargs.get("db", None)
        self.redis = kwargs.get("redis", None)
        self.apifox = kwargs.get("apifox", None)
        self.debug = config_model["debug"]
        self.token_handle = token_handle
        self.guid = guid
        # 取ip
        self.ip = self.request.remote_ip
        # 取地址加参数
        self.uri = self.request.uri
        # 取请求路径
        self.path = self.request.path
        # 取用户代理
        self.ua = self.request.headers.get("user-agent")
        # 取主机
        self.host = self.request.headers.get("host")
        # 取身份验证
        self.token = self.request.headers.get("authorization", "")
        self.token = "" if self.token == "undefined" else self.token
        # 校验身份
        self.user_id = ""
        self.user_info = {}
        if self.token:
            # 去除杂质
            temp = self.token.split()
            if temp:
                self.token = temp[-1]

            self.user_info = token_handle(token=self.token)
            if self.user_info and isinstance(self.user_info, dict):
                self.user_id = self.user_info["user_id"]
            else:
                self.token = self.user_id = ""

        # 如果是GET方法,转换参数
        if self.request.method == "GET" or self.request.method == "DELETE":
            self.params = arguments_format(self.request.query)

        # POST方法
        elif self.request.method == "POST" or self.request.method == "PUT":
            # 取数据类型
            content_type = self.request.headers.get("Content-Type")
            if not content_type:
                self.params = {}

            elif content_type.startswith("application/json"):
                self.params = self.request.body.decode("utf-8")
                # 处理 JSON 格式的请求数据

            elif content_type.startswith("application/x-www-form-urlencoded"):
                self.params = arguments_format(self.request.body.decode("utf-8"))
                # 处理 Form 表单数据

            elif content_type.startswith("multipart/form-data"):
                self.params = arguments_format(
                    self.request.body_arguments, self.request.files
                )
                # 处理文件上传数据

            elif content_type.startswith("text/plain"):
                self.params = self.request.body.decode("utf-8")
                # 处理纯文本数据

            elif content_type.startswith("application/xml"):
                self.params = self.request.body.decode("utf-8")
                # 处理 XML 数据

            elif content_type.startswith("application/x-msgpack"):
                pass
                # self.params = self.request.body.decode('gbk')
                # 处理 msgpack 数据

            else:
                # 其他未知数据格式
                self.params = self.request.body
                print("未知")

            # 将参数转换成JSON
            if isinstance(self.params, str):
                try:
                    self.params = json.loads(self.params)
                except Exception:
                    self.params = {}

        # elif self.request.method == "OPTIONS":
        #     pass
        #     # self.set_status(200)
        #     # self.finish()
        super().on_finish()

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def response(self, msg: str = "", success: bool = False, result: dict = {}) -> dict:
        """返回对象

        Args:
            msg (str, optional): _description_. Defaults to None.
            code (int, optional): _description_. Defaults to None.
            result (dict, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """

        # 初始化data
        data = {"data": {}, "success": success, "msg": msg}
        # 如果有返回对象
        if result:
            # 判断返回对象是否为字符串
            if isinstance(result, str):
                result = json.loads(result)

            # 如果为调试模式
            if self.debug:
                # 赋值错误信息和语句
                data["error"] = result.get("error", "")
                data["sql"] = result.get("sql", "")

            # 拿到返回对象中的data
            res = result.get("data", result)
            # 赋值给data
            if isinstance(res, list):
                data["data"]["list"] = res
            else:
                data["data"] = res
        return data

    async def get(self, *args, **kwargs):
        await self.post(*args, **kwargs)

    async def put(self, *args, **kwargs):
        await self.post(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        await self.post(*args, **kwargs)

    async def post(self, *args, **kwargs):
        # result={}
        # # data = await self.db.execute_async("select * from interfaces", result)
        # # f=self.db.fields_default
        # l=[]
        # f={}
        # f["名称"]="id"
        # f["主键"]=True
        # f["类型"]="SERIAL"
        # f["备注"]="索引"
        # l.append(f)
        # f = {}
        # f["名称"]="user_name"
        # f["类型"]="VARCHAR"
        # f["备注"]="名称"
        # f["长度"]="20"
        # l.append(f)

        # await self.db.table_create_async(table_name="test",fields=l,table_remark="测试",result=result)
        await self.complete(data="Welcome")

    async def complete(self, handler=None, data=None) -> None:
        """完成请求"""
        if handler:
            # 判断是否有处理函数
            data = await handler.handler(self)

        if not isinstance(data, str):
            data = json.dumps(data)
        self.write(data)
        # 有处理函数走处理函数,没有处理函数走data返回
        # self.write(await handler.handler(self) if handler else data)
        # 判断是否有token
        if self.token:
            # 存在token就设置协议头
            self.set_header("Authorization", self.token)
        # 完成请求
        self.finish()


def make_app(routes: list[dict] = config_model["routes"], db: Optional[Database] = None, redis: Optional[Redis] = None,apifox: Optional[Apifox] = None):
    # 初始化应用
    url_specs = []
    # 遍历路由列表
    for route in routes:
        # 获取路由字符串
        class_str = route.get("class", None)
        if not class_str:
            continue

        # 获取路由信息
        handler_url = route.get("url", None)
        if not handler_url:
            if "Handler" not in class_str:
                continue
            handler_url = "/" + \
                class_str.replace("Handler", "").lower()+"/([^/]*)"
        try:
            # 将路由字符串转换为类
            handler_class = globals()[class_str]
        except KeyError:
            continue
        # 获取路由名称,不存在时使用类名
        handler_name = route.get("name", class_str)
        # 添加路由到列表
        url_specs.append(routing.URLSpec(
            handler_url, handler_class, {"name": handler_name, "db": db, "redis": redis,"apifox":apifox}))
    if not url_specs:
        # 如果路由列表为空，则使用默认路由
        return make_app(db=db, redis=redis,apifox=apifox)
        # 添加路由
    return web.Application(url_specs)


if __name__ == "__main__":
    # global db
    # 初始化配置
    config()
    port = config_model["server"]["port"]
    if not port_check(port):
        log(f"{port}端口被占用，启动失败", "错误")
        exit()
    routes = config_model["routes"]

    # 获取io循环
    loop = ioloop.IOLoop.current()
    # 连接redis
    redis = Redis(**config_model["redis"])
    # 获取数据库类型
    database_type = config_model["database"]["type"]
    # 数据库类型是否存在
    if database_type:
        # 使用使用连接池
        if config_model["database"]["pool"]:
            # 将外部连接池开关赋值给内部
            config_model["database"][database_type]["pool"] = config_model["database"][
                "pool"
            ]
            # #将当前IO循环赋值给数据库配置
            # config_model["database"][database_type]["loop"] = loop
        # 将外部debug开关赋值给数据库debug
        config_model["database"][database_type]["debug"] = config_model["debug"]
        # 连接数据库
        db = Database(**config_model["database"][database_type])

        # 异步初始化数据库
        loop.run_sync(lambda: init(db))

        # 初始化应用
        apifox= Apifox( project="服务器",team="天纳", token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjAxMTU2LCJ0cyI6IjhiYjUxNDUzNGE3MDEwODEiLCJpYXQiOjE3MjI0MDg4NDI2MzB9.xY0pj4fcJNegFmjzS9erhqWq40It2cV6eBUQIDSW-NI",)
        app = make_app(routes=routes, db=db, redis=redis,apifox=apifox)

        # 监听服务端口
        app.listen(port)
        log(f"http://localhost:{port}")
    loop.start()
