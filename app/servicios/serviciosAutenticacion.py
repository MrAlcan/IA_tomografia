from app.servicios.serviciosUsuario import ServiciosUsuario
from flask_jwt_extended import create_access_token

class ServiciosAutenticacion:
    def autenticar(nombre, contrasena):
        usuario, respuesta = ServiciosUsuario.verificar_contrasena(nombre, contrasena)
        if usuario:
            #hacer cosas del jwt
            cuerpo_identidad = {'id_usuario': usuario.id_usuario,
                                 'cuenta_usuario': usuario.nombre_cuenta_usuario,
                                 'id_rol': usuario.id_rol_usuario,
                                 'nombres_usuario': usuario.nombres_usuario,
                                 'apellido_paterno': usuario.apellido_paterno_usuario,
                                 'apellido_materno': usuario.apellido_materno_usuario}
            token = create_access_token(identity=cuerpo_identidad)
            return token, usuario.id_rol_usuario
        elif respuesta==404:
            print("Usuario no encontrado")
            return respuesta, None
        else:
            print("Contraseña incorrecta")
            return respuesta, None