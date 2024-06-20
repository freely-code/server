#加解密文件

def token_handle(user_info={}, token="", expire=604800):
    """
    生成token
    :param user_info: 用户id 该参数不为空则为生成
    :param token: 该参数不为空 则校验
    :param expire: 过期时间 单位分
    :return: token user_info不为空时返回token,token不为空时,成功返回用户信息 失败返回失败空
    """
    JWT_EXPIER_TIME = int(time.time()+expire)
    JWT_SCRECT = "tianna"
    JWT_ALGORITHM = "HS256"
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }

    if user_info:
        # 生成token
        user_info["expire"] = JWT_EXPIER_TIME
        token = jwt.encode(payload=user_info,
                           key=JWT_SCRECT, algorithm=JWT_ALGORITHM, headers=headers)
        return token

    if token:
        try:
            user_info = jwt.decode(token, 'tianna', algorithms=['HS256'])
            if time.time() > int(user_info.pop("expire")):
                return {}
                return "token过期"
            return user_info

        except jwt.PyJWTError as e:
            return {}
            return "token无效"


def md5(txt, length=16):
    md5_hash = hashlib.md5(txt.encode()).hexdigest()
    if length == 16:
        md5_hash = md5_hash[8:24]
    return md5_hash


def guid():
    return str(uuid.uuid4()).replace("-", "")[8:24]
