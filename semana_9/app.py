from flask import Flask, render_template, request, redirect, url_for
from database import GestionFisio, Paciente # Importamos tu lógica de POO

# 1. Inicialización única de la aplicación
app = Flask(__name__)
gestion = GestionFisio() # Instancia de tu clase de gestión

# 2. RUTA PRINCIPAL
@app.route('/')
def home():
    return render_template('index.html')

# 3. RUTA ACERCA DE
@app.route('/about')
def about():
    return render_template('about.html')

# 4. GESTIÓN DE PACIENTES (Tu nueva sección de esta semana)

# Ver lista de pacientes (READ)
@app.route('/pacientes')
def lista_pacientes():
    todos = gestion.obtener_lista_pacientes()
    return render_template('pacientes.html', lista=todos)

# Registrar paciente (CREATE)
@app.route('/registrar', methods=['POST'])
def registrar():
    # Obtenemos los datos del formulario HTML
    id_p = request.form['id']
    nom = request.form['nombre']
    eda = request.form['edad']
    tel = request.form['telefono']
    mot = request.form['motivo']
    
    # Aplicamos POO creando el objeto
    nuevo = Paciente(id_p, nom, eda, tel, mot)
    # Guardamos en la base de datos
    gestion.registrar_paciente(nuevo)
    return redirect(url_for('lista_pacientes'))

# Eliminar paciente (DELETE)
@app.route('/eliminar/<int:id_p>')
def eliminar(id_p):
    gestion.eliminar_paciente(id_p)
    return redirect(url_for('lista_pacientes'))

# 5. RUTA DINÁMICA (Citas individuales)
@app.route('/cita/<paciente>')
def agendar_cita(paciente):
    return render_template('cita.html', paciente=paciente)

# 6. Ejecución del servidor
if __name__ == '__main__':
    app.run(debug=True)
    # Actualizar paciente (UPDATE)
@app.route('/actualizar', methods=['POST'])
def actualizar():
    # Recibimos los datos del formulario de edición
    id_p = request.form['id']
    nuevo_tel = request.form['telefono']
    nuevo_mot = request.form['motivo']
    
    # Llamamos al método de la clase GestionFisio
    gestion.actualizar_paciente(id_p, nuevo_tel, nuevo_mot)
    
    # Redirigimos a la lista para ver los cambios
    return redirect(url_for('lista_pacientes'))