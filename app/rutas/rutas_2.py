from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request
from flask import Blueprint, render_template, request, redirect, url_for
from functools import wraps
from datetime import datetime
from app.servicios.serviciosAutenticacion import ServiciosAutenticacion
from app.servicios.serviciosVistas import ServiciosVistas
from app.servicios.serviciosRol import ServiciosRol
from app.servicios.serviciosUsuario import ServiciosUsuario
from app.servicios.serviciosPaciente import ServiciosPaciente
import numpy as np
import cv2

from flask import request, jsonify
import jwt

def token_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cookie_cabecera = request.headers['Cookie'].split('; ')
        print(cookie_cabecera)
        ac_co_tok = cookie_cabecera[0].split('=')
        csrf_tok = cookie_cabecera[1].split('=')
        cuerpo_token = {
            f'{ac_co_tok[0]}': f'{ac_co_tok[1]}',
            f'{csrf_tok[0]}': f'{csrf_tok[1]}'
        }
        #token = request.headers.get('Authorization').split()[1]  # Bearer <token>
        print(cuerpo_token['access_token_cookie'])
        
        try:
            data = jwt.decode(cuerpo_token['access_token_cookie'], 'llave_secreta_aplicacion', algorithms=['HS256'])
            print(data['sub'])
            user_id = data['sub']['id_usuario']
            datos_usuario = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(datos_usuario, *args, **kwargs)
    
    return wrapper



main_bp = Blueprint('main', __name__)


@main_bp.route('/ingresar', methods=['GET'])
def ingresar():
    current_time = datetime.now()
    return render_template('ingresar.html', current_time=current_time)

@main_bp.route('/ingresar', methods=['POST'])
def validar_usuario():
    print("ingreso al backend")
    datos_login = request.get_json()
    print(datos_login)
    #respuesta, refresh_token, id_rol = ServiciosAutenticacion.autenticar(datos_login['nombre_usuario'], datos_login['contrasena'])
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
        resp = make_response(redirect(url_for('main.vista_inicio')))
        set_access_cookies(resp, respuesta)
        #set_refresh_cookies(resp, refresh_token)
        #set_access_cookies(respuesta)
        #print(resp)
        cuerpo = {'codigo': 200,
                  'token': respuesta}
        return resp
        #return resp

@main_bp.route('/inicio', methods=['POST', 'GET'])
@jwt_required()
def vista_inicio():
    identidad = get_jwt_identity()
    print(identidad)
    current_time = datetime.now()
    return render_template('inicio.html', current_time=current_time, identidad=identidad)

@main_bp.route('/usuarios', methods=['POST', 'GET'])
@jwt_required()
def usuarios():
    identidad = get_jwt_identity()
    print(identidad)
    usuarios = ServiciosVistas.obtener_usuarios_roles()
    if request.method == 'POST':
        #no hay post
        print("helloda")
    return render_template('usuarios.html', identidad=identidad, usuarios=usuarios)

@main_bp.route('/usuarios/agregar', methods=['GET'])
@jwt_required()
def agregar_usuarios():
    identidad = get_jwt_identity()
    #identidad = ''
    print(identidad)
    roles = ServiciosRol.obtener_todos()
    if(request.method == 'POST'):
        #datos = request.get_data()
        print("helloda")
        None
    return render_template('crear_usuario.html', identidad=identidad, roles=roles)


@main_bp.route('/usuarios/agregar', methods=['POST'])
#@jwt_required()
@token_requerido # para cualquier post o put
def agregar_usuarios_post(datos_usuario):

    print("helloda")
    datos = request.form
    print(datos)
    nuevo_usuario = ServiciosUsuario.crear(nombre=datos['input_nombre_cuenta'], nombre_per=datos['input_nombres'],contrasena=datos['input_contrasena'],ap_paterno=datos['input_apellido_paterno'],ap_materno=datos['input_apellido_materno'],cargo=datos['input_cargo'],carnet=datos['input_carnet'],id_rol=datos['input_rol'])
    
    identidad = datos_usuario
    print(identidad)
    
        #datos = request.get_data()
    print("helloda")
    if nuevo_usuario:
        cuerpo = {  'codigo': 200,
                    'identidad': identidad,
                    'nuevo_usuario': nuevo_usuario}
        return redirect(url_for('main.usuarios'))
    else:
        cuerpo = {  'codigo': 400,
                    'identidad': identidad,
                    'nuevo_usuario': None}
        return cuerpo
    #return jsonify(cuerpo)
    #return "ff"


@main_bp.route('/usuarios/editar/<id>', methods=['GET'])
@jwt_required()
def editar_usuarios(id):
    identidad = get_jwt_identity()
    usuario_editar = ServiciosUsuario.obtener_id(id)
    print(usuario_editar)
    roles = ServiciosRol.obtener_todos()
    
    if usuario_editar:
        cuerpo = {'codigo': 200,
              'identidad': identidad,
              'usuario_editar': usuario_editar}
    else:
        cuerpo = {'codigo': 200,
              'identidad': identidad,
              'usuario_editar': usuario_editar}
    return render_template('editar_usuario.html', identidad=identidad, usuario_editar=usuario_editar, roles=roles)

@main_bp.route('/usuarios/editar/<id>', methods=['POST'])
@token_requerido
def editar_usuarios_post(datos_usuario, id):
    identidad = datos_usuario
    print(identidad)
    datos = request.form
    print(datos)
    usuario_modificado = ServiciosUsuario.actualizar(id=id, nombre=datos['input_nombre_cuenta'], nombre_per=datos['input_nombres'],ap_paterno=datos['input_apellido_paterno'],ap_materno=datos['input_apellido_materno'],cargo=datos['input_cargo'],carnet=datos['input_carnet'],id_rol=datos['input_rol'])
    if usuario_modificado:
        return redirect(url_for('main.usuarios'))
    else:
        print('hubo un error')
        return jsonify({'codigo': 400}) # mejorar


@main_bp.route('/pacientes', methods=['GET'])
@jwt_required()
def pacientes():
    identidad = get_jwt_identity()
    pacientes = ServiciosPaciente.obtener_todos()
    print(pacientes)
    cuerpo = {'codigo': 200,
              'identidad': identidad,
              'pacientes': pacientes}
    return render_template('pacientes.html', identidad=identidad, pacientes=pacientes)

@main_bp.route('/pacientes/agregar', methods=['GET'])
@jwt_required()
def agregar_pacientes():
    identidad = get_jwt_identity()
    return render_template('/crear_paciente.html', identidad=identidad)

@main_bp.route('/pacientes/agregar', methods=['POST'])
@token_requerido
def agregar_pacientes_post(datos_usuario):
    identidad = datos_usuario
    datos = request.form
    nuevo_paciente = ServiciosPaciente.crear(nombres=datos['input_nombres'], apellido_paterno=datos['input_apellido_paterno'], apellido_materno=datos['input_apellido_materno'], carnet=datos['input_carnet'], seguro=datos['input_seguro'], fecha_nacimiento=datos['input_fecha_nacimiento'], edad=datos['input_edad'])
    if nuevo_paciente:
        return redirect(url_for('main.pacientes'))
    else:
        return jsonify({'codigo': 400})

@main_bp.route('/pacientes/editar/<id>', methods=['GET'])
@jwt_required()
def editar_pacientes(id):
    identidad = get_jwt_identity()
    paciente_editar = ServiciosPaciente.obtener_id(id)
    print(paciente_editar)
    return render_template('editar_paciente.html', identidad=identidad, paciente_editar=paciente_editar)

@main_bp.route('/pacientes/editar/<id>', methods=['POST'])
@token_requerido
def editar_paciente_post(datos_usuario, id):
    identidad = datos_usuario
    datos = request.form
    paciente_modificado = ServiciosPaciente.actualizar(id=id, nombres=datos['input_nombres'], apellido_paterno=datos['input_apellido_paterno'], apellido_materno=datos['input_apellido_materno'], carnet=datos['input_carnet'], seguro=datos['input_seguro'], fecha_nacimiento=datos['input_fecha_nacimiento'], edad=datos['input_edad'])
    if paciente_modificado:
        return redirect(url_for('main.pacientes'))
    else:
        return jsonify({'codigo': 400})