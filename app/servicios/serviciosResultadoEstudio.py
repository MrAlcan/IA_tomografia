from app.configuraciones.extensiones import db
from app.modelos.resultadoEstudio import ResultadoEstudio
from app.modelos.consulta import Consulta
from app.modelos.paciente import Paciente
from app.modelos.usuario import Usuario
from app.serializadores.serializadorResultadoEstudio import ResultadoEstudioSchema

class ServiciosResultadoEstudio():
    def crear(fecha, ruta, doctor, paciente, consulta, resultado):
        nuevo_resultado = ResultadoEstudio(fecha, ruta, doctor, paciente, consulta, resultado)
        db.session.add(nuevo_resultado)
        db.session.commit()
        respuesta = ResultadoEstudioSchema.serializar_unico(nuevo_resultado)
        if respuesta:
            return respuesta
        else:
            return None
        
    @staticmethod
    def obtener_todos():
        datos = ResultadoEstudio.query.all()
        resultados = []
        for resultado in datos:
            datos_resultado = {
                'id_resultado': resultado.id_resultado,
                'fecha_estudio': resultado.fecha_estudio,
                'ruta': resultado.ruta_carpeta_imagenes_estudio,
                'resultado_estudio': resultado.resultado_estudio,
                'doctor': {
                    'nombre': resultado.doctor.nombres_usuario,  
                    'apellido_p': resultado.doctor.apellido_paterno_usuario, 
                    'apellido_m': resultado.doctor.apellido_materno_usuario,   
                },
                'paciente': {
                    'nombre': resultado.paciente.nombres_paciente,  
                    'apellido_p': resultado.paciente.apellido_paterno_paciente,  
                    'apellido_m': resultado.paciente.apellido_materno_paciente,
                    'carnet': resultado.paciente.carnet_paciente, 
                    'id_paciente': resultado.paciente.id_paciente,
                },
                'consulta': {
                    'codigo': resultado.consulta.codigo_consulta,  
                    'id_consulta': resultado.consulta.id_consulta,  
                }
            }
            resultados.append(datos_resultado)
        return resultados
    
    def obtener_id(id):
        resultados = ResultadoEstudio.query.get(id)
        respuesta = ResultadoEstudioSchema.serializar_unico(resultados)
        if resultados:
            return respuesta
        else:
            return None
        
    @staticmethod
    def actualizar(id, paciente=None, consulta=None):
        try:
            resultado = ResultadoEstudio.query.get(id)
            if resultado:
                resultado.id_paciente_estudio = paciente
                resultado.id_consulta_estudio = consulta
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al actualizar el resultado: {e}")
            return False