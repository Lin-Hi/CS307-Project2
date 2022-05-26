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
    age = SelectField(
        label="age",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    gender = SelectField(
        label="gender",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    number = SelectField(
        label="number",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    supply_center = SelectField(
        label="supply center",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )

    mobile_number = SelectField(
        label="mobile number",
        coerce=int,
        choices=[(1, "Selected"), (2, "Not Selected")]
    )
    type = SelectField(
        label="type",
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
    age_filter = StringField(
        label="age filter",
        validators=[]
    )
    gender_filter = StringField(
        label="gender filter",
        validators=[]
    )
    number_filter = StringField(
        label="number filter",
        validators=[]
    )
    supply_center_filter = StringField(
        label="supply center filter",
        validators=[]
    )
    mobile_number_filter = StringField(
        label="mobile number filter",
        validators=[]
    )
    type_filter = StringField(
        label="type filter",
        validators=[]
    )
    submit = SubmitField(
        label="Confirm"
    )
