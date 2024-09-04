class SerializadorPaciente():
    def serializar(pacientes):
        if pacientes:
            lista_pacientes = []
            for paciente in pacientes:
                cuerpo = {
                    'id_paciente' : paciente.id_paciente,
                    'nombres' : paciente.nombres_paciente,
                    'apellido_paterno' : paciente.apellido_paterno_paciente,
                    'apellido_materno' : paciente.apellido_materno_paciente,
                    'carnet' : paciente.carnet_paciente,
                    'seguro' : paciente.seguro_paciente,
                    'fecha_nacimiento' : paciente.fecha_nacimiento_paciente,
                    'paciente' : paciente.edad_paciente
                }
                lista_pacientes.append(cuerpo)
            return lista_pacientes
        else:
            return None
    
    def serializar_unico(paciente):
        if paciente:
            cuerpo = {
                'id_paciente' : paciente.id_paciente,
                'nombres' : paciente.nombres_paciente,
                'apellido_paterno' : paciente.apellido_paterno_paciente,
                'apellido_materno' : paciente.apellido_materno_paciente,
                'carnet' : paciente.carnet_paciente,
                'seguro' : paciente.seguro_paciente,
                'fecha_nacimiento' : paciente.fecha_nacimiento_paciente,
                'paciente' : paciente.edad_paciente
            }
            return cuerpo
        else:
            return None