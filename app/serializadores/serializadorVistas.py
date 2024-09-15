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
    
    def serializar_pacientes_hoja_control(datos):
        if datos:
            lista_datos = []
            for paciente, hoja in datos:
                cuerpo = {
                    'id_hoja' : hoja.id_hoja_control,
                    'peso' : hoja.peso_paciente,
                    'talla' : hoja.talla_paciente,
                    'fecha' : hoja.fecha_control,
                    'numero_hoja' : hoja.numero_hoja,
                    'pieza' : hoja.pieza_paciente,
                    'id_paciente' : hoja.id_paciente_hoja,
                    'nombres' : paciente.nombres_paciente,
                    'apellido_paterno' : paciente.apellido_paterno_paciente,
                    'apellido_materno' : paciente.apellido_materno_paciente,
                    'carnet' : paciente.carnet_paciente,
                    'seguro' : paciente.seguro_paciente,
                    'fecha_nacimiento' : paciente.fecha_nacimiento_paciente,
                    'edad' : paciente.edad_paciente
                }
                lista_datos.append(cuerpo)
            return lista_datos
        else:
            return None