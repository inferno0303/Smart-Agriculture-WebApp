from mysql_orm import *
from common_lib import *
from flask import *


register = Blueprint('register', __name__)


@register.route('/')
def render_threshold_page():
    return send_file('pages/register/register.html')


# TODO 注册api
@register.route('/submit_register', methods=['POST'])
def submit_register():
    try:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        if username != '' and password != '' and email != '' and phone_number != '':
            print(username, password, email, phone_number)
            data = db.session.query(user.username).filter(user.username == username).first()
            if data is None:
                new_user_record = user(username=username, password=password, email=email, phone_number=phone_number, sensor_count=4)
                db.session.add(new_user_record)
                db.session.commit()
                return api_resp(code=0, msg='注册成功')
            else:
                return api_resp(code=-1, msg='已存在该用户')
        else:
            return api_resp_permission_error()
    except Exception as e:
        print(e)
        return api_resp_permission_error()

