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