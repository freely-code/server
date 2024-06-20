#字符串模块
from datetime import datetime
from urllib import parse
def str2bool(txt:str)->bool:
    print("999")
    # 字符串转逻辑
    if isinstance(txt, bool):
        return txt
    return txt.lower() in ('yes', 'true', 't', 'y', '1')


# 格式化参数
def arguments_format(arguments, files=None):
    """格式化参数,将参数转换成json

    Args:
        arguments (_type_): _description_
        files (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    if not arguments:
        return {}
    params = {}

    # 有文件时的处理
    if files:
        for key in arguments:
            value = [bytes.decode('utf-8') for bytes in arguments[key]]
            if len(value) < 2:
                params[key] = value[0]
            else:
                params[key] = value

        for key in files:
            value = files[key]
            if key in params:
                if isinstance(params[key], str):
                    params[key] = [params[key]]
                params[key].append(value)
            else:
                if len(value) < 2:
                    params[key] = value[0]
                else:
                    params[key] = value

        return params

    # 只有参数时的处理
    array = arguments.split("&")
    for item in array:
        key, value = item.split("=")
        value = parse.unquote(value)
        if key in params:
            if isinstance(params[key], str):
                params[key] = [params[key]]
            params[key].append(value)
        else:
            params[key] = value
    return params


def str_middle_all(text, front, back):
    """批量取文本中间

    Args:
        text (str): 文本
        front (str): 前面字符
        back (str): 后面字符
    """
    return re.findall(f'{front}([\s\S]*?){back}', text)


def validate_phone(phone):
    # 手机号校验
    pattern = re.compile(r'^1[3-9]\d{9}$')
    return bool(pattern.match(phone))



def validate_email(email):
    # 邮箱校验
    pattern = re.compile(r'^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$')
    return bool(pattern.match(email))
