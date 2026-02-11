from flask import Flask

# Creamos la instancia de la aplicación
app = Flask(__name__)

# 1. RUTA PRINCIPAL (Paso 2 de la tarea)
# Muestra el nombre del sistema y el propósito del negocio
@app.route('/')
def home():
    return '''
        <h1>Centro de Fisioterapia - Píllaro</h1>
        <p>Bienvenido al sistema de gestión de la <b>Fis. Mayra Campaña</b>.</p>
        <p>Ubicación: Cantón Píllaro, Provincia de Tungurahua.</p>
    '''

# 2. RUTA DINÁMICA (Paso 3 de la tarea)
# Recibe el nombre del paciente y devuelve un mensaje coherente
@app.route('/cita/<paciente>')
def agendar_cita(paciente):
    return f'''
        <h2>Gestión de Citas</h2>
        <p>Bienvenida, <b>{paciente}</b>. Tu solicitud en el Centro de Fisioterapia está en proceso.</p>
    '''

if __name__ == '__main__':
    # Ejecutamos el servidor en modo depuración para ver cambios en tiempo real
    app.run(debug=True)