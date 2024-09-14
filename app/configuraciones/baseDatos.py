from app.servicios.serviciosUsuario import ServiciosUsuario
from app.modelos.rol import Rol
from app.configuraciones.extensiones import db

def iniciar_datos():
    roles = Rol.query.all()
    administrador = ServiciosUsuario.obtener_nombre(nombre='administrador')

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

