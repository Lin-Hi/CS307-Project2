# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    name = SelectField(
        label="name",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    country = SelectField(
        label="country",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    city = SelectField(
        label="city",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    supply_center = SelectField(
        label="supply_center",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    industry = SelectField(
        label="industry",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )

    constraint = SelectField(
        label="constraint",
        coerce=int,
        choices=[(1, "Yes"), (2, "No")]
    )
    name_filter = StringField(
        label="name filter",
        validators=[]
    )
    country_filter = StringField(
        label="country filter",
        validators=[ ]
    )
    city_filter = StringField(
        label="city filter",
        validators=[ ]
    )
    supply_center_filter  = StringField(
        label="supply_center filter",
        validators=[ ]
    )
    industry_filter = StringField(
        label="industry filter",
        validators=[ ]
    )
    submit = SubmitField(
        label="发送"
    )
