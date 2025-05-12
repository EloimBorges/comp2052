# Eloim N. Borges Millete
# R00572231
# COMP 2052

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

app.config["SECRET_KEY"] = "mi_clave_secreta"

class RegisterForm(FlaskForm):
    nombre = StringField("Nombre", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="Debe tener al menos 3 caracteres.")
    ])
    
    correo = StringField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debe ingresar un correo con el formato apropiado con su @ y .com.")
    ])
    
    contraseña = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="Debe tener al menos 6 caracteres.")
    ])
    
    submit = SubmitField("Registrarse")

@app.route("/", methods=["GET"])
def index():
    return register() # Llamar a la función register() en la dirección http://127.0.0.1:5000

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        message = f"Usuario registrado Exitosamente: {form.nombre.data}"
        return render_template("home.html", message=message)
    return render_template("index.html.jinja2", form=form)

if __name__ == "__main__":
    app.run(debug=True)
