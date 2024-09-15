from app.configuraciones.extensiones import db
from app.serializadores.serializadorHojaControl import SerializadorHojaControl
from app.modelos.hojaControl import HojaControl
from app.modelos.paciente import Paciente

def obtener_ultima_hoja(hojas):
    respuesta = 0
    if hojas:
        for hoja in hojas:
            if(hoja.numero_hoja>respuesta):
                respuesta = hoja.numero_hoja
    respuesta = respuesta + 1
    return respuesta

class ServiciosHojaControl():
    def obtener_todos():
        #hojas_controles = HojaControl.query.all()
        #respuesta = SerializadorHojaControl.serializar(hojas_controles)
        vista = db.session.query(Paciente, HojaControl).join(HojaControl).all()
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_id(id):
        #hoja_control = HojaControl.query.get(id)
        #respuesta = SerializadorHojaControl.serializar_unico(hoja_control)
        vista = db.session.query(Paciente, HojaControl).join(HojaControl).filter_by(id_hoja_control=id)
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def crear(peso, talla, servicio, pieza, paciente):
        hojas_control = HojaControl.query.filter_by(id_paciente_hoja=paciente)
        numero_hoja = obtener_ultima_hoja(hojas_control)
        nueva_hoja_control = HojaControl(peso, talla, servicio, numero_hoja, pieza, paciente)
        db.session.add(nueva_hoja_control)
        db.session.commit()
        respuesta = SerializadorHojaControl.serializar_unico(nueva_hoja_control)
        return respuesta
    
    def actualizar(id, peso=None, talla=None, servicio=None, pieza=None):
        hoja_control_editar = HojaControl.query.get(id)
        if hoja_control_editar:
            if peso:
                hoja_control_editar.peso_paciente = peso
            if talla:
                hoja_control_editar.talla_paciente = talla
            if servicio:
                hoja_control_editar.fecha_control = servicio
            if pieza:
                hoja_control_editar.pieza_paciente = pieza
            db.session.commit()
            respuesta = SerializadorHojaControl.serializar_unico(hoja_control_editar)
            return respuesta
        else:
            return None
