from app.servicios.serviciosUsuario import ServiciosUsuario
from flask_jwt_extended import create_access_token, create_refresh_token

class ServiciosAutenticacion:
    def actualizar_token(id_usuario):
        usuario = ServiciosUsuario.obtener_id(id_usuario)
        if usuario:
            #hacer cosas del jwt
            primer_nombre = str(usuario['nombres']).split(' ')[0]
            cuerpo_identidad = {'id_usuario': usuario['id_usuario'],
                                 'cuenta_usuario': usuario['cuenta'],
                                 'id_rol': usuario['id_rol'],
                                 'nombres_usuario': primer_nombre,
                                 'nombres_completos': usuario['nombres'],
                                 'apellido_paterno': usuario['apellido_paterno'],
                                 'apellido_materno': usuario['apellido_materno'],
                                 'cargo_usuario': usuario['cargo'],
                                 'carnet_usuario': usuario['carnet']}
            token = create_access_token(identity=cuerpo_identidad)
            #refresh_token = create_refresh_token(identity=cuerpo_identidad)
            return token, usuario['id_rol']
            #return token, refresh_token, usuario.id_rol_usuario
        else:
            return 400, None
        


    def autenticar(nombre, contrasena):
        usuario, respuesta = ServiciosUsuario.verificar_contrasena(nombre, contrasena)
        if usuario:
            #hacer cosas del jwt
            primer_nombre = str(usuario.nombres_usuario).split(' ')[0]
            cuerpo_identidad = {'id_usuario': usuario.id_usuario,
                                 'cuenta_usuario': usuario.nombre_cuenta_usuario,
                                 'id_rol': usuario.id_rol_usuario,
                                 'nombres_usuario': primer_nombre,
                                 'nombres_completos': usuario.nombres_usuario,
                                 'apellido_paterno': usuario.apellido_paterno_usuario,
                                 'apellido_materno': usuario.apellido_materno_usuario,
                                 'cargo_usuario': usuario.cargo_usuario,
                                 'carnet_usuario': usuario.carnet_usuario}
            token = create_access_token(identity=cuerpo_identidad)
            #refresh_token = create_refresh_token(identity=cuerpo_identidad)
            return token, usuario.id_rol_usuario
            #return token, refresh_token, usuario.id_rol_usuario
        elif respuesta==404:
            print("Usuario no encontrado")
            return respuesta, None
        else:
            print("Contraseña incorrecta")
            return respuesta, None