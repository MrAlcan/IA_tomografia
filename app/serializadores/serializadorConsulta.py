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
                    'id_paciente' : consulta.id_paciente_consulta
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
                'id_paciente' : consulta.id_paciente_consulta
            }
            return cuerpo
        else:
            return None