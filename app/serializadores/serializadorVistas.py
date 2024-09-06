class SerializadorVistas:
    def serializar_usuarios_roles(datos):
        if datos:
            lista_datos = []
            for rol, usuario in datos:
                cuerpo = {
                    'id_usuario' : usuario.id_usuario,
                    'cuenta' : usuario.nombre_cuenta_usuario,
                    'contrasena' : usuario.contrasena_usuario,
                    'nombres' : usuario.nombres_usuario,
                    'apellido_paterno' : usuario.apellido_paterno_usuario,
                    'apellido_materno' : usuario.apellido_materno_usuario,
                    'carnet' : usuario.carnet_usuario,
                    'cargo' : usuario.cargo_usuario,
                    'id_rol' : usuario.id_rol_usuario,
                    'nombre_rol' : rol.nombre_rol
                }
                lista_datos.append(cuerpo)
            return lista_datos
        else:
            return None