from mysql_orm import *
from common_lib import *
from flask import *
from sqlalchemy import func


alarm = Blueprint('alarm', __name__)


@alarm.route('/')
def render_history_page():
    return send_file('pages/alarm/alarm.html')


@alarm.route('/get_device_th')
def get_device_th():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            ret = db_get_device_th(username)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_get_device_th(username):
    username = str(username)
    ret_data = []
    data = db.session.query(device_th.username, device_th.device_id, device_th.record_type, device_th.low_th, device_th.high_th).filter(device_th.username == username).distinct()
    for i in data:
        ret_data.append({'username': i.username, 'device_id': i.device_id, 'record_type': i.record_type, 'low_th': i.low_th, 'high_th': i.high_th})
    print(ret_data)
    return ret_data


@alarm.route('/get_alarm_info')
def get_alarm_info():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            ret = db_get_alarm_info(username)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_get_alarm_info(username):
    username = str(username)
    # 先获取阈值
    ret_data = []
    data = db.session.query(device_th.username, device_th.device_id, device_th.record_type, device_th.low_th, device_th.high_th).filter(device_th.username == username).distinct()
    for i in data:
        ret_data.append({'username': i.username, 'device_id': i.device_id, 'record_type': i.record_type, 'low_th': i.low_th, 'high_th': i.high_th})
    # 再遍历记录
    ret_data2 = []
    for i in ret_data:
        data2 = db.session.query(device_rec).filter(device_rec.username == i['username'], device_rec.device_id == i['device_id'], device_rec.record_type == i['record_type'], db.or_(device_rec.record_value > i['high_th'], device_rec.record_value < i['low_th']))
        for j in data2:
            print(j, '***')
            ret_data2.append({'username': j.username, 'device_id': j.device_id, 'record_type': j.record_type, 'record_value': j.record_value, 'unit': j.unit, 'record_time': j.record_time.strftime("%Y-%m-%d %H:%M")})
    return ret_data2
