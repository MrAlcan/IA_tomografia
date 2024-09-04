class SerializadorControlEstado():
    def serializar(controles_estado):
        if controles_estado:
            lista_controles = []
            for control in controles_estado:
                cuerpo = {
                    'id_control' : control.id_control_estado,
                    'antibiotico' : control.antibiotico_estado,
                    'dias_internado' : control.dias_internado,
                    'fecha' : control.fecha_estado,
                    'dias_post' : control.dias_post_operatorio,
                    'id_hoja' : control.id_hoja_control_estado
                }
                lista_controles.append(cuerpo)
            return lista_controles
        else:
            return None
    
    def serializar_unico(control):
        if control:
            cuerpo = {
                'id_control' : control.id_control_estado,
                'antibiotico' : control.antibiotico_estado,
                'dias_internado' : control.dias_internado,
                'fecha' : control.fecha_estado,
                'dias_post' : control.dias_post_operatorio,
                'id_hoja' : control.id_hoja_control_estado
            }
            return cuerpo
        else:
            return None