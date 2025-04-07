class ResultadoEstudioSchema:
    def serializar(resultados):
        if resultados:
            lista_resultados = []
            for resultado in resultados:
                cuerpo = {
                    'id_resultado': resultado.id_resultado,
                    'fecha_estudio': resultado.fecha_estudio,
                    'ruta_carpeta_imagenes_estudio': resultado.ruta_carpeta_imagenes_estudio,
                    'resultado_estudio': resultado.resultado_estudio,
                    'id_doctor_estudio': resultado.id_doctor_estudio,
                    'id_paciente_estudio': resultado.id_paciente_estudio,
                    'id_consulta_estudio': resultado.id_consulta_estudio
                }
                lista_resultados.append(cuerpo)
            return lista_resultados
        else:
            return None
    
    def serializar_unico(resultado):
        if resultado:
            cuerpo = {
                'id_resultado': resultado.id_resultado,
                'fecha_estudio': resultado.fecha_estudio,
                'ruta_carpeta_imagenes_estudio': resultado.ruta_carpeta_imagenes_estudio,
                'resultado_estudio': resultado.resultado_estudio,
                'id_doctor_estudio': resultado.id_doctor_estudio,
                'id_paciente_estudio': resultado.id_paciente_estudio,
                'id_consulta_estudio': resultado.id_consulta_estudio
            }
            return cuerpo
        else:
            return None
        
    def serializar_todos_vista(datos):
        if datos:
            lista_consultas = []
            for paciente, registros, usuario in datos:
                cuerpo = {
                    'id_resultado': registros.id_resultado,
                    'fecha_estudio': registros.fecha_estudio,
                    'ruta_carpeta_imagenes_estudio': registros.ruta_carpeta_imagenes_estudio,
                    'resultado_estudio': registros.resultado_estudio,
                    'id_doctor_estudio': registros.id_doctor_estudio,
                    'id_paciente_estudio': registros.id_paciente_estudio,
                    'id_consulta_estudio': registros.id_consulta_estudio,
                    'id_diagnostico': registros.id_diagnostico,
                    'probabilidad': registros.probabilidad,
                    
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
