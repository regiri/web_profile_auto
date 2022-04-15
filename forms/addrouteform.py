from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TimeField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from data import db_session
from data.buses import Bus
from data.drivers import Driver


def bus_choices():
    db_sess = db_session.create_session()
    return db_sess.query(Bus).all()


def driver_choices():
    db_sess = db_session.create_session()
    return db_sess.query(Driver).all()


class RouteForm(FlaskForm):
    route_name = StringField('Название маршрута', validators=[DataRequired()])
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])
    start_time = TimeField('Время начала', validators=[DataRequired()])
    end_time = TimeField('Время окончания', validators=[DataRequired()])
    start_point = StringField('Место старта', validators=[DataRequired()])
    end_point = StringField('Место финиша', validators=[DataRequired()])
    driver = QuerySelectField('Водитель', validators=[DataRequired()], query_factory=driver_choices)
    bus = QuerySelectField('Автобус', validators=[DataRequired()], query_factory=bus_choices)

    submit = SubmitField('Подтвердить')

