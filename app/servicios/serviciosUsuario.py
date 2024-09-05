from app.modelos.usuario import Usuario
from app.serializadores.serializadorUsuario import SerializadorUsuario
from app.configuraciones.extensiones import db, bcrypt

class ServiciosUsuario():
    def crear(nombre, contrasena, nombre_per, ap_paterno, ap_materno, carnet, cargo, id_rol):
        contrasena_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')
        nuevo_usuario = Usuario(nombre, contrasena_hash, nombre_per, ap_paterno, ap_materno, carnet, cargo, id_rol)
        db.session.add(nuevo_usuario)
        db.session.commit()
        respuesta = SerializadorUsuario.serializar_unico(nuevo_usuario)
        return respuesta

    def actualizar(id, nombre=None, contrasena=None, nombre_per=None, ap_paterno=None, ap_materno=None, carnet=None, cargo=None, id_rol=None):
        usuario_modificado = Usuario.query.get(id)
        if usuario_modificado:
            if nombre:
                usuario_modificado.nombre_cuenta_usuario = nombre
            if contrasena:
                if bcrypt.check_password_hash(usuario_modificado.contrasena_usuario, contrasena):
                    usuario_modificado.contrasena_usuario = bcrypt.generate_password_hash(contrasena).decode('utf-8')
                else:
                    return None
            if nombre_per:
                usuario_modificado.nombres_usuario = nombre_per
            if ap_paterno:
                usuario_modificado.apellido_paterno_usuario = ap_paterno
            if ap_materno:
                usuario_modificado.apellido_materno_usuario = ap_materno
            if carnet:
                usuario_modificado.carnet_usuario = carnet
            if id_rol:
                usuario_modificado.id_rol_usuario = id_rol
            db.session.commit()
            respuesta = SerializadorUsuario.serializar_unico(usuario_modificado)
            return respuesta
        else:
            return None
        
    
    def obtener_todos():
        usuarios = Usuario.query.all()
        respuesta = SerializadorUsuario.serializar(usuarios)
        return respuesta
    
    def obtener_id(id):
        usuario = Usuario.query.get(id)
        respuesta = SerializadorUsuario.serializar_unico(usuario)
        return respuesta
    
    def obtener_nombre(nombre):
        usuario = Usuario.query.filter_by(nombre_cuenta_usuario = nombre).first()
        respuesta = SerializadorUsuario.serializar_unico(usuario)
        return respuesta
    
    def verificar_contrasena(nombre, contrasena):
        usuario = Usuario.query.filter_by(nombre_cuenta_usuario = nombre).first()
        if usuario:
            if bcrypt.check_password_hash(usuario.contrasena_usuario, contrasena):
                return usuario, 200
            else:
                return None, 401
        else:
            return None, 404