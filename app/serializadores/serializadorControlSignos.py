class SerializadorControlSignos():
    def serializar(controles_signos):
        if controles_signos:
            lista_controles = []
            for control in controles_signos:
                cuerpo = {
                    'id_control_signos' : control.id_control_signos,
                    'fecha' : control.fecha_control,
                    'hora' : control.hora_control,
                    'presion_sistolica' : control.presion_sistolica_control,
                    'presion_diastolica' : control.presion_diastolica_control,
                    'respiracion' : control.respiracion_control,
                    'saturacion' : control.saturacion_control,
                    'diuresis' : control.diuresis_control,
                    'catarsis' : control.catarsis_control,
                    'id_hoja' : control.id_hoja_signos,
                    'id_registro_enfermeria' : control.id_registro_control
                }
                lista_controles.append(cuerpo)
            return lista_controles
        else:
            return None
        
    def serializar_unico(control):
        if control:
            cuerpo = {
                'id_control_signos' : control.id_control_signos,
                'fecha' : control.fecha_control,
                'hora' : control.hora_control,
                'presion_sistolica' : control.presion_sistolica_control,
                'presion_diastolica' : control.presion_diastolica_control,
                'respiracion' : control.respiracion_control,
                'saturacion' : control.saturacion_control,
                'diuresis' : control.diuresis_control,
                'catarsis' : control.catarsis_control,
                'id_hoja' : control.id_hoja_signos,
                'id_registro_enfermeria' : control.id_registro_control
            }
            return cuerpo
        else:
            return None