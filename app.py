from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# MODIFICACIÓN: Importamos también la función 'leer_pacientes_json'
from inventario.gestion_datos import guardar_paciente_en_archivos, leer_pacientes_json

# 1. Configuración de la Aplicación y Base de Datos (ORM)
app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'vitalfisio_v2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. Definición del Modelo de Datos (Requisito 2.4)
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)  # Cédula
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    motivo = db.Column(db.Text)

with app.app_context():
    db.create_all()

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# NUEVA RUTA: Reporte de lectura de archivos JSON (Requisito 2.2)
@app.route('/reporte')
def reporte_archivos():
    # Obtenemos los datos directamente del archivo JSON
    datos_json = leer_pacientes_json()
    total = len(datos_json)
    # Renderizamos la nueva plantilla datos.html
    return render_template('datos.html', pacientes=datos_json, total=total)

@app.route('/pacientes')
def lista_pacientes():
    todos = Paciente.query.all()
    return render_template('pacientes.html', lista=todos)

@app.route('/registrar', methods=['POST'])
def registrar():
    id_p = request.form['id']
    nom = request.form['nombre']
    eda = request.form['edad']
    tel = request.form['telefono']
    mot = request.form['motivo']
    
    nuevo = Paciente(id=id_p, nombre=nom, edad=eda, telefono=tel, motivo=mot)
    db.session.add(nuevo)
    db.session.commit()
    
    # B. Persistencia en Archivos (TXT, JSON, CSV)
    guardar_paciente_en_archivos(id_p, nom, mot)
    
    return redirect(url_for('lista_pacientes'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    id_p = request.form['id']
    paciente = Paciente.query.get(id_p)
    
    if paciente:
        paciente.telefono = request.form['telefono']
        paciente.motivo = request.form['motivo']
        db.session.commit()
        
    return redirect(url_for('lista_pacientes'))

@app.route('/eliminar/<int:id_p>')
def eliminar(id_p):
    paciente = Paciente.query.get(id_p)
    if paciente:
        db.session.delete(paciente)
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

@app.route('/cita/<paciente>')
def agendar_cita(paciente):
    return render_template('cita.html', paciente=paciente)

if __name__ == '__main__':
    app.run(debug=True)