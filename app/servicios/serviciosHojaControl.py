from app.configuraciones.extensiones import db
from app.serializadores.serializadorHojaControl import SerializadorHojaControl
from app.modelos.hojaControl import HojaControl
from app.modelos.paciente import Paciente
from app.modelos.consulta import Consulta
from app.servicios.serviciosControlEstado import ServiciosControlEstado
from app.servicios.serviciosControlSignos import ServiciosControlSignos
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
import queue
from io import BytesIO


def obtener_ultima_hoja(hojas):
    respuesta = 0
    if hojas:
        for hoja in hojas:
            if(hoja.numero_hoja>respuesta):
                respuesta = hoja.numero_hoja
    respuesta = respuesta + 1
    return respuesta

class ServiciosHojaControl():
    def obtener_todos():
        #hojas_controles = HojaControl.query.all()
        #respuesta = SerializadorHojaControl.serializar(hojas_controles)
        vista = db.session.query(Paciente, HojaControl).join(HojaControl).all()
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_todos_paciente(id):
        #hojas_controles = HojaControl.query.all()
        #respuesta = SerializadorHojaControl.serializar(hojas_controles)
        vista = db.session.query(Paciente, HojaControl, Consulta)\
            .join(HojaControl, HojaControl.id_consulta_hoja==Consulta.id_consulta)\
            .join(Paciente, Consulta.id_paciente_consulta==Paciente.id_paciente)\
            .filter(Paciente.id_paciente==id)
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_todos_consulta(id):
        vista = db.session.query(Paciente, HojaControl, Consulta)\
            .join(HojaControl, HojaControl.id_consulta_hoja==Consulta.id_consulta)\
            .join(Paciente, Consulta.id_paciente_consulta==Paciente.id_paciente)\
            .filter(Consulta.id_consulta==id)
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_id(id):
        #hoja_control = HojaControl.query.get(id)
        #respuesta = SerializadorHojaControl.serializar_unico(hoja_control)
        vista = db.session.query(Paciente, HojaControl, Consulta)\
            .join(HojaControl, HojaControl.id_consulta_hoja==Consulta.id_consulta)\
            .join(Paciente, Consulta.id_paciente_consulta==Paciente.id_paciente)\
            .filter(HojaControl.id_hoja_control==id).first()
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control_unico(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def crear(peso, talla, servicio, pieza, paciente, consulta):
        hojas_control = HojaControl.query.filter_by(id_paciente_hoja=paciente)
        numero_hoja = obtener_ultima_hoja(hojas_control)
        nueva_hoja_control = HojaControl(peso, talla, servicio, numero_hoja, pieza, paciente, consulta)
        db.session.add(nueva_hoja_control)
        db.session.commit()
        respuesta = SerializadorHojaControl.serializar_unico(nueva_hoja_control)
        return respuesta
    
    def actualizar(id, peso=None, talla=None, servicio=None, pieza=None):
        hoja_control_editar = HojaControl.query.get(id)
        if hoja_control_editar:
            if peso:
                hoja_control_editar.peso_paciente = peso
            if talla:
                hoja_control_editar.talla_paciente = talla
            if servicio:
                hoja_control_editar.fecha_control = servicio
            if pieza:
                hoja_control_editar.pieza_paciente = pieza
            db.session.commit()
            respuesta = SerializadorHojaControl.serializar_unico(hoja_control_editar)
            return respuesta
        else:
            return None
    
    def obtener_hojas_paciente(id):
        print(id)
        lista_hojas = []
        hojas = db.session.query(Paciente, HojaControl).join(HojaControl).filter_by(id_paciente_hoja=id).all()
        hojas = SerializadorHojaControl.serializar_pacientes_hoja_control(hojas)

        if hojas:

            for hoja in hojas:
                print(hoja)
                #lista_estados = []
                #lista_signos = []
                id_hoja = hoja['id_hoja']
                lista_estados = ServiciosControlEstado.obtener_hoja(id_hoja)
                lista_signos = ServiciosControlSignos.obtener_hoja(id_hoja)
                cuerpo = {
                    'datos_hoja': hoja,
                    'datos_estados': lista_estados,
                    'datos_signos': lista_signos
                }
                lista_hojas.append(cuerpo)
            return lista_hojas
        else:
            return None
    


        


    def generar_informe(hoja, estados, signos, nombre_usuario):
        '''w, h = letter
        c = canvas.Canvas('prueba.pdf', letter)'''

        buffer = BytesIO()


        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle('Titulo', fontSize=18, alignment=1, fontName="Helvetica-Bold", underline=True)
        estilo_subtitulo = ParagraphStyle('Subtitulo', fontSize=10, alignment=0)  # Para el nombre de usuario y fecha
        estilo_tabla_paragrah = ParagraphStyle('Normala', fontSize=7, alignment=0)
        estilo_datos = estilos['Normal']

        logo_direccion = os.path.join(os.getcwd(),'app', 'static', 'assets', 'images', 'logo.png')
        print(logo_direccion)

        # Agregar logo del hospital
        logo = "logo.png"  # Ruta al logo
        imagen_logo = Image(logo_direccion, 2 * inch, 1 * inch)  # Ajustar el tamaño del logo
        #imagen_logo.hAlign = 'LEFT'
        #elementos.append(imagen_logo)


        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generado_por = Paragraph(f"<b>Generado por:</b> {nombre_usuario}<br/><b>Fecha de generación:</b> {fecha_actual}", estilo_subtitulo)
        #generado_por = Paragraph(f"<b>Generado por:</b> {nombre_usuario}", estilo_subtitulo)
        #generado_por = f"<b>Generado por:</b> {nombre_usuario}"

        #elementos.append(generado_por)
        #tabla_encabezado = Table([[imagen_logo, generado_por]], colWidths=[4 * inch, 4 * inch])
        #elementos.append(tabla_encabezado)
        def add_header(canvas, doc):
            width, height = letter
            imagen_logo.drawOn(canvas, (0.5*inch), height - (0.5*inch) - imagen_logo.drawHeight)
            #tabla_encabezado.drawOn(canvas, (0.5*inch), height - (0.5*inch) - imagen_logo.drawHeight)
            
            # Obtener el ancho del texto
            #ancho_texto = canvas.stringWidth(generado_por, "Helvetica", 12)
            
            # Posicionar el texto a una pulgada del margen derecho
            posicion_texto_x = (0.3*inch)
            posicion_texto_y = (0.3*inch)
            generado_por.wrapOn(canvas, width, height)
            
            # Dibujar el texto
            generado_por.drawOn(canvas, posicion_texto_x, posicion_texto_y)
            #canvas.drawString(posicion_texto_x, posicion_texto_y, generado_por)

        # Espacio entre elementos
        elementos.append(Spacer(1, 12))

        # Título del documento centrado y subrayado
        titulo = Paragraph("<u>Hoja de Signos Vitales</u>", estilo_titulo)
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

        # Generar el PDF  ----------------  pdf.build(elementos)
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)

        buffer.seek(0)
        return buffer

        #return 200


    def generar_informe_tomografia_pdf(id_diagnostico, id_paciente, listado2, nombre_usuario,nombre_paciente):
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle('Titulo', fontSize=18, alignment=1, fontName="Helvetica-Bold", underline=True)
        estilo_subtitulo_2 = ParagraphStyle('Subtitulo', fontSize=15, alignment=0)  
        estilo_subtitulo = ParagraphStyle('Subtitulo', fontSize=10, alignment=0) 
        estilo_datos = estilos['Normal']



        logo_direccion = os.path.join(os.getcwd(), 'app', 'static', 'assets', 'images', 'logo.png')
        imagen_logo = Image(logo_direccion, 2 * inch, 1 * inch)  

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generado_por = Paragraph(f"<b>Generado por:</b> {nombre_usuario}<br/><b>Fecha de generación:</b> {fecha_actual}", estilo_subtitulo)
        # Agregar elementos al PDF
        elementos.append(Spacer(1, 55))
       
        elementos.append(Spacer(1, 20))

        def add_header(canvas, doc):
            width, height = letter
            imagen_logo.drawOn(canvas, (0.5 * inch), height - (0.5 * inch) - imagen_logo.drawHeight)
            titulo_x = width / 2  
            titulo_y = height - (2.0 * inch) 
            canvas.setFont("Helvetica-Bold", 18)
            canvas.drawString(titulo_x - 120, titulo_y, "Informe de Estudio Realizado")
            posicion_texto_x = (0.3*inch)
            posicion_texto_y = (0.3*inch)
            generado_por.wrapOn(canvas, width, height)
            generado_por.drawOn(canvas, posicion_texto_x, posicion_texto_y)

        elementos.append(Spacer(1, 20))
        elementos.append(Paragraph(f"<b>Nombre del Paciente:</b> {nombre_paciente}", estilo_datos))
        elementos.append(Spacer(1, 30))
        conta=0
        contaT=0
        contaS=0
        for resultado in listado2:
            if str(resultado['id_diagnostico']) != str(id_diagnostico):
                continue  

            conta=conta+1
            
            if resultado['resultado_estudio'] == 1:
                diagnostico_texto = "CON TUMOR" 
                contaT=contaT+1
            else:
                diagnostico_texto = "SIN TUMOR" 
                contaS=contaS+1

            elementos.append(Paragraph(f"<b>Imagen Evaluada Nro:</b> {conta}", estilo_datos))
            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(f"<b>Diagnóstico:</b> {diagnostico_texto}", estilo_datos))
            elementos.append(Spacer(1, 5))
            info_paciente = (
                f"Fecha de Estudio: {resultado['fecha_estudio']}"
            )
            elementos.append(Paragraph(info_paciente, estilo_datos))
            elementos.append(Spacer(1, 5))

            ruta_relativa = os.path.join('app', 'static', 'imagenes')
            ruta = os.path.abspath(ruta_relativa)
            imagen_path = os.path.join(ruta, resultado['ruta_carpeta_imagenes_estudio'])
            
            if os.path.exists(imagen_path):
                elementos.append(Paragraph(f"<b>Ruta de Imagen:</b> {resultado['ruta_carpeta_imagenes_estudio']}", estilo_datos))
                try:
                    elementos.append(Spacer(1, 20))
                    imagen = Image(imagen_path, 2 * inch, 2 * inch)
                    elementos.append(imagen)
                    if(conta%2==0):
                        elementos.append(Spacer(1, 90))
                    else:
                        elementos.append(Spacer(1, 30))
                except Exception as e:
                    print(f"Error al cargar la imagen: {e}")
                    elementos.append(Paragraph("Error al cargar la imagen", estilo_datos))
            else:
                elementos.append(Paragraph("Imagen no encontrada", estilo_datos))
            
        elementos.append(Spacer(1, 20))
        elementos.append(Spacer(1, 20))
        elementos.append(Paragraph(f"<b>RESUMEN DIAGNOSTICO</b> ", estilo_subtitulo_2))
        elementos.append(Spacer(1, 25))
        elementos.append(Paragraph(f"<b>Nombre del Paciente:</b> {nombre_paciente}", estilo_datos))
        elementos.append(Spacer(1, 5))
        elementos.append(Paragraph(f"<b>Numero de Imagenes:</b> {conta}", estilo_datos))
        elementos.append(Spacer(1, 5))
        elementos.append(Paragraph(f"<b>Numero de Imagenes con Tumor:</b> {contaT}", estilo_datos))
        elementos.append(Spacer(1, 5))
        elementos.append(Paragraph(f"<b>Numero de Imagenes sin Tumor:</b> {contaS}", estilo_datos))
        elementos.append(Spacer(1, 5))
        
            
        elementos.append(Spacer(1, 5))
        dato = (contaT * 100.0) / conta
        elementos.append(Paragraph(f"<b>Probabilidad de Tumor:</b> {dato:.2f}%", estilo_datos))
        
        pdf.build(elementos, onFirstPage=add_header, onLaterPages=add_header)
        buffer.seek(0)

        return buffer
