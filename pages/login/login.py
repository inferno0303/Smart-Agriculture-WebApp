from mysql_orm import *
from common_lib import *
from flask import *
import datetime


login = Blueprint('login', __name__)


def check_username_password(username, password):
    ret = db.session.query(user).filter(user.username == username, user.password == password).first()
    return ret


@login.route('/')
def render_login_page():
    return send_file('pages/login/login.html')


@login.route('/check_cookie')
def check_cookie():
    try:
        user_cookie = str(request.cookies.get('LOGIN_SESSION'))
        result = query_cookie_pool(cookie=user_cookie)
        # 空cookie，设置cookie
        if result is None:
            new_cookie = generate_new_cookie()
            add_new_cookie_to_redis(cookie=new_cookie)
            resp = make_response(api_resp(code=0))
            resp.set_cookie('LOGIN_SESSION', value=new_cookie)
            return resp
        # cookie无登陆状态
        elif result == '':
            return api_resp(code=1)
        # cookie有登陆状态
        else:
            return api_resp(code=2)
    except Exception as e:
        print(e)
        return api_err_resp(msg=e)


@login.route('/login_api', methods=['POST'])
def login_api():
    try:
        username = request.form['username']
        password = request.form['password']
        user_cookie = request.cookies.get('LOGIN_SESSION')
        db_ret = check_username_password(username=username, password=password)
        print(db_ret)
        # 用户名密码错误
        if db_ret is None:
            return api_resp(code=-1, msg='用户名或密码错误')
        # 用户名密码有效
        else:
            # 更新最近登录
            data = db.session.query(user).filter(user.username == username, user.password == password).first()
            data.last_login = datetime.datetime.now()
            db.session.commit()
            # 检查cookie池
            redis_ret = query_cookie_pool(cookie=user_cookie)
            # 空cookie，设置cookie，并维护该cookie
            if redis_ret is None:
                new_cookie = generate_new_cookie()
                add_new_cookie_to_redis(cookie=new_cookie)
                mark_cookie_valid(cookie=new_cookie, value=username)
                resp = make_response(api_resp(code=0, msg='登陆成功'))
                resp.set_cookie('LOGIN_SESSION', value=new_cookie)
                return resp
            # 维护该cookie
            else:
                mark_cookie_valid(cookie=user_cookie, value=username)
                return api_resp(code=0, msg='登陆成功')
    except Exception as e:
        print(e)
        return api_err_resp(msg=e)
