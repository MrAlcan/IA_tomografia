from app.modelos.indicacionesMedicas import IndicacionesMedicas
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
    