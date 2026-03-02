import json
import csv
import os

# Configuramos la ruta hacia la carpeta data
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'data')

def guardar_paciente_en_archivos(id_p, nombre, motivo):
    """Guarda la información en los tres formatos solicitados."""

    # 1. TXT
    ruta_txt = os.path.join(DATA_PATH, 'datos.txt')
    with open(ruta_txt, 'a', encoding='utf-8') as f:
        f.write(f"ID: {id_p} | Nombre: {nombre} | Motivo: {motivo}\n")

    # 2. JSON
    ruta_json = os.path.join(DATA_PATH, 'datos.json')
    registro = {"id": id_p, "nombre": nombre, "motivo": motivo}
    lista = []
    if os.path.exists(ruta_json) and os.path.getsize(ruta_json) > 0:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            try:
                lista = json.load(f)
            except:
                lista = []
    lista.append(registro)
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

    # 3. CSV
    ruta_csv = os.path.join(DATA_PATH, 'datos.csv')
    with open(ruta_csv, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow([id_p, nombre, motivo])

# IMPORTANTE: Esta función debe estar FUERA de la anterior (sin espacios al inicio)
def leer_pacientes_json():
    """Lee el archivo JSON y devuelve la lista de pacientes."""
    ruta_json = os.path.join(DATA_PATH, 'datos.json')
    if os.path.exists(ruta_json) and os.path.getsize(ruta_json) > 0:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []