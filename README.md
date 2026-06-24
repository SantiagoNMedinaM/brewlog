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
| **Feed de recetas** | Repositorio social de recetas con metadatos técnicos normalizados (dosis, ratio, temperatura, tiempo, método, molienda). Grid responsive con filtros por método de extracción. |
| **Detalle de receta** | Vista editorial con imagen hero, parámetros técnicos destacados y preparación paso a paso. |
| **Conversor de molienda** | Convierte el punto de molienda entre marcas de molinos usando el tamaño de partícula en micrones como referencia común. Recálculo en tiempo real. |
| **Calculadora de ratio + cronómetro** | Cálculo bidireccional de la proporción café/agua y cronómetro de extracción con tiempo objetivo por método. |
| **Bitácora de catas** | Registro personal de los granos probados, con puntaje estilo SCA (1–100) y notas sensoriales (aroma, sabor, textura, retrogusto). |
| **Autenticación** | Pantalla de login/registro con tabs, validación inline y barra de fortaleza de contraseña. |

---

## 🛠️ Stack

- **HTML5** semántico
- **CSS3** con sistema de _design tokens_ (custom properties) + **Bootstrap 5** como base de grilla
- **JavaScript** vanilla (sin frameworks ni build step)
- Tipografías: **Playfair Display** (display) + **Inter** (cuerpo)
- **Modo claro / oscuro** persistente con `localStorage`

---

## 📂 Estructura del proyecto

```
brewlog/
├── assets/
│   ├── css/
│   │   ├── tokens.css        # Variables de diseño (color, tipografía, espaciado, dark mode)
│   │   ├── main.css          # Estilos base globales + overrides de Bootstrap
│   │   └── pages/            # Estilos por sección (auth, recipes, tools, journal)
│   └── js/
│       ├── auth.js           # Validación, tabs y toggle de contraseña
│       ├── grind-converter.js
│       └── ratio-calculator.js
├── views/
│   ├── auth/login.html       # Login + registro
│   ├── recipes/              # feed.html, detail.html
│   ├── tools/                # grind-converter.html, ratio-calculator.html
│   ├── journal/              # index.html, create.html
│   └── profile/
└── .design/                  # Documentación de diseño (brief, IA, tokens, tareas)
```

---

## 🚀 Cómo ejecutarlo

Al ser HTML/CSS/JS estático, no requiere instalación. Cualquiera de estas opciones:

**Opción 1 — Servidor con Python**
```bash
python -m http.server 8080
```
Luego abrir `http://localhost:8080/views/auth/login.html`

**Opción 2 — Live Server (VS Code)**
Abrir `views/auth/login.html` y hacer clic en **Go Live**.

**Opción 3 — Directo**
Abrir los archivos `.html` con doble clic en el navegador.

---

## 📐 Modelo de datos

Entidades principales: `Usuario`, `Receta`, `Molino`, `Equipamiento`,
`Bitacora_Cata` y `Conversion_Molienda`. El diseño completo del modelo
entidad-relación está documentado en la entrega de la Primera Etapa.

---

## 📄 Documentación de diseño

El proyecto se desarrolló siguiendo un flujo de diseño estructurado, documentado
en la carpeta [`.design/brewlog/`](.design/brewlog/):

- `DESIGN_BRIEF.md` — problema, principios y dirección estética
- `INFORMATION_ARCHITECTURE.md` — sitemap, navegación y flujos de usuario
- `TASKS.md` — desglose del build en tareas
