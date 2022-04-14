from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BusForm(FlaskForm):
    number = StringField('Номер автобуса', validators=[DataRequired()])
    brand = StringField('Марка автобуса', validators=[DataRequired()])
    last_maintenance = DateField('Последнее ТО', validators=[DataRequired()])
    next_maintenance = DateField('Следующее ТО', validators=[DataRequired()])
    seats_number = IntegerField('Количество посадочных мест', validators=[DataRequired()])
    about = TextAreaField('Комментарий')

    submit = SubmitField('Создать автобус')
