from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import EqualTo, ValidationError
from pia import db
from pia.models import User


class RegisterForm(FlaskForm):
    names = StringField("Nombre")
    family_names = StringField("Apellidos")
    username = StringField('Nombre de usuario')
    email = StringField('Correo Electrónico')
    password = PasswordField('Contraseña')
    confirm_password = PasswordField('Validar contraseña', validators=[
                                     EqualTo('password', "Debe coincidir con tu contraseña")])
    submit = SubmitField("Registrarse")

    def validate_username(self, username):
        user = db.session.query(User).filter_by(Usuario=username.data).first()
        if user:
            raise ValidationError("Este usuario ya está registrado")

    def validate_email(self, email):
        user = db.session.query(User).filter_by(vCorreo=email.data).first()
        if user:
            raise ValidationError("Este correo electrónico ya está registrado")


class LoginForm(FlaskForm):
    username = StringField('Usuario')
    password = PasswordField('Contraseña')
    submit = SubmitField("Iniciar Sesión")


class BuyForm(FlaskForm):
    card_name = StringField("Nombre de la tarjeta")
    card_number = StringField("Número de la tarjeta")
    expiration_date = StringField("Fecha de expiración")
    cvv = PasswordField("CVV")
    submit = SubmitField("Reservar")