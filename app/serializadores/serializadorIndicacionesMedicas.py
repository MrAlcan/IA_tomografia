class SerializadorIndicacionesMedicas():
    def serializar(indicaciones):
        if indicaciones:
            lista_indicaciones = []
            for indicacion in indicaciones:
                cuerpo = {
                    'id_indicacion' : indicacion.id_indicaciones,
                    'fecha' : indicacion.fecha_indicaciones,
                    'hora' : indicacion.hora_indicaciones,
                    'descripcion' : indicacion.descripcion_indicaciones,
                    'id_doctor' : indicacion.id_doctor_cargo,
                    'id_paciente' : indicacion.id_paciente_indicaciones,
                    'id_consulta' : indicacion.id_consulta_indicaciones
                }
                lista_indicaciones.append(cuerpo)
            return lista_indicaciones
        else:
            return None
    
    def serializar_unico(indicacion):
        if indicacion:
            cuerpo = {
                'id_indicacion' : indicacion.id_indicaciones,
                'fecha' : indicacion.fecha_indicaciones,
                'hora' : indicacion.hora_indicaciones,
                'descripcion' : indicacion.descripcion_indicaciones,
                'id_doctor' : indicacion.id_doctor_cargo,
                'id_paciente' : indicacion.id_paciente_indicaciones,
                'id_consulta' : indicacion.id_consulta_indicaciones
            }
            return cuerpo
        else:
            return None
        
    def serializar_todos_vista(datos):
        if datos:
            lista_consultas = []
            for paciente, registros, usuario in datos:
                cuerpo = {
                    'id_indicacion' : registros.id_indicaciones,
                    'fecha_ind' : registros.fecha_indicaciones,
                    'hora_ind' : registros.hora_indicaciones,
                    'id_paciente': registros.id_paciente_indicaciones,
                    'desc_ind' : registros.descripcion_indicaciones,
                    'consulta_ind' : registros.id_consulta_indicaciones,
                    'nombres_paciente' : paciente.nombres_paciente,
                    'apellido_paterno_paciente' : paciente.apellido_paterno_paciente,
                    'apellido_materno_paciente' : paciente.apellido_materno_paciente,
                    'carnet_paciente' : paciente.carnet_paciente,
                    'seguro_paciente' : paciente.seguro_paciente,
                    'fecha_nacimiento_paciente' : paciente.fecha_nacimiento_paciente,
                    'edad_paciente' : paciente.edad_paciente,
                    'nombres_usuario' : usuario.nombres_usuario,
                    'apellido_paterno_usuario' : usuario.apellido_paterno_usuario,
                    'apellido_materno_usuario' : usuario.apellido_materno_usuario,
                    'carnet_usuario' : usuario.carnet_usuario,
                    'cargo_usuario' : usuario.cargo_usuario,
                    'id_rol_usuario' : usuario.id_rol_usuario
                }
                lista_consultas.append(cuerpo)
            return lista_consultas
        else:
            return None