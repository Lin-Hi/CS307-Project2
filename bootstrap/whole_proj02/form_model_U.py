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
        validators=[ ]
    )
    name = StringField(
        label="name",
        validators=[]
    )
    unit_price = StringField(
        label="unit_price",
        validators=[ ]

    )
    constraint = SelectField(
        label="constraint",
        coerce=int,
        choices=[(1, "Yes"), (2, "No")]
    )
    number_filter = StringField(
        label="number filter",
        validators=[ ]
    )
    model_filter = StringField(
        label="model filter",
        validators=[ ]
    )
    name_filter = StringField(
        label="name filter",
        validators=[]
    )
    unit_price_filter  = StringField(
        label="unit price filter",
        validators=[ ]
    )
    submit = SubmitField(
        label="Confirm"
    )
