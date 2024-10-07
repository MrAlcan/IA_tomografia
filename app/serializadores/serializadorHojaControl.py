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
                    'id_paciente' : hoja.id_paciente_hoja,
                    'id_consulta' : hoja.id_consulta_hoja
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
                'id_paciente' : hoja.id_paciente_hoja,
                'id_consulta' : hoja.id_consulta_hoja
            }
            return cuerpo
        else:
            return None
    
    def serializar_pacientes_hoja_control(datos):
        if datos:
            lista_datos = []
            for paciente, hoja, consulta in datos:
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
                    'edad' : paciente.edad_paciente,
                    'id_consulta' : hoja.id_consulta_hoja,
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
                    'codigo_consulta' : consulta.codigo_consulta,
                    'estado_consulta' : consulta.estado_consulta,
                    'fecha' : consulta.fecha_consulta
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
                    'edad' : datos[0].edad_paciente,
                    'id_consulta' : datos[1].id_consulta_hoja,
                    'motivo' : datos[2].motivo_consulta,
                    'historia_enfermedad' : datos[2].historia_enfermedad_actual,
                    'enfermedades' : datos[2].enfermedades_consulta,
                    'tabaco' : datos[2].consumo_tabaco,
                    'alcohol' : datos[2].consumo_alcohol,
                    'drogas' : datos[2].consumo_drogas,
                    'diagnostico' : datos[2].diagnostico_consulta,
                    'tratamiento' : datos[2].tratamiento_consulta,
                    'internacion' : datos[2].internacion_consulta,
                    'id_doctor' : datos[2].id_doctor_tratante,
                    'codigo_consulta' : datos[2].codigo_consulta,
                    'estado_consulta' : datos[2].estado_consulta,
                    'fecha' : datos[2].fecha_consulta
            }

            return cuerpo
        else:
            return None