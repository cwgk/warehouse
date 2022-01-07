from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField \
    , FloatField, DateField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, Optional, Length
from datetime import datetime


class GoodsForm(FlaskForm):
    g_name = StringField('物品名称', validators=[DataRequired(), Length(1, 20)])
    base_num = IntegerField('数量', validators=[Optional(strip_whitespace=True)])
    g_type = StringField('单位', validators=[Length(0, 10)])
    base_weight = FloatField('重量', validators=[Optional(strip_whitespace=True)])
    submit = SubmitField('新增物品')


class EditGoodForm(FlaskForm):
    base_num = IntegerField('数量', validators=[InputRequired()])
    g_type = StringField('单位', validators=[Length(0, 10)])
    base_weight = FloatField('重量', validators=[InputRequired()])
    submit_edit = SubmitField('修改')


class SearchForm(FlaskForm):
    g_name = StringField(validators=[Length(0, 20)])
    submit_search = SubmitField('Go')


class DeleteGoodForm(FlaskForm):
    submit_del = SubmitField('删除')


class WHForm(FlaskForm):
    g_name = StringField('物品名称', validators=[DataRequired(), Length(1, 20)])
    g_num = IntegerField('数量', validators=[Optional(strip_whitespace=True)])
    g_type = SelectField('单位', choices=[('', ''), ('吨桶', '吨桶'), ('吨袋', '吨袋')])
    weight = FloatField('重量', validators=[Optional(strip_whitespace=True)])
    from_where = StringField('起运地', validators=[DataRequired(), Length(1, 10)])
    to_where = StringField('到达地', validators=[DataRequired(), Length(1, 10)])
    trans_date = DateField("运输日期")
    license_num = StringField('车牌号', validators=[DataRequired(), Length(1, 20)])
    to_company = StringField('到货公司', validators=[DataRequired(), Length(1, 20)])
    remarks = StringField('备注', validators=[Optional(strip_whitespace=True), Length(1, 20)])
    need_goods_f = FloatField('塑胶卡板', validators=[Optional(strip_whitespace=True)])
    need_goods_s = FloatField('废纸箱', validators=[Optional(strip_whitespace=True)])
    submit = SubmitField()


class DateForm(FlaskForm):
    currentYear = datetime.now().year
    years_data = [('2000', '全部')] + list((str(m), str(m) + '年') for m in range(2021, currentYear + 1))
    months_data = [('0', '全部'), ('1', '一月'), ('2', '二月'), ('3', '三月'), ('4', '四月'),
                   ('5', '五月'), ('6', '六月'), ('7', '七月'), ('8', '八月'), ('9', '九月'),
                   ('10', '十月'), ('11', '十一月'), ('12', '十二月')]
    years = SelectField(choices=years_data)
    months = SelectField(choices=months_data)
    day = IntegerField('号', validators=[Optional(strip_whitespace=True)])
    to_day = IntegerField('号', validators=[Optional(strip_whitespace=True)])
    submit = SubmitField("物流查询")
