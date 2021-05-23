from mysql_orm import *
from common_lib import *
from flask import *
import datetime


admin = Blueprint('admin', __name__)


@admin.route('/')
def render_threshold_page():
    return send_file('pages/admin/admin.html')


# TODO 获取用户信息api
@admin.route('/get_all_users')
def get_all_users():
    try:
        admin = request.args.get('admin')
        admin_pass = request.args.get('admin_pass')
        if admin == 'admin' and admin_pass == '123456':
            ret = []
            data = db.session.query(user).all()
            for i in data:
                ret.append({'username': i.username, 'password': i.password, 'email': i.email, 'phone_number': i.phone_number, 'last_login': str(i.last_login), 'sensor_count': i.sensor_count})
            return api_resp(code=0, msg=ret)
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()


# TODO 获取用户信息api
@admin.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        # admin = request.args.get('admin')
        # admin_pass = request.args.get('admin_pass')
        # if admin == 'admin' and admin_pass == '123456':
        if 'ok':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            phone_number = request.form['phone_number']
            print(username, password, "****")
            data = db.session.query(user).filter(user.username == username, user.password == password, user.email == email, user.phone_number == phone_number).first()
            if data is not None:
                db.session.delete(data)
                db.session.commit()
                return api_resp(code=0, msg='删除用户成功')
            else:
                return api_resp(code=-1, msg='删除用户失败')
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()
