class SerializadorRol():

    def serializar(roles):
        if roles:
            lista_roles = []
            for rol in roles:
                cuerpo = {
                    'id_rol': rol.id_rol,
                    'nombre': rol.nombre_rol,
                    'descripcion': rol.descripcion_rol
                }
                lista_roles.append(cuerpo)
            return lista_roles
        else:
            return None
        
    def serializar_unico(rol):
        if rol:
            cuerpo = {
                'id_rol': rol.id_rol,
                'nombre': rol.nombre_rol,
                'descripcion': rol.descripcion_rol
            }
            return cuerpo
        else:
            return None