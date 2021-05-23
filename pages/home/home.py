from mysql_orm import *
from common_lib import *
from flask import *


home = Blueprint('home', __name__)


def db_get_user_infos(username):
    username = str(username)
    data = db.session.query(user).filter(user.username == username).limit(1).values(user.username, user.password, user.email, user.phone_number, user.last_login, user.sensor_count)
    data = [i for i in data][0]
    ret = {'username': data.username, 'password': data.password, 'email': data.email, 'phone_number': data.phone_number, 'last_login': str(data.last_login), 'sensor_count': data.sensor_count}
    return ret


# TODO home首页
@home.route('/')
def render_home_page():
    return send_file('pages/home/home.html')


# TODO 用户信息
@home.route('/get_user_infos')
def get_user_infos():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            ret = db_get_user_infos(username)
            print(ret)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


# 设备最新信息
@home.route('/get_current_device_infos')
def get_current_device_infos():
    try:
        user_cookies = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookies)
        if username:
            ret = db_get_current_device_infos(username)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_get_current_device_infos(username):
    username = str(username)
    ret_data = []
    data = db.session.query(device_rec.username, device_rec.device_id, device_rec.record_type).group_by(device_rec.username, device_rec.device_id, device_rec.record_type).having(device_rec.username == username)
    for i in data:
        print(i)
        data2 = db.session.query(device_rec.device_id, device_rec.record_type, device_rec.record_value, device_rec.unit, device_rec.record_time).filter(device_rec.username == i.username, device_rec.device_id == i.device_id, device_rec.record_type == i.record_type).order_by(device_rec.record_time.desc()).limit(1)
        for j in data2:
            ret_data.append({'device_id': j.device_id, 'record_type': j.record_type, 'record_value': j.record_value, 'uint': j.unit, 'record_time': str(j.record_time)})
    print(ret_data)
    return ret_data


# 设备阈值
@home.route('/get_device_th')
def get_device_th():
    try:
        user_cookies = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookies)
        if username:
            ret = db_get_device_th(username)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


# 退出登录
@home.route('/exit_login')
def exit_login():
    try:
        user_cookies = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookies)
        if username:
            remove_cookie(cookie=user_cookies)
            return api_resp(code=0, msg='已退出登录')
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_get_device_th(username):
    return 'ok'




