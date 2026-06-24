# ☕ BrewLog — Plataforma para la Comunidad del Café de Especialidad

Aplicación web para la comunidad del café de especialidad. Centraliza en un
solo lugar las herramientas que hoy están dispersas: recetas técnicas, conversión
de molienda entre molinos, bitácora personal de catas y calculadora de ratio con
cronómetro.

> Trabajo Integrador — **Tecnologías para App Web**
> Licenciatura en Ciencias de la Computación / Ingeniería

---

## ✨ Funcionalidades

| Módulo | Descripción |
|--------|-------------|
| **Autenticación real** | Registro y login con contraseñas hasheadas y sesiones de usuario (Flask-Login). |
| **Feed de recetas** | Repositorio de recetas con metadatos técnicos (dosis, ratio, temperatura, tiempo, método, molienda). Filtros por método. Las recetas se guardan en la base de datos. |
| **Detalle de receta** | Vista editorial con imagen, parámetros técnicos y descripción. |
| **Conversor de molienda** | Convierte el punto de molienda entre marcas usando los micrones como referencia común (lógica en JavaScript). |
| **Calculadora de ratio + cronómetro** | Cálculo bidireccional de la proporción café/agua y cronómetro de extracción (JavaScript). |
| **Bitácora de catas** | Registro personal y privado de los granos probados, con puntaje (1–100) y notas sensoriales. Cada usuario ve solo sus catas. |

---

## 🛠️ Stack

**Backend**
- **Python 3** + **Flask** (framework web)
- **SQLite** + **SQLAlchemy** (base de datos vía ORM)
- **Flask-Login** (sesiones de usuario)
- **Werkzeug** (hash seguro de contraseñas)
- **Jinja2** (motor de plantillas)

**Frontend**
- **HTML5** semántico + **Bootstrap 5** (grilla)
- **CSS3** con sistema de _design tokens_ (custom properties) + modo claro/oscuro
- **JavaScript** vanilla (herramientas interactivas)
- Tipografías: **Playfair Display** + **Inter**

---

## 📂 Estructura del proyecto

```
brewlog/
├── run.py                  # Punto de entrada: arranca el servidor
├── config.py               # Configuración (base de datos, clave secreta)
├── requirements.txt        # Dependencias de Python
│
├── app/                    # Paquete principal de la aplicación
│   ├── __init__.py         # App factory: arma la app y registra todo
│   ├── extensions.py       # Instancias de db y login_manager
│   ├── models.py           # Modelos/tablas (Usuario, Receta, Molino, etc.)
│   ├── seed.py             # Carga de datos iniciales
│   ├── routes/             # Lógica de cada sección (blueprints)
│   │   ├── auth.py         # Registro, login, logout
│   │   ├── recipes.py      # Feed, detalle, crear receta
│   │   ├── journal.py      # Bitácora de catas
│   │   └── tools.py        # Conversor y calculadora
│   ├── templates/          # Plantillas Jinja2 (heredan de base.html)
│   └── static/             # CSS y JavaScript
│
└── .design/                # Documentación de diseño (brief, IA, tareas)
```

---

## 🚀 Cómo ejecutarlo

**Requisito:** Python 3 instalado.

```bash
# 1. Crear el entorno virtual e instalar dependencias (solo la primera vez)
python -m venv venv
venv\Scripts\activate           # En Windows
pip install -r requirements.txt

# 2. Inicializar la base de datos (solo la primera vez)
flask --app app init-db

# 3. Levantar la aplicación
python run.py
```

Luego abrir **http://localhost:5000** en el navegador.

**Cuenta de prueba:** `demo@brewlog.com` / `demo1234`
(o registrá tu propia cuenta desde la pantalla de inicio).

> Para reiniciar la base de datos: borrar `brewlog.db` y volver a ejecutar
> `flask --app app init-db`.

---

## 📐 Modelo de datos

Entidades principales implementadas como modelos SQLAlchemy en
[`app/models.py`](app/models.py): `Usuario`, `Receta`, `Molino`,
`Equipamiento` y `BitacoraCata`, con sus claves primarias y foráneas.

---

## 📄 Documentación de diseño

El proyecto se desarrolló siguiendo un flujo de diseño estructurado, documentado
en la carpeta [`.design/brewlog/`](.design/brewlog/):

- `DESIGN_BRIEF.md` — problema, principios y dirección estética
- `INFORMATION_ARCHITECTURE.md` — sitemap, navegación y flujos de usuario
- `TASKS.md` — desglose del build en tareas
