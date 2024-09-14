from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from app.servicios.serviciosAutenticacion import ServiciosAutenticacion
from app.servicios.serviciosVistas import ServiciosVistas
from app.servicios.serviciosRol import ServiciosRol
from app.servicios.serviciosUsuario import ServiciosUsuario
import numpy as np
import cv2
main_bp = Blueprint('main', __name__)
import os
from PIL import Image

from io import BytesIO



ruta_modelo_relativa = os.path.join('app', 'ia', 'deteccion_tumor.keras')
ruta_modelo = os.path.abspath(ruta_modelo_relativa)

print(f"ruta del modelo: {ruta_modelo}")
'''
try:
    modelo = load_model(ruta_modelo)
    print("modelo cargado con éxito.")
except Exception as e:
    print(f"error al cargar el modelo: {e}")




@main_bp.route('/tomografia_resultados', methods=['GET', 'POST'])
def vista_tomografia_resultados():
    current_time = datetime.now()
    resultados = []

    if request.method == 'POST':
        if 'fileInput' not in request.files:
            return redirect(url_for('main.vista_tomografia_resultados'))

        files = request.files.getlist('fileInput')

        for file in files:
            if file.filename == '':
                resultados.append("Nombre de archivo vacío")
                continue

            try:
                # Leer la imagen desde el archivo usando PIL
                img = Image.open(BytesIO(file.read()))
                img = img.resize((150, 150))  # Redimensionar la imagen
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array /= 255.0  # Normalizar si es necesario

                # Hacer predicción
                pred = modelo.predict(img_array)
                pred_class = np.argmax(pred, axis=1)[0]

                etiquetas = ['sin_tumor', 'con_tumor']
                resultado = etiquetas[pred_class]
                resultados.append(resultado)

            except Exception as e:
                resultados.append(f"Error procesando {file.filename}: {str(e)}")

    return render_template('tomografia_resultados.html', current_time=current_time, resultados=resultados)
'''

#-----------------VISTAS----------------------------------------
@main_bp.route('/ingresar', methods=['GET'])
def ingresar():
    current_time = datetime.now()
    return render_template('ingresar.html', current_time=current_time)

@main_bp.route('/inicio', methods=['GET'])
def vista_inicio():
    current_time = datetime.now()
    return render_template('inicio.html', current_time=current_time)


@main_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def vista_usuarios():
    usuarios = ServiciosVistas.obtener_usuarios_roles()
    datos_usuario = get_jwt_identity()
    current_time = datetime.now()
    return render_template('usuarios.html', current_time=current_time, usuarios=usuarios, usuario_sesion=datos_usuario)

@main_bp.route('/usuarios/agregar', methods=['GET'])
def vista_agregar_usuarios():
    current_time = datetime.now()
    return render_template('crear_usuario.html', current_time=current_time)

@main_bp.route('/usuarios/editar/<id>', methods=['GET'])
def vista_editar_usuarios(id):
    id_usuario_editar = id
    current_time = datetime.now()
    return render_template('editar_usuario.html', current_time=current_time, id_usuario_editar=id_usuario_editar)

@main_bp.route('/tomografia_listar', methods=['GET'])
def vista_tomografia_listar():
    current_time = datetime.now()
    return render_template('tomografia_listar.html', current_time=current_time)

# @main_bp.route('/tomografia_resultados', methods=['GET'])
# def vista_tomografia_resultados():
#     current_time = datetime.now()
#     return render_template('tomografia_resultados.html', current_time=current_time)

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
def inicio():
    print("entro al api")
    #datos_usuario = get_jwt_identity()
    #print(datos_usuario)
    #cuerpo = {'codigo':200,
    #          'identidad': datos_usuario}
    cuerpo = {'codigo':200}
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

@main_bp.route('/api/usuarios/agregar', methods=['GET'])
@jwt_required()
def api_agregar_usuarios_get():
    identidad = get_jwt_identity()
    roles = ServiciosRol.obtener_todos()
    cuerpo = {  'codigo': 200,
                'identidad': identidad,
                'roles': roles}
    return jsonify(cuerpo)

@main_bp.route('/api/usuarios/agregar', methods=['POST'])
@jwt_required()
def api_agregar_usuarios_post():
    identidad = get_jwt_identity()
    datos_usuario = request.get_json()
    nuevo_usuario = ServiciosUsuario.crear(datos_usuario['nombre_cuenta'], datos_usuario['contrasena'], datos_usuario['nombres'], datos_usuario['ap_paterno'], datos_usuario['ap_materno'], datos_usuario['carnet'], datos_usuario['cargo'], datos_usuario['id_rol'])
    if nuevo_usuario:
        cuerpo = {  'codigo': 200,
                    'identidad': identidad,
                    'nuevo_usuario': nuevo_usuario}
    else:
        cuerpo = {  'codigo': 400,
                    'identidad': identidad,
                    'nuevo_usuario': None}
    return jsonify(cuerpo)

@main_bp.route('/api/usuarios/editar/<id>', methods=['GET'])
@jwt_required()
def api_editar_usuarios_get(id):
    identidad = get_jwt_identity()
    roles = ServiciosRol.obtener_todos()
    usuario_editar = ServiciosUsuario.obtener_id(id)
    cuerpo = {  'codigo': 200,
                'identidad': identidad,
                'roles': roles,
                'usuario_editar': usuario_editar}
    return jsonify(cuerpo)

@main_bp.route('/api/usuarios/editar/<id>', methods=['POST'])
@jwt_required()
def api_editar_usuarios_post(id):
    identidad = get_jwt_identity()
    datos_usuario = request.get_json()
    nuevo_usuario = ServiciosUsuario.actualizar(id, datos_usuario['nombre_cuenta'], datos_usuario['contrasena'], datos_usuario['nombres'], datos_usuario['ap_paterno'], datos_usuario['ap_materno'], datos_usuario['carnet'], datos_usuario['cargo'], datos_usuario['id_rol'])
    if nuevo_usuario:
        print("editado")
        cuerpo = {  'codigo': 200,
                    'identidad': identidad,
                    'nuevo_usuario': nuevo_usuario}
    else:
        cuerpo = {  'codigo': 400,
                    'identidad': identidad,
                    'nuevo_usuario': None}
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

