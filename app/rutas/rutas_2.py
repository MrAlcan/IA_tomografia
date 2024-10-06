from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, verify_jwt_in_request, unset_jwt_cookies
from flask import Blueprint, render_template, request, redirect, url_for
from functools import wraps
from datetime import datetime
from app.servicios.serviciosAutenticacion import ServiciosAutenticacion
from app.servicios.serviciosVistas import ServiciosVistas
from app.servicios.serviciosRol import ServiciosRol
from app.servicios.serviciosUsuario import ServiciosUsuario
from app.servicios.serviciosPaciente import ServiciosPaciente
from app.servicios.serviciosHojaControl import ServiciosHojaControl
from app.servicios.serviciosControlEstado import ServiciosControlEstado
from app.servicios.serviciosControlSignos import ServiciosControlSignos
from app.servicios.serviciosIndicaciones import ServiciosIndicaciones
from app.servicios.serviciosEnfermeria import ServiciosEnfermeras
from app.servicios.serviciosConsultas import ServiciosConsultas
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
from app.servicios.serviciosResultadoEstudio import ServiciosResultadoEstudio

from flask import request, jsonify
import jwt

def no_iniciar_sesion(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Verifica si hay un token válido en las cookies
            current_user = get_jwt_identity()  # Obtén la identidad del usuario (si el token es válido)
            print(current_user)
            return redirect(url_for('main.vista_inicio'))  # Si está autenticado, redirige a otra vista
        except:
            # Si no hay token o si el token no es válido, permite acceder a la vista de login
            return f(*args, **kwargs)
    return wrapper

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


@main_bp.route('/', methods=['GET'])
def ingresar():
    current_time = datetime.now()
    print(request.headers)
    return render_template('ingresar.html', current_time=current_time)

@main_bp.route('/ingresar', methods=['POST'])
@no_iniciar_sesion
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

@main_bp.route('/cerrar_sesion', methods=['GET'])
@jwt_required()
def cerrar_sesion():
    resp = make_response(redirect(url_for('main.ingresar')))  # Redirige a la página de login o inicio
    unset_jwt_cookies(resp)  # Elimina las cookies del JWT
    return resp  # Retorna la respuesta con las cookies eliminadas

@main_bp.route('/configuracion')
@jwt_required()
def configuracion():
    identidad = get_jwt_identity()
    return render_template('configuracion.html', identidad = identidad)

@main_bp.route('/configuracion', methods=['POST'])
@token_requerido
def configuracion_post(datos_usuario):
    identidad = datos_usuario
    print(identidad)
    datos = request.form
    print(datos)
    usuario_modificado = ServiciosUsuario.actualizar(id=identidad['id_usuario'], nombre=datos['input_nombre_cuenta'], nombre_per=datos['input_nombres'],ap_paterno=datos['input_apellido_paterno'],ap_materno=datos['input_apellido_materno'],cargo=datos['input_cargo'],carnet=datos['input_carnet'])
    if usuario_modificado:
        respuesta, id_rol = ServiciosAutenticacion.actualizar_token(identidad['id_usuario'])
        resp = make_response(redirect(url_for('main.vista_inicio')))
        set_access_cookies(resp, respuesta)
        return resp
    else:
        print('hubo un error')
        return jsonify({'codigo': 400}) # mejorar
    
@main_bp.route('/configuracion/contrasena', methods=['GET', 'POST'])
@token_requerido
def editar_contrasena(datos_usuario):
    identidad = datos_usuario
    estado = False
    antigua = ''
    nueva = ''
    if request.method=='POST':
        datos = request.form
        print(datos)
        antigua_contrasena = datos['input_antigua_contrasena']
        nueva_contrasena = datos['input_nueva_contrasena']
        print(identidad['id_usuario'])
        respuesta = ServiciosUsuario.cambiar_contrasena(identidad['id_usuario'], antigua_contrasena, nueva_contrasena)
        if respuesta == 200:
            print("contrasena modificada exitosamente")
            return redirect(url_for('main.vista_inicio'))
        else:
            antigua = antigua_contrasena
            nueva = nueva_contrasena
            estado = True
            #return render_template('cambiar_contrasena.html', identidad = identidad, estado=estado, antigua=antigua, nueva=nueva)

    return render_template('cambiar_contrasena.html', identidad = identidad, estado=estado, antigua=antigua, nueva=nueva)

'''
@main_bp.route('/configuracion/contrasena/<estado>/<antigua>/<nueva>', methods=['GET'])
@jwt_required()
def editar_contrasena(estado = None, antigua=None, nueva=None):
    print(estado)
    print(estado)
    print(antigua)
    print(nueva)
    
    
    identidad = get_jwt_identity()
    return render_template('cambiar_contrasena.html', identidad = identidad, estado=estado, antigua=antigua, nueva=nueva)

@main_bp.route('/configuracion/contrasena', methods=['POST'])
@token_requerido
def editar_contrasena_post(datos_usuario):
    identidad = datos_usuario
    datos = request.form
    print(datos)
    antigua_contrasena = datos['input_antigua_contrasena']
    nueva_contrasena = datos['input_nueva_contrasena']
    print(identidad['id_usuario'])
    respuesta = ServiciosUsuario.cambiar_contrasena(identidad['id_usuario'], antigua_contrasena, nueva_contrasena)
    if respuesta == 200:
        print("contrasena modificada exitosamente")
        return redirect(url_for('main.vista_inicio'))
    else:
        print('contrasenas desiguales')
        return redirect(url_for('main.editar_contrasena', estado = 'True', antigua = antigua_contrasena, nueva = nueva_contrasena))
'''

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
    roles = ServiciosRol.obtener_todos()
    if request.method == 'POST':
        #no hay post
        print("helloda")
    return render_template('usuarios.html', identidad=identidad, usuarios=usuarios, roles=roles)

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
    print(id)
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
    

@main_bp.route('/control_signos_vitales', methods=['GET'])
@jwt_required()
def control_signos_vitales():
    identidad = get_jwt_identity()
    hojas_control = ServiciosHojaControl.obtener_todos()
    pacientes = ServiciosPaciente.obtener_todos()
    return render_template('hoja_control.html', identidad = identidad, hojas_control = hojas_control, pacientes = pacientes)

@main_bp.route('/control_signos_vitales/agregar', methods = ['GET'])
@jwt_required()
def agregar_control_signos_vitales():
    identidad = get_jwt_identity()
    pacientes = ServiciosPaciente.obtener_todos()
    return render_template('crear_hoja_control.html', identidad=identidad, pacientes=pacientes)

@main_bp.route('/control_signos_vitales/agregar', methods=['POST'])
@token_requerido
def agregar_control_signos_vitales_post(datos_usuario):
    identidad = datos_usuario
    datos = request.form
    print(datos)
    nueva_hoja = ServiciosHojaControl.crear(datos['input_peso'], datos['input_talla'], datos['input_servicio'], datos['input_pieza'], datos['input_paciente'])
    print(nueva_hoja)
    if nueva_hoja:
        return redirect(url_for('main.control_signos_vitales'))
    else:
        return jsonify({'codigo': 400})

@main_bp.route('/control_signos_vitales/editar/<id>', methods=['GET'])
@jwt_required()
def control_signos_vitales_editar(id):
    identidad = get_jwt_identity()
    editar_hoja_control = ServiciosHojaControl.obtener_id(id)
    print(editar_hoja_control)
    paciente_control = ServiciosPaciente.obtener_id(editar_hoja_control['id_paciente'])
    return render_template('editar_hoja_control.html', identidad = identidad, editar_hoja = editar_hoja_control, paciente = paciente_control)

@main_bp.route('/control_signos_vitales/editar/<id>', methods=['POST'])
@token_requerido
def control_signos_vitales_editar_post(datos_usuario, id):
    identidad = datos_usuario
    datos = request.form
    editar_hoja_control = ServiciosHojaControl.actualizar(id, datos['input_peso'], datos['input_talla'], datos['input_servicio'], datos['input_pieza'])
    if editar_hoja_control:
        return redirect(url_for('main.control_signos_vitales')) 
    else:
        return jsonify({'codigo': 400})

@main_bp.route('/control_signos_vitales/ver/<id>', methods=['GET'])
@jwt_required()
def control_signos_vitales_ver(id):
    identidad = get_jwt_identity()
    hoja_control = ServiciosHojaControl.obtener_id(id)
    control_estados = ServiciosControlEstado.obtener_hoja(id)
    control_signos = ServiciosControlSignos.obtener_hoja(id)
    return render_template('ver_hoja_control.html', identidad=identidad, hoja=hoja_control, estados=control_estados, signos=control_signos)

@main_bp.route('/control_signos_vitales/agregar_estado/<id>', methods=['GET'])
@jwt_required()
def control_estado_agregar(id):
    identidad = get_jwt_identity()
    hoja_control = ServiciosHojaControl.obtener_id(id)
    return render_template('crear_control_estado.html', identidad=identidad, hoja=hoja_control)

@main_bp.route('/control_signos_vitales/agregar_estado/<id>', methods = ['POST'])
@token_requerido
def control_estado_agregar_post(datos_usuario, id):
    identidad = datos_usuario
    datos = request.form
    #print(datos)
    control_estado_nuevo = ServiciosControlEstado.crear(datos['input_antibiotico'], datos['input_dias_internado'], datos['input_fecha'], datos['input_dias_post'], id)
    if control_estado_nuevo:
        return redirect(url_for('main.control_signos_vitales_ver', id=id))
    else:
        return jsonify({'codigo': 400})

@main_bp.route('/control_signos_vitales/editar_estado/<id>/<hoja>', methods = ['POST'])
@token_requerido
def control_estado_editar_post(datos_usuario, id, hoja):
    identidad = datos_usuario
    datos = request.form
    control_estado_editar = ServiciosControlEstado.actualizar(id, datos['input_antibiotico'], datos['input_dias_internado'], datos['input_fecha'], datos['input_dias_post'])
    if control_estado_editar:
        return redirect(url_for('main.control_signos_vitales_ver', id=hoja))
    else:
        return jsonify({'codigo': 400})


@main_bp.route('/control_signos_vitales/agregar_signo/<id>', methods=['GET'])
@jwt_required()
def control_signo_agregar(id):
    identidad = get_jwt_identity()
    hoja_control = ServiciosHojaControl.obtener_id(id)
    return render_template('crear_control_signo.html', identidad=identidad, hoja=hoja_control)

@main_bp.route('/control_signos_vitales/agregar_signo/<id>', methods=['POST'])
@token_requerido
def control_signo_agregar_post(datos_usuario, id):
    identidad = datos_usuario
    datos = request.form
    control_signo_nuevo = ServiciosControlSignos.crear(datos['input_fecha'], datos['input_hora'], datos['input_presion_sistolica'], datos['input_presion_diastolica'], datos['input_respiracion'], datos['input_saturacion'], datos['input_diuresis'], datos['input_catarsis'], id)
    if control_signo_nuevo:
        return redirect(url_for('main.control_signos_vitales_ver', id=id))
    else:
        return jsonify({'codigo':400})
    


############# SOLICITAR EVALUACION GUARDA ############

@main_bp.route('/tomografia_resultados/agregar', methods=['POST'])
@token_requerido
def tomografia_resultados_agregar(datos_usuario):
    datos = request.form
    codigo_paciente = datos.get('codigoPaciente')
    doctor = datos.get('doctor')
    id_consulta_estudio = datos.get('idConsulta')

    if 'entradaImagenes' not in request.files:
        return jsonify({'mensaje': 'error en solicitud'}), 400

    imagenes = request.files.getlist('entradaImagenes')
    ruta_relativa = os.path.join('app', 'static','imagenes')
    ruta = os.path.abspath(ruta_relativa)

    fecha = datetime.now().date()
    hora = datetime.now()
    fecha_formateada = fecha.strftime('%Y%m%d')
    hora_formateada = hora.strftime('%H%M%S')

    carpeta_nombre = f"{codigo_paciente}_{id_consulta_estudio or 'vacio'}_{fecha_formateada}_{hora_formateada}"
    carpeta_path = os.path.join(ruta, carpeta_nombre)
    if not os.path.exists(carpeta_path):
        os.makedirs(carpeta_path)

    for imagen in imagenes:
        if imagen.filename:
            filename = secure_filename(imagen.filename)
            ruta_imagen = os.path.join(carpeta_path, filename)
            imagen.save(ruta_imagen)
            ruta_relativa_imagen = os.path.join(carpeta_nombre, filename).replace("\\", "/")

            resultado = ServiciosResultadoEstudio.crear(
                fecha=fecha,
                ruta=ruta_relativa_imagen,  
                doctor=doctor,
                paciente=codigo_paciente,
                consulta=id_consulta_estudio, 
                resultado=1
            )
            
            if not resultado:
                return jsonify({'mensaje': f'Error al crear registro para {filename}'}), 400

    return redirect(url_for('main.tomografia_listar'))
    
############ VISTA LISTADO ##################

@main_bp.route('/tomografia_listar', methods=['GET'])
@jwt_required()
def tomografia_listar():
    identidad = get_jwt_identity()
    listado = ServiciosResultadoEstudio.obtener_todos()
    consultas = ServiciosConsultas.obtener_todos()
    pacientes = ServiciosPaciente.obtener_todos()
    return render_template('tomografia_listar.html', identidad=identidad, listado=listado, pacientes=pacientes, consultas=consultas)

############ VISTA LISTADO ENFERMERA INDIC##################

@main_bp.route('/indicaciones_doctor', methods=['GET'])
@jwt_required()
def indicaciones_doctor():
    identidad = get_jwt_identity()
    listado = ServiciosIndicaciones.obtener_todos()
    return render_template('indicaciones_doctor.html', identidad=identidad, listado=listado)

############ VISTA LISTADO DOCTOR INDIC##################

@main_bp.route('/indicaciones_enfermeras', methods=['GET'])
@jwt_required()
def indicaciones_enfermeras():
    identidad = get_jwt_identity()
    listado = ServiciosEnfermeras.obtener_todos()
    return render_template('indicaciones_enfermeras.html', identidad=identidad, listado=listado)


#################OBTENER ID PARA LISTA TOMOGRAFIA##################
@main_bp.route('/obtener_nombre_paciente/<int:id>', methods=['GET'])
@jwt_required()
def obtener_nombre_paciente(id):
    paciente = ServiciosPaciente.obtener_id(id)
    print(paciente)
    if paciente:
        return jsonify(paciente)
    else:
        return jsonify({'nose encontro'})


############ VISTA PPARA EVALUACION ##################
@main_bp.route('/tomografia_resultados', methods=['GET'])
@jwt_required()

def tomografia_resultados():
    identidad = get_jwt_identity()
    consultas = ServiciosConsultas.obtener_todos()
    pacientes = ServiciosPaciente.obtener_todos()
    print(pacientes)
    return render_template('tomografia_resultados.html', identidad=identidad, consultas=consultas,pacientes=pacientes) 


#############ID DE LISTA PARA MODAL#################
@main_bp.route('/obtener_resultado/<id>', methods=['GET'])
@jwt_required()
def obtener_resultado(id):
    print(id)
    resultado = ServiciosResultadoEstudio.query.get(id)
    
    if resultado:
        # Preparar los datos para enviarlos como respuesta en JSON
        data = {
            'id_resultado': resultado.id_resultado,
            'codigo_paciente': resultado.paciente.codigo,
            'nombre_completo': f"{resultado.paciente.nombre} {resultado.paciente.apellido_p} {resultado.paciente.apellido_m}",
            'consulta_codigo': resultado.consulta.codigo,
            'doctor_nombre': f"{resultado.doctor.nombre} {resultado.doctor.apellido_p} {resultado.doctor.apellido_m}",
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Resultado no encontrado'}), 404


from datetime import datetime

@main_bp.route('/resultados/editar/<id>', methods=['POST'])
@token_requerido
def resultados_editar(datos_usuario, id):
    identidad = datos_usuario
   
    datos = request.form
    print(datos)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    datos_modificado = ServiciosResultadoEstudio.actualizar(id=id, paciente=datos['codigoModal2'],consulta=datos['consultaModal2'])
    
    if datos_modificado:
        return redirect(url_for('main.tomografia_listar'))
    else:
        print('Hubo un error al actualizar')
        return jsonify({'codigo': 400, 'mensaje': 'no act'}), 400
    
    
    

