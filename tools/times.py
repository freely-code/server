import time
from datetime import datetime


def time2str(time_p=time.localtime(time.time()), format=0, part=0, zero=False, easy=False, date_format='', time_format=''):
    """时间转字符串

    Args:
        time_p (struct_time): 日期时间 struct_time类型的时间
        format (int): 返回格式 0|年-月-日 时:分:秒 1|N年N月N日N时N分N秒 2|00000000000000 3|时间戳(暂时废弃)
        part (int): 返回部分 0|全部 1|年月日 2|年月 3|月日 4|时分秒 5|时分 6|分秒
        zero (bool): 时间归零 将时间设置为00:00:00,仅返回部分为0有效
        easy (bool): 简单年份 将年份前面两位去掉
        date_format (str): 日期格式 %Y-%m-%d 这个参数不为空时,前面除时间外所有参数失效
        time_format (str): 时间格式 %H-%M-%S 这个参数不为空时,前面除时间外所有参数失效

    Returns:
        str: 返回字符串类型的时间
    """

    if not isinstance(time_p, time.struct_time):
        time_p = time.localtime(time.time())

    if date_format or time_format:
        return time.strftime(date_format+' '+time_format, time_p)

    if format == 0:
        if part == 1:
            return time.strftime('%y' if easy else '%Y'+'-%m-%d', time_p)
        elif part == 2:
            return time.strftime('%y' if easy else '%Y'+'-%m', time_p)
        elif part == 3:
            return time.strftime('%m-%d', time_p)
        elif part == 4:
            return time.strftime('%H:%M:%S', time_p)
        elif part == 5:
            return time.strftime('%H:%M', time_p)
        elif part == 6:
            return time.strftime('%M:%S', time_p)
        else:
            date_format = '%y-%m-%d' if easy else '%Y-%m-%d'
            time_format = '00:00:00' if zero else '%H:%M:%S'
            return time.strftime(date_format+' '+time_format, time_p)

    if format == 1:
        if part == 1:
            return time.strftime('%y' if easy else '%Y'+'年%m月%d日', time_p)
        elif part == 2:
            return time.strftime('%y' if easy else '%Y'+'年%m月', time_p)
        elif part == 3:
            return time.strftime('%m月%d日', time_p)
        elif part == 4:
            return time.strftime('%H时%M分%S秒', time_p)
        elif part == 5:
            return time.strftime('%H时%M分', time_p)
        elif part == 6:
            return time.strftime('%M分%S秒', time_p)
        else:
            date_format = '%y年%m月%d日' if easy else '%Y年%m月%d日'
            time_format = '0时0分0秒' if zero else '%H时%M分%S秒'
            return time.strftime(date_format+time_format, time_p)

    if format == 2:
        if part == 1:
            return time.strftime('%y' if easy else '%Y'+'%m%d', time_p)
        elif part == 2:
            return time.strftime('%y' if easy else '%Y'+'%m', time_p)
        elif part == 3:
            return time.strftime('%m%d', time_p)
        elif part == 4:
            return time.strftime('%H%M%S', time_p)
        elif part == 5:
            return time.strftime('%H%M', time_p)
        elif part == 6:
            return time.strftime('%M%S', time_p)
        else:
            date_format = '%y%m%d' if easy else '%Y%m%d'
            time_format = '000' if zero else '%H%M%S'
            return time.strftime(date_format+time_format, time_p)


def datetime2str(datetime_p=datetime.now(), format=0, part=0, zero=False, easy=False, date_format='', time_format=''):
    """日期时间转字符串

    Args:
        datetime (struct_time): 日期时间 struct_time类型的时间
        format (int): 返回格式 0|年-月-日 时:分:秒 1|N年N月N日N时N分N秒 2|00000000000000 3|时间戳(暂时废弃)
        part (int): 返回部分 0|全部 1|年月日 2|年月 3|月日 4|时分秒 5|时分 6|分秒
        zero (bool): 时间归零 将时间设置为00:00:00,仅返回部分为0有效
        easy (bool): 简单年份 将年份前面两位去掉
        date_format (str): 日期格式 %Y-%m-%d 这个参数不为空时,前面除时间外所有参数失效
        time_format (str): 时间格式 %H-%M-%S 这个参数不为空时,前面除时间外所有参数失效

    Returns:
        str: 返回字符串类型的时间
    """

    if not isinstance(datetime_p, datetime):
        datetime_p = datetime.now()

    if date_format or time_format:
        return datetime.strftime(datetime_p, date_format+' '+time_format)

    if format == 0:
        if part == 1:
            return datetime.strftime(datetime_p, '%y' if easy else '%Y'+'-%m-%d')
        elif part == 2:
            return datetime.strftime(datetime_p, '%y' if easy else '%Y'+'-%m')
        elif part == 3:
            return datetime.strftime(datetime_p, '%m-%d')
        elif part == 4:
            return datetime.strftime(datetime_p, '%H:%M:%S')
        elif part == 5:
            return datetime.strftime(datetime_p, '%H:%M')
        elif part == 6:
            return datetime.strftime(datetime_p, '%M:%S')
        else:
            date_format = '%y-%m-%d' if easy else '%Y-%m-%d'
            time_format = '00:00:00' if zero else '%H:%M:%S'
            return datetime.strftime(datetime_p, date_format+' '+time_format)

    if format == 1:
        if part == 1:
            return datetime.strftime(datetime_p, '%y' if easy else '%Y'+'年%m月%d日')
        elif part == 2:
            return datetime.strftime(datetime_p, '%y' if easy else '%Y'+'年%m月')
        elif part == 3:
            return datetime.strftime(datetime_p, '%m月%d日')
        elif part == 4:
            return datetime.strftime(datetime_p, '%H时%M分%S秒')
        elif part == 5:
            return datetime.strftime(datetime_p, '%H时%M分')
        elif part == 6:
            return datetime.strftime(datetime_p, '%M分%S秒')
        else:
            date_format = '%y年%m月%d日' if easy else '%Y年%m月%d日'
            time_format = '0时0分0秒' if zero else '%H时%M分%S秒'
            return datetime.strftime(datetime_p, date_format+time_format)

    if format == 2:
        if part == 1:
            return datetime.strftime(datetime_p, '%y' if easy else '%Y'+'%m%d')
        elif part == 2:
            return datetime.strftime(datetime_p, '%y' if easy else '%Y'+'%m')
        elif part == 3:
            return datetime.strftime(datetime_p, '%m%d')
        elif part == 4:
            return datetime.strftime(datetime_p, '%H%M%S')
        elif part == 5:
            return datetime.strftime(datetime_p, '%H%M')
        elif part == 6:
            return datetime.strftime(datetime_p, '%M%S')
        else:
            date_format = '%y%m%d' if easy else '%Y%m%d'
            time_format = '000' if zero else '%H%M%S'
            return datetime.strftime(datetime_p, date_format+time_format)


def time_different(max_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), min_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> int:
    """计算两个时间的时间差
        Args:
            max_time (str | datetime.datetime): 最大时间
            min_time (str | datetime.datetime): 最小时间
            
        Returns:
            int: 返回时间差
            
    """

    time1 = datetime.strptime(max_time, "%Y-%m-%d %H:%M:%S") if isinstance(max_time, str) else max_time
    time2 = datetime.strptime(min_time, "%Y-%m-%d %H:%M:%S") if isinstance(max_time, str) else min_time
    res=time1-time2    
    # return abs(res.days)*24*60*60+abs(res.seconds)
    return res.days*24*60*60+res.seconds



def time_now():
    # 取现行时间
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def time_stamp():
    # 取现行时间戳
    return time.time()
