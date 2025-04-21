from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta GET /
@app.route("/", methods=["GET"])
def home():
    return "Bienvenido al inicio de mi API Capstone"

# Ruta GET /info
@app.route("/info", methods=["GET"])
def info():
    return {
        "nombre_app": "API Capstone M1 L2",
        "version": "0.1 Beta",
        "descripcion": "Esta API maneja mensajes enviados desde un cliente como rest o postman"
    }

# Ruta POST /mensaje
@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json
    mensaje_usuario = data.get("mensaje", "Mensaje vacío")
    return {
        "respuesta": f"Hola, recibimos tu mensaje: '{mensaje_usuario}' Envio EXITOSO!"
    }

if __name__ == "__main__":
    app.run(debug=True)
