# Build Tasks: BrewLog

Generated from: .design/brewlog/DESIGN_BRIEF.md
Date: 2026-05-15

---

## Foundation

- [x] **tokens.css**: Variables CSS completas (colores semánticos, tipografía, espaciado, sombras, motion, dark mode). _Archivo: `assets/css/tokens.css`._
- [x] **main.css**: Hoja de estilos principal. Importa tokens.css, resetea estilos base de Bootstrap que conflictúen, define tipografía global (`body`, headings) con las fuentes Playfair Display + Inter. _Archivo: `assets/css/main.css`._
- [x] **Estructura de carpetas**: Estructura de directorios completa creada (`assets/css/pages/`, `assets/js/`, `assets/img/`, `views/auth/`, `views/recipes/`, `views/tools/`, `views/journal/`, `views/profile/`).

## Core UI

- [x] **Navbar**: Componente sticky dark con logo "BrewLog" + links de navegación (Recetas, Herramientas, Bitácora) + avatar/dropdown de usuario. Hamburger en mobile. _Reutilizado en feed, detail, tools y journal._
- [x] **Auth: pantalla de Login/Registro**: Layout split-screen (imagen + formulario). Tabs que intercambian entre login y registro con fade JS. Validación inline en blur. Toggle de contraseña. _Archivos: `views/auth/login.html` + `assets/js/auth.js` + `assets/css/pages/auth.css`._
- [x] **Recipe Card**: Card con imagen, badge de método, título, metadatos técnicos (dosis, ratio, temp, tiempo), autor + likes. Hover con elevación. _En `views/recipes/feed.html` + `assets/css/pages/recipes.css`._
- [x] **Recipe Feed**: Grid responsive de Recipe Cards (1/2/3 col) + filtros de método por pills. CTA "Nueva Receta". _Archivo: `views/recipes/feed.html`._
- [x] **Recipe Detail**: Layout editorial con hero a ancho completo, parámetros técnicos en grilla, cuerpo narrativo con pasos, acciones (guardar/convertir). _Archivo: `views/recipes/detail.html`._

## Interactions & States

- [x] **Auth — validación JS**: Aplica `.is-valid` / `.is-invalid` en blur, verifica coincidencia de contraseñas, barra de fortaleza. _Archivo: `assets/js/auth.js`._
- [x] **Conversor de Molienda**: Dos selects de molino (origen/destino) + input de punto + resultado en tiempo real (sin botón). Conversión vía micrones. Tabla de equivalencias colapsable. _Archivos: `views/tools/grind-converter.html` + `assets/js/grind-converter.js` + `assets/css/pages/tools.css`._
- [x] **Calculadora de Ratio + Cronómetro**: Inputs café/agua/ratio con recálculo bidireccional. Cronómetro Start/Pause/Reset con tiempo objetivo por método y feedback visual/háptico. _Archivos: `views/tools/ratio-calculator.html` + `assets/js/ratio-calculator.js`._
- [x] **Bitácora de Catas — lista**: Lista de entradas con puntaje, grano, notas en chips, fecha. Estado vacío de referencia. _Archivos: `views/journal/index.html` + `assets/css/pages/journal.css`._
- [x] **Bitácora de Catas — formulario nueva entrada**: Campos de grano (nombre, origen, tostador), método, receta vinculada, slider de puntaje 1-100, textareas de notas, toggle recomendaría. _Archivo: `views/journal/create.html`._

## Responsive & Polish

- [ ] **Responsive pass**: Verificar que todas las páginas funcionen en 375px (mobile), 768px (tablet) y 1280px (desktop). Corregir overflow horizontal, tamaño de touch targets (mínimo 44px), texto mínimo 16px en mobile.
- [ ] **Dark mode toggle**: Botón en la navbar que alterna `data-theme="dark"` en `<html>`. Persistencia con `localStorage`. Asegurarse de que todos los componentes usen tokens (sin hex hardcodeados).
- [ ] **Accessibility pass**: Verificar contraste WCAG AA en colores de texto, labels asociados a inputs, aria-labels en botones sin texto, focus rings visibles en todos los elementos interactivos.

## Review

- [ ] **Design review**: Correr /design-review contra `.design/brewlog/DESIGN_BRIEF.md` cuando el build esté completo.

---

## Orden de build recomendado

1. Estructura de carpetas → main.css → Navbar
2. Auth (login/registro) + validación JS — primera pantalla visible
3. Recipe Card → Recipe Feed — establece la dirección visual del contenido
4. Conversor de Molienda — herramienta más compleja lógicamente
5. Calculadora + Cronómetro
6. Bitácora (lista + formulario)
7. Responsive pass → Dark mode → Accessibility
