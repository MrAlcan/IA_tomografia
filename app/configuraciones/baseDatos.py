from app.servicios.servUsuarios import ServiciosUsuario
from app.modelos.grado import Grado
from app.modelos.rol import Rol
from app.configuraciones.extensiones import db

def iniciar_datos():
    grados = Grado.query.all()
    roles = Rol.query.all()
    administrador = ServiciosUsuario.obtener_nombre(nombre='administrador')

    if not grados:
        grados_nuevos = []
        grados_nuevos.append(Grado('General', 'General ...', 'Gral.'))
        grados_nuevos.append(Grado('General de Brigada', 'General de Brigada ...', 'Gral. de Brig.'))
        grados_nuevos.append(Grado('General de Division ...', 'General de Division ...', 'Gral. de Div.'))
        grados_nuevos.append(Grado('Coronel', 'Coronel ...', 'Cnl.'))
        grados_nuevos.append(Grado('Teniente Coronel', 'Teniente Coronel ...', 'Tcnel.'))
        grados_nuevos.append(Grado('Mayor', 'Mayor ...', 'My.'))
        grados_nuevos.append(Grado('Capitan', 'Capitan ...', 'Cap.'))
        grados_nuevos.append(Grado('Teniente', 'Teniente ...', 'Tte.'))
        grados_nuevos.append(Grado('Subteniente', 'Subteniente ...', 'Sbtte.'))
        grados_nuevos.append(Grado( 'Suboficial Maestre', 'Suboficial Maestre ...', 'Sof. Mtre.'))
        grados_nuevos.append(Grado( 'Suboficial Mayor', 'Suboficial Mayor ...', 'Sof. My.'))
        grados_nuevos.append(Grado( 'Suboficial Primero', 'Suboficial Primero ...', 'Sof. 1°'))
        grados_nuevos.append(Grado( 'Suboficial Segundo', 'Suboficial Segundo ...', 'Sof. 2°'))
        grados_nuevos.append(Grado( 'Suboficial Inicial', 'Suboficial Inicial ...', 'Sof. In.'))
        grados_nuevos.append(Grado( 'Sargento Primero', 'Sargento Primero ...', 'Sgto. 1°'))
        grados_nuevos.append(Grado( 'Sargento Segundo', 'Sargento Segundo ...', 'Sgto. 2°'))
        grados_nuevos.append(Grado( 'Sargento Inicial', 'Sargento Inicial ...', 'Sgto. In.'))
        grados_nuevos.append(Grado( 'Civil', 'Civil ...', 'Civ.'))
        grados_nuevos.append(Grado( 'Ingeniero', 'Ingeniero ...', 'Ing.'))
        grados_nuevos.append(Grado( 'Licenciado', 'Licenciado ...', 'Lic.'))
        grados_nuevos.append(Grado( 'Doctor', 'Doctor ...', 'Doc.'))
        db.session.add_all(grados_nuevos)
        db.session.commit()

    if not roles:
        roles_nuevos = []
        roles_nuevos.append(Rol('Administrador','Administrador total del sistema'))
        roles_nuevos.append(Rol('Perito','Perito investigador encargado de recabar las imagenes'))
        roles_nuevos.append(Rol('Experto','Experto en balistica'))
        roles_nuevos.append(Rol('Usuario','Usuario normal'))
        db.session.add_all(roles_nuevos)
        db.session.commit()

    if not administrador:
        nuevo_administrador = ServiciosUsuario.crear('administrador', 'administrador', 'administrador', 'administrador', 'administrador', 'administrador', 1, 19, 1)
        print("usuario admin creado")

