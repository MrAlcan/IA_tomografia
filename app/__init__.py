from flask import Flask
from app.configuraciones.extensiones import db, jwt, bcrypt
from app.rutas.rutas import main_bp

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

    # Inicialización de extensiones
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Registro de blueprints
    app.register_blueprint(main_bp)

    return app
