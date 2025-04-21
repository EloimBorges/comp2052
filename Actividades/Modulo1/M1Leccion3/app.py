# Eloim N. Borges Millete
# R00572231
# COMP 2052

from flask import Flask, request, jsonify
import json
import os #Permite a python interactuar con comandos del Sistema Operativo

app = Flask(__name__)

# Lista en memoria (Queda vacia cada vez se ejecuta el programa)
usuarios = []

# Función para cargar los datos desde el archivo JSON
def cargar_datos():
    if os.path.exists('datos.json'):
        with open('datos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"usuarios": [], "productos": []}

# Almacenamiento en memoria de los usuarios y productos
data = cargar_datos()
usuarios = data["usuarios"]
productos = data["productos"]

# Ruta GET /
@app.route("/", methods=["GET"])
def home():
    return "Bienvenido a la practica de manipulacion de datos en formato json"

# Ruta GET /info
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "sistema": "Capstone: Gestión de Usuarios y Productos",
        "version": "0.5 Gamma",
        "Descripcion": "Aplicar los conceptos aprendidos sobre la manipulación de datos"
    })

# Ruta POST /crear_usuario
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    data = request.json
    nombre = data.get("nombre")
    correo = data.get("correo")

    if not nombre or not correo:
        return jsonify({"error": "Faltan datos obligatorios, verificar nombre o correo"}), 400

    # Crear nuevo usuario y ID
    nuevo_id = max([u["id"] for u in usuarios], default=0) + 1
    usuario = {
        "id": nuevo_id,
        "nombre": nombre,
        "correo": correo,
        "roles": ["cliente"]
    }
    usuarios.append(usuario)

    return jsonify({"usuario": usuario, "mensaje": "Usuario creado exitosamente"})


# Ruta GET /usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(debug=True)
