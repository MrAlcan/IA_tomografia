from app.configuraciones.extensiones import db
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.serializadores.serializadorVistas import SerializadorVistas
from app.modelos.paciente import Paciente
from app.modelos.hojaControl import HojaControl

class ServiciosVistas:
    def obtener_usuarios_roles():
        vista = db.session.query(Rol, Usuario).join(Usuario).all()
        print(vista)
        #rol = vista.roles
        #usuario = vista.usuarios
        #print(rol)
        #print(usuario)
        
        #respuesta = SerializadorVistas.serializar_usuarios_roles(usuario)
        respuesta = SerializadorVistas.serializar_usuarios_roles(vista)
        
        return respuesta

    def obtener_pacientes_hojas_control():
        vista = db.session.query(Paciente, HojaControl).join(HojaControl).all()
        respuesta = SerializadorVistas.serializar_pacientes_hoja_control(vista)
        return respuesta