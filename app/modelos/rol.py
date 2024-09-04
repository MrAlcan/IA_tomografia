from app.configuraciones.extensiones import db

class Rol(db.Model):
    __tablename__ = 'roles'

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), nullable=False)
    descripcion_rol = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, descripcion):
        self.nombre_rol = nombre
        self.descripcion_rol = descripcion