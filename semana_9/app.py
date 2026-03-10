import os
import json
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# 1. CONFIGURACIÓN DE RUTAS (Vital para encontrar módulos en Render)
base_dir = os.path.abspath(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

# 2. IMPORTACIÓN DE CONEXIÓN MYSQL (XAMPP)
obtener_conexion = None
try:
    # Intento robusto de importación para local y nube
    from conexion.conexion import obtener_conexion 
except (ImportError, ModuleNotFoundError):
    try:
        from conexion import obtener_conexion
    except Exception as e:
        print(f"Aviso: MySQL solo disponible en local: {e}")

app = Flask(__name__)

# 3. CONFIGURACIÓN DE BASE DE DATOS (SQLite con Ruta Absoluta Forzada)
# Esto evita que Render cree la base de datos en carpetas temporales volátiles
db_path = os.path.join(base_dir, 'vitalfisio.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 4. MODELO DE DATOS (SQLite)
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.String(10), primary_key=True) 
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    motivo = db.Column(db.Text)

# 5. FUNCIÓN DE PERSISTENCIA TRIPLE (Mantenida intacta para escalar)
def guardar_en_archivos(id_p, nombre, motivo):
    ruta_data = os.path.join(base_dir, 'inventario', 'data')
    if not os.path.exists(ruta_data):
        os.makedirs(ruta_data, exist_ok=True)

    # TXT
    with open(os.path.join(ruta_data, 'datos.txt'), 'a', encoding='utf-8') as f:
        f.write(f"ID: {id_p} | Paciente: {nombre} | Motivo: {motivo}\n")

    # JSON
    archivo_json = os.path.join(ruta_data, 'datos.json')
    datos_lista = []
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
                if isinstance(contenido, list): datos_lista = contenido
        except: pass
    
    datos_lista.append({"id": id_p, "nombre": nombre, "motivo": motivo})
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos_lista, f, indent=4, ensure_ascii=False)

    # CSV
    archivo_csv = os.path.join(ruta_data, 'datos.csv')
    es_nuevo = not os.path.exists(archivo_csv)
    with open(archivo_csv, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        if es_nuevo: escritor.writerow(['ID', 'Nombre', 'Motivo'])
        escritor.writerow([id_p, nombre, motivo])

# --- RUTAS DE NAVEGACIÓN (Corregidas para evitar BuildError) ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pacientes')
def lista_pacientes():
    # Agregamos un try-except aquí para que la web no muera si hay error de DB
    try:
        todos = Paciente.query.all()
        return render_template('pacientes.html', lista=todos)
    except Exception as e:
        print(f"Error cargando pacientes: {e}")
        return render_template('pacientes.html', lista=[])

@app.route('/ver_archivos')
def ver_archivos():
    ruta_json = os.path.join(base_dir, 'inventario', 'data', 'datos.json')
    datos = []
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except: pass
    return render_template('datos.html', datos=datos)

# --- OPERACIONES PACIENTES (SQLite) ---

@app.route('/registrar', methods=['POST'])
def registrar():
    id_p = request.form.get('id')
    nom = request.form.get('nombre')
    eda = request.form.get('edad')
    tel = request.form.get('telefono')
    mot = request.form.get('motivo')
    
    if Paciente.query.get(id_p):
        return "Error: La cédula ya está registrada", 400
        
    nuevo = Paciente(id=id_p, nombre=nom, edad=eda, telefono=tel, motivo=mot)
    db.session.add(nuevo)
    db.session.commit()
    guardar_en_archivos(id_p, nom, mot)
    return redirect(url_for('lista_pacientes'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    paciente = Paciente.query.get(request.form.get('id'))
    if paciente:
        paciente.telefono = request.form.get('telefono')
        paciente.motivo = request.form.get('motivo')
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

@app.route('/eliminar/<string:id_p>')
def eliminar(id_p):
    p = Paciente.query.get(id_p)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

# --- GESTIÓN DE USUARIOS (MySQL - Local) ---

@app.route('/usuarios')
def lista_usuarios():
    if obtener_conexion is None:
        return "Módulo MySQL no disponible en este servidor (Render). Use la versión local para esta función.", 503
    
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
        return "Error: MySQL no disponible.", 500
    
    nom = request.form.get('nombre')
    mail = request.form.get('email')
    pw = request.form.get('password')
    
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)", (nom, mail, pw))
        conn.commit()
        conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/cita/<nombre>')
def confirmar_cita(nombre):
    return f'<div style="text-align:center; margin-top:50px; font-family:Arial;"><h1 style="color: #d81b60;">VitalFisio Píllaro</h1><p>Cita para <b>{nombre}</b> confirmada.</p><a href="/">Volver</a></div>'

# --- BLOQUE DE INICIO OPTIMIZADO ---
if __name__ == '__main__':
    with app.app_context():
        # Esto asegura que las tablas existan siempre antes de que el servidor responda
        db.create_all() 
        
    port = int(os.environ.get('PORT', 5000))
    # En Render 'debug' debe ser False para producción, pero en local ayuda tenerlo en True
    app.run(host='0.0.0.0', port=port, debug=True)