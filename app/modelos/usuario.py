from app.configuraciones.extensiones import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_cuenta_usuario = db.Column(db.String(50), nullable=False)
    contrasena_usuario = db.Column(db.String(255), nullable=False)
    nombres_usuario = db.Column(db.String(30), nullable =False)
    apellido_paterno_usuario = db.Column(db.String(15), nullable=False)
    apellido_materno_usuario = db.Column(db.String(15), nullable=False)
    carnet_usuario = db.Column(db.String(20), nullable=False)
    cargo_usuario = db.Column(db.String(30), nullable=False)
    id_rol_usuario = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)

    def __init__(self, nombre_cuenta, contrasena, nombres, apellido_paterno, apellido_materno, carnet, cargo, rol):
        self.nombre_cuenta_usuario = nombre_cuenta
        self.contrasena_usuario = contrasena
        self.nombres_usuario = nombres
        self.apellido_paterno_usuario = apellido_paterno
        self.apellido_materno_usuario = apellido_materno
        self.carnet_usuario = carnet
        self.cargo_usuario = cargo
        self.id_rol_usuario = rol