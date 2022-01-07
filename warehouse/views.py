from flask import flash, redirect, url_for, render_template, request

from warehouse import app, db
from warehouse.models import GoodID, Goods, EnterWH, GoodTrends
from warehouse.forms import WHForm, DateForm, GoodsForm, EditGoodForm, DeleteGoodForm, SearchForm
from datetime import datetime, date
from calendar import monthrange


def get_id(g_name):
    exist = GoodID.query.filter(GoodID.g_name == g_name).first()
    if exist is None:
        cur_id = GoodID.query.order_by(GoodID.good_id.desc()).first()
        if cur_id is None:
            db.session.add(GoodID(g_name=g_name))
        else:
            db.session.add(GoodID(good_id=cur_id.good_id + 1, g_name=g_name))
        db.session.commit()
        return GoodID.query.filter(GoodID.g_name == g_name).first().good_id
    else:
        return exist.good_id


def get_name(name):
    return name.replace(" ", "")


@app.route('/join', methods=['GET', 'POST'])
def join():
    form = WHForm()
    if form.validate_on_submit():
        g_name = get_name(form.g_name.data)
        g_id = get_id(g_name)
        g_num = form.g_num.data
        g_type = form.g_type.data
        weight = form.weight.data
        if g_num is None:
            g_num = 0
        if weight is None:
            weight = 0
        trans_date = form.trans_date.data
        from_where = form.from_where.data
        to_where = form.to_where.data
        license_num = form.license_num.data
        to_company = form.to_company.data
        remarks = form.remarks.data
        need_goods_f = form.need_goods_f.data
        need_goods_s = form.need_goods_s.data
        if need_goods_f is None:
            need_goods_f = 0
        if need_goods_s is None:
            need_goods_s = 0
        enter_order = EnterWH(good_id=g_id, g_name=g_name, g_num=g_num, g_type=g_type, weight=weight,
                              trans_date=trans_date,
                              from_where=from_where, to_where=to_where, license_num=license_num, to_company=to_company,
                              remarks=remarks, need_goods_f=need_goods_f, need_goods_s=need_goods_s)
        db.session.add(enter_order)
        db.session.commit()
        flash('新增入库成功！')
        refresh_good_trends(g_id)
        return redirect(url_for('index'))
    return render_template('join.html', form=form)


@app.route('/out', methods=['GET', 'POST'])
def goods_out():
    form = WHForm()
    if form.validate_on_submit():
        g_name = get_name(form.g_name.data)
        g_id = get_id(g_name)
        g_num = form.g_num.data
        g_type = form.g_type.data
        weight = form.weight.data
        if g_num is None:
            g_num = 0
        if weight is None:
            weight = 0
        if g_num > 0:
            g_num = 0 - g_num
        if weight > 0:
            weight = 0 - weight
        trans_date = form.trans_date.data
        from_where = form.from_where.data
        to_where = form.to_where.data
        license_num = form.license_num.data
        to_company = form.to_company.data
        remarks = form.remarks.data
        need_goods_f = form.need_goods_f.data
        need_goods_s = form.need_goods_s.data
        if need_goods_f is None:
            need_goods_f = 0
        if need_goods_s is None:
            need_goods_s = 0
        enter_order = EnterWH(good_id=g_id, g_name=g_name, g_num=g_num, g_type=g_type, weight=weight,
                              trans_date=trans_date,
                              from_where=from_where, to_where=to_where, license_num=license_num, to_company=to_company,
                              remarks=remarks, need_goods_f=need_goods_f, need_goods_s=need_goods_s)
        db.session.add(enter_order)
        db.session.commit()
        flash('出库成功！')
        refresh_good_trends(g_id)
        return redirect(url_for('index'))
    return render_template('out.html', form=form)


@app.route('/', defaults={'sort': 0}, methods=['GET', 'POST'])
@app.route('/sorts/<int:sort>', methods=['GET', 'POST'])
def index(sort):
    cur_year = datetime.now().year
    cur_month = datetime.now().month
    form = DateForm(years=cur_year, months=cur_month)
    search_form = SearchForm()
    if form.submit.data and form.validate_on_submit():
        year = form.years.data
        month = form.months.data
        return redirect(url_for('detail', year=year, month=month, sort=0))
    if search_form.submit_search.data and search_form.validate_on_submit():
        data = search_form.g_name.data
        trends_goods = GoodTrends.query.filter(GoodTrends.g_name.like('%' + data + '%')).all()
        print('search_good = ', search_form.g_name.data)
        if search_form.g_name.data == '':
            return redirect(url_for('index', sort=0))
        else:
            return render_template('home.html', form=form, search_form=search_form, trends_goods=trends_goods)
    if sort == 0:
        trends_goods = GoodTrends.query.order_by(GoodTrends.trends_date.desc()).all()
    elif sort == 1:
        trends_goods = GoodTrends.query.order_by(GoodTrends.g_name.asc()).all()
    elif sort == 2:
        trends_goods = GoodTrends.query.order_by(GoodTrends.total_num.asc()).all()
    elif sort == 3:
        trends_goods = GoodTrends.query.order_by(GoodTrends.total_weight.asc()).all()
    else:
        trends_goods = GoodTrends.query.all()

    return render_template('home.html', form=form, search_form=search_form, trends_goods=trends_goods)


@app.route('/creat', methods=['GET', 'POST'])
def creat():
    form = GoodsForm()
    if form.validate_on_submit():
        g_name = get_name(form.g_name.data)
        base_num = form.base_num.data
        g_type = form.g_type.data
        base_weight = form.base_weight.data
        if base_num is None:
            base_num = 0
        if base_weight is None:
            base_weight = 0
        g_id = get_id(g_name)
        name_is_exit = Goods.query.filter(Goods.g_name == g_name).first()
        print('g_id= ', g_id)
        if name_is_exit is None:
            new_good = Goods(g_name=g_name, good_id=g_id, base_num=base_num, g_type=g_type, base_weight=base_weight)
            db.session.add(new_good)
            db.session.commit()
            init_good_trends(g_id)
            flash('成功新增物品！')
            return redirect(url_for('creat'))
        else:
            flash('该物品已存在，请直接编辑')
            return redirect(url_for('creat'))
    goods = Goods.query.all()
    return render_template('creat.html', form=form, goods=goods)


@app.route('/edit_good/<int:good_id>', methods=['GET', 'POST'])
def edit_good(good_id):
    form = EditGoodForm()
    del_form = DeleteGoodForm()
    print('good_id = ', good_id)
    good_info = Goods.query.filter(Goods.good_id == good_id).one()
    if form.validate_on_submit():
        base_num = form.base_num.data
        base_weight = form.base_weight.data
        if base_num is None:
            base_num = 0
        if base_weight is None:
            base_weight = 0
        print('num = ', form.base_num.data)
        good_info.base_num = base_num
        good_info.g_type = form.g_type.data
        good_info.base_weight = base_weight
        db.session.commit()
        flash('修改成功！')
        init_good_trends(good_id)
        return redirect(url_for('creat'))
    if del_form.validate_on_submit():
        print('del_good')
        db.session.delete(good_info)
        db.session.commit()
        flash('删除成功！')
        init_good_trends(good_id)
        return redirect(url_for('creat'))
    form.base_num.data = good_info.base_num
    form.g_type.data = good_info.g_type
    form.base_weight.data = good_info.base_weight
    return render_template('edit_good.html', good=good_info, form=form, del_form=del_form)


@app.route('/detail/<int:year>/<int:month>/<int:sort>', methods=['GET', 'POST'])
def detail(year, month, sort):
    form = DateForm(years=year, months=month)
    if form.validate_on_submit():
        year1 = form.years.data
        month1 = form.months.data
        # day = form.day.data
        # to_day = form.to_day.data
        return redirect(url_for('detail', year=year1, month=month1, sort=0))
    if year == 2000:
        start = date(year=year, month=1, day=1)
        end = date(year=datetime.now().year, month=12, day=31)
        cur_title = '全部'
    elif month == 0:
        start = date(year=year, month=1, day=1)
        end = date(year=year, month=12, day=31)
        cur_title = str(year) + '年'
    else:
        start = date(year=year, month=month, day=1)
        end = date(year=year, month=month, day=monthrange(year, month)[1])
        cur_title = str(year) + '年' + str(month) + '月'
    if sort == 0:
        enter_order = EnterWH.query.filter(EnterWH.trans_date <= end).filter(EnterWH.trans_date >= start).order_by(
            EnterWH.trans_date.desc()).all()
    elif sort == 1:
        enter_order = EnterWH.query.filter(EnterWH.trans_date <= end).filter(EnterWH.trans_date >= start).order_by(
            EnterWH.g_name.asc()).all()
    elif sort == 2:
        enter_order = EnterWH.query.filter(EnterWH.trans_date <= end).filter(EnterWH.trans_date >= start).order_by(
            EnterWH.g_num.asc()).all()
    elif sort == 3:
        enter_order = EnterWH.query.filter(EnterWH.trans_date <= end).filter(EnterWH.trans_date >= start).order_by(
            EnterWH.weight.asc()).all()
    else:
        enter_order = EnterWH.query.filter(EnterWH.trans_date <= end).filter(EnterWH.trans_date >= start).all()

    return render_template('detail.html', form=form, cur_title=cur_title,
                           cur_year=year, cur_month=month, goods=enter_order)


@app.route('/good_detail/<int:good_id>', methods=['GET', 'POST'])
def good_detail(good_id):
    trend_detail = EnterWH.query.filter(EnterWH.good_id == good_id).all()
    cur_title = GoodID.query.filter(GoodID.good_id == good_id).first().g_name
    return render_template('good_detail.html', good_detail=trend_detail, cur_title=cur_title)


def refresh_good_trends(good_id):
    new_info = EnterWH.query.order_by(EnterWH.id.desc()).first()
    good_exist = GoodTrends.query.filter(GoodTrends.good_id == good_id).first()
    if good_exist is None:
        good_id = new_info.good_id
        g_name = new_info.g_name
        trends_num = new_info.g_num
        total_num = trends_num
        g_type = new_info.g_type
        trends_weight = new_info.weight
        total_weight = trends_weight
        trends_date = new_info.trans_date
        good_trends = GoodTrends(g_name=g_name, good_id=good_id, total_num=total_num, trends_num=trends_num,
                                 g_type=g_type, total_weight=total_weight, trends_weight=trends_weight,
                                 trends_date=trends_date)
        db.session.add(good_trends)
        db.session.commit()
    else:
        good_exist.trends_num = new_info.g_num
        good_exist.total_num = good_exist.base_num + new_info.g_num
        good_exist.trends_weight = new_info.weight
        good_exist.total_weight = good_exist.base_weight + new_info.weight
        good_exist.trends_date = new_info.trans_date
        print('new_info.g_type=', new_info.g_type)
        if new_info.g_type != '':
            good_exist.g_type = new_info.g_type
        db.session.commit()


def init_good_trends(good_id):
    good_info = Goods.query.filter(Goods.good_id == good_id).first()
    good_exist = GoodTrends.query.filter(GoodTrends.good_id == good_id).first()
    if good_exist is None:
        good_id = good_info.good_id
        g_name = good_info.g_name
        base_num = good_info.base_num
        base_weight = good_info.base_weight
        g_type = good_info.g_type
        good_trends = GoodTrends(g_name=g_name, good_id=good_id, base_num=base_num, total_num=base_num,
                                 g_type=g_type, base_weight=base_weight, total_weight=base_weight)
        print('trends_num=', good_trends.trends_num, '  trends_weight=', good_trends.trends_weight)
        db.session.add(good_trends)
        db.session.commit()
    else:
        if good_info is not None:
            good_exist.base_num = good_info.base_num
            good_exist.total_num = good_exist.base_num + good_exist.trends_num
            good_exist.base_weight = good_info.base_weight
            good_exist.total_weight = good_exist.base_weight + good_exist.trends_weight
            db.session.commit()
        else:
            good_exist.base_num = 0
            good_exist.total_num = good_exist.base_num + good_exist.trends_num
            good_exist.base_weight = 0
            good_exist.total_weight = good_exist.base_weight + good_exist.trends_weight
            db.session.commit()


@app.template_filter('my_date')
def m_date(value):
    value = value[5:6].replace('0', '') + value[6:7] + '月' + value[8:9].replace('0', '') + value[9:] + '日'
    return value


@app.template_filter('my_num')
def m_num(value):
    return int(value)


@app.template_global()
def mo_data():
    return 0
