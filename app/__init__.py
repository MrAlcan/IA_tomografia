from flask import Flask
from app.configuraciones.extensiones import db, jwt, bcrypt
from app.rutas.rutas import main_bp

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_tomografias'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'llave_secreta_aplicacion'

    # Inicialización de extensiones
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Registro de blueprints
    app.register_blueprint(main_bp)

    return app
