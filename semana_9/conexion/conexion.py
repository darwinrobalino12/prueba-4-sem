import mysql.connector
import os

def obtener_conexion():
    # 1. Prioridad: Variables de Entorno (Render / Clever Cloud)
    # Si no existen, usa los valores por defecto para tu XAMPP local (3307)
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '3307') # <--- Aquí el puerto de tu XAMPP
    db_user = os.environ.get('DB_USER', 'root')
    db_pass = os.environ.get('DB_PASS', '') 
    db_name = os.environ.get('DB_NAME', 'vitalfisio')

    try:
        conexion = mysql.connector.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            password=db_pass,
            database=db_name,
            connect_timeout=15
        )
        
        if conexion.is_connected():
            return conexion

    except mysql.connector.Error as err:
        print(f"Error crítico de conexión: {err}")
        return None
    