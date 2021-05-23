import time
import hashlib
import redis
from flask import jsonify
from ConfigReader import get_redis_config


def generate_new_cookie():
    time_stamp = time.time()
    md5 = hashlib.md5()
    md5.update(str(time_stamp).encode())
    new_cookie = str(md5.hexdigest())
    return new_cookie


def api_resp(code, msg=''):
    data = {'code': code, 'msg': msg}
    return jsonify(data)


def api_resp_permission_error():
    return jsonify({'code': -1, 'msg': '登陆状态过期，请重新登陆'})


def api_err_resp(code=-200, msg='服务器内部错误'):
    data = {'code': code, 'msg': str(msg)}
    return jsonify(data)


# 初始化REDIS
REDIS_CONFIG = get_redis_config()
REDIS_HOST = REDIS_CONFIG['REDIS_HOST']
REDIS_PASSWORD = REDIS_CONFIG['REDIS_PASSWORD']
REDIS_PORT = REDIS_CONFIG['REDIS_PORT']
REDIS_DB = REDIS_CONFIG['REDIS_DB']
REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT, db=REDIS_DB, socket_connect_timeout=1, decode_responses=True)
REDIS_CONNECT = redis.Redis(connection_pool=REDIS_POOL)


# 公共查询，cookie相关
def query_cookie_pool(cookie):
    return REDIS_CONNECT.get(name=str(cookie))


def add_new_cookie_to_redis(cookie):
    return REDIS_CONNECT.set(name=str(cookie), value='', ex=5000)


def mark_cookie_valid(cookie, value):
    return REDIS_CONNECT.set(name=str(cookie), value=value, ex=5000)


def remove_cookie(cookie):
    return REDIS_CONNECT.delete(str(cookie))


def check_permission(cookie):
    username = query_cookie_pool(cookie=cookie)
    if username is None or username == '':
        return False
    else:
        REDIS_CONNECT.set(name=str(cookie), value=username, ex=5000)
        return username



