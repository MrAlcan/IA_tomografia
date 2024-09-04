class SerializadorResultadoEstudio():
    def serializar(resultados):
        if resultados:
            lista_resultados = []
            for resultado in resultados:
                cuerpo = {
                    'id_resultado' : resultado.id_resultado,
                    'fecha' : resultado.fecha_estudio,
                    'ruta_carpeta' : resultado.ruta_carpeta_imagenes_estudio,
                    'resultado' : resultado.resultado_estudio,
                    'id_doctor' : resultado.id_doctor_estudio,
                    'id_paciente' : resultado.id_paciente_estudio,
                    'id_consulta' : resultado.id_consulta_estudio
                }
                lista_resultados.append(cuerpo)
            return lista_resultados
        else:
            return None
    
    def serializar_unico(resultado):
        if resultado:
            cuerpo = {
                'id_resultado' : resultado.id_resultado,
                'fecha' : resultado.fecha_estudio,
                'ruta_carpeta' : resultado.ruta_carpeta_imagenes_estudio,
                'resultado' : resultado.resultado_estudio,
                'id_doctor' : resultado.id_doctor_estudio,
                'id_paciente' : resultado.id_paciente_estudio,
                'id_consulta' : resultado.id_consulta_estudio
            }
            return cuerpo
        else:
            return None