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
        vista = db.session.query(Paciente, HojaControl).join(HojaControl).filter(HojaControl.activo==1).all()
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
            .filter(Paciente.id_paciente==id, HojaControl.activo==1)
        respuesta = SerializadorHojaControl.serializar_pacientes_hoja_control(vista)
        if respuesta:
            return respuesta
        else:
            return None
    
    def obtener_todos_consulta(id):
        vista = db.session.query(Paciente, HojaControl, Consulta)\
            .join(HojaControl, HojaControl.id_consulta_hoja==Consulta.id_consulta)\
            .join(Paciente, Consulta.id_paciente_consulta==Paciente.id_paciente)\
            .filter(Consulta.id_consulta==id, HojaControl.activo==1)
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
            .filter(HojaControl.id_hoja_control==id, HojaControl.activo==1).first()
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
                hoja_control_editar.servicio_paciente = servicio
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
        hojas = db.session.query(Paciente, HojaControl).join(HojaControl).filter_by(id_paciente_hoja=id, activo = 1).all()
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


    def eliminar(id):
        datos = HojaControl.query.get(id)
        datos.activo = 0
        db.session.commit()
        return True