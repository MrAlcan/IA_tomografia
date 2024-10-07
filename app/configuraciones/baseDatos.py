from app.servicios.serviciosUsuario import ServiciosUsuario
from app.modelos.rol import Rol
from app.modelos.paciente import Paciente
from app.modelos.consulta import Consulta
from app.modelos.registroEnfermeria import RegistroEnfermeria
from app.configuraciones.extensiones import db
from datetime import date, time
from app.modelos.indicacionesMedicas import IndicacionesMedicas


def iniciar_datos():
    roles = Rol.query.all()
    pacientes = Paciente.query.all()
    enfermeria_registros = RegistroEnfermeria.query.all()
    consultas = Consulta.query.all()
    administrador = ServiciosUsuario.obtener_nombre(nombre='administrador')
   
    indicaciones_medicas = IndicacionesMedicas.query.all()
    if not roles:
        roles_nuevos = []
        roles_nuevos.append(Rol('Administrador','Administrador total del sistema'))
        roles_nuevos.append(Rol('Doctor (a)','Perito investigador encargado de recabar las imagenes'))
        roles_nuevos.append(Rol('Enfermero (a)','Experto en balistica'))
        db.session.add_all(roles_nuevos)
        db.session.commit()

    if not administrador:
        nuevo_administrador = ServiciosUsuario.crear('administrador', 'administrador', 'administrador', 'administrador', 'administrador', 'administrador', 'Administrador', 1)
        print("usuario admin creado")
    
    '''
    if not pacientes:
        paciente_nuevo = Paciente(
            nombres='1',
            apellido_paterno='1',
            apellido_materno='1',
            carnet='1',
            seguro='1',
            fecha_nacimiento=date(2000, 1, 1), 
            edad=1
        )
        db.session.add(paciente_nuevo)
        db.session.commit()


    if not consultas:
        consulta_nueva = Consulta(
            motivo='1',
            historia='1',
            enfermedades='1',
            tabaco='No',
            alcohol='No',
            drogas='No',
            diagnostico='1',
            tratamiento='1',
            doctor=1,  
            paciente=1,  
            internacion=0,
            codigo_consulta=1001,
            estado_consulta=1,
            fecha=date.today()
        )
        db.session.add(consulta_nueva)
        db.session.commit()

    

    if not enfermeria_registros:
        registro_nuevo = RegistroEnfermeria(
            procedimiento='Primer Procedimiento', 
            observaciones='Sin observaciones adicionales', 
            fecha=date.today(), 
            hora=time(9, 0),  
            enfermera=1,
            paciente=1  
        )
        db.session.add(registro_nuevo) 
        db.session.commit()  

    if not indicaciones_medicas:
        nueva_indicacion = IndicacionesMedicas(
            fecha=date.today(), 
            hora=time(10, 0),  
            descripcion='Indicaciones iniciales para el paciente',  
            doctor_cargo=1,  
            paciente=1  
        )
        db.session.add(nueva_indicacion) 
        db.session.commit() '''