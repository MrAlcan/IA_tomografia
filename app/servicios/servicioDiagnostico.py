from app.configuraciones.extensiones import db
from app.modelos.diagnostico import Diagnostico
from app.modelos.consulta import Consulta
from app.modelos.paciente import Paciente
from app.modelos.usuario import Usuario
from app.serializadores.serializadorDiagnostico import SerializadorDiagnostico

class ServiciosDiagnostico():
    def crear(fecha, ruta, doctor, paciente, consulta, resultado):
        nuevo_resultado = Diagnostico(fecha, ruta, doctor, paciente, consulta, resultado)
        db.session.add(nuevo_resultado)
        db.session.commit()
        respuesta = SerializadorDiagnostico.serializar_unico(nuevo_resultado)
        if respuesta:
            return respuesta
        else:
            return None
  
    
    def obtener_id(id):
        resultados = Diagnostico.query.get(id)
        respuesta = SerializadorDiagnostico.serializar_unico(resultados)
        if resultados:
            return respuesta
        else:
            return None
        
  
        
    def obtener_lista_id(id):
        datos = db.session.query(Paciente, Diagnostico, Usuario)\
            .join(Diagnostico, Paciente.id_paciente == Diagnostico.id_paciente_diagnostico)\
            .join(Usuario, Diagnostico.id_doctor_diagnostico== Usuario.id_usuario)\
            .filter(Paciente.id_paciente==id)
        respuesta = SerializadorDiagnostico.serializar_todos_vista(datos)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None
        