#系统模块
import datetime

def port_check(port: int) -> bool:
    import socket
    # 检查端口是否可用
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        return sock.connect_ex(('localhost', port)) != 0
    except Exception as e:
        print(f"Error checking port: {e}")
        return False
    finally:
        sock.close()

def log(txt: str="\r\n",level: str="信息"):
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{time_now}>[{level}]:{txt}\r\n")
