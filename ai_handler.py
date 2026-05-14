"""
ai_handler.py — EBOT BASIC-IA
Detecta la intención del usuario usando NVIDIA NIM (Llama 3.1 8B).
Se conecta a handlers.py sin romper nada existente.
"""

import os
import json
import requests

# ── Config NVIDIA NIM ─────────────────────────────────────────────────────────
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_MODEL   = "meta/llama-3.1-8b-instruct"

# ── Intents válidos ───────────────────────────────────────────────────────────
INTENTS_VALIDOS = {
    "TURNO",        # quiere sacar un turno
    "MIS_TURNOS",   # quiere ver sus turnos
    "CANCELAR",     # quiere cancelar un turno
    "MENSAJE",      # quiere enviar un mensaje
    "URGENCIA",     # es urgente
    "INFORMES",     # pide info / horarios
    "SALIR",        # se despide
    "MENU",         # saludo o no se entiende → mostrar menú
}

# ── Prompt del sistema ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Sos un clasificador de intenciones para un bot de turnos médicos en WhatsApp.
Tu única tarea es leer el mensaje del usuario y devolver un JSON con la intención detectada.

Intenciones posibles:
- TURNO: quiere sacar, pedir o reservar un turno
- MIS_TURNOS: quiere ver sus turnos ya sacados
- CANCELAR: quiere cancelar un turno existente
- MENSAJE: quiere dejar un mensaje o consulta
- URGENCIA: es una emergencia o algo urgente
- INFORMES: pide horarios, precios, información general
- SALIR: se despide, dice chau, gracias y listo
- MENU: saludo genérico, no se entiende, o no encaja en ninguna categoría

Respondé ÚNICAMENTE con un JSON válido, sin texto adicional, sin explicaciones.
Formato exacto:
{"intent": "NOMBRE_INTENT", "confianza": 0.0}

La confianza va de 0.0 a 1.0.
El mensaje puede estar en español rioplatense, con errores ortográficos o abreviaturas. Interpretá con sentido común."""


def detectar_intent(mensaje: str) -> dict:
    """
    Recibe el mensaje del usuario y devuelve:
    {"intent": "TURNO", "confianza": 0.95}
    
    Si falla la API, devuelve intent MENU como fallback seguro.
    """
    if not NVIDIA_API_KEY:
        return {"intent": "MENU", "confianza": 0.0, "error": "Sin API key"}

    payload = {
        "model": NVIDIA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": mensaje},
        ],
        "temperature": 0.1,   # baja temperatura = respuestas más consistentes
        "max_tokens": 60,     # solo necesitamos el JSON corto
        "top_p": 0.9,
    }

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type":  "application/json",
    }

    try:
        response = requests.post(
            NVIDIA_API_URL,
            headers=headers,
            json=payload,
            timeout=8,  # si tarda más de 8 seg, fallback
        )
        response.raise_for_status()

        data        = response.json()
        raw_content = data["choices"][0]["message"]["content"].strip()

        # Limpiar posibles backticks que el modelo agregue
        raw_content = raw_content.replace("```json", "").replace("```", "").strip()

        resultado = json.loads(raw_content)

        # Validar que el intent sea uno conocido
        if resultado.get("intent") not in INTENTS_VALIDOS:
            resultado["intent"] = "MENU"

        return resultado

    except requests.exceptions.Timeout:
        return {"intent": "MENU", "confianza": 0.0, "error": "Timeout NVIDIA NIM"}

    except requests.exceptions.RequestException as e:
        return {"intent": "MENU", "confianza": 0.0, "error": f"Error de red: {str(e)}"}

    except (json.JSONDecodeError, KeyError) as e:
        return {"intent": "MENU", "confianza": 0.0, "error": f"Respuesta inválida: {str(e)}"}


def redirigir_por_intent(numero, intent_data, msg, handlers_module):
    """
    Recibe el intent detectado y llama a la función correcta de handlers.py.
    
    Uso en handlers.py (en el FALLBACK):
        from ai_handler import detectar_intent, redirigir_por_intent
        intent = detectar_intent(body)
        redirigir_por_intent(numero, intent, msg, sys.modules[__name__])
    """
    intent = intent_data.get("intent", "MENU")

    acciones = {
        "TURNO":      lambda: handlers_module._iniciar_turno(numero, msg),
        "MIS_TURNOS": lambda: handlers_module._mis_turnos(numero, msg),
        "MENSAJE":    lambda: handlers_module._iniciar_mensaje(numero, msg),
        "URGENCIA":   lambda: handlers_module._urgencia(numero, msg),
        "INFORMES":   lambda: handlers_module._informes(numero, msg),
        "SALIR":      lambda: handlers_module._salir(numero, msg),
        "MENU":       lambda: msg.body(handlers_module.MENU_PACIENTE),
        "CANCELAR":   lambda: msg.body("Para cancelar un turno escribí *2* para ver tus turnos primero."),
    }

    accion = acciones.get(intent, acciones["MENU"])
    accion()


# ── Test rápido (correr directo: python ai_handler.py) ───────────────────────
if __name__ == "__main__":
    casos = [
        "hola buenas",
        "quiero sacar turno para el jueves",
        "cuándo tengo turno?",
        "es urgente necesito hablar",
        "mandame info de los horarios",
        "gracias chau",
        "kiero 1 turno",          # con errores ortográficos
        "necesito cancelar",
    ]

    print("=" * 50)
    print(f"Modelo: {NVIDIA_MODEL}")
    print("=" * 50)

    for caso in casos:
        resultado = detectar_intent(caso)
        print(f"'{caso}'")
        print(f"  → {resultado}")
        print()
