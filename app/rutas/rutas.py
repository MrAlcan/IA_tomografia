from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, render_template
from datetime import datetime

from app.servicios.serviciosAutenticacion import ServiciosAutenticacion
from app.servicios.serviciosVistas import ServiciosVistas

main_bp = Blueprint('main', __name__)

#-----------------VISTAS----------------------------------------
@main_bp.route('/ingresar', methods=['GET'])
def vista_iniciar_sesion():
    current_time = datetime.now()
    return render_template('ingresar.html', current_time=current_time)

@main_bp.route('/inicio', methods=['GET'])
def vista_inicio():
    current_time = datetime.now()
    return render_template('inicio.html', current_time=current_time)

@main_bp.route('/usuarios', methods=['GET'])
def vista_usuarios():
    current_time = datetime.now()
    return render_template('usuarios.html', current_time=current_time)

#-------------API--------------------------------------------

'''
@main_bp.route('/ingresar', methods=['GET'])
def iniciar_sesion():
    current_time = datetime.now()
    return render_template('ingresar.html', current_time=current_time)
'''

@main_bp.route('/ingresar', methods=['POST'])
def validar_usuario():
    print("ingreso al backend")
    datos_login = request.get_json()
    print(datos_login)
    respuesta, id_rol = ServiciosAutenticacion.autenticar(datos_login['nombre_usuario'], datos_login['contrasena'])
    print(respuesta)
    if respuesta==404:
        cuerpo = {'codigo': 404,
                  'respuesta': 'Usuario no encontrado'}
        return jsonify(cuerpo)
    elif respuesta==401:
        cuerpo = {'codigo': 401,
                  'respuesta': 'Contraseña incorrecta'}
        return jsonify(cuerpo)
    else:
        cuerpo = {'codigo': 200,
                  'token': respuesta,
                  'rol': id_rol}
        print(respuesta)
        return jsonify(cuerpo)
'''
@main_bp.route('/inicio', methods=['GET'])
@jwt_required
def inicio():
    datos_usuario = get_jwt_identity()
    print(datos_usuario)
    current_time = datetime.now()
    return render_template('inicio.html', current_time=current_time)
'''

@main_bp.route('/api/inicio', methods=['GET'])
@jwt_required()
def inicio():
    print("entro al api")
    datos_usuario = get_jwt_identity()
    print(datos_usuario)
    cuerpo = {'codigo':200,
              'identidad': datos_usuario}
    return jsonify(cuerpo)

@main_bp.route('/api/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    identidad = get_jwt_identity()
    usuarios = ServiciosVistas.obtener_usuarios_roles()
    cuerpo = {  'codigo': 200,
                'identidad': identidad,
                'usuarios': usuarios}
    return jsonify(cuerpo)

@main_bp.route('/register', methods=['POST'])
def register():
    return jsonify({"msg": "User created successfully"}), 201


@main_bp.route('/')
def index():
    current_time = datetime.now()
    return render_template('inicio.html', current_time=current_time)

'''
@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401

@main_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
'''