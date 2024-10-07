from app.configuraciones.extensiones import db

class IndicacionesMedicas(db.Model):
    __tablename__ = 'indicaciones_medicas'

    id_indicaciones = db.Column(db.Integer, primary_key=True)
    fecha_indicaciones = db.Column(db.Date, nullable=False)
    hora_indicaciones = db.Column(db.Time, nullable=True)
    descripcion_indicaciones = db.Column(db.Text, nullable = False)
    id_doctor_cargo = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_consulta_indicaciones = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)

    def __init__(self, fecha, hora, descripcion, doctor_cargo, consulta):
        self.fecha_indicaciones = fecha
        self.hora_indicaciones = hora
        self.descripcion_indicaciones = descripcion
        self.id_doctor_cargo = doctor_cargo
        self.id_consulta_indicaciones = consulta