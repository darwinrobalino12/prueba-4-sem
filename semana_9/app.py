from flask import Flask, url_for

# Creamos la instancia de la aplicación
app = Flask(__name__)

# 1. RUTA PRINCIPAL (Paso 2 de la tarea)
@app.route('/')
def home():
    return f"""
    <html>
        <head>
            <title>Fisioterapia Píllaro</title>
            <link rel="stylesheet" href="{url_for('static', filename='estilos.css')}">
        </head>
        <body>
            <h1>Centro de Fisioterapia - Píllaro</h1>
            <p>Bienvenido al sistema de gestión de la <b>Fis. Mayra Campaña</b>.</p>
            <p>Ubicación: Cantón Píllaro, Provincia de Tungurahua.</p>
        </body>
    </html>
    """

# 2. RUTA DINÁMICA (Paso 3 de la tarea)
@app.route('/cita/<paciente>')
def agendar_cita(paciente):
    return f"""
    <html>
        <head>
            <title>Cita - {paciente}</title>
            <link rel="stylesheet" href="{url_for('static', filename='estilos.css')}">
        </head>
        <body>
            <h1>Gestión de Citas</h1>
            <p>Bienvenida, <b>{paciente}</b>. Tu solicitud en el Centro de Fisioterapia está en proceso.</p>
            <hr>
            <a href="/">Volver al inicio</a>
        </body>
    </html>
    """

if __name__ == '__main__':
    # Ejecutamos el servidor en modo depuración
    app.run(debug=True)