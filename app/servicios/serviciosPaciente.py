from app.modelos.paciente import Paciente
from app.serializadores.serializadorPaciente import SerializadorPaciente
from app.configuraciones.extensiones import db

class ServiciosPaciente():
    def obtener_todos():
        pacientes = Paciente.query.all()
        respuesta = SerializadorPaciente.serializar(pacientes)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_id(id):
        paciente = Paciente.query.get(id)
        respuesta = SerializadorPaciente.serializar_unico(paciente)
        if paciente:
            return respuesta
        else:
            return None
    
    def crear(nombres, apellido_paterno, apellido_materno, carnet, seguro, fecha_nacimiento, edad):
        nuevo_paciente = Paciente(nombres, apellido_paterno, apellido_materno, carnet, seguro, fecha_nacimiento, edad)
        db.session.add(nuevo_paciente)
        db.session.commit()
        respuesta = SerializadorPaciente.serializar_unico(nuevo_paciente)
        if respuesta:
            return respuesta
        else:
            return None
    
    def actualizar(id, nombres=None, apellido_paterno=None, apellido_materno=None, carnet=None, seguro=None, fecha_nacimiento=None, edad=None):
        usuario_editar = Paciente.query.get(id)
        if usuario_editar:
            if nombres:
                usuario_editar.nombres_paciente = nombres
            if apellido_paterno:
                usuario_editar.apellido_paterno_paciente = apellido_paterno
            if apellido_materno:
                usuario_editar.apellido_materno_paciente = apellido_materno
            if carnet:
                usuario_editar.carnet_paciente = carnet
            if seguro:
                usuario_editar.seguro_paciente = seguro
            if fecha_nacimiento:    
                usuario_editar.fecha_nacimiento_paciente = fecha_nacimiento
            if edad:
                usuario_editar.edad_paciente = edad
            db.session.commit()
            respuesta = SerializadorPaciente.serializar_unico(usuario_editar)
            return respuesta
        else:
            return None

    def generar_reporte_completo(id, nombres_usuario):
        print(nombres_usuario)