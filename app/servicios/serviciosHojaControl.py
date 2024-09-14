from app.configuraciones.extensiones import db
from app.serializadores.serializadorHojaControl import SerializadorHojaControl
from app.modelos.hojaControl import HojaControl

class ServiciosHojaControl():
    def obtener_todos():
        hojas_controles = HojaControl.query.all()
        respuesta = SerializadorHojaControl.serializar(hojas_controles)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_id(id):
        hoja_control = HojaControl.query.get(id)
        respuesta = SerializadorHojaControl.serializar_unico(hoja_control)
        if respuesta:
            return respuesta
        else:
            return None
    
    def crear(peso, talla, fecha, numero_hoja, pieza, paciente):
        nueva_hoja_control = HojaControl(peso, talla, fecha, numero_hoja, pieza, paciente)
        db.session.add(nueva_hoja_control)
        db.session.commit()
        respuesta = SerializadorHojaControl.serializar_unico(nueva_hoja_control)
        return respuesta
    
    def actualizar(id, peso=None, talla=None, fecha=None, numero_hoja=None, pieza=None, paciente=None):
        hoja_control_editar = HojaControl.query.get(id)
        if hoja_control_editar:
            if peso:
                hoja_control_editar.peso_paciente = peso
            if talla:
                hoja_control_editar.talla_paciente = talla
            if fecha:
                hoja_control_editar.fecha_control = fecha
            if numero_hoja:
                hoja_control_editar.numero_hoja = numero_hoja
            if pieza:
                hoja_control_editar.pieza_paciente = pieza
            if paciente:
                hoja_control_editar.id_paciente_hoja = paciente
            db.session.commit()
            respuesta = SerializadorHojaControl.serializar_unico(hoja_control_editar)
            return respuesta
        else:
            return None
