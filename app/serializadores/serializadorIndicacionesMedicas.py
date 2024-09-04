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
                    'id_paciente' : indicacion.id_paciente_indicaciones
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
                'id_paciente' : indicacion.id_paciente_indicaciones
            }
            return cuerpo
        else:
            return None