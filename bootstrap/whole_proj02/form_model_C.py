# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    number = StringField(
        label="number",
        validators=[ ]
    )
    model = StringField(
        label="model",
        validators=[DataRequired(), ]
    )
    name = StringField(
        label="name",
        validators=[]
    )
    unit_price = StringField(
        label="unit_price",
        validators=[ ]

    )
    submit = SubmitField(
        label="Confirm"
    )
