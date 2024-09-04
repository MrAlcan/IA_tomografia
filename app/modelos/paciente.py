from app.configuraciones.extensiones import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id_paciente = db.Column(db.Integer, primary_key=True)
    nombres_paciente = db.Column(db.String(30), nullable=False)
    apellido_paterno_paciente = db.Column(db.String(15), nullable=False)
    apellido_materno_paciente = db.Column(db.String(15), nullable=True)
    carnet_paciente = db.Column(db.String(20), nullable=True)
    seguro_paciente = db.Column(db.String(50), nullable=True)
    fecha_nacimiento_paciente = db.Column(db.Date, nullable=True)
    edad_paciente = db.Column(db.Integer, nullable=True)

    def __init__(self, nombres, apellido_paterno, apellido_materno, carnet, seguro, fecha_nacimiento, edad):
        self.nombres_paciente = nombres
        self.apellido_paterno_paciente = apellido_paterno
        self.apellido_materno_paciente = apellido_materno
        self.carnet_paciente = carnet
        self.seguro_paciente = seguro
        self.fecha_nacimiento_paciente = fecha_nacimiento
        self.edad_paciente = edad
        
    