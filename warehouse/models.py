from datetime import datetime
from warehouse import db


class EnterWH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer)
    g_name = db.Column(db.String(100))
    g_num = db.Column(db.Integer)
    g_type = db.Column(db.String(50))
    weight = db.Column(db.FLOAT)
    from_where = db.Column(db.String(50))
    to_where = db.Column(db.String(50))
    trans_date = db.Column(db.String(50))
    license_num = db.Column(db.String(50))
    to_company = db.Column(db.String(50))
    remarks = db.Column(db.String(50))
    need_goods_f = db.Column(db.FLOAT(50))
    need_goods_s = db.Column(db.FLOAT(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer)
    g_name = db.Column(db.String(100), unique=True)
    base_num = db.Column(db.Integer)
    g_type = db.Column(db.String(50))
    base_weight = db.Column(db.FLOAT)


class GoodTrends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer)
    g_name = db.Column(db.String(100), unique=True)
    base_num = db.Column(db.Integer, default=0)
    total_num = db.Column(db.Integer, default=0)
    trends_num = db.Column(db.Integer, default=0)
    g_type = db.Column(db.String(50))
    base_weight = db.Column(db.Integer, default=0.0)
    total_weight = db.Column(db.FLOAT, default=0.0)
    trends_weight = db.Column(db.FLOAT, default=0.0)
    trends_date = db.Column(db.String(50))


class GoodID(db.Model):
    good_id = db.Column(db.Integer, primary_key=True, default=10000)
    g_name = db.Column(db.String(100), unique=True)



