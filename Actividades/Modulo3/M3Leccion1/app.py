from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulación de base de datos
usuarios_raw = {
    'admin': {
        'password': 'supersecretopoderoso',
        'role': 'admin'
    },
    'cliente': {
        'password': 'supersecretonormal',
        'role': 'cliente'
    }
}

# Transformar contraseñas en hashes
usuarios = {}
for user, data in usuarios_raw.items():
    usuarios[user] = {
        'password': generate_password_hash(data['password']),
        'role': data['role']
    }

# Clase de Usuario
class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = usuarios[username]['role']

# Loader de sesión
@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

# Decorador para rutas exclusivas de admin
def solo_admin(funcion):
    def decorador(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return funcion(*args, **kwargs)
    decorador.__name__ = funcion.__name__
    return decorador

# Ruta principal protegida
@app.route('/')
@login_required
def home():
    return render_template('home.html.jinja2', nombre=current_user.id, rol=current_user.role)

# Ruta solo para administradores
@app.route('/admin')
@login_required
@solo_admin
def admin_panel():
    return f"<h2>Zona Administrativa</h2><p>Bienvenido, {current_user.id}</p>"

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and check_password_hash(usuarios[username]['password'], password):
            user = Usuario(username)
            login_user(user)
            return redirect(url_for('home'))

        return render_template("error.html.jinja2", error_code=401, 
                               error_message="Credenciales inválidas")

    return render_template('login.html.jinja2')

# Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)