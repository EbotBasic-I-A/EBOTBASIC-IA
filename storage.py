"""
storage.py — persistencia en JSON (E-BOT BASIC 🦙)

Todos los datos se guardan en archivos .json en disco.
No requiere base de datos ni dependencias externas.

Archivos generados automáticamente:
    estado.json    →  estados de conversación por usuario
    turnos.json    →  turnos agendados
    bloqueos.json  →  horarios bloqueados
    mensajes.json  →  mensajes de pacientes
"""

import json
import os

# ─────────────────────────────────────────────────────────────────────────────
# Directorio de datos
# Por defecto: carpeta "data/" junto al proyecto.
# Podés cambiarlo con la variable de entorno DATA_DIR.
# ─────────────────────────────────────────────────────────────────────────────

DATA_DIR = os.getenv("DATA_DIR", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def _path(key: str) -> str:
    """
    Convierte una clave en un path de archivo .json dentro de DATA_DIR.

    Ejemplos:
        "estados_usuarios"  →  "data/estados_usuarios.json"
        "turnos.json"       →  "data/turnos.json"
    """
    # Si la clave ya tiene extensión .json la respetamos,
    # si no, la agregamos.
    filename = key if key.endswith(".json") else f"{key}.json"
    return os.path.join(DATA_DIR, filename)


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────

def cargar_json(key: str) -> dict:
    """
    Lee un documento JSON del disco por clave.
    Retorna {} si el archivo no existe o está corrupto.
    """
    path = _path(key)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Archivo corrupto o ilegible → empezamos limpio
        return {}


def guardar_json(key: str, data: dict):
    """
    Guarda un documento JSON en disco por clave.
    Escribe de forma atómica para evitar corrupción ante reinicios.
    """
    path = _path(key)
    tmp  = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)   # rename atómico
    except OSError as e:
        # En producción podés loguear el error aquí
        raise RuntimeError(f"Error guardando {path}: {e}") from e
