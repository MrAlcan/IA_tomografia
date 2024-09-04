from app.configuraciones.extensiones import db

class HojaControl(db.Model):
    __tablename__ = 'hoja_control'

    id_hoja_control = db.Column(db.Integer, primary_key=True)
    peso_paciente = db.Column(db.Float, nullable=False)
    talla_paciente = db.Column(db.Float, nullable=False)
    fecha_control = db.Column(db.Date, nullable=False)
    numero_hoja = db.Column(db.Integer, nullable=True)
    pieza_paciente = db.Column(db.String(20), nullable=False)
    id_paciente_hoja = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)

    def __init__(self, peso, talla, fecha, numero, pieza, paciente):
        self.peso_paciente = peso
        self.talla_paciente = talla
        self.fecha_control = fecha
        self.numero_hoja = numero
        self.pieza_paciente = pieza
        self.id_paciente_hoja = paciente