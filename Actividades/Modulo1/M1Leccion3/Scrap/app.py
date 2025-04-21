# Eloim N. Borges Millete
# R00572231
# COMP 2052





# Quize utilizar archivos csv con los cuales estoy mas familiarizado, 
# pero no me atendi corractamente a la segunda parte de la actividad.
# Lado positivo si funciona



from flask import Flask, request, jsonify
import csv #Modulo de interaccion csv
import os #Permite a python interactuar con comandos del Sistema Operativo

app = Flask(__name__)

# Lista en memoria para almacenar usuarios temporalmente
usuarios_en_memoria = []

# Función para cargar usuarios desde un archivo CSV
def cargar_usuarios():
    usuarios = []
    if os.path.exists('usuarios.csv'): #Utilizar file existente de esta disponible
        with open('usuarios.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['id'] = int(row['id'])
                row['roles'] = row['roles'].split(';')  # Convertir string a lista
                usuarios.append(row)
    return usuarios

# Función para guardar un nuevo usuario en el archivo CSV
def guardar_usuario(usuario):
    file_exists = os.path.isfile('usuarios.csv')
    with open('usuarios.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'nombre', 'correo', 'roles']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        usuario['roles'] = ';'.join(usuario['roles'])  # convertir lista a string
        writer.writerow(usuario)

# Ruta GET /info
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "sistema": "Capstone: Gestión de Usuarios y Productos",
        "version": "0.3 Beta",
        "Descripcion": "Aplicar los conceptos aprendidos sobre la manipulación de datos"
    })

# Ruta GET /usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    # Cargar usuarios desde el CSV + agregar los que están en memoria
    usuarios = cargar_usuarios() + usuarios_en_memoria
    return jsonify(usuarios)

# Ruta POST /crear_usuario
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    data = request.json
    nombre = data.get("nombre")
    correo = data.get("correo")

    if not nombre or not correo:
        return jsonify({"error": "Faltan datos obligatorios, verificar nombre o correo"}), 400

    usuarios = cargar_usuarios()
    nuevo_id = max([u['id'] for u in usuarios], default=0) + 1
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": nombre,
        "correo": correo,
        "roles": ["cliente"]
    }

    usuarios_en_memoria.append(nuevo_usuario)

    return jsonify({"mensaje": "Usuario creado temporalmente", "usuario": nuevo_usuario})

if __name__ == "__main__":
    app.run(debug=True)
