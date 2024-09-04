from app.configuraciones.extensiones import db

class ControlEstado(db.Model):
    __tablename__ = 'control_estado'

    id_control_estado = db.Column(db.Integer, primary_key=True)
    antibiotico_estado = db.Column(db.String(100), nullable=True)
    dias_internado = db.Column(db.String(20), nullable=True)
    fecha_estado = db.Column(db.Date, nullable=True)
    dias_post_operatorio = db.Column(db.String(20), nullable=True)
    id_hoja_control_estado = db.Column(db.Integer, db.ForeignKey('hoja_control.id_hoja_control'), nullable=False)

    def __init__(self, antibiotico, dias_internado, fecha, dias_post_operatorio, hoja_control):
        self.antibiotico_estado = antibiotico
        self.dias_internado = dias_internado
        self.fecha_estado = fecha
        self.dias_post_operatorio = dias_post_operatorio
        self.id_hoja_control_estado = hoja_control