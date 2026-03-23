from conexion.conexion import obtener_conexion

class PacienteService:
    @staticmethod
    def listar():
        db = obtener_conexion()
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pacientes")
            res = cursor.fetchall()
            db.close()
            return res
        return []

    @staticmethod
    def insertar(nombre, apellido, cedula, telefono, email):
        db = obtener_conexion()
        cursor = db.cursor()
        sql = "INSERT INTO pacientes (nombre, apellido, cedula, telefono, email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, apellido, cedula, telefono, email))
        db.commit()
        db.close()

    @staticmethod
    def eliminar(id_paciente):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id_paciente = %s", (id_paciente,))
        db.commit()
        db.close()