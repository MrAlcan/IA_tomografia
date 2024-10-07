from app.modelos.paciente import Paciente
from app.serializadores.serializadorPaciente import SerializadorPaciente
from app.servicios.serviciosHojaControl import ServiciosHojaControl
from app.servicios.serviciosConsultas import ServiciosConsultas
from app.servicios.serviciosEnfermeria import ServiciosEnfermeras
from app.servicios.serviciosIndicaciones import ServiciosIndicaciones
from app.configuraciones.extensiones import db

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from datetime import datetime
import queue
from io import BytesIO

class ServiciosPaciente():
    def obtener_todos():
        pacientes = Paciente.query.all()
        respuesta = SerializadorPaciente.serializar(pacientes)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_id(id):
        paciente = Paciente.query.get(id)
        respuesta = SerializadorPaciente.serializar_unico(paciente)
        if paciente:
            return respuesta
        else:
            return None
    
    def crear(nombres, apellido_paterno, apellido_materno, carnet, seguro, fecha_nacimiento, edad):
        nuevo_paciente = Paciente(nombres, apellido_paterno, apellido_materno, carnet, seguro, fecha_nacimiento, edad)
        db.session.add(nuevo_paciente)
        db.session.commit()
        respuesta = SerializadorPaciente.serializar_unico(nuevo_paciente)
        if respuesta:
            return respuesta
        else:
            return None
    
    def actualizar(id, nombres=None, apellido_paterno=None, apellido_materno=None, carnet=None, seguro=None, fecha_nacimiento=None, edad=None):
        usuario_editar = Paciente.query.get(id)
        if usuario_editar:
            if nombres:
                usuario_editar.nombres_paciente = nombres
            if apellido_paterno:
                usuario_editar.apellido_paterno_paciente = apellido_paterno
            if apellido_materno:
                usuario_editar.apellido_materno_paciente = apellido_materno
            if carnet:
                usuario_editar.carnet_paciente = carnet
            if seguro:
                usuario_editar.seguro_paciente = seguro
            if fecha_nacimiento:    
                usuario_editar.fecha_nacimiento_paciente = fecha_nacimiento
            if edad:
                usuario_editar.edad_paciente = edad
            db.session.commit()
            respuesta = SerializadorPaciente.serializar_unico(usuario_editar)
            return respuesta
        else:
            return None

    def generar_reporte_completo(id, nombre_usuario, datos):


        buffer = BytesIO()


        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []

        formato_fecha = '%Y-%m-%d'

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


        
        contador_hoja = 1


        # A partir de aqui se genera los documentos pdfs


        for dato in datos:
            consulta = dato['consulta']
            hojas = dato['hojas']


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

            

            if consulta['internacion']==1:
                fecha_inicio = datetime.strptime(dato['fecha_inicio'], formato_fecha)
                fecha_final = datetime.strptime(dato['fecha_final'], formato_fecha)

                #fecha_inicio = dato['fecha_inicio']
                #fecha_final = dato['fecha_final']
                dias_internado = int((fecha_final - fecha_inicio).days) + 1
                tiempo_internacion = Paragraph(f"Interado por {dias_internado} días, de {dato['fecha_inicio']} a {dato['fecha_final']}", estilo_datos)
                elementos.append(tiempo_internacion)
            

            elementos.append(Spacer(1, 20))

            subtitulo_medico_tratante = Paragraph(f"<b>Medico Tratante:</b>", estilo_subtitulo)
            elementos.append(subtitulo_medico_tratante)

            #elementos.append(Spacer(1, 20))

            medico_tratante = Paragraph(f"Dr. {consulta['nombres_usuario']} {consulta['apellido_paterno_usuario']} {consulta['apellido_materno_usuario']}", estilo_datos)
            elementos.append(medico_tratante)

            elementos.append(PageBreak())

            for hoja_control in hojas:
                elementos.append(Spacer(1, 12))

                signos = hoja_control['signos']
                estados = hoja_control['estados']
                hoja = hoja_control['hoja']

                # Título del documento centrado y subrayado
                titulo = Paragraph(f"<u>Hoja de Signos Vitales / Consulta N° {consulta['id_consulta']}</u>", estilo_titulo)
                elementos.append(titulo)

                # Espacio antes de los datos personales
                elementos.append(Spacer(1, 20))

                datos_paciente = Table([[Paragraph(f"<b>Nombres y Apellidos del Paciente:</b> {hoja['nombres']} {hoja['apellido_paterno']} {hoja['apellido_materno']}", estilo_datos), '', ''],
                                        [Paragraph(f"<b>Servicio:</b> {hoja['servicio']}", estilo_datos), Paragraph(f"<b>Pieza:</b> {hoja['pieza']}", estilo_datos), Paragraph(f"<b>Número de Hoja:</b> {hoja['numero_hoja']}", estilo_datos)],
                                        [Paragraph(f"<b>Peso:</b> {hoja['peso']}", estilo_datos), Paragraph(f"<b>Talla:</b> {hoja['talla']}", estilo_datos), Paragraph(f"<b>Edad:</b> {hoja['edad']}", estilo_datos)]])

                '''datos_paciente = Table([[Paragraph(f"<b>Nombres y Apellidos del Paciente:</b> {hoja['nombres']} {hoja['apellido_paterno']} {hoja['apellido_materno']}<br/><b>Servicio:</b> {hoja['servicio']}<br/><b>Peso:</b> {hoja['peso']}", estilo_datos),
                                        Paragraph(f"<br/><b>Pieza:</b> {hoja['pieza']}<br/><b>Talla:</b> {hoja['talla']}", estilo_datos),
                                        Paragraph(f"<br/><b>Número de Hoja:</b> {hoja['numero_hoja']}<br/><b>Edad:</b> {hoja['edad']}", estilo_datos)]])'''
                datos_paciente.setStyle(TableStyle([('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                                                    ('SPAN',(0,0),(2,0)),]))
                #nombres_paciente = Paragraph(f"<b>Nombres y Apellidos del Paciente:</b> {hoja['nombres']} {hoja['apellido_paterno']} {hoja['apellido_materno']}", estilo_datos)
                datos_paciente_paragraph = Paragraph(f"Nombre: {hoja['nombres']}<br/>Edad: {hoja['edad']}<br/>"
                                                    f"Peso: {hoja['peso']}<br/>Talla: {hoja['talla']}", estilo_datos)
                
                #elementos.append(nombres_paciente)
                elementos.append(datos_paciente)

                # Espacio antes de la tabla
                elementos.append(Spacer(1, 20))

                horas_signos = ['6', '10', '15', '21']

                cola_signos = queue.Queue()

                if signos:
                    for signo in signos:
                        cola_signos.put(signo)
                print('-'*100)
                print('-'*100)
                print(cola_signos)
                print('-'*100)
                print('-'*100)
                
                
                lista_dias_int = ['Días Internado']
                lista_dias_post = ['Días Post Oper.']
                lista_fechas = ['Fecha']
                
                lista_antibiotico = ['Antibiótico']

                lista_PA = ['P.A.']
                lista_respiracion = ['Respiración']
                lista_saturacion = ['Sat. de O2']
                lista_diuresis = ['Diuresis']
                lista_catarsis = ['Catarsis']
                '''
                'presion_sistolica' : control.presion_sistolica_control,
                            'presion_diastolica' : control.presion_diastolica_control,
                            'respiracion' : control.respiracion_control,
                            'saturacion' : control.saturacion_control,
                            'diuresis' : control.diuresis_control,
                            'catarsis' : control.catarsis_control,
                '''

                tam_celda_estados = [1.1 * inch]
                tam_celda_signos = [1.1 * inch]

                for estado in estados:
                    #contador_estados = contador_estados + 1
                    lista_dias_int.append(estado['dias_internado'])
                    lista_dias_post.append(estado['dias_post'])
                    lista_antibiotico.append(estado['antibiotico'])
                    fecha_string = estado['fecha'].strftime("%d-%m-%Y")
                    lista_fechas.append(fecha_string)
                    tam_celda_estados.append(1*inch)

                    for i in range(4):
                        tam_celda_signos.append(0.25*inch)
                        if not cola_signos.empty():
                            primer = cola_signos.queue[0]
                            if primer['fecha'] == estado['fecha']:
                                if primer['hora'] == horas_signos[i]:
                                    #lista_PA.append(Paragraph(f"{primer['presion_sistolica']} / {primer['presion_diastolica']}", estilo_tabla_paragrah))
                                    lista_PA.append(f"{primer['presion_sistolica']}\n/\n{primer['presion_diastolica']}")
                                    lista_respiracion.append(f"{primer['respiracion']}")
                                    lista_saturacion.append(f"{primer['saturacion']}")
                                    if primer['diuresis'] == 1:
                                        lista_diuresis.append('+')
                                    else:
                                        lista_diuresis.append('-')
                                    if primer['catarsis'] == 1:
                                        lista_catarsis.append('+')
                                    else:
                                        lista_catarsis.append('-')
                                    #lista_diuresis.append(f"{primer['diuresis']}")
                                    #lista_catarsis.append(f"{primer['catarsis']}")
                                    cola_signos.get()
                                else:
                                    lista_PA.append("")
                                    lista_respiracion.append("")
                                    lista_saturacion.append("")
                                    lista_diuresis.append("")
                                    lista_catarsis.append("")
                            else:
                                break
                        else:
                            lista_PA.append("")
                            lista_respiracion.append("")
                            lista_saturacion.append("")
                            lista_diuresis.append("")
                            lista_catarsis.append("")
                    
                tabla_estados = [lista_dias_int, lista_dias_post, lista_fechas, lista_antibiotico]
                tabla_signos = [lista_PA, lista_respiracion, lista_saturacion, lista_diuresis, lista_catarsis]

                print(tabla_estados)
                print(tabla_signos)







                # Crear la tabla de presión
                tabla_datos = [["Hora de muestra", "Presión"]] + estados
                tabla = Table(tabla_datos, colWidths=[2 * inch, 2 * inch])

                tabla_estados_pdf = Table(tabla_estados, colWidths=tam_celda_estados)
                tabla_signos_pdf = Table(tabla_signos, colWidths=tam_celda_signos)
                
                # Estilo de la tabla
                estilo_tabla = TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.gray),
                    #('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (0, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (0, -1), 10),
                    #('BACKGROUND', (1, 0), (-1, -1), colors.beige),
                    ('FONTSIZE', (1, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
                tabla_estados_pdf.setStyle(estilo_tabla)
                tabla_signos_pdf.setStyle(estilo_tabla)

                # Agregar la tabla al PDF
                elementos.append(tabla_estados_pdf)
                elementos.append(Spacer(1, 20))
                elementos.append(tabla_signos_pdf)
                elementos.append(PageBreak())
                







        # Generar el PDF  ----------------  pdf.build(elementos)
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)

        buffer.seek(0)
        return buffer

        
