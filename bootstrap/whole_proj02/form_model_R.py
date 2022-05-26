# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    number = SelectField(
        label="number",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    model = SelectField(
        label="model",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )

    name = SelectField(
        label="name",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    unit_price = SelectField(
        label="unit price",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
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
