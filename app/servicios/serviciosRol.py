from app.modelos.rol import Rol
from app.serializadores.serializadorRol import SerializadorRol

class ServiciosRol():
    def obtener_todos():
        roles = Rol.query.all()
        respuesta = SerializadorRol.serializar(roles)
        return respuesta