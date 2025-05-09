from app.modelos.indicacionesMedicas import IndicacionesMedicas
from app.modelos.usuario import Usuario
from app.modelos.paciente import Paciente
from app.modelos.consulta import Consulta
from app.modelos.hojaControl import HojaControl
from app.serializadores.serializadorIndicacionesMedicas import SerializadorIndicacionesMedicas
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

class ServiciosIndicaciones():
    def obtener_todos():
        lista = IndicacionesMedicas.query.filter_by(activo = 1)
        respuesta = SerializadorIndicacionesMedicas.serializar(lista)
        if respuesta:
            return respuesta
        else:
            return None

    
    def crear(fecha, hora,descripcion, doctor,consulta, paciente):
        nuevo_resultado = IndicacionesMedicas(fecha, hora,descripcion, doctor,consulta, paciente)
        db.session.add(nuevo_resultado)
        db.session.commit()
        respuesta = SerializadorIndicacionesMedicas.serializar_unico(nuevo_resultado)
        
        if respuesta:
            return respuesta
        else:
            return None
        

    def obtener_lista_id(id):
        datos = db.session.query(Paciente, IndicacionesMedicas, Usuario)\
            .join(IndicacionesMedicas, Paciente.id_paciente == IndicacionesMedicas.id_paciente_indicaciones)\
            .join(Usuario, IndicacionesMedicas.id_doctor_cargo == Usuario.id_usuario)\
            .filter(Paciente.id_paciente==id, IndicacionesMedicas.activo==1)
        respuesta = SerializadorIndicacionesMedicas.serializar_todos_vista(datos)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None
        

    def actualizar(id,fecha=None, hora=None,descripcion=None, doctor=None):
        consulta_editar = IndicacionesMedicas.query.get(id)
        print("__________________")
        print(consulta_editar)
        if consulta_editar:
            if fecha:
                consulta_editar.fecha_indicaciones = fecha
            if hora:
                consulta_editar.hora_indicaciones = hora
            if descripcion:
                consulta_editar.descripcion_indicaciones = descripcion
            if doctor:
                consulta_editar.id_doctor_cargo = doctor
           
           
            db.session.commit()
            respuesta = SerializadorIndicacionesMedicas.serializar_unico(consulta_editar)
            return respuesta
        else:
            return None
        
    def eliminar(id):
        datos = IndicacionesMedicas.query.get(id)
        datos.activo = 0
        db.session.commit()
        return True
    
    def generar_pdf_consulta(nombre_usuario, codigo_consulta):
        

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

        titulo = Paragraph(f"<u>INDICACIONES MÉDICAS</u>", estilo_titulo)
        elementos.append(titulo)

        # Espacio antes de los datos personales
        elementos.append(Spacer(1, 20))


        
        
        consulta = Consulta.query.filter(Consulta.activo==1, Consulta.codigo_consulta==codigo_consulta).first()

        if not consulta:
            return None
        
        hoja = HojaControl.query.filter(HojaControl.activo==1, HojaControl.id_consulta_hoja==consulta.id_consulta).first()

        if not hoja:
            return None
        
        paciente = Paciente.query.filter(Paciente.activo==1, Paciente.id_paciente == consulta.id_paciente_consulta).first()
        
        indicaciones = IndicacionesMedicas.query.filter(IndicacionesMedicas.activo==1, IndicacionesMedicas.id_consulta_indicaciones==consulta.id_consulta).order_by(IndicacionesMedicas.fecha_indicaciones, IndicacionesMedicas.hora_indicaciones).all()

        doctores_ob = Usuario.query.filter(Usuario.id_rol_usuario==2).all()

        doctores = {}

        if doctores_ob:
            for doctor in doctores_ob:
                doctores[str(doctor.id_usuario)] = doctor.nombres_usuario + " " + doctor.apellido_paterno_usuario + " " + doctor.apellido_materno_usuario

        tabla_indicaciones = []

        fila_encabezado_datos_personales = ['Ap. Paterno', '', 'Ap. Materno', 'Nombres', 'Servicio', 'Pieza', 'N° H.C.']
        fila_datos_personales = [paciente.apellido_paterno_paciente, '',paciente.apellido_materno_paciente, paciente.nombres_paciente, hoja.servicio_paciente, hoja.pieza_paciente, hoja.numero_hoja]
        fila_encabezado_indicaciones = ['FECHA', 'HORA', 'DESCRIPCIÓN', '', '', '', 'DOCTOR']

        tabla_indicaciones.append(fila_encabezado_datos_personales)
        tabla_indicaciones.append(fila_datos_personales)
        tabla_indicaciones.append(fila_encabezado_indicaciones)

        '''estilo_tabla = TableStyle([
                ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                ('SPAN',(0,0),(1,0)),
                ('SPAN',(0,1),(1,1)),
                ('SPAN',(2,2),(5,2)),
            ])'''
        
        estilo_tabla = [
                ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('SPAN',(0,0),(1,0)),
                ('SPAN',(0,1),(1,1)),
                ('SPAN',(2,2),(5,2))
            ]
        
        ind = 0

        if not indicaciones:
            fila_vacia = ['Sin indicaciones', '', '', '', '', '', '']
            tabla_indicaciones.append(fila_vacia)
            estilo_tabla.append(('SPAN',(3,0),(3,6)))
        else:
            for indicacion in indicaciones:
                ind = ind + 1
                descripcion_med = str(indicacion.descripcion_indicaciones).replace('\n', '<br />')
                fila_datos = [indicacion.fecha_indicaciones, indicacion.hora_indicaciones, Paragraph(f"{descripcion_med}"), '', '', '', doctores[str(indicacion.id_doctor_cargo)]]
                tabla_indicaciones.append(fila_datos)
                estilo_tabla.append(('SPAN',(2,2+ind),(5,2+ind)))
                print(indicacion.descripcion_indicaciones)
                if '\n' in indicacion.descripcion_indicaciones:
                    print("tiene enters")
                    lecturas = indicacion.descripcion_indicaciones.split('\n')[0]
                    print(lecturas)
                    print(lecturas[0])
                    print(lecturas[-1])
                    print(lecturas[-2])
                    print(lecturas[-3])
        

        estilo_tabla = TableStyle(estilo_tabla)

        tabla_pdf_indicaciones = Table(tabla_indicaciones)

        tabla_pdf_indicaciones.setStyle(estilo_tabla)

        elementos.append(tabla_pdf_indicaciones)

        elementos.append(Spacer(1, 20))

         # Generar el PDF  ----------------  pdf.build(elementos)
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)

        buffer.seek(0)
        return buffer