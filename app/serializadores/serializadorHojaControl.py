class SerializadorHojaControl():
    def serializar(hojas_control):
        if hojas_control:
            lista_hojas_control = []
            for hoja in hojas_control:
                cuerpo = {
                    'id_hoja' : hoja.id_hoja_control,
                    'peso' : hoja.peso_paciente,
                    'talla' : hoja.talla_paciente,
                    'servicio' : hoja.servicio_paciente,
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
                'servicio' : hoja.servicio_paciente,
                'numero_hoja' : hoja.numero_hoja,
                'pieza' : hoja.pieza_paciente,
                'id_paciente' : hoja.id_paciente_hoja
            }
            return cuerpo
        else:
            return None
    
    def serializar_pacientes_hoja_control(datos):
        if datos:
            lista_datos = []
            for paciente, hoja in datos:
                cuerpo = {
                    'id_hoja' : hoja.id_hoja_control,
                    'peso' : hoja.peso_paciente,
                    'talla' : hoja.talla_paciente,
                    'servicio' : hoja.servicio_paciente,
                    'numero_hoja' : hoja.numero_hoja,
                    'pieza' : hoja.pieza_paciente,
                    'id_paciente' : hoja.id_paciente_hoja,
                    'nombres' : paciente.nombres_paciente,
                    'apellido_paterno' : paciente.apellido_paterno_paciente,
                    'apellido_materno' : paciente.apellido_materno_paciente,
                    'carnet' : paciente.carnet_paciente,
                    'seguro' : paciente.seguro_paciente,
                    'fecha_nacimiento' : paciente.fecha_nacimiento_paciente,
                    'edad' : paciente.edad_paciente
                }
                lista_datos.append(cuerpo)
            return lista_datos
        else:
            return None
    
    def serializar_pacientes_hoja_control_unico(datos):
        if datos:
            #print(datos[0])
            cuerpo = {
                    'id_hoja' : datos[1].id_hoja_control,
                    'peso' : datos[1].peso_paciente,
                    'talla' : datos[1].talla_paciente,
                    'servicio' : datos[1].servicio_paciente,
                    'numero_hoja' : datos[1].numero_hoja,
                    'pieza' : datos[1].pieza_paciente,
                    'id_paciente' : datos[1].id_paciente_hoja,
                    'nombres' : datos[0].nombres_paciente,
                    'apellido_paterno' : datos[0].apellido_paterno_paciente,
                    'apellido_materno' : datos[0].apellido_materno_paciente,
                    'carnet' : datos[0].carnet_paciente,
                    'seguro' : datos[0].seguro_paciente,
                    'fecha_nacimiento' : datos[0].fecha_nacimiento_paciente,
                    'edad' : datos[0].edad_paciente
            }

            return cuerpo
        else:
            return None