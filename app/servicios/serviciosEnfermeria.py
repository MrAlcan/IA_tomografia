from app.modelos.registroEnfermeria import RegistroEnfermeria
from app.modelos.usuario import Usuario
from app.modelos.paciente import Paciente
from app.serializadores.serializadorRegistroEnfermeria import SerializadorRegistroEnfermeria

from app.configuraciones.extensiones import db

class ServiciosEnfermeras():
    def obtener_todos():
        lista = RegistroEnfermeria.query.all()
        respuesta = SerializadorRegistroEnfermeria.serializar(lista)
        if respuesta:
            return respuesta
        else:
            return None
        
    def crear(procedimiento, observaciones, fecha, hora,id_enfermera, paciente):
        nuevo_resultado = RegistroEnfermeria(procedimiento, observaciones, fecha, hora,id_enfermera, paciente)
        db.session.add(nuevo_resultado)
        db.session.commit()
        respuesta = SerializadorRegistroEnfermeria.serializar_unico(nuevo_resultado)
        
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_lista_id(id):
        datos = db.session.query(Paciente, RegistroEnfermeria, Usuario)\
            .join(RegistroEnfermeria, Paciente.id_paciente == RegistroEnfermeria.id_paciente)\
            .join(Usuario, RegistroEnfermeria.id_enfermera_cargo == Usuario.id_usuario)\
            .filter(Paciente.id_paciente==id)
        respuesta = SerializadorRegistroEnfermeria.serializar_todos_vista(datos)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None
 

    def actualizar(id,procedimiento=None, observaciones=None, fecha=None, hora=None,id_enfermera=None):
        consulta_editar = RegistroEnfermeria.query.get(id)
        
        if consulta_editar:
            if procedimiento:
                consulta_editar.procedimiento_enfermeria = procedimiento
            if observaciones:
                consulta_editar.observaciones_enfermeria = observaciones
            if fecha:
                consulta_editar.fecha_registro = fecha
            if hora:
                consulta_editar.hora_registro = hora
            if id_enfermera:
                consulta_editar.id_enfermera_cargo = id_enfermera
           
            db.session.commit()
            respuesta = SerializadorRegistroEnfermeria.serializar_unico(consulta_editar)
            return respuesta
        else:
            return None
        

