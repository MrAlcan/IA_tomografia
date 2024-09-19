from app.modelos.registroEnfermeria import RegistroEnfermeria
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
    