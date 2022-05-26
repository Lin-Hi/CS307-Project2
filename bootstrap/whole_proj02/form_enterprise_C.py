# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    name = StringField(
        label="name",
        validators=[DataRequired(), ]
    )
    country = StringField(
        label="country",
        validators=[ ]
    )
    city = StringField(
        label="city",
        validators=[ ]
    )
    supply_center  = StringField(
        label="supply_center",
        validators=[ ]
    )
    industry = StringField(
        label="industry",
        validators=[ ]
    )

    submit = SubmitField(
        label="Confirm"
    )
