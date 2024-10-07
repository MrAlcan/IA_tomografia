from app.modelos.indicacionesMedicas import IndicacionesMedicas
from app.modelos.usuario import Usuario
from app.modelos.paciente import Paciente
from app.serializadores.serializadorIndicacionesMedicas import SerializadorIndicacionesMedicas
from app.configuraciones.extensiones import db

class ServiciosIndicaciones():
    def obtener_todos():
        lista = IndicacionesMedicas.query.all()
        respuesta = SerializadorIndicacionesMedicas.serializar(lista)
        if respuesta:
            return respuesta
        else:
            return None

    
    def crear(fecha, hora,descripcion, doctor, paciente):
        nuevo_resultado = IndicacionesMedicas(fecha, hora,descripcion, doctor, paciente)
        db.session.add(nuevo_resultado)
        db.session.commit()
        respuesta = SerializadorIndicacionesMedicas.serializar_unico(nuevo_resultado)
        
        if respuesta:
            return respuesta
        else:
            return None
        

    def obtener_lista_id(id):
        datos = db.session.query(Paciente, IndicacionesMedicas, Usuario)\
            .join(IndicacionesMedicas, Paciente.id_paciente == IndicacionesMedicas.id_paciente_indicaciones)\
            .join(Usuario, IndicacionesMedicas.id_doctor_cargo == Usuario.id_usuario)\
            .filter(Paciente.id_paciente==id)
        respuesta = SerializadorIndicacionesMedicas.serializar_todos_vista(datos)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None
        

    def actualizar(id,fecha=None, hora=None,descripcion=None, doctor=None):
        consulta_editar = IndicacionesMedicas.query.get(id)
        print("__________________")
        print(consulta_editar)
        if consulta_editar:
            if fecha:
                consulta_editar.fecha_indicaciones = fecha
            if hora:
                consulta_editar.hora_indicaciones = hora
            if descripcion:
                consulta_editar.descripcion_indicaciones = descripcion
            if doctor:
                consulta_editar.id_doctor_cargo = doctor
           
           
            db.session.commit()
            respuesta = SerializadorIndicacionesMedicas.serializar_unico(consulta_editar)
            return respuesta
        else:
            return None