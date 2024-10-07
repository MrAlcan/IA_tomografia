class SerializadorRegistroEnfermeria():
    def serializar(registros):
        if registros:
            lista_registros = []
            for registro in registros:
                cuerpo = {
                    'id_registro' : registro.id_registro_enfermeria,
                    'procedimiento' : registro.procedimiento_enfermeria,
                    'observaciones' : registro.observaciones_enfermeria,
                    'fecha' : registro.fecha_registro,
                    'hora' : registro.hora_registro,
                    'id_enfermera' : registro.id_enfermera_cargo,
                    'id_consulta_registro' : registro.id_consulta_registro
                }
                lista_registros.append(cuerpo)
            return lista_registros
        else:
            return None
        
    def serializar_unico(registro):
        if registro:
            cuerpo = {
                'id_registro' : registro.id_registro_enfermeria,
                'procedimiento' : registro.procedimiento_enfermeria,
                'observaciones' : registro.observaciones_enfermeria,
                'fecha' : registro.fecha_registro,
                'hora' : registro.hora_registro,
                'id_enfermera' : registro.id_enfermera_cargo,
                'id_consulta_registro' : registro.id_consulta_registro
            }
            return cuerpo
        else:
            return None
        
    def serializar_todos_vista(datos):
        if datos:
            lista_consultas = []
            for paciente, registros, usuario in datos:
                cuerpo = {
                    'id_enf' : registros.id_registro_enfermeria,
                    'fecha_enf' : registros.fecha_registro,
                    'hora_enf' : registros.hora_registro,
                    'observaciones_enf' : registros.observaciones_enfermeria,
                    'procedimiento_enf' : registros.procedimiento_enfermeria,
                    'id_paciente': paciente.id_paciente,
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
    
    

    def serializar_unica_vista(datos):
        if datos:
            
            cuerpo = {
                    'nombres_paciente' : datos[0].nombres_paciente,
                    'apellido_paterno_paciente' : datos[0].apellido_paterno_paciente,
                    'apellido_materno_paciente' : datos[0].apellido_materno_paciente,
                    'carnet_paciente' : datos[0].carnet_paciente,
                    'seguro_paciente' : datos[0].seguro_paciente,
                    'fecha_nacimiento_paciente' : datos[0].fecha_nacimiento_paciente,
                    'edad_paciente' : datos[0].edad_paciente,
                    
                    'fecha_enf' : datos[1].fecha_registro,
                    'hora_enf' : datos[1].hora_registro,
                    'observaciones_enf' : datos[1].observaciones_enfermeria,
                    'procedimiento_enf' : datos[1].procedimiento_enfermeria,
                    'nombres_usuario' : datos[2].nombres_usuario,
                    'apellido_paterno_usuario' : datos[2].apellido_paterno_usuario,
                    'apellido_materno_usuario' : datos[2].apellido_materno_usuario,
                    'carnet_usuario' : datos[2].carnet_usuario,
                    'cargo_usuario' : datos[2].cargo_usuario,
                    'id_rol_usuario' : datos[2].id_rol_usuario
            }
                
            return cuerpo
        else:
            return None
        

    def serializar_unico(consulta):
        if consulta:
            cuerpo = {
                'id_enf' : consulta.id_registro_enfermeria,
                'fecha_enf' : consulta.fecha_registro,
                'hora_enf' : consulta.hora_registro,
                'observaciones_enf' : consulta.observaciones_enfermeria,
                'procedimiento_enf' : consulta.procedimiento_enfermeria,
                'enfermera': consulta.id_enfermera_cargo,
                'id_pcaiente': consulta.id_paciente
            }
            return cuerpo
        else:
            return None