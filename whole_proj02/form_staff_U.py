# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    name = StringField(
        label="name",
        validators=[]
    )
    age = StringField(
        label="age",
        validators=[]
    )
    gender = StringField(
        label="gender",
        validators=[]
    )
    number = StringField(
        label="number",
        validators=[]
    )
    supply_center = StringField(
        label="supply_center",
        validators=[]

    )
    mobile_number = StringField(
        label="mobile_number",
        validators=[]
    )

    type = StringField(
        label="type",
        validators=[]
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
