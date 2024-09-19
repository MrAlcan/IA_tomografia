from app.configuraciones.extensiones import db
from app.modelos.paciente import Paciente
from app.modelos.usuario import Usuario
from app.modelos.consulta import Consulta

class ResultadoEstudio(db.Model):
    __tablename__ = 'resultado_estudios'

    id_resultado = db.Column(db.Integer, primary_key=True)
    fecha_estudio = db.Column(db.Date, nullable=True)
    ruta_carpeta_imagenes_estudio = db.Column(db.String(255), nullable=True)
    resultado_estudio = db.Column(db.Integer, default=0, nullable=True)
    id_doctor_estudio = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_paciente_estudio = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_consulta_estudio = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)

    # Relaciones
    doctor = db.relationship('Usuario', backref='resultados')
    paciente = db.relationship('Paciente', backref='resultados')
    consulta = db.relationship('Consulta', backref='resultados')

    def __init__(self, fecha, ruta, doctor, paciente, consulta, resultado=None):
        self.fecha_estudio = fecha
        self.ruta_carpeta_imagenes_estudio = ruta
        self.resultado_estudio = resultado
        self.id_doctor_estudio = doctor
        self.id_paciente_estudio = paciente
        self.id_consulta_estudio = consulta
