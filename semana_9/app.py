import os
import json
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# 1. CONFIGURACIÓN DE RUTAS (Vital para Render)
base_dir = os.path.abspath(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

# 2. IMPORTACIÓN DE CONEXIÓN MYSQL
obtener_conexion = None
try:
    from conexion.conexion import obtener_conexion 
except (ImportError, ModuleNotFoundError):
    try:
        from conexion import obtener_conexion
    except Exception as e:
        print(f"Aviso: MySQL solo disponible en local: {e}")

app = Flask(__name__)
app.secret_key = 'vitalfisio_2026_nueva' 

# 3. CONFIGURACIÓN DE BASE DE DATOS (SQLite para Pacientes)
db_path = os.path.join(base_dir, 'vitalfisio.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 4. CONFIGURACIÓN FLASK-LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# 5. MODELOS
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.String(10), primary_key=True) 
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    motivo = db.Column(db.Text)

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = str(id_usuario)  
        self.nombre = nombre
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    if obtener_conexion is None: return None
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return Usuario(user_data['id_usuario'], user_data['nombre'], user_data['mail'], user_data['password'])
        except: return None
        finally: conn.close()
    return None

# 6. PERSISTENCIA TRIPLE (TXT, JSON, CSV)
def guardar_en_archivos(id_p, nombre, motivo):
    ruta_data = os.path.join(base_dir, 'inventario', 'data')
    if not os.path.exists(ruta_data):
        os.makedirs(ruta_data, exist_ok=True)
    
    with open(os.path.join(ruta_data, 'datos.txt'), 'a', encoding='utf-8') as f:
        f.write(f"ID: {id_p} | Paciente: {nombre} | Motivo: {motivo}\n")
    
    archivo_json = os.path.join(ruta_data, 'datos.json')
    datos_lista = []
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos_lista = json.load(f)
        except: pass
    datos_lista.append({"id": id_p, "nombre": nombre, "motivo": motivo})
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos_lista, f, indent=4, ensure_ascii=False)
    
    archivo_csv = os.path.join(ruta_data, 'datos.csv')
    es_nuevo = not os.path.exists(archivo_csv)
    with open(archivo_csv, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        if es_nuevo: escritor.writerow(['ID', 'Nombre', 'Motivo'])
        escritor.writerow([id_p, nombre, motivo])

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ajustado para que coincida con tu HTML 'mail' o 'email'
        email = request.form.get('mail') or request.form.get('email')
        password = request.form.get('password')
        conn = obtener_conexion() if obtener_conexion else None
        
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (email,))
                user_data = cursor.fetchone()
                if user_data:
                    if user_data['password'] == password or check_password_hash(user_data['password'], password):
                        user_obj = Usuario(user_data['id_usuario'], user_data['nombre'], user_data['mail'], user_data['password'])
                        login_user(user_obj)
                        return redirect(url_for('lista_pacientes'))
                flash("Credenciales incorrectas", "danger")
            except Exception as e:
                flash(f"Error en base de datos: {e}", "danger")
            finally: conn.close()
        else:
            flash("MySQL (Usuarios) no disponible. Verifique conexión.", "warning")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/ver_archivos')
@login_required
def ver_archivos():
    ruta_data = os.path.join(base_dir, 'inventario', 'data')
    archivos_lista = os.listdir(ruta_data) if os.path.exists(ruta_data) else []
    archivo_json = os.path.join(ruta_data, 'datos.json')
    datos_json = []
    if os.path.exists(archivo_json):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
        except: pass
    return render_template('archivos.html', archivos=archivos_lista, datos_json=datos_json)

# --- GESTIÓN DE PACIENTES (SQLite) ---

@app.route('/pacientes')
@login_required
def lista_pacientes():
    todos = Paciente.query.all()
    return render_template('pacientes.html', lista=todos)

@app.route('/registrar', methods=['POST'])
@login_required
def registrar():
    id_p, nom = request.form.get('id'), request.form.get('nombre')
    eda, tel, mot = request.form.get('edad'), request.form.get('telefono'), request.form.get('motivo')
    if not Paciente.query.get(id_p):
        nuevo = Paciente(id=id_p, nombre=nom, edad=eda, telefono=tel, motivo=mot)
        db.session.add(nuevo)
        db.session.commit()
        guardar_en_archivos(id_p, nom, mot)
    return redirect(url_for('lista_pacientes'))

@app.route('/actualizar', methods=['POST'])
@login_required
def actualizar():
    p = Paciente.query.get(request.form.get('id'))
    if p:
        p.telefono = request.form.get('telefono')
        p.motivo = request.form.get('motivo')
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

@app.route('/eliminar/<id_p>')
@login_required
def eliminar(id_p):
    p = Paciente.query.get(id_p)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('lista_pacientes'))

# --- GESTIÓN DE USUARIOS (MySQL) ---

@app.route('/usuarios')
@login_required
def lista_usuarios():
    if not obtener_conexion: return "MySQL no disponible.", 503
    conn = obtener_conexion()
    if not conn: return "Error de conexión MySQL.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/registrar_usuario', methods=['POST'])
@login_required
def registrar_usuario():
    nom, mail, pw = request.form.get('nombre'), request.form.get('email'), request.form.get('password')
    conn = obtener_conexion()
    if conn:
        try:
            pw_hash = generate_password_hash(pw)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)", (nom, mail, pw_hash))
            conn.commit()
            flash("Usuario registrado exitosamente en MySQL", "success")
        except Exception as e: flash(f"Error: {e}", "danger")
        finally: conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/eliminar_usuario/<int:id_u>')
@login_required
def eliminar_usuario(id_u):
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_u,))
            conn.commit()
            flash("Usuario eliminado", "warning")
        except Exception as e: flash(f"Error: {e}", "danger")
        finally: conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/cita/<nombre>')
def confirmar_cita(nombre):
    return f'<div style="text-align:center; margin-top:50px; font-family:Arial;"><h1 style="color: #0d6efd;">VitalFisio Píllaro</h1><p>Cita para <b>{nombre}</b> confirmada.</p><a href="/">Volver</a></div>'

# --- INICIALIZACIÓN ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)