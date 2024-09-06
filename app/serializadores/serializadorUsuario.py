class SerializadorUsuario():
    def serializar(usuarios):
        if usuarios:
            lista_usuarios = []
            for usuario in usuarios:
                cuerpo = {
                    'id_usuario' : usuario.id_usuario,
                    'cuenta' : usuario.nombre_cuenta_usuario,
                    'contrasena' : usuario.contrasena_usuario,
                    'nombres' : usuario.nombres_usuario,
                    'apellido_paterno' : usuario.apellido_paterno_usuario,
                    'apellido_materno' : usuario.apellido_materno_usuario,
                    'carnet' : usuario.carnet_usuario,
                    'cargo' : usuario.cargo_usuario,
                    'id_rol' : usuario.id_rol_usuario
                }
                lista_usuarios.append(cuerpo)
            return lista_usuarios
        else:
            return None
    
    def serializar_unico(usuario):
        if usuario:
            cuerpo = {
                'id_usuario' : usuario.id_usuario,
                'cuenta' : usuario.nombre_cuenta_usuario,
                'contrasena' : usuario.contrasena_usuario,
                'nombres' : usuario.nombres_usuario,
                'apellido_paterno' : usuario.apellido_paterno_usuario,
                'apellido_materno' : usuario.apellido_materno_usuario,
                'carnet' : usuario.carnet_usuario,
                'cargo' : usuario.cargo_usuario,
                'id_rol' : usuario.id_rol_usuario
            }
            return cuerpo
        else:
            return None
    
    def serializar_usuarios_roles(usuarios):
        if usuarios:
            lista_usuarios = []
            for usuario in usuarios:
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
                    'nombre_rol': usuario.nombre_rol
                }
                lista_usuarios.append(cuerpo)
            return lista_usuarios
        else:
            return None