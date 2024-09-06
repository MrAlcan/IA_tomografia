from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, render_template
from datetime import datetime

from app.servicios.serviciosAutenticacion import ServiciosAutenticacion

rutas_vistas = Blueprint('main', __name__)

@rutas_vistas.route('/ingresar', methods=['GET'])
def vista_iniciar_sesion():
    current_time = datetime.now()
    return render_template('ingresar.html', current_time=current_time)

@rutas_vistas.route('/inicio', methods=['GET'])
def vista_inicio():
    current_time = datetime.now()
    return render_template('inicio.html', current_time=current_time)

@rutas_vistas.route('/usuarios', methods=['GET'])
def vista_usuarios():
    current_time = datetime.now()
    return render_template('usuarios.html', current_time=current_time)