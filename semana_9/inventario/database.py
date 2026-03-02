import sqlite3
import json
import csv
import os

class Paciente:
    def __init__(self, id_paciente, nombre, edad, telefono, motivo):
        self.id = id_paciente
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.motivo = motivo

class GestionFisio:
    def __init__(self):
        self.db_name = "vitalfisio.db"
        # Definimos la ruta de la carpeta data
        self.ruta_data = os.path.join(os.path.dirname(__file__), 'inventario', 'data')
        if not os.path.exists(self.ruta_data):
            os.makedirs(self.ruta_data)
        self._inicializar_db()

    def _inicializar_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes 
                              (id INTEGER PRIMARY KEY, nombre TEXT, edad INTEGER, 
                               telefono TEXT, motivo TEXT)''')
            conn.commit()

    # --- NUEVO MÉTODO PARA SEMANA 12 ---
    def guardar_en_archivos(self, p):
        """Guarda un paciente en JSON y CSV para cumplir la Semana 12"""
        # 1. Guardar en JSON (formato lista de objetos)
        ruta_json = os.path.join(self.ruta_data, 'datos.json')
        datos_json = []
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r') as f:
                try:
                    datos_json = json.load(f)
                except: datos_json = []
        
        datos_json.append({"id": p.id, "nombre": p.nombre, "motivo": p.motivo})
        with open(ruta_json, 'w') as f:
            json.dump(datos_json, f, indent=4)

        # 2. Guardar en CSV
        ruta_csv = os.path.join(self.ruta_data, 'datos.csv')
        es_nuevo = not os.path.exists(ruta_csv)
        with open(ruta_csv, 'a', newline='') as f:
            escritor = csv.writer(f)
            if es_nuevo:
                escritor.writerow(['ID', 'Nombre', 'Motivo'])
            escritor.writerow([p.id, p.nombre, p.motivo])

    def registrar_paciente(self, p):
        """CREATE - SQLite + Archivos"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pacientes VALUES (?, ?, ?, ?, ?)", 
                           (p.id, p.nombre, p.edad, p.telefono, p.motivo))
            conn.commit()
        # Llamamos a la persistencia de archivos
        self.guardar_en_archivos(p)

    # (Mantén el resto de tus métodos: obtener_lista_pacientes, eliminar, etc. igual)
    def obtener_lista_pacientes(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pacientes")
            filas = cursor.fetchall()
            return [Paciente(*f) for f in filas]
            
    def eliminar_paciente(self, id_paciente):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
            conn.commit()