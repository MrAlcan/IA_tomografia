from app.configuraciones.extensiones import db, text
from app.servicios.serviciosUsuario import ServiciosUsuario


def iniciar_vistas():
    vista_usuarios_roles = ServiciosUsuario.obtener_vista_usuario_rol()
    if vista_usuarios_roles==None:
        db.session.execute(text('''
            CREATE VIEW usuarios_roles AS
            SELECT * 
            FROM usuarios
            INNER JOIN roles ON usuarios.id_usuario = roles.id_rol;
        '''))
        db.session.commit()