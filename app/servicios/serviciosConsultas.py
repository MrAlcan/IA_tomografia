from app.modelos.consulta import Consulta
from app.modelos.usuario import Usuario
from app.modelos.paciente import Paciente
from app.serializadores.serializadorConsulta import SerializadorConsulta

from app.configuraciones.extensiones import db

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
import queue
from io import BytesIO
import os

class ServiciosConsultas():
    def obtener_todos():
        lista = Consulta.query.all()
        respuesta = SerializadorConsulta.serializar(lista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_todos_usuario_paciente():
        #vista = db.session.query(Paciente, Consulta, Usuario).join(Consulta).join(Usuario).all()
        vista = db.session.query(Paciente, Consulta, Usuario)\
            .join(Consulta, Paciente.id_paciente == Consulta.id_paciente_consulta)\
            .join(Usuario, Consulta.id_doctor_tratante == Usuario.id_usuario)\
            .all()
        respuesta = SerializadorConsulta.serializar_todos_vista(vista)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None

    def obtener_usuario_paciente(id):
        vista = db.session.query(Paciente, Consulta, Usuario)\
            .join(Consulta, Paciente.id_paciente == Consulta.id_paciente_consulta)\
            .join(Usuario, Consulta.id_doctor_tratante == Usuario.id_usuario)\
            .filter(Consulta.id_consulta == id).first()
        respuesta = SerializadorConsulta.serializar_unica_vista(vista)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_usuario_paciente_id(id):
        #vista = db.session.query(Paciente, Consulta, Usuario).join(Consulta).join(Usuario).all()
        vista = db.session.query(Paciente, Consulta, Usuario)\
            .join(Consulta, Paciente.id_paciente == Consulta.id_paciente_consulta)\
            .join(Usuario, Consulta.id_doctor_tratante == Usuario.id_usuario)\
            .filter(Paciente.id_paciente==id)
        
        respuesta = SerializadorConsulta.serializar_todos_vista(vista)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None

    def crear(motivo, historia, enfermedades, tabaco, alcohol, drogas, diagnostico, tratamiento, doctor, paciente, internacion, codigo_consulta ,estado_consulta=None, fecha=None):
        nueva_consulta = Consulta(motivo, historia, enfermedades, tabaco, alcohol, drogas, diagnostico, tratamiento, doctor, paciente, internacion, codigo_consulta ,estado_consulta, fecha)
        db.session.add(nueva_consulta)
        db.session.commit()
        respuesta = SerializadorConsulta.serializar_unico(nueva_consulta)
        if respuesta:
            return respuesta
        else:
            return None
    
    def actualizar(id, motivo=None, historia=None, enfermedades=None, tabaco=None, alcohol=None, drogas=None, diagnostico=None, tratamiento=None, doctor=None, paciente=None, internacion=None, codigo_consulta=None ,estado_consulta=None, fecha=None):
        consulta_editar = Consulta.query.get(id)
        if consulta_editar:
            if motivo:
                consulta_editar.motivo_consulta = motivo
            if historia:
                consulta_editar.historia_enfermedad_actual = historia
            if enfermedades:
                consulta_editar.enfermedades_consulta = enfermedades
            if tabaco:
                consulta_editar.consumo_tabaco = tabaco
            if alcohol:
                consulta_editar.consumo_alcohol = alcohol
            if drogas:
                consulta_editar.consumo_drogas = drogas
            if diagnostico:
                consulta_editar.diagnostico_consulta = diagnostico
            if tratamiento:
                consulta_editar.tratamiento_consulta = tratamiento
            if internacion:
                consulta_editar.internacion_consulta = internacion
            if doctor:
                consulta_editar.id_doctor_tratante = doctor
            if paciente:
                consulta_editar.id_paciente_consulta = paciente
            if codigo_consulta:
                consulta_editar.codigo_consulta = codigo_consulta
            if estado_consulta:
                consulta_editar.estado_consulta = estado_consulta
            if fecha:
                consulta_editar.fecha_consulta = fecha
            db.session.commit()
            respuesta = SerializadorConsulta.serializar_unico(consulta_editar)
            return respuesta
        else:
            return None
    
    def generar_informe(consulta, nombre_usuario):
        buffer = BytesIO()


        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle('Titulo', fontSize=18, alignment=1, fontName="Helvetica-Bold", underline=True)
        estilo_subtitulo = ParagraphStyle('Subtitulo', fontSize=10, alignment=0)  # Para el nombre de usuario y fecha
        estilo_tabla_paragrah = ParagraphStyle('Normala', fontSize=7, alignment=0)
        estilo_datos = estilos['Normal']
        estilo_alineamiento_tablas = TableStyle()

        logo_direccion = os.path.join(os.getcwd(),'app', 'static', 'assets', 'images', 'logo.png')
        print(logo_direccion)

 
        logo = "logo.png" 
        imagen_logo = Image(logo_direccion, 2 * inch, 1 * inch) 



        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generado_por = Paragraph(f"<b>Generado por:</b> {nombre_usuario}<br/><b>Fecha de generación:</b> {fecha_actual}", estilo_subtitulo)

        def add_header(canvas, doc):
            width, height = letter
            imagen_logo.drawOn(canvas, (0.3*inch), height - (0.3*inch) - imagen_logo.drawHeight)
            
            posicion_texto_x = (0.3*inch)
            posicion_texto_y = (0.3*inch)
            generado_por.wrapOn(canvas, width, height)
            
            generado_por.drawOn(canvas, posicion_texto_x, posicion_texto_y)





        # Espacio entre elementos
        elementos.append(Spacer(1, 12))

        titulo = Paragraph(f"<u>Consulta N° {consulta['id_consulta']}</u>", estilo_titulo)
        elementos.append(titulo)

        # Espacio antes de los datos personales
        elementos.append(Spacer(1, 20))

        datos_paciente = Table([[Paragraph(f"<b>Nombres y Apellidos del Paciente:</b> {consulta['nombres_paciente']} {consulta['apellido_paterno_paciente']} {consulta['apellido_materno_paciente']}", estilo_datos), ''],
                                [Paragraph(f"<b>Carnet de Identidad:</b> {consulta['carnet_paciente']}", estilo_datos), Paragraph(f"<b>Seguro:</b> {consulta['seguro_paciente']}", estilo_datos)],
                                [Paragraph(f"<b>Fecha de Nacimiento:</b> {consulta['fecha_nacimiento_paciente']}", estilo_datos), Paragraph(f"<b>Edad:</b> {consulta['edad_paciente']}", estilo_datos)]])

        '''datos_paciente = Table([[Paragraph(f"<b>Nombres y Apellidos del Paciente:</b> {hoja['nombres']} {hoja['apellido_paterno']} {hoja['apellido_materno']}<br/><b>Servicio:</b> {hoja['servicio']}<br/><b>Peso:</b> {hoja['peso']}", estilo_datos),
                                 Paragraph(f"<br/><b>Pieza:</b> {hoja['pieza']}<br/><b>Talla:</b> {hoja['talla']}", estilo_datos),
                                 Paragraph(f"<br/><b>Número de Hoja:</b> {hoja['numero_hoja']}<br/><b>Edad:</b> {hoja['edad']}", estilo_datos)]])'''
        datos_paciente.setStyle(TableStyle([('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                                            ('SPAN',(0,0),(1,0)),]))
        
        
        #elementos.append(nombres_paciente)
        elementos.append(datos_paciente)

        # Espacio antes de la tabla
        elementos.append(Spacer(1, 20))

        subtitulo_fecha_consulta = Paragraph(f"<b>Fecha Consulta: </b> {consulta['fecha']}", estilo_datos)
        elementos.append(subtitulo_fecha_consulta)

        elementos.append(Spacer(1,20))

        subtitulo_motivo_consulta = Paragraph(f"<b>Motivo de Consulta:</b>", estilo_subtitulo)
        elementos.append(subtitulo_motivo_consulta)

        #elementos.append(Spacer(1,20))

        motivo_consulta = Paragraph(f"{consulta['motivo']}", estilo_datos)
        elementos.append(motivo_consulta)

        elementos.append(Spacer(1,20))

        subtitulo_historia_enfermedad_actual = Paragraph(f"<b>Historia de la Enfermedad Actual:</b>", estilo_subtitulo)
        elementos.append(subtitulo_historia_enfermedad_actual)

        #elementos.append(Spacer(1, 20))

        historia_enfermedad_actual = Paragraph(f"{consulta['historia_enfermedad']}", estilo_datos)
        elementos.append(historia_enfermedad_actual)

        elementos.append(Spacer(1, 20))

        subtitulo_enfermedades = Paragraph(f"<b>Enfermedades:</b>", estilo_subtitulo)
        elementos.append(subtitulo_enfermedades)

        #elementos.append(Spacer(1,20))

        enfermedades = Paragraph(f"{consulta['enfermedades']}", estilo_datos)
        elementos.append(enfermedades)

        elementos.append(Spacer(1,20))

        subtitulo_habitos = Paragraph(f"<b>Habitos</b>", estilo_subtitulo)
        elementos.append(subtitulo_habitos)

        #elementos.append(Spacer(1, 20))
        print(consulta['tabaco'])
        print(consulta['alcohol'])
        print(consulta['drogas'])

        tabla_habitos = Table([[Paragraph(f"<b>Tabaco: </b>", estilo_datos), Paragraph(f"{consulta['tabaco']}", estilo_datos)],
                               [Paragraph(f"<b>Alcohol: </b>", estilo_datos), Paragraph(f"{consulta['alcohol']}", estilo_datos)],
                               [Paragraph(f"<b>Drogas: </b>", estilo_datos), Paragraph(f"{consulta['drogas']}", estilo_datos)]])
        
        tabla_habitos.setStyle(TableStyle([('ALIGNMENT', (0, 0), (-1, -1), 'LEFT')]))
        elementos.append(tabla_habitos)

        elementos.append(Spacer(1, 20))

        subtitulo_diagnostico = Paragraph(f"<b>Diagnostico:</b>", estilo_subtitulo)
        elementos.append(subtitulo_diagnostico)

        #elementos.append(Spacer(1, 20))

        diagnostico = Paragraph(f"{consulta['diagnostico']}", estilo_datos)
        elementos.append(diagnostico)

        elementos.append(Spacer(1, 20))

        subtitulo_tratamiento = Paragraph(f"<b>Tratamiento:</b>", estilo_subtitulo)
        elementos.append(subtitulo_tratamiento)

        #elementos.append(Spacer(1, 20))

        tratamiento = Paragraph(f"{consulta['tratamiento']}", estilo_datos)
        elementos.append(tratamiento)

        elementos.append(Spacer(1, 20))

        subtitulo_internacion = Paragraph(f"<b>Paciente debera ser internado:</b>", estilo_subtitulo)
        elementos.append(subtitulo_internacion)

        #elementos.append(Spacer(1, 20))

        texto_internacion = ''

        if consulta['internacion']==1:
            texto_internacion = 'SI'
        else:
            texto_internacion = 'NO'

        internacion = Paragraph(f"{texto_internacion}", estilo_datos)
        elementos.append(internacion)

        elementos.append(Spacer(1, 20))

        subtitulo_medico_tratante = Paragraph(f"<b>Medico Tratante:</b>", estilo_subtitulo)
        elementos.append(subtitulo_medico_tratante)

        #elementos.append(Spacer(1, 20))

        medico_tratante = Paragraph(f"Dr. {consulta['nombres_usuario']} {consulta['apellido_paterno_usuario']} {consulta['apellido_materno_usuario']}", estilo_datos)
        elementos.append(medico_tratante)


        # Generar el PDF  ----------------  pdf.build(elementos)
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)

        buffer.seek(0)
        return buffer
