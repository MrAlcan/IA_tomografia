from app.configuraciones.extensiones import db
from app.modelos.controlEstado import ControlEstado
from app.serializadores.serializadorControlEstado import SerializadorControlEstado

class ServiciosControlEstado():
    def obtener_todos():
        controles_estado = ControlEstado.query.all()
        respuesta = SerializadorControlEstado.serializar(controles_estado)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_id(id):
        control_estado = ControlEstado.query.get(id)
        respuesta = SerializadorControlEstado.serializar_unico(control_estado)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_hoja(id_hoja):
        control_estado = ControlEstado.query.filter_by(id_hoja_control_estado = id_hoja)
        respuesta = SerializadorControlEstado.serializar(control_estado)
        if respuesta:
            return respuesta
        else:
            return None
    
    def crear(antibiotico, dias_internado, fecha, dias_post_operatorio, hoja_control):
        nuevo_control_estado = ControlEstado(antibiotico, dias_internado, fecha, dias_post_operatorio, hoja_control)
        db.session.add(nuevo_control_estado)
        db.session.commit()
        respuesta = SerializadorControlEstado.serializar_unico(nuevo_control_estado)
        if respuesta:
            return respuesta
        else:
            return None
    
    def actualizar(id, antibiotico, dias_internado, fecha, dias_post_operatorio, hoja_control):
        editar_control = ControlEstado.query.get(id)
        if editar_control:
            if antibiotico:
                editar_control.antibiotico_estado = antibiotico
            if dias_internado:
                editar_control.dias_internado = dias_internado
            if fecha:
                editar_control.fecha_estado = fecha
            if dias_post_operatorio:
                editar_control.dias_post_operatorio = dias_post_operatorio
            if hoja_control:
                editar_control.id_hoja_control_estado = hoja_control
            db.session.commit()
            respuesta = SerializadorControlEstado.serializar_unico(editar_control)
            if respuesta:
                return respuesta
            else:
                return None
        else:
            return None