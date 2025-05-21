# Re hecho para proy





from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields import DecimalField, IntegerField, DateField

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario (solo accesible por Admin)
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    role = SelectField(
        'Rol',
        choices=[('Admin', 'Admin'), ('Supervisor', 'Supervisor'), ('Empleado', 'Empleado')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar un ítem del inventario
class ItemForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    precio_estimado = DecimalField('Precio estimado', validators=[DataRequired()])
    ubicacion = StringField('Ubicación')
    fecha_adquisicion = DateField('Fecha de adquisición', format='%Y-%m-%d')

    submit = SubmitField('Guardar')