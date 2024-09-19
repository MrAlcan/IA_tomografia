from app.modelos.consulta import Consulta
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