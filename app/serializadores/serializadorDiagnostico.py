class SerializadorDiagnostico:
    def serializar(resultados):
        if resultados:
            lista_resultados = []
            for resultado in resultados:
                cuerpo = {
                    'id_diagnostico': resultado.id_diagnostico,
                    'fecha_diagnostico': resultado.fecha_diagnostico,
                    'ruta_carpeta_diagnostico': resultado.ruta_carpeta_diagnostico,
                    'resultado_diagnostico': resultado.resultado_diagnostico,
                    'id_doctor_diagnostico': resultado.id_doctor_diagnostico,
                    'id_paciente_diagnostico': resultado.id_paciente_diagnostico,
                    'id_consulta_diagnostico': resultado.id_consulta_diagnostico
                }
                lista_resultados.append(cuerpo)
            return lista_resultados
        else:
            return None
    
    def serializar_unico(resultado):
        if resultado:
            cuerpo = {
                'id_diagnostico': resultado.id_diagnostico,
                'fecha_diagnostico': resultado.fecha_diagnostico,
                'ruta_carpeta_diagnostico': resultado.ruta_carpeta_diagnostico,
                'resultado_diagnostico': resultado.resultado_diagnostico,
                'id_doctor_diagnostico': resultado.id_doctor_diagnostico,
                'id_paciente_diagnostico': resultado.id_paciente_diagnostico,
                'id_consulta_diagnostico': resultado.id_consulta_diagnostico
            }
            return cuerpo
        else:
            return None
        
    def serializar_todos_vista(datos):
        if datos:
            lista_consultas = []
            for paciente, registros, usuario in datos:
                cuerpo = {
                    'id_diagnostico': registros.id_diagnostico,
                    'fecha_diagnostico': registros.fecha_diagnostico,
                    'ruta_carpeta_diagnostico': registros.ruta_carpeta_diagnostico,
                    'resultado_diagnostico': registros.resultado_diagnostico,
                    'id_doctor_diagnostico': registros.id_doctor_diagnostico,
                    'id_paciente_diagnostico': registros.id_paciente_diagnostico,
                    'id_consulta_diagnostico': registros.id_consulta_diagnostico,
                
                    
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
