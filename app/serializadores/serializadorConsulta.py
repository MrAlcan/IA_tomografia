class SerializadorConsulta():
    def serializar(consultas):
        if consultas:
            lista_consultas = []
            for consulta in consultas:
                cuerpo = {
                    'id_consulta' : consulta.id_consulta,
                    'motivo' : consulta.motivo_consulta,
                    'historia_enfermedad' : consulta.historia_enfermedad_actual,
                    'enfermedades' : consulta.enfermedades_consulta,
                    'tabaco' : consulta.consumo_tabaco,
                    'alcohol' : consulta.consumo_alcohol,
                    'drogas' : consulta.consumo_drogas,
                    'diagnostico' : consulta.diagnostico_consulta,
                    'tratamiento' : consulta.tratamiento_consulta,
                    'internacion' : consulta.internacion_consulta,
                    'id_doctor' : consulta.id_doctor_tratante,
                    'id_paciente' : consulta.id_paciente_consulta,
                    'codigo_consulta' : consulta.codigo_consulta,
                    'estado_consulta' : consulta.estado_consulta,
                    'fecha' : consulta.fecha_consulta
                }
                lista_consultas.append(cuerpo)
            return lista_consultas
        else:
            return None
    
    def serializar_unico(consulta):
        if consulta:
            cuerpo = {
                'id_consulta' : consulta.id_consulta,
                'motivo' : consulta.motivo_consulta,
                'historia_enfermedad' : consulta.historia_enfermedad_actual,
                'enfermedades' : consulta.enfermedades_consulta,
                'tabaco' : consulta.consumo_tabaco,
                'alcohol' : consulta.consumo_alcohol,
                'drogas' : consulta.consumo_drogas,
                'diagnostico' : consulta.diagnostico_consulta,
                'tratamiento' : consulta.tratamiento_consulta,
                'internacion' : consulta.internacion_consulta,
                'id_doctor' : consulta.id_doctor_tratante,
                'id_paciente' : consulta.id_paciente_consulta,
                'codigo_consulta' : consulta.codigo_consulta,
                'estado_consulta' : consulta.estado_consulta,
                'fecha' : consulta.fecha_consulta
            }
            return cuerpo
        else:
            return None
    
    def serializar_todos_vista(datos):
        if datos:
            lista_consultas = []
            for paciente, consulta, usuario in datos:
                cuerpo = {
                    'id_consulta' : consulta.id_consulta,
                    'motivo' : consulta.motivo_consulta,
                    'historia_enfermedad' : consulta.historia_enfermedad_actual,
                    'enfermedades' : consulta.enfermedades_consulta,
                    'tabaco' : consulta.consumo_tabaco,
                    'alcohol' : consulta.consumo_alcohol,
                    'drogas' : consulta.consumo_drogas,
                    'diagnostico' : consulta.diagnostico_consulta,
                    'tratamiento' : consulta.tratamiento_consulta,
                    'internacion' : consulta.internacion_consulta,
                    'id_doctor' : consulta.id_doctor_tratante,
                    'id_paciente' : consulta.id_paciente_consulta,
                    'codigo_consulta' : consulta.codigo_consulta,
                    'estado_consulta' : consulta.estado_consulta,
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
                    'id_rol_usuario' : usuario.id_rol_usuario,
                    'fecha' : consulta.fecha_consulta
                }
                lista_consultas.append(cuerpo)
            return lista_consultas
        else:
            return None
    
    def serializar_unica_vista(datos):
        if datos:
            
            cuerpo = {
                    'id_consulta' : datos[1].id_consulta,
                    'motivo' : datos[1].motivo_consulta,
                    'historia_enfermedad' : datos[1].historia_enfermedad_actual,
                    'enfermedades' : datos[1].enfermedades_consulta,
                    'tabaco' : datos[1].consumo_tabaco,
                    'alcohol' : datos[1].consumo_alcohol,
                    'drogas' : datos[1].consumo_drogas,
                    'diagnostico' : datos[1].diagnostico_consulta,
                    'tratamiento' : datos[1].tratamiento_consulta,
                    'internacion' : datos[1].internacion_consulta,
                    'id_doctor' : datos[1].id_doctor_tratante,
                    'id_paciente' : datos[1].id_paciente_consulta,
                    'codigo_consulta' : datos[1].codigo_consulta,
                    'estado_consulta' : datos[1].estado_consulta,
                    'nombres_paciente' : datos[0].nombres_paciente,
                    'apellido_paterno_paciente' : datos[0].apellido_paterno_paciente,
                    'apellido_materno_paciente' : datos[0].apellido_materno_paciente,
                    'carnet_paciente' : datos[0].carnet_paciente,
                    'seguro_paciente' : datos[0].seguro_paciente,
                    'fecha_nacimiento_paciente' : datos[0].fecha_nacimiento_paciente,
                    'edad_paciente' : datos[0].edad_paciente,
                    'nombres_usuario' : datos[2].nombres_usuario,
                    'apellido_paterno_usuario' : datos[2].apellido_paterno_usuario,
                    'apellido_materno_usuario' : datos[2].apellido_materno_usuario,
                    'carnet_usuario' : datos[2].carnet_usuario,
                    'cargo_usuario' : datos[2].cargo_usuario,
                    'id_rol_usuario' : datos[2].id_rol_usuario,
                    'fecha' : datos[1].fecha_consulta
            }
                
            return cuerpo
        else:
            return None