class SerializadorHojaControl():
    def serializar(hojas_control):
        if hojas_control:
            lista_hojas_control = []
            for hoja in hojas_control:
                cuerpo = {
                    'id_hoja' : hoja.id_hoja_control,
                    'peso' : hoja.peso_paciente,
                    'talla' : hoja.talla_paciente,
                    'fecha' : hoja.fecha_control,
                    'numero_hoja' : hoja.numero_hoja,
                    'pieza' : hoja.pieza_paciente,
                    'id_paciente' : hoja.id_paciente_hoja
                }
                lista_hojas_control.append(cuerpo)
            return lista_hojas_control
        else:
            return None
    
    def serializar_unico(hoja):
        if hoja:
            cuerpo = {
                'id_hoja' : hoja.id_hoja_control,
                'peso' : hoja.peso_paciente,
                'talla' : hoja.talla_paciente,
                'fecha' : hoja.fecha_control,
                'numero_hoja' : hoja.numero_hoja,
                'pieza' : hoja.pieza_paciente,
                'id_paciente' : hoja.id_paciente_hoja
            }
            return cuerpo
        else:
            return None