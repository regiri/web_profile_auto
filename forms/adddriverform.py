from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField
from wtforms.validators import DataRequired
import phonenumbers


class DriverForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    lastname = StringField('Отчество', validators=[DataRequired()])
    phone_number = TelField('Номер телефона', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')

    def validate_phone(self):
        try:
            phone = phonenumbers.parse(self.phone_number.data)
            if not phonenumbers.is_valid_number(phone):
                return False
            return True
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
