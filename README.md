# E-BOT BASIC-IA 🤖

Bot de turnos para WhatsApp con inteligencia artificial.
Entiende lenguaje natural, saluda al primer contacto y envía recordatorios automáticos.

**Ideal para:** profesionales independientes que quieren un bot inteligente con costo casi cero.

---

## Stack

- Python + Flask
- Twilio WhatsApp
- NVIDIA NIM (Llama 3.1 8B) — detección de intención
- JSON en disco (sin PostgreSQL, sin Redis)
- Deploy en Railway

---

## Diferencias con EBOT BASIC

| Feature | BASIC | BASIC-IA |
|---|---|---|
| Menú numerado | ✅ | ✅ |
| Lenguaje natural | ❌ | ✅ |
| Saludo primer contacto | ❌ | ✅ |
| "No entendí" inteligente | ❌ | ✅ |
| Recordatorio 24hs | ❌ | ✅ |
| Base de datos | JSON | JSON |

---

## Estructura

```
ebot-basic-ia/
├── app.py              # servidor Flask + webhook Twilio
├── config.py           # variables de entorno + personalización
├── handlers.py         # lógica de conversación + IA
├── ai_handler.py       # detección de intención via NVIDIA NIM
├── scheduler.py        # recordatorios automáticos de turnos
├── services.py         # turnos, bloqueos, mensajes
├── storage.py          # lectura/escritura JSON en disco
├── requirements.txt
├── .env.example
├── Procfile
└── data/
    ├── estados_usuarios.json
    ├── turnos.json
    ├── bloqueos.json
    └── mensajes.json
```

---

## Variables de entorno

```env
# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# NVIDIA NIM
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Bot (personalizable por cliente)
BOT_NOMBRE=E-Bot I.A.
BOT_SALUDO=¡Hola! Soy 🤖 E-Bot I.A.\n¿En qué te puedo ayudar?
BOT_NO_ENTENDI=No entendí 😅 Te muestro el menú:
RECORDATORIO_TEXTO=📅 Recordatorio: tenés turno mañana {fecha} a las {hora} hs.\nSi necesitás cancelar respondé este mensaje. 🤖 E-Bot I.A.

# Admin
MODO_TEST=false
ADMINS=whatsapp:+549XXXXXXXXXX
```

---

## Cómo funciona la IA

El usuario puede escribir en lenguaje natural en cualquier momento:

```
"quiero sacar un turno"     → inicia flujo de turno
"cuándo tengo turno?"       → muestra sus turnos
"es urgente"                → da número de urgencias
"chau gracias"              → se despide
"kiero 1 turno"             → entiende igual (errores ortográficos)
```

Si no entiende el mensaje responde:
```
No entendí 😅 Te muestro el menú:
🤖 E-Bot I.A.
1 Turno
2 Mis turnos
...
```

---

## Recordatorio automático

`scheduler.py` corre todos los días a las 8am via Railway Cron.
Busca los turnos del día siguiente y manda un WhatsApp a cada paciente.

**Configurar en Railway:**
- Service → Settings → Cron Schedule: `0 8 * * *`
- Start Command: `python scheduler.py`
- Mismo repo que el bot principal

**Costo aproximado:**
| Volumen | Costo Twilio/mes |
|---|---|
| 50 turnos | $0.25 USD |
| 200 turnos | $1.00 USD |
| 500 turnos | $2.50 USD |

---

## Panel Admin

- **Modo test** (`MODO_TEST=true`): escribí `adm` desde cualquier número
- **Producción** (`MODO_TEST=false`): solo los números en `ADMINS` acceden

### Opciones admin
```
1 Turnos hoy
2 Próximos turnos
3 Mensajes de pacientes
4 Crear turno manual
5 Cancelar turno
6 Bloquear agenda
7 Salir
```

---

## Personalización por cliente

Todo el texto del bot se configura desde variables de entorno en Railway — sin tocar código:

- `BOT_NOMBRE` — nombre del bot
- `BOT_SALUDO` — mensaje de bienvenida
- `BOT_NO_ENTENDI` — mensaje cuando no comprende
- `RECORDATORIO_TEXTO` — texto del recordatorio (soporta `{nombre}`, `{fecha}`, `{hora}`)

---

## Deploy en Railway

1. Subir repo a GitHub
2. Railway → New Project → GitHub repo
3. Agregar variables de entorno
4. Deploy automático

**Scheduler (recordatorios):**
1. Railway → New Service → Empty Service
2. Conectar mismo repo
3. Start Command: `python scheduler.py`
4. Cron Schedule: `0 8 * * *`
5. Copiar variables de entorno

---

## Horarios

Configurados en `services.py`:

```python
HORA_INICIO = time(9, 0)
HORA_FIN    = time(19, 0)
INTERVALO   = 60  # minutos
```

---

## Precio sugerido

- **$40–60 USD/mes** (servicio + mantenimiento)
- **Pago único de instalación** + soporte por separado
