import os
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from .modelos import db


load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuramos la URI de la base de datos desde el archivo .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de la clave secreta para JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Vinculamos la base de datos a la app
    db.init_app(app)

    # NUEVO: Inicialización del gestor de tokens
    jwt = JWTManager(app)

    # --- Importamos y registramos el Blueprint de productos.py ---
    from .rutas.productos import productos_bp
    app.register_blueprint(productos_bp, url_prefix='/api')

    # --- Importamos y registramos el Blueprint de auth.py ---
    from .rutas.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')

    return(app)






