import psycopg2
from psycopg2 import sql
from config.confloader import load_config
import logging
import os
import bcrypt
import json
from psycopg2.extras import Json
from config.confloader import load_config, get_db_config

#env_settings = load_config()
DISK_MOUNT_PATH = '/mnt/volume'
# Cargar configuraciones desde YAML o .env

# Nota: Las funciones relacionadas con archivos (create_drive y get_drive) 
# necesitarán una solución diferente, ya que PostgreSQL no maneja archivos directamente.
# Podrías considerar usar un sistema de archivos separado o un servicio de almacenamiento en la nube.

# Cargar toda la configuración
try:
    env_settings = load_config()
    #print(f"Configuración cargada: {env_settings}")
except Exception as e:
    logging.error(f"Error al cargar la configuración: {e}")
    raise

# Obtener la configuración específica de PostgreSQL
db_config = get_db_config(env_settings)

def create_drive(username, file):
    file_name = f"{username}/table.xlsx"
    file_path = os.path.join(DISK_MOUNT_PATH, file_name)

    # Crea el directorio si no existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Guarda el archivo en el disco montado
    with open(file_path, 'wb') as f:
        f.write(file.read())
        
    return file_path  # Devuelve la ruta del archivo guardado

def get_drive(username):
    file_name = f"{username}/table.xlsx"
    file_path = os.path.join(DISK_MOUNT_PATH, file_name)

    # Verifica si el archivo existe antes de intentar leerlo
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()  # Devuelve los datos binarios del archivo
    else:
        return None
