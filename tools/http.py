import aiohttp,asyncio,json


async def __fetch(session, url,data=None,headers=None,cookies=None,proxy=None, timeout=60):
    """
    :param session: aiohttp.ClientSession
    :param url: str
    :return: str
    单个启动 a=asyncio.run(__fetch(url=url,data=data,headers=headers,proxy=proxy,cookies=cookies))
    """

    # # 设置单个超时
    timeout = aiohttp.ClientTimeout(timeout)
    try:
        if data:   
            if headers and "Content-Type" not in headers:
                headers["Content-Type"]="application/json"
            async with session.post(url=url,data=data,headers=headers,cookies=cookies,proxy=proxy, timeout=timeout) as response:
                return await response.content.read()
        else:
            async with session.get(url=url,headers=headers,cookies=cookies,proxy=proxy, timeout=timeout) as response:
                return await response.content.read()
    except:
        return bytes()


async def http_pool(url,data=None,headers=None,cookies=None,proxy=None, callback=None, timeout=60):
    """
    等待所有任务完成
    :param url: str
    :return: str
    """
    # # 设置全局超时
    # timeout = aiohttp.ClientTimeout(timeout)
    # 最大请求数
    connector = aiohttp.TCPConnector(limit=1000)
    async with aiohttp.ClientSession(connector=connector) as session:
        if isinstance(url, str):
            urls = [url]
        else:
            urls = url
        tasks = [asyncio.create_task(
            __fetch(session=session, url=url,data=data,headers=headers,cookies=cookies,proxy=proxy, timeout=timeout)) for url in urls]
        for task in asyncio.as_completed(tasks):
            response = await task
            if callback:
                callback(response=response)
        return response


async def http_pool_ex(url,data=None,headers=None,cookies=None,proxy=None, callback=None, timeout=60):
    """
    完成一个任务 回调一个任务 
    :param url: str
    :return: str
    """

    # # 设置全局超时
    # timeout = aiohttp.ClientTimeout(timeout)
    # 最大请求数
    connector = aiohttp.TCPConnector(limit=1000)
    async with aiohttp.ClientSession(connector=connector) as session:
        if isinstance(url, str):
            urls = [url]
        else:
            urls = url
        tasks = [asyncio.create_task(
            __fetch(session=session, url=url,data=data,headers=headers,cookies=cookies,proxy=proxy, timeout=timeout)) for url in urls]
        while True:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for t in done:
                response = t.result()
                if callback:
                    callback(response=response)
            if pending:  # 还有未完成的任务，那么继续使用 wait
                tasks = pending
            else:
                break
        return response





async def http(url, data=None,headers=None,cookies=None,proxy=None, timeout=60):
    """单个http
    Args:
        urls (_type_): _description_
        data (_type_, optional): _description_. Defaults to None.
        headers (_type_, optional): _description_. Defaults to None.
        cookies (_type_, optional): _description_. Defaults to None.
        proxy (_type_, optional): _description_. Defaults to None.
        callback (_type_, optional): _description_. Defaults to None.
        callback (_type_, optional): _description_. Defaults to None.
        timeout (int, optional): _description_. Defaults to 60.
    """
    try:
        async with aiohttp.ClientSession() as session:
            if data:   
                if headers and "Content-Type" not in headers:
                    headers["Content-Type"]="application/json"
                if isinstance(data, dict):
                    data=json.dumps(data)
                async with session.post(url=url,data=data,headers=headers,cookies=cookies,proxy=proxy,allow_redirects=True) as response:
                    return  await response.content.read()
            else:
                async with session.get(url=url,headers=headers,cookies=cookies,proxy=proxy,allow_redirects=True) as response:
                    return await response.content.read()
    except Exception as e:
        print(f"Error in http: {e}")
        return bytes()


def fun(response):
    print(response.decode('utf-8'), '\r\n')


async def aa():
    urls = [
        "http://httpbin.org/get",
        "http://httpbin.org/get1",
        "http1://httpbin.org/get",
    ]

    t1 = asyncio.create_task(http(urls, callback=fun, timeout=60))

    urls = "http://baidu.com"

    t2 = asyncio.create_task(http(urls, callback=fun, timeout=60))
    await asyncio.gather(t1, t2)


# 使用示例
if __name__ == "__main__":
    #aa()
    a=asyncio.run(http("http://baidu.com"))
    print(a.decode('utf-8'))