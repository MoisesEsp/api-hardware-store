from flask import Blueprint, blueprints, request, jsonify
from sqlalchemy import Identity
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.modelos import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()

    if not datos or not 'username' in datos or not 'password' in datos:
        return jsonify({"error": "Faltan credenciales (username, password)"}), 400
    
    # Buscamos al usuario en la base de datos
    usuario = Usuario.query.filter_by(username=datos['username']). first()

    # Comparamos la contraseña en texto plano con el hash almacenado
    if usuario and check_password_hash(usuario.password_hash, datos['password']):
        # Generamos el token asignando el ID del usuario como identidad
        token= create_access_token(identity=str(usuario.id))
        return jsonify({"token": token}), 200
    else:
        return jsonify({"mensaje": "Credenciales invalidas"}),401