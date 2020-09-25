from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, IntegerField, SubmitField
)
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField, DateField


class NewPortfolioForm(FlaskForm):
    name = StringField(
        label='Nombres(s)',
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    last_name1 = StringField(
        label='Apellido paterno',
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    last_name2 = StringField(
        label='Apellido materno',
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    email = EmailField(
        label='Correo electrónico',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            Email(message='Introduce un correo electrónico válido')
        ]
    )
    portfolio_type = SelectField(
        label='Tipo de portafolio',
        choices=[
            ('classic', 'Clásico'),
            ('flexible', 'Flexible'),
            ('starter', 'Starter'),
        ],
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    pay_method = SelectField(
        label='Modalidad de pago',
        choices=[('dynamic', 'Dinámico'), ('standard', 'Estándar')],
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    currency = SelectField(
        choices=['MXN', 'USD'],
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    amount = IntegerField(
        label='Cantidad a invertir',
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    folio = StringField(
        label='Folio'
    )
    start_date = DateField(
        label='Fecha de inicio',
        validators=[DataRequired(message='Este campo es obligatorio')]
    )
    end_date = DateField(
        label='Fecha final',
        validators=[DataRequired(message='Este campo es obligatorio')]
    )