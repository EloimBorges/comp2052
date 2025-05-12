# Eloim N. Borges Millete
# R00572231
# COMP 2052

from flask import Flask, request, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configurar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configurar Flask-Principal
Principal(app)

# Permisos por rol
admin_permission = Permission(RoleNeed("admin"))
dueno_permission = Permission(RoleNeed("dueño"))
supervisor_permission = Permission(RoleNeed("supervisor"))
empleado_permission = Permission(RoleNeed("empleado"))

# Permiso compuesto: solo roles válidos
inventario_roles = ["admin", "dueño", "supervisor", "empleado"]
inventario_permission = Permission(*[RoleNeed(r) for r in inventario_roles])


# Clase de usuario con rol
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Usuarios personalizados con roles
users = {
    "pos": User(1, "pos", "admin"),
    "fernando": User(2, "fernando", "dueño"),
    "odalys": User(3, "odalys", "supervisor"),
    "kay": User(4, "kay", "empleado")
}

# Cargar usuario desde ID
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

# Conectar identidad con rol
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, "role"):
        identity.provides.add(RoleNeed(current_user.role))

# Ruta de login
@app.route("/login/<username>")
def login(username):
    user = users.get(username)
    if user:
        login_user(user)
        identity_changed.send(app, identity=Identity(user.id))
        return f"Bienvenido {user.username}, rol: {user.role}"
    return "Usuario no encontrado", 404

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Sesión cerrada"

# Ruta comun
@app.route("/inventario")
@login_required
@inventario_permission.require(http_exception=403)
def ver_inventario():
    return f"{current_user.username} accedió al inventario."


# Rutas protegidas por rol
@app.route("/db_settings")
@login_required
@admin_permission.require(http_exception=403)
def admin_panel():
    return f"Panel de configuracion de la Base de Datos: Hola {current_user.username}"

@app.route("/empleados")
@login_required
@dueno_permission.require(http_exception=403)
def dueno_panel():
    return f"Panel de empleados: Hola {current_user.username}"

@app.route("/modificar_inventario")
@login_required
@supervisor_permission.require(http_exception=403)
def supervisor_panel():
    return f"Modificar inventario: Hola {current_user.username}"

@app.route("/caja_registradora")
@login_required
@empleado_permission.require(http_exception=403)
def empleado_panel():
    return f"Caja Registradora: Bienvenido {current_user.username}"

@app.errorhandler(403)
def acceso_denegado(e):
    return "Acceso denegado: no tienes permisos correctos para esta sección.", 403


if __name__ == "__main__":
    app.run(debug=True)
