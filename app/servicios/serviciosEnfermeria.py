from app.modelos.registroEnfermeria import RegistroEnfermeria
from app.modelos.usuario import Usuario
from app.modelos.paciente import Paciente
from app.modelos.consulta import Consulta
from app.modelos.hojaControl import HojaControl
from app.modelos.indicacionesMedicas import IndicacionesMedicas
from app.serializadores.serializadorRegistroEnfermeria import SerializadorRegistroEnfermeria

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

class ServiciosEnfermeras():
    def obtener_todos():
        lista = RegistroEnfermeria.query.filter_by(activo = 1)
        respuesta = SerializadorRegistroEnfermeria.serializar(lista)
        if respuesta:
            return respuesta
        else:
            return None
        
    def crear(procedimiento, observaciones, fecha, hora,id_enfermera,consulta, paciente):
        nuevo_resultado = RegistroEnfermeria(procedimiento, observaciones, fecha, hora, id_enfermera,consulta, paciente)
        db.session.add(nuevo_resultado)
        db.session.commit()
        respuesta = SerializadorRegistroEnfermeria.serializar_unico(nuevo_resultado)
        
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_lista_id(id):
        datos = db.session.query(Paciente, RegistroEnfermeria, Usuario)\
            .join(RegistroEnfermeria, Paciente.id_paciente == RegistroEnfermeria.id_paciente)\
            .join(Usuario, RegistroEnfermeria.id_enfermera_cargo == Usuario.id_usuario)\
            .filter(Paciente.id_paciente==id, RegistroEnfermeria.activo==1)
        respuesta = SerializadorRegistroEnfermeria.serializar_todos_vista(datos)
        print(respuesta)
        if respuesta:
            return respuesta
        else:
            return None
 

    def actualizar(id,procedimiento=None, observaciones=None, fecha=None, hora=None,id_enfermera=None):
        consulta_editar = RegistroEnfermeria.query.get(id)
        
        if consulta_editar:
            if procedimiento:
                consulta_editar.procedimiento_enfermeria = procedimiento
            if observaciones:
                consulta_editar.observaciones_enfermeria = observaciones
            if fecha:
                consulta_editar.fecha_registro = fecha
            if hora:
                consulta_editar.hora_registro = hora
            if id_enfermera:
                consulta_editar.id_enfermera_cargo = id_enfermera
           
            db.session.commit()
            respuesta = SerializadorRegistroEnfermeria.serializar_unico(consulta_editar)
            return respuesta
        else:
            return None
        

    def eliminar(id):
        datos = RegistroEnfermeria.query.get(id)
        datos.activo = 0
        db.session.commit()
        return True
    

    def generar_pdf_enfermeria(nombre_usuario, codigo_consulta):
        

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

        titulo = Paragraph(f"<u>REPORTE ENFERMERÍA</u>", estilo_titulo)
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
        
        indicaciones = RegistroEnfermeria.query.filter(RegistroEnfermeria.activo==1, RegistroEnfermeria.id_consulta_registro==consulta.id_consulta).order_by(RegistroEnfermeria.fecha_registro, RegistroEnfermeria.hora_registro).all()



        doctores_ob = Usuario.query.filter(Usuario.id_rol_usuario==2).all()

        doctores = {}

        if doctores_ob:
            for doctor in doctores_ob:
                doctores[str(doctor.id_usuario)] = doctor.nombres_usuario + " " + doctor.apellido_paterno_usuario + " " + doctor.apellido_materno_usuario

        tamanos_columnas_datos = [4*inch, 1.5*inch, 1.5*inch]
        datos_per = Table([[Paragraph(f"Nombres y Apellidos: {paciente.nombres_paciente} {paciente.apellido_paterno_paciente} {paciente.apellido_materno_paciente}", estilo_subtitulo), Paragraph(f"Pieza: {hoja.pieza_paciente}", estilo_subtitulo), Paragraph(f"N° Hoja: {hoja.numero_hoja}", estilo_subtitulo)]], colWidths=tamanos_columnas_datos) 

        elementos.append(datos_per)

        elementos.append(Spacer(1, 20))

        tabla_indicaciones = []

        tamanos_columnas = [1*inch, 1*inch, 2*inch, 2*inch, 1*inch]

        fila_encabezado_datos_personales = ['S.O.A.P.I.E.  S=SUBJETIVO  O=OBJETIVO  A=DIAGNÓSTICO  P=OBJETIVO INT.  I=INTERVENCIÓN  E=EVALUACIÓN', '', '', '', '']
        
        fila_encabezado_indicaciones = ['FECHA', 'HORA', 'PROCEDIMIENTO', 'OBSERVACIONES', 'FIRMA Y SELLO']

        tabla_indicaciones.append(fila_encabezado_datos_personales)
        tabla_indicaciones.append(fila_encabezado_indicaciones)

      
        
        estilo_tabla = [
                
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('FONTSIZE', (0, 0), (4, 0), 9),
                ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('SPAN',(0,0),(4,0))
            ]
        
        ind = 0

        if not indicaciones:
            fila_vacia = ['Sin indicaciones', '', '', '', '', '', '']
            tabla_indicaciones.append(fila_vacia)
            #estilo_tabla.append(('SPAN',(3,0),(3,6)))
        else:
            for indicacion in indicaciones:
                ind = ind + 1
                descripcion_med = str(indicacion.procedimiento_enfermeria).replace('\n', '<br />')
                observaciones_med = str(indicacion.observaciones_enfermeria).replace('\n', '<br />')
                fila_datos = [indicacion.fecha_registro, indicacion.hora_registro, Paragraph(f"{descripcion_med}"), Paragraph(f"{observaciones_med}"), '']
                tabla_indicaciones.append(fila_datos)
                #estilo_tabla.append(('SPAN',(2,2+ind),(5,2+ind)))
                
        

        estilo_tabla = TableStyle(estilo_tabla)

        tabla_pdf_indicaciones = Table(tabla_indicaciones, colWidths=tamanos_columnas)

        tabla_pdf_indicaciones.setStyle(estilo_tabla)

        elementos.append(tabla_pdf_indicaciones)

        elementos.append(Spacer(1, 20))

         # Generar el PDF  ----------------  pdf.build(elementos)
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)

        buffer.seek(0)
        return buffer