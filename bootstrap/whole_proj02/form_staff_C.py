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
    age = StringField(
        label="age",
        validators=[DataRequired(), ]
    )
    gender = StringField(
        label="gender",
        validators=[]
    )
    number = StringField(
        label="number",
        validators=[DataRequired(), ]
    )
    supply_center = StringField(
        label="supply_center",
        validators=[DataRequired(), ]

    )
    mobile_number = StringField(
        label="mobile_number",
        validators=[DataRequired(), ]
    )

    type = StringField(
        label="type",
        validators=[DataRequired(), ]
    )

    submit = SubmitField(
        label="Confirm"
    )
