from fpdf import FPDF

class ReporteService:
    @staticmethod
    def generar_pdf_pacientes(pacientes):
        pdf = FPDF()
        pdf.add_page()
        
        # --- CONFIGURACIÓN DE CABECERA ---
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(13, 110, 253)  # Azul VitalFisio
        pdf.cell(190, 15, "VITALFISIO - REPORTE DE PACIENTES", 0, 1, 'C')
        pdf.ln(5)
        
        # --- ENCABEZADO DE LA TABLA ---
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(13, 110, 253) # Fondo azul para el encabezado
        pdf.set_text_color(255, 255, 255) # Texto blanco
        
        # Definimos anchos de columnas: Cédula (40), Nombre (100), Teléfono (50)
        pdf.cell(40, 10, "Cédula / ID", 1, 0, 'C', True)
        pdf.cell(100, 10, "Nombre del Paciente", 1, 0, 'C', True)
        pdf.cell(50, 10, "Teléfono", 1, 1, 'C', True)
        
        # --- CUERPO DE LA TABLA ---
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0) # Volver a texto negro
        
        fill = False # Para hacer filas alternadas (cebra)
        for p in pacientes:
            # Configurar color de fondo para filas alternas
            if fill:
                pdf.set_fill_color(245, 245, 245) # Gris muy claro
            else:
                pdf.set_fill_color(255, 255, 255) # Blanco
            
            # Dibujar celdas
            pdf.cell(40, 10, str(p['cedula']), 1, 0, 'C', True)
            pdf.cell(100, 10, f"{p['nombre']} {p['apellido']}".strip(), 1, 0, 'L', True)
            pdf.cell(50, 10, str(p.get('telefono', 'N/A')), 1, 1, 'C', True)
            
            fill = not fill # Cambia el color para la siguiente fila
            
        # --- PIE DE PÁGINA SIMPLE ---
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "Documento generado automáticamente por Sistema VitalFisio 2026", 0, 0, 'C')
        
        # Retornar como bytes
        return pdf.output(dest='S').encode('latin-1')