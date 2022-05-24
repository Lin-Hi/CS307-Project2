# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    # StringField <input type='text' name='name' required>
    # PasswordField <input type='password' name='password' required>
    name = StringField(
        label="name",
        validators=[DataRequired(), ]
    )
    country = StringField(
        label="country",
        validators=[DataRequired(), ]
    )
    city = StringField(
        label="city",
        validators=[ ]
    )
    supply_center  = StringField(
        label="supply_center",
        validators=[DataRequired(), ]
    )
    industry = StringField(
        label="industry",
        validators=[DataRequired(), ]
    )

    submit = SubmitField(
        label="发送"
    )
