import sqlite3

# --- CLASE PACIENTE (POO) ---
# Cumple con el requisito de atributos específicos y métodos (constructor)
class Paciente:
    def __init__(self, id_paciente, nombre, edad, telefono, motivo):
        self.id = id_paciente
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.motivo = motivo

# --- CLASE GESTION (POO + Colecciones + CRUD SQLite) ---
class GestionFisio:
    def __init__(self):
        # Nombre de la base de datos SQLite
        self.db_name = "vitalfisio.db"
        self._inicializar_db()

    def _inicializar_db(self):
        """Crea la tabla de pacientes si no existe (Persistencia)"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes 
                              (id INTEGER PRIMARY KEY, nombre TEXT, edad INTEGER, 
                               telefono TEXT, motivo TEXT)''')
            conn.commit()

    def registrar_paciente(self, p):
        """Operación: CREATE - Recibe un objeto de la clase Paciente"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pacientes (id, nombre, edad, telefono, motivo) VALUES (?, ?, ?, ?, ?)", 
                           (p.id, p.nombre, p.edad, p.telefono, p.motivo))
            conn.commit()

    def obtener_lista_pacientes(self):
        """Operación: READ - Retorna una LISTA de objetos Paciente (Colección)"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pacientes")
            filas = cursor.fetchall()
            # Transformamos los datos planos de la DB en una colección de objetos POO
            return [Paciente(*f) for f in filas]

    def buscar_por_nombre(self, nombre_buscado):
        """Uso de colecciones para filtrar de forma eficiente"""
        todos = self.obtener_lista_pacientes()
        # Filtramos la lista usando una List Comprehension
        return [p for p in todos if nombre_buscado.lower() in p.nombre.lower()]

    def actualizar_paciente(self, id_paciente, nuevo_tel, nuevo_motivo):
        """Operación: UPDATE - Actualiza datos específicos por ID"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE pacientes 
                              SET telefono = ?, motivo = ? 
                              WHERE id = ?''', (nuevo_tel, nuevo_motivo, id_paciente))
            conn.commit()

    def eliminar_paciente(self, id_paciente):
        """Operación: DELETE - Elimina un registro por su ID único"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
            conn.commit()