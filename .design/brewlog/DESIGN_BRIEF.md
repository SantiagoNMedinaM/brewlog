# Design Brief: BrewLog — Plataforma para la Comunidad del Café de Especialidad

## Problem

El home brewer o barista aficionado que practica café de especialidad no tiene un lugar único donde consultar recetas técnicas confiables, convertir la molienda de su molino al que usa una receta ajena, ni registrar sus propias experiencias de cata de forma estructurada. El conocimiento está fragmentado en foros, grupos y notas personales, y cada preparación parte desde cero.

## Solution

Una plataforma web centralizada que combina cuatro herramientas en una experiencia cohesiva: un feed de recetas técnicas con metadatos normalizados, un conversor de puntos de molienda entre marcas de molinos, una bitácora personal de catas y una calculadora de ratio con cronómetro. El usuario puede descubrir una receta, adaptarla a su equipo y registrar el resultado sin salir de la app.

## Experience Principles

1. **Precisión sobre simplificación** — La plataforma no esconde la complejidad técnica del café. Los datos (gramos, ratio, temperatura, micrones) se presentan de forma legible, no como ruido.
2. **Personal antes que social** — La bitácora y las herramientas son de uso privado por defecto. Compartir es una elección deliberada, no el default.
3. **Consistencia sobre variedad** — Una sola paleta, una sola escala tipográfica, una sola lógica de cards. El contenido es el protagonista.

## Aesthetic Direction

- **Philosophy**: Editorial / Magazine — el café de especialidad tiene una cultura visual fuerte. Las recetas merecen el tratamiento de un artículo de revista especializada: tipografía grande, jerarquía clara, imagen protagonista.
- **Tone**: Cálido, artesanal, confiable. No minimalista frío. No rústico kitsch. El punto medio entre una tostadora de especialidad y una guía Michelin.
- **Reference points**: Standart Coffee, Counter Culture Coffee, revistas como Standart Magazine. Interfaces como Whisk (recipes) o Notion (estructura limpia).
- **Anti-references**: Starbucks app (demasiado comercial), Reddit (demasiado crudo), apps de delivery (demasiado transaccional).

## Existing Patterns

El proyecto tiene prácticas anteriores en Bootstrap 5 con el siguiente stack ya validado:

- **Typography**: Inter (body, 300/400/500) + Montserrat (headings, 500/700) — ambas ya cargadas en el proyecto anterior. Para el proyecto definitivo se actualiza a: **Playfair Display** (display/h1-h2) + **Inter** (body).
- **Colors**: Paleta café ya usada: `#3b2818` (primary), `#24180e` (dark), `#fcfbf9` (background). Se expande con la paleta completa de tokens.
- **Spacing**: Bootstrap 5 spacing scale (4px base) — se extiende con custom properties.
- **Components**: Ningún componente reutilizable definido aún. Todo es nuevo.

## Component Inventory

| Component | Status | Notes |
|---|---|---|
| tokens.css | New | Variables CSS para toda la paleta, tipografía y espaciado |
| Navbar | New | Sticky, dark, con logo + nav links + botón CTA |
| Auth split-screen | New | Login + Registro con tabs, validación HTML5 + JS |
| Recipe Card | New | Imagen + metadatos técnicos + badge de método |
| Recipe Feed | New | Grid responsive de Recipe Cards con filtros |
| Recipe Detail | New | Layout editorial: imagen hero + datos técnicos + notas |
| Grind Converter | New | Select de molino origen/destino + input de punto + resultado |
| Ratio Calculator | New | Inputs de dosis/volumen + cronómetro integrado |
| Tasting Journal | New | Lista de entradas + formulario de nueva cata |
| Tasting Entry Form | New | Inputs de puntuación, notas de sabor, aroma, textura |

## Key Interactions

- **Auth tabs**: click en "Registrarse" / "Iniciar Sesión" intercambia el formulario con fade. Sin recarga de página.
- **Toggle password**: botón de ojo en input de contraseña alterna `type="password"` / `type="text"`.
- **Validación inline**: clases `.is-valid` / `.is-invalid` se aplican al `blur` del input, no al submit.
- **Grind Converter**: al cambiar cualquier input (molino origen, molino destino, punto de molienda), el resultado se recalcula en tiempo real sin botón de submit.
- **Cronómetro**: botón Start/Stop/Reset. Muestra tiempo en formato `MM:SS`. Vibra (si está en mobile) al llegar al tiempo objetivo.
- **Recipe Card hover**: elevación suave (`translateY(-2px)` + sombra mayor). Sin animaciones de escalado.

## Responsive Behavior

- **Mobile (375px)**: columna única. Navbar colapsa a hamburger. Auth ocupa ancho completo sin panel de imagen. Cards en una columna.
- **Tablet (768px)**: grid de 2 columnas para cards. Auth muestra panel de imagen lateral.
- **Desktop (1280px+)**: grid de 3 columnas para recipe feed. Split-screen 50/50 en auth.
- Navegación: hamburger en mobile, barra horizontal completa en desktop.

## Accessibility Requirements

- Contraste mínimo WCAG AA (4.5:1 para texto de cuerpo, 3:1 para texto grande).
- Todos los inputs con `<label>` asociado mediante `for`/`id`.
- Botones con `aria-label` cuando no tienen texto visible (toggle password, close modal).
- Focus rings visibles en todos los elementos interactivos.
- Imágenes de recetas con `alt` descriptivo.
- `prefers-reduced-motion`: desactivar todas las transiciones CSS dentro de esta media query.

## Out of Scope

- Backend real (base de datos, autenticación server-side, API). Todo con datos mock/estáticos.
- Sistema de likes o comentarios en recetas.
- Notificaciones o sistema de mensajería.
- Upload de imágenes (se usan URLs de Unsplash como placeholder).
- PWA / Service Workers.
- Testing automatizado.
