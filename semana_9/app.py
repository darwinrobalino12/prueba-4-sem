from flask import Flask, render_template, url_for

# 1. Inicialización de la aplicación
app = Flask(__name__)

# 2. RUTA PRINCIPAL (Página de Inicio)
# Ahora renderiza 'index.html', el cual hereda de 'base.html'
@app.route('/')
def home():
    # Buscamos el archivo dentro de la carpeta /templates/
    return render_template('index.html')

# 3. RUTA ACERCA DE (Nueva ruta requerida)
@app.route('/about')
def about():
    # Renderizamos la información del Centro de Fisioterapia
    return render_template('about.html')

# 4. RUTA DINÁMICA (Gestión de pacientes)
# Recibe el nombre del paciente por la URL y lo envía a la plantilla
@app.route('/cita/<paciente>')
def agendar_cita(paciente):
    # 'paciente=paciente' pasa el valor de la URL a la variable en el HTML
    return render_template('cita.html', paciente=paciente)

# 5. Ejecución del servidor
if __name__ == '__main__':
    # El modo debug permite ver cambios en tiempo real sin reiniciar
    app.run(debug=True)