import mysql.connector
import os

def obtener_conexion():
    # 1. Intentamos obtener datos de variables de entorno (para Render/Clever Cloud)
    # IMPORTANTE: Los nombres deben coincidir con los de Render (DB_PASS)
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '3307') # Tu puerto local XAMPP
    db_user = os.environ.get('DB_USER', 'root')
    db_pass = os.environ.get('DB_PASS', '')    # Cambiado de DB_PASSWORD a DB_PASS
    db_name = os.environ.get('DB_NAME', 'vitalfisio')

    try:
        # Intentamos la conexión
        conexion = mysql.connector.connect(
            host=db_host,
            port=int(db_port), # Aseguramos que el puerto sea un entero
            user=db_user,
            password=db_pass,
            database=db_name,
            connect_timeout=10 # Aumentamos un poco el tiempo para la nube
        )
        
        if conexion.is_connected():
            # Imprime la dirección para saber si estamos en local o nube
            print(f"Conexión exitosa a MySQL en: {db_host}")
            return conexion

    except mysql.connector.Error as err:
        # Este error saldrá en los logs de Render si la configuración falla
        print(f"Error crítico al conectar a MySQL ({db_host}): {err}")
        return None