from app import *
cookie = Blueprint('cookie', __name__)


def query_cookie_pool(cookie):
    return REDIS_CONNECT.get(name=str(cookie))


def add_new_cookie_to_redis(cookie):
    return REDIS_CONNECT.set(name=str(cookie), value='', ex=5000)


@cookie.route('/check_cookie')
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
