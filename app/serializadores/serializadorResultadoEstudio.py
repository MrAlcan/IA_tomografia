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
