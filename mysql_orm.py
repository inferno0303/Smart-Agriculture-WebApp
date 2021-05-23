from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

# 基类
db = SQLAlchemy()


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    phone_number = db.Column(db.VARCHAR)
    last_login = db.Column(db.DateTime)
    sensor_count = db.Column(db.Integer)
    keys = ['id', 'username', 'password', 'email', 'phone_number', 'last_login', 'sensor_count']

    def __repr__(self):
        return '<ORM repr> (%s, %s, %s, %s)' % (self.id, self.username, self.password, self.email)


class device_rec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR)
    device_id = db.Column(db.VARCHAR)
    record_type = db.Column(db.VARCHAR)
    record_value = db.Column(db.VARCHAR)
    unit = db.Column(db.VARCHAR)
    record_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<ORM repr> (%s, %s, %s, %s)' % (self.id, self.record_value, self.unit, self.record_time)


class device_th(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR)
    device_id = db.Column(db.VARCHAR)
    record_type = db.Column(db.VARCHAR)
    low_th = db.Column(db.VARCHAR)
    high_th = db.Column(db.VARCHAR)

    def __repr__(self):
        return '<ORM repr> (%s, %s, %s, %s)' % (self.id, self.username, self.low_th, self.high_th)



# TODO 管理员ORM
class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    phone_number = db.Column(db.VARCHAR)
    admin_flag = db.Column(db.VARCHAR)

    def __repr__(self):
        return '<ORM repr> (%s, %s, %s, %s)' % (self.id, self.username, self.password, self.admin_flag)