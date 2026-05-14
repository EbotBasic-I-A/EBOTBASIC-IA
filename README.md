# E-BOT BASIC 🦙

Bot de turnos para WhatsApp. Sin base de datos — todo se guarda en archivos JSON en disco.

**Ideal para:** profesionales independientes que quieren un bot funcional con costo casi cero.

---

## Stack

- Python + Flask
- Twilio WhatsApp
- JSON en disco (sin PostgreSQL, sin Redis)
- Deploy en cualquier VPS barato o Render free

---

## Estructura

```
ebot-basic/
├── app.py            # servidor Flask + webhook Twilio
├── config.py         # variables de entorno
├── handlers.py       # lógica de conversación
├── services.py       # turnos, bloqueos, mensajes
├── storage.py        # lectura/escritura JSON en disco
├── requirements.txt
├── .env.example
├── Procfile          # para Render / Railway
└── data/             # carpeta generada automáticamente
    ├── estados_usuarios.json
    ├── turnos.json
    ├── bloqueos.json
    └── mensajes.json
```

---

## Instalación local

```bash
git clone <repo>
cd ebot-basic
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # completar con tus credenciales
python app.py
```

---

## Deploy en Render (free)

1. Crear cuenta en [render.com](https://render.com)
2. New → Web Service → conectar repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Agregar las variables de entorno del `.env.example`
6. Deploy

> ⚠️ Render free tiene filesystem efímero — los JSON se pierden al reiniciar.
> Para persistencia real usá un VPS con disco persistente (DigitalOcean, Hetzner, etc.)

---

## Deploy en VPS (recomendado para producción)

```bash
# En el servidor
git clone <repo>
cd ebot-basic
pip install -r requirements.txt
cp .env.example .env    # editar con credenciales reales
gunicorn app:app --bind 0.0.0.0:5000 --daemon
```

La carpeta `data/` se crea automáticamente y persiste entre reinicios.

---

## Configuración Twilio

1. Twilio Console → Messaging → Sandbox (o número comprado)
2. Webhook URL: `https://TU_DOMINIO/webhook`
3. Método: POST

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

## Horarios

Configurados en `services.py`:

```python
HORA_INICIO = time(9, 0)
HORA_FIN    = time(19, 0)
INTERVALO   = 60  # minutos
```

Modificar esos valores para adaptar al cliente.

---

## Archivos de datos

| Archivo | Contenido |
|---|---|
| `data/estados_usuarios.json` | Estado de conversación por número |
| `data/turnos.json` | Turnos agendados |
| `data/bloqueos.json` | Horarios bloqueados |
| `data/mensajes.json` | Mensajes enviados por pacientes |

---

## Precio sugerido

- **$20–30 USD/mes** (servicio + mantenimiento)
- **Pago único de instalación** + soporte por separado
