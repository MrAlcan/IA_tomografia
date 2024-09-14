from flask import Flask, render_template, send_from_directory, redirect, url_for
from app.configuraciones.extensiones import db, jwt, bcrypt
from app.rutas.rutas_2 import main_bp
from datetime import datetime
from app.configuraciones.baseDatos import iniciar_datos
from app.modelos.vistas import iniciar_vistas
from datetime import timedelta


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_tomografias'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'llave_secreta_aplicacion'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies'] # posiblemente no se use
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
    #app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # Habilitar protección CSRF
    #app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Ruta para la cookie de acceso
    #app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'  # Ruta para la cookie de refresco

    # Inicialización de extensiones
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('main.ingresar'))  # Redirigir al login si el token ha expirado

    # Manejador de errores para token inválido o faltante
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return redirect(url_for('main.ingresar'))
    
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return redirect(url_for('main.ingresar'))

    # Registro de blueprints
    app.register_blueprint(main_bp)

    @app.before_request
    def print_request_time():
        print(f"Hora de solicitud: {datetime.now()}")

    return app
