import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",    # Usamos la IP local para mayor estabilidad
            port=3307,           # IMPORTANTE: Tu XAMPP usa el puerto 3307
            user="root",         
            password="",         
            database="vitalfisio" 
        )
        if conexion.is_connected():
            print("Conexión exitosa a MySQL (XAMPP en puerto 3307)")
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None