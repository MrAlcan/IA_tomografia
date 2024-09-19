from app.configuraciones.extensiones import db

class ControlSignos(db.Model):
    __tablename__ = 'control_signos'

    id_control_signos = db.Column(db.Integer, primary_key=True)
    fecha_control = db.Column(db.Date, nullable=False)
    hora_control = db.Column(db.String(3), nullable=False)
    presion_sistolica_control = db.Column(db.Integer, nullable=False)
    presion_diastolica_control = db.Column(db.Integer, nullable=False)
    respiracion_control = db.Column(db.Integer, nullable=False)
    saturacion_control = db.Column(db.Integer, nullable=False)
    diuresis_control = db.Column(db.Integer, nullable=False)
    catarsis_control = db.Column(db.Integer, nullable=False)
    id_hoja_signos = db.Column(db.Integer, db.ForeignKey('hoja_control.id_hoja_control'), nullable=False)
    #id_registro_control = db.Column(db.Integer, db.ForeignKey('registro_enfermeria.id_registro_enfermeria', nullable=False))

    #def __init__(self, fecha, hora, presion_sistolica, presion_diastolica, respiracion, saturacion, diuresis, catarsis, hoja_control, registro_enfermeria):
    def __init__(self, fecha, hora, presion_sistolica, presion_diastolica, respiracion, saturacion, diuresis, catarsis, hoja_control):
        self.fecha_control = fecha
        self.hora_control = hora
        self.presion_sistolica_control = presion_sistolica
        self.presion_diastolica_control = presion_diastolica
        self.respiracion_control = respiracion
        self.saturacion_control = saturacion
        self.diuresis_control = diuresis
        self.catarsis_control = catarsis
        self.id_hoja_signos = hoja_control
        #self.id_registro_control = registro_enfermeria