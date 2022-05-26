# 专门存储表单的操作
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    RadioField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp


class RegisterForm(FlaskForm):
    name = StringField(
        label="name",
        validators=[ DataRequired(), ]
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

    submit = SubmitField(
        label="Confirm"
    )
