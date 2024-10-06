from app.modelos.consulta import Consulta
from app.modelos.usuario import Usuario
from app.modelos.paciente import Paciente
from app.serializadores.serializadorConsulta import SerializadorConsulta

from app.configuraciones.extensiones import db

class ServiciosConsultas():
    def obtener_todos():
        lista = Consulta.query.all()
        respuesta = SerializadorConsulta.serializar(lista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_todos_usuario_paciente():
        #vista = db.session.query(Paciente, Consulta, Usuario).join(Consulta).join(Usuario).all()
        vista = db.session.query(Paciente, Consulta, Usuario)\
            .join(Consulta, Paciente.id_paciente == Consulta.id_paciente_consulta)\
            .join(Usuario, Consulta.id_doctor_tratante == Usuario.id_usuario)\
            .all()
        respuesta = SerializadorConsulta.serializar_todos_vista(vista)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None

    def obtener_usuario_paciente(id):
        vista = db.session.query(Paciente, Consulta, Usuario)\
            .join(Consulta, Paciente.id_paciente == Consulta.id_paciente_consulta)\
            .join(Usuario, Consulta.id_doctor_tratante == Usuario.id_usuario)\
            .filter_by(Consulta.id_consulta == id)
        respuesta = SerializadorConsulta.serializar_unica_vista(vista)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None

    def crear(motivo, historia, enfermedades, tabaco, alcohol, drogas, diagnostico, tratamiento, doctor, paciente, internacion, codigo_consulta ,estado_consulta=None):
        nueva_consulta = Consulta(motivo, historia, enfermedades, tabaco, alcohol, drogas, diagnostico, tratamiento, doctor, paciente, internacion, codigo_consulta ,estado_consulta)
        db.session.add(nueva_consulta)
        db.session.commit()
        respuesta = SerializadorConsulta.serializar_unico(nueva_consulta)
        if respuesta:
            return respuesta
        else:
            return None
    
    def actualizar(id, motivo=None, historia=None, enfermedades=None, tabaco=None, alcohol=None, drogas=None, diagnostico=None, tratamiento=None, doctor=None, paciente=None, internacion=None, codigo_consulta=None ,estado_consulta=None):
        consulta_editar = Consulta.query.get(id)
        if consulta_editar:
            if motivo:
                consulta_editar.motivo_consulta = motivo
            if historia:
                consulta_editar.historia_enfermedad_actual = historia
            if enfermedades:
                consulta_editar.enfermedades_consulta = enfermedades
            if tabaco:
                consulta_editar.consumo_tabaco = tabaco
            if alcohol:
                consulta_editar.consumo_alcohol = alcohol
            if drogas:
                consulta_editar.consumo_drogas = drogas
            if diagnostico:
                consulta_editar.diagnostico_consulta = diagnostico
            if tratamiento:
                consulta_editar.tratamiento_consulta = tratamiento
            if internacion:
                consulta_editar.internacion_consulta = internacion
            if doctor:
                consulta_editar.id_doctor_tratante = doctor
            if paciente:
                consulta_editar.id_paciente_consulta = paciente
            if codigo_consulta:
                consulta_editar.codigo_consulta = codigo_consulta
            if estado_consulta:
                consulta_editar.estado_consulta = estado_consulta
            db.session.commit()
            respuesta = SerializadorConsulta.serializar_unico(consulta_editar)
            return respuesta
        else:
            return None