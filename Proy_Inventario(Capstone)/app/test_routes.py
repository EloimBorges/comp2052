from flask import Blueprint, request, jsonify
from app.models import db, Item
from datetime import datetime

# Blueprint exclusivo para pruebas vía REST
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    return '<h1>API de Inventario Personal - Modo Prueba</h1>'


@main.route('/items', methods=['GET'])
def listar_items():
    items = Item.query.all()
    data = [
        {
            'id': item.id,
            'nombre': item.nombre,
            'categoria': item.categoria,
            'cantidad': item.cantidad,
            'precio_estimado': float(item.precio_estimado),
            'ubicacion': item.ubicacion,
            'fecha_adquisicion': item.fecha_adquisicion.isoformat() if item.fecha_adquisicion else None,
            'owner_id': item.owner_id
        }
        for item in items
    ]
    return jsonify(data), 200


@main.route('/items/<int:id>', methods=['GET'])
def obtener_item(id):
    item = Item.query.get_or_404(id)
    data = {
        'id': item.id,
        'nombre': item.nombre,
        'categoria': item.categoria,
        'cantidad': item.cantidad,
        'precio_estimado': float(item.precio_estimado),
        'ubicacion': item.ubicacion,
        'fecha_adquisicion': item.fecha_adquisicion.isoformat() if item.fecha_adquisicion else None,
        'owner_id': item.owner_id
    }
    return jsonify(data), 200


@main.route('/items', methods=['POST'])
def crear_item():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        fecha = datetime.strptime(data.get('fecha_adquisicion'), "%Y-%m-%d").date() if data.get('fecha_adquisicion') else None
    except ValueError:
        return jsonify({'error': 'Fecha de adquisición inválida. Use formato YYYY-MM-DD.'}), 400

    item = Item(
        nombre=data.get('nombre'),
        categoria=data.get('categoria'),
        cantidad=data.get('cantidad'),
        precio_estimado=data.get('precio_estimado'),
        ubicacion=data.get('ubicacion'),
        fecha_adquisicion=fecha,
        owner_id=data.get('owner_id')
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({'message': 'Ítem creado', 'id': item.id}), 201


@main.route('/items/<int:id>', methods=['PUT'])
def actualizar_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()

    if 'fecha_adquisicion' in data and data['fecha_adquisicion']:
        try:
            data['fecha_adquisicion'] = datetime.strptime(data['fecha_adquisicion'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Fecha de adquisición inválida. Use formato YYYY-MM-DD.'}), 400

    item.nombre = data.get('nombre', item.nombre)
    item.categoria = data.get('categoria', item.categoria)
    item.cantidad = data.get('cantidad', item.cantidad)
    item.precio_estimado = data.get('precio_estimado', item.precio_estimado)
    item.ubicacion = data.get('ubicacion', item.ubicacion)
    item.fecha_adquisicion = data.get('fecha_adquisicion', item.fecha_adquisicion)
    item.owner_id = data.get('owner_id', item.owner_id)

    db.session.commit()
    return jsonify({'message': 'Ítem actualizado'}), 200


@main.route('/items/<int:id>', methods=['DELETE'])
def eliminar_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Ítem eliminado'}), 200