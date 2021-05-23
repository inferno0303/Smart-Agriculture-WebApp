from mysql_orm import *
from common_lib import *
from flask import *


threshold = Blueprint('threshold', __name__)


def db_get_all_device_id(username):
    username = str(username)
    ret_data = []
    data = db.session.query(device_rec.username, device_rec.device_id).group_by(device_rec.username, device_rec.device_id).having(device_rec.username == username)
    for i in data:
        print(i)
        ret_data.append({'username': i.username, 'device_id': i.device_id})
    return ret_data


def db_setting_th(username, device_id, setting_th):
    username = str(username)
    device_id = str(device_id)
    setting_th = list(setting_th)
    for i in setting_th:
        print(i)
        data = db.session.query(device_th).filter(device_th.username == username, device_th.device_id == device_id, device_th.record_type == i['record_type']).limit(1)
        for j in data:
            j.low_th = i['low_th']
            j.high_th = i['high_th']
            db.session.commit()
    return True


@threshold.route('/')
def render_threshold_page():
    return send_file('pages/threshold/threshold.html')


# TODO 获取device_id列表
@threshold.route('/get_all_device_id')
def get_all_device_id():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            ret = db_get_all_device_id(username)
            print(ret)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


# TODO 根据device_id获取设备阈值信息
@threshold.route('/get_record_type_by_device_id')
def get_record_type_by_device_id():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            device_id = request.args.get("device_id")
            ret = db_get_record_type_by_device_id(username, device_id)
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


def db_get_record_type_by_device_id(username, device_id):
    username = str(username)
    device_id = str(device_id)
    ret_data = []
    data = db.session.query(device_rec.record_type).filter(device_rec.username == username, device_rec.device_id == device_id).distinct()
    for i in data:
        data2 = db.session.query(device_th.low_th, device_th.high_th).filter(device_th.username == username, device_th.device_id == device_id, device_th.record_type == i.record_type)
        for j in data2:
            ret_data.append({'record_type': i.record_type, 'low_th': j.low_th, 'high_th': j.high_th})
    print(ret_data)
    return ret_data


# TODO 根据device_id设置阈值
@threshold.route('/setting_th', methods=['POST'])
def setting_th():
    try:
        user_cookie = request.cookies['LOGIN_SESSION']
        username = check_permission(cookie=user_cookie)
        if username:
            device_id = request.form['device_id']
            setting_th = request.form['setting_th']
            setting_th = json.loads(setting_th)
            ret = db_setting_th(username, device_id, setting_th)
            return api_resp(code=0, msg='修改成功')
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()