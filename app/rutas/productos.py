from flask import Blueprint, jsonify, request
from app.modelos import db,Categoria, Producto
from flask_jwt_extended import jwt_required

# Inicializamos el Blueprint
productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])


def obtener_productos():
    # 1. Consultamos TODOS los productos de la base de datos usando el ORM
    # Esto equivale a "SELECT * FROM productos"
    productos_db = Producto.query.all()

    # 2. Serializamos: Convertimos los objetos de Python a diccionarios (JSON)
    lista_productos = []
    for p in productos_db:
        lista_productos.append({
            "id": p.id,
            "nombre": p.nombre,
            "especificaciones": p.especificaciones,
            "precio": p.precio,
            "stock": p.stock,
            # ¡Magia relacional! SQLAlchemy busca automáticamente la categoría asociada
            "categoria": p.categoria.nombre 
        })
    # 3. Respondemos con el JSON y un código HTTP 200 (OK)
    return jsonify(lista_productos), 200

# --- RUTA POST: Añadir nuevo producto ---
@productos_bp.route('/productos', methods=['POST'])
@jwt_required()
def crear_producto():
    # 1. Extraemos el JSON que envía el cliente
    datos = request.get_json()

    # 2. Validación básica de seguridad (evitar que la app colapse si faltan datos)
    if not datos or not 'nombre' in datos or not 'precio' in datos or not 'categoria_id' in datos:
        return jsonify({"error": "Faltan datos obligatorios (nombre, precio, categoria_id)"}), 400
    
    # 3. Verificamos que la categoría indicada realmente exista en la base de datos
    categoria_exste =  Categoria.query.get(datos['categoria_id'])
    if not categoria_exste:
        return jsonify({"error": "El id de categoria proporcionado no existe."}),404

    # 4. Construimos el objeto Producto
    nuevo_producto = Producto(
        nombre = datos['nombre'],
        especificaciones = datos.get('especificaciones', ''), # .get() evita error si no viene este campo
        precio=datos['precio'],
        stock = datos.get('stock', 0),
        categoria_id = datos['categoria_id']

    )

    # 5. Lo preparamos y lo guardamos
    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify({"mensaje": "producto agregado exitosamente", "id_producto": nuevo_producto.id}), 201




# --- RUTA PUT: Actualizar precio o stock ---
@productos_bp.route('/productos/<int:id>', methods=['PUT'])
@jwt_required()
def actuyalizar_producto(id):
    # 1. Buscamos el producto por su ID
    producto = Producto.query.get(id)

    # Si no existe, devolvemos error 404
    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404
    
    datos = request.get_json()

    # 2. Actualizamos solo los campos que vengan en la petición
    if 'precio' in datos:
        producto.precio = datos['precio']
    if 'stock' in datos:
        producto.stock = datos['stock']
    
    # 3. Guardamos los cambios
    db.session.commit()

    return jsonify({"mensaje":"Dato de producto actualizado correctamente"}), 200


# --- RUTA DELETE: Eliminar un producto ---
@productos_bp.route('/productos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_producto(id):
    # 1. Buscamos el producto por su ID
    producto = Producto.query.get(id)

    # Si no existe, devolvemos error 404
    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404
    
   # Eliminamos el objeto de la sesión
    db.session.delete(producto)
    # 3. Guardamos los cambios
    db.session.commit()

    return jsonify({"mensaje":"E producto a sido eliminado correctamente"}), 200

