from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

from src.adapter.constants.constants import ADDRESS_MAX_LENGTH, ADDRESS_MIN_LENGTH, NAME_MAX_LENGTH, NAME_MIN_LENGTH


class BaseOrderForm(FlaskForm):
    name = StringField(
        "Name:",
        validators=[
            validators.DataRequired(),
            validators.InputRequired(),
            validators.Length(min=NAME_MIN_LENGTH, max=NAME_MAX_LENGTH),
        ])
    address = StringField(
        "Address:",
        validators=[
            validators.DataRequired(),
            validators.InputRequired(),
            validators.Length(min=ADDRESS_MIN_LENGTH, max=ADDRESS_MAX_LENGTH),
        ])


# TODO combine it
class OrderForm(BaseOrderForm):
    submit = SubmitField("Submit order")
