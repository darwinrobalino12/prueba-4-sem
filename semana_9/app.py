import os
import json
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- CONFIGURACIÓN DE RUTAS PARA IMPORTACIÓN ---
# Esto fuerza a Python a mirar dentro de 'semana_9' para encontrar 'conexion'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    # Intento de importación robusto
    from conexion.conexion import obtener_conexion 
except (ImportError, ModuleNotFoundError) as e:
    print(f"Aviso: Error al importar conexion: {e}")
    # Intento alternativo
    try:
        from conexion import obtener_conexion
    except:
        obtener_conexion = None

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS (SQLite) ---
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'vitalfisio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO DE DATOS (SQLite) ---
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.String(10), primary_key=True) 
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    motivo = db.Column(db.Text)

# --- FUNCIÓN DE PERSISTENCIA TRIPLE (TXT, JSON, CSV) ---
def guardar_en_archivos(id_p, nombre, motivo):
    ruta_data = os.path.join(base_dir, 'inventario', 'data')
    if not os.path.exists(ruta_data):
        os.makedirs(ruta_data)

    # 1. TXT
    with open(os.path.join(ruta_data, 'datos.txt'), 'a', encoding='utf-8') as f:
        f.write(f"ID: {id_p} | Paciente: {nombre} | Motivo: {motivo}\n")

    # 2. JSON
    archivo_json = os.path.join(ruta_data, 'datos.json')
    datos_lista = []
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
                if isinstance(contenido, list):
                    datos_lista = contenido
        except:
            datos_lista = []
    
    datos_lista.append({"id": id_p, "nombre": nombre, "motivo": motivo})
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos_lista, f, indent=4, ensure_ascii=False)

    # 3. CSV
    archivo_csv = os.path.join(ruta_data, 'datos.csv')
    es_nuevo = not os.path.exists(archivo_csv)
    with open(archivo_csv, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        if es_nuevo:
            escritor.writerow(['ID', 'Nombre', 'Motivo'])
        escritor.writerow([id_p, nombre, motivo])

# --- RUTAS ESTÁNDAR ---
@app.route('/')
def home():
    return render_template('index.html')

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
    
    if Paciente.query.get(id_p):
        return "Error: La cédula ya está registrada", 400

    nuevo = Paciente(id=id_p, nombre=nom, edad=eda, telefono=tel, motivo=mot)
    db.session.add(nuevo)
    db.session.commit()
    
    guardar_en_archivos(id_p, nom, mot)
    return redirect(url_for('lista_pacientes'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    paciente = Paciente.query.get(request.form['id'])
    if paciente:
        paciente.telefono = request.form['telefono']
        paciente.motivo = request.form['motivo']
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

@app.route('/eliminar/<string:id_p>') 
def eliminar(id_p):
    p = Paciente.query.get(id_p)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ver_archivos')
def ver_archivos():
    ruta_json = os.path.join(base_dir, 'inventario', 'data', 'datos.json')
    datos = []
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except:
            datos = []
    return render_template('datos.html', datos=datos)

# --- NUEVAS RUTAS PARA GESTIÓN DE USUARIOS (MySQL / XAMPP) ---

@app.route('/usuarios')
def lista_usuarios():
    if obtener_conexion is None:
        return "Error: No se pudo cargar el módulo de conexión a MySQL.", 500
        
    conn = obtener_conexion()
    usuarios = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    if obtener_conexion is None:
        return "Error: No se pudo cargar el módulo de conexión a MySQL.", 500

    nom = request.form['nombre']
    mail = request.form['email']
    pw = request.form['password']
    
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)", (nom, mail, pw))
        conn.commit()
        conn.close()
    return redirect(url_for('lista_usuarios'))

# --- RUTA DINÁMICA ---
@app.route('/cita/<nombre>')
def confirmar_cita(nombre):
    return f'''
    <div style="text-align:center; margin-top:50px; font-family:Arial;">
        <h1 style="color: #d81b60;">VitalFisio Píllaro</h1>
        <p style="font-size:1.2rem;">Bienvenido/a, <strong>{nombre}</strong>.</p>
        <p>Tu cita de rehabilitación ha sido registrada exitosamente en nuestro sistema.</p>
        <a href="/" style="color: #1976d2;">Volver al Inicio</a>
    </div>
    '''

# --- BLOQUE DE INICIO ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    import sys
import os

# Esto fuerza a Python a mirar en la carpeta actual para encontrar 'conexion'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from conexion.conexion import obtener_conexion
except (ImportError, ModuleNotFoundError):
    from conexion import obtener_conexion