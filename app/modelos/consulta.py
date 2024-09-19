from app.configuraciones.extensiones import db

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id_consulta = db.Column(db.Integer, primary_key=True)
    motivo_consulta = db.Column(db.Text, nullable=False)
    historia_enfermedad_actual = db.Column(db.Text, nullable=False)
    enfermedades_consulta = db.Column(db.String(200), nullable=True)
    consumo_tabaco = db.Column(db.String(10), nullable=True)
    consumo_alcohol = db.Column(db.String(10), nullable=True)
    consumo_drogas = db.Column(db.String(10), nullable=True)
    diagnostico_consulta = db.Column(db.Text, nullable=True)
    tratamiento_consulta = db.Column(db.Text, nullable=True)
    internacion_consulta = db.Column(db.Integer, default=0, nullable=True)
    id_doctor_tratante = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_paciente_consulta = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    codigo_consulta = db.Column(db.Integer, default=0, nullable=True)
    estado_consulta = db.Column(db.Integer, default=1, nullable=True)

    def __init__(self, motivo, historia, enfermedades, tabaco, alcohol, drogas, diagnostico, tratamiento, doctor, paciente, internacion, codigo_consulta ,estado_consulta):
        self.motivo_consulta = motivo
        self.historia_enfermedad_actual = historia
        self.enfermedades_consulta = enfermedades
        self.consumo_tabaco = tabaco
        self.consumo_alcohol = alcohol
        self.consumo_drogas = drogas
        self.diagnostico_consulta = diagnostico
        self.tratamiento_consulta = tratamiento
        self.internacion_consulta = internacion
        self.id_doctor_tratante = doctor
        self.id_paciente_consulta = paciente
        self.codigo_consulta = codigo_consulta
        self.estado_consulta = estado_consulta
        