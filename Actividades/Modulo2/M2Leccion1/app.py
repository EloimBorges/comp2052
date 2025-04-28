# Eloim N. Borges Millete
# R00572231
# COMP 2052

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "title": "Pagina Principal",
        "message": "¡Bienvenido a nuestra app con Flask y Jinja2!",
        "tareas": ["Completar Registro", "Subir Foto de Perfil", "Verificar Correo"]
    }
    # Crea un diccionario llamado data que contiene: un título, un mensaje, una lista.
    return render_template('index.html', data=data)
    # Renderiza la plantilla index.html, enviando el diccionario data

@app.route('/about')
def about():
    data = {"title": "Sobre Nosotros", "descripcion": "Esta es una pagina de ejemplo creada para practicar con plantillas."}
    return render_template('about.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
