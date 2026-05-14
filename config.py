"""
config.py — configuración de E-BOT BASIC 🦙
Variables de entorno (setear en .env o en el panel de tu VPS/Render):
    MODO_TEST           true | false   (default: true)
    ADMINS              whatsapp:+5491100000000,whatsapp:+5491199999999
    TWILIO_ACCOUNT_SID  tu SID de Twilio
    TWILIO_AUTH_TOKEN   tu token de Twilio
    TWILIO_WHATSAPP_FROM whatsapp:+14155238886
    DATA_DIR            carpeta donde se guardan los JSON (default: data/)
"""
import os

# ── Modo test ─────────────────────────────────────────────────────────────────
# true  →  cualquier usuario puede escribir "adm" para entrar al panel admin
# false →  solo los números en ADMINS acceden al panel admin
MODO_TEST = os.getenv("MODO_TEST", "true").lower() == "true"

# ── Admins ────────────────────────────────────────────────────────────────────
_admins_raw = os.getenv("ADMINS", "")
ADMINS = [a.strip() for a in _admins_raw.split(",") if a.strip()]

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID   = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN    = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# ── Claves de archivos JSON ───────────────────────────────────────────────────
TURNOS_FILE   = "turnos.json"
BLOQUEOS_FILE = "bloqueos.json"
MENSAJES_FILE = "mensajes.json"

# ── Personalización del bot ───────────────────────────────────────────────────
# Modificar estos valores para adaptar el bot a cada cliente
BOT_NOMBRE = os.getenv("BOT_NOMBRE", "E-Bot I.A.")
BOT_SALUDO = os.getenv("BOT_SALUDO", "¡Hola! Soy 🤖 E-Bot I.A.\n¿En qué te puedo ayudar?")
BOT_NO_ENTENDI = os.getenv("BOT_NO_ENTENDI", "No entendí 😅 Te muestro el menú:")
