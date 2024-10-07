from app.configuraciones.extensiones import db
from app.modelos.paciente import Paciente
from app.modelos.usuario import Usuario
from app.modelos.consulta import Consulta

class Diagnostico(db.Model):
    __tablename__ = 'diagnostico'

    id_diagnostico = db.Column(db.Integer, primary_key=True)
    fecha_diagnostico = db.Column(db.Date, nullable=True)
    ruta_carpeta_diagnostico = db.Column(db.String(255), nullable=True)
    resultado_diagnostico = db.Column(db.Integer, default=0, nullable=True)
    id_doctor_diagnostico= db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_paciente_diagnostico = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_consulta_diagnostico  = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)
    # Relaciones
    doctor = db.relationship('Usuario', backref='resultados')
    paciente = db.relationship('Paciente', backref='resultados')
    consulta = db.relationship('Consulta', backref='resultados')

    def __init__(self, fecha, ruta, doctor, paciente, consulta, resultado=None):
        self.fecha_diagnostico = fecha
        self.ruta_carpeta_diagnostico = ruta
        self.resultado_diagnostico = resultado
        self.id_doctor_diagnostico = doctor
        self.id_paciente_diagnostico= paciente
        self.id_consulta_diagnostico = consulta
