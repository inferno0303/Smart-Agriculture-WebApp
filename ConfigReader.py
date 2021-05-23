import configparser


def get_mysql_config():
    db_config = configparser.ConfigParser()
    db_config.read('database_config.ini')
    MYSQL_USER = db_config.get('MYSQL', 'DB_USER')
    MYSQL_PASSWORD = db_config.get('MYSQL', 'DB_PASSWORD')
    MYSQL_HOST = db_config.get('MYSQL', 'DB_HOST')
    MYSQL_DB = db_config.get('MYSQL', 'DB_DB')
    infos = {'MYSQL_USER': MYSQL_USER, 'MYSQL_PASSWORD': MYSQL_PASSWORD, 'MYSQL_HOST': MYSQL_HOST, 'MYSQL_DB': MYSQL_DB}
    print('获取MYSQL数据库连接信息：', infos)
    return infos


def get_redis_config():
    redis_config = configparser.ConfigParser()
    redis_config.read('database_config.ini')
    REDIS_HOST = redis_config.get('REDIS', 'HOST')
    REDIS_PASSWORD = redis_config.get('REDIS', 'PASSWORD')
    REDIS_PORT = redis_config.get('REDIS', 'PORT')
    REDIS_DB = redis_config.get('REDIS', 'DB')
    infos = {'REDIS_HOST': REDIS_HOST, 'REDIS_PASSWORD': REDIS_PASSWORD, 'REDIS_PORT': REDIS_PORT, 'REDIS_DB': REDIS_DB}
    print('获取REDIS数据库连接信息：', infos)
    return infos


if __name__ == '__main__':
    get_mysql_config()
    get_redis_config()
