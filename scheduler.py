"""
scheduler.py — Recordatorio automático de turnos 🦙
Correr una vez al día (recomendado: 8:00 hs) via Railway Cron.

Busca todos los turnos del día siguiente y manda un WhatsApp
de recordatorio a cada paciente via Twilio.

Variables de entorno necesarias (ya las tenés en Railway):
    TWILIO_ACCOUNT_SID
    TWILIO_AUTH_TOKEN
    TWILIO_WHATSAPP_FROM
"""

import os
import sys
from datetime import datetime, timedelta
from twilio.rest import Client
from storage import cargar_json
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    TURNOS_FILE,
)

# ── Personalización del recordatorio ─────────────────────────────────────────
# Modificar para adaptar al cliente
RECORDATORIO_TEXTO = os.getenv(
    "RECORDATORIO_TEXTO",
    "📅 Recordatorio: tenés turno mañana {fecha} a las {hora} hs.\n"
    "Si necesitás cancelar respondé este mensaje. 🦙 E-Bot I.A."
)


def obtener_turnos_manana() -> list[dict]:
    """Devuelve los turnos del día siguiente."""
    manana = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    turnos = cargar_json(TURNOS_FILE).get("data", [])
    return [t for t in turnos if t["fecha"] == manana]


def enviar_recordatorio(turno: dict, client: Client) -> bool:
    """
    Manda el WhatsApp de recordatorio a un paciente.
    Retorna True si fue exitoso, False si falló.
    """
    texto = RECORDATORIO_TEXTO.format(
        nombre=turno["nombre"],
        fecha=turno["fecha"],
        hora=turno["hora"],
    )

    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=turno["telefono"],
            body=texto,
        )
        print(f"✅ Recordatorio enviado a {turno['nombre']} ({turno['telefono']}) — SID: {message.sid}")
        return True

    except Exception as e:
        print(f"❌ Error enviando a {turno['nombre']} ({turno['telefono']}): {e}")
        return False


def main():
    print(f"{'='*50}")
    print(f"🦙 E-Bot Scheduler — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*50}")

    # Verificar credenciales
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("❌ Faltan credenciales de Twilio. Verificar variables de entorno.")
        sys.exit(1)

    # Obtener turnos de mañana
    turnos = obtener_turnos_manana()
    manana = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

    if not turnos:
        print(f"📭 Sin turnos para mañana ({manana}). Nada que enviar.")
        sys.exit(0)

    print(f"📋 Turnos para mañana ({manana}): {len(turnos)}")
    print()

    # Iniciar cliente Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Enviar recordatorios
    enviados = 0
    fallidos = 0

    for turno in turnos:
        exito = enviar_recordatorio(turno, client)
        if exito:
            enviados += 1
        else:
            fallidos += 1

    # Resumen
    print()
    print(f"{'='*50}")
    print(f"✅ Enviados: {enviados}")
    if fallidos:
        print(f"❌ Fallidos: {fallidos}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
