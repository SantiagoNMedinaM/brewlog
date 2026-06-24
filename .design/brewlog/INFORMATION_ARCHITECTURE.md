# Information Architecture: BrewLog

## Site Map

- Auth `/auth/`
  - Login `/auth/login.html`
  - Registro `/auth/register.html`
- Feed de Recetas `/recipes/`  ← página principal post-login
  - Detalle de Receta `/recipes/detail.html?id=:id`
  - Nueva Receta `/recipes/create.html`
- Herramientas `/tools/`
  - Conversor de Molienda `/tools/grind-converter.html`
  - Calculadora de Ratio `/tools/ratio-calculator.html`
- Mi Bitácora `/journal/`
  - Nueva Entrada `/journal/create.html`
  - Detalle de Entrada `/journal/entry.html?id=:id`
- Perfil `/profile/index.html`

## Navigation Model

- **Primary navigation** (visible post-login): Recetas · Herramientas · Mi Bitácora
- **Secondary navigation**: dentro de /tools/, tabs entre Conversor y Calculadora
- **Utility navigation**: avatar del usuario (dropdown) → Perfil / Cerrar sesión
- **Mobile navigation**: hamburger → drawer lateral con los mismos ítems en columna

La navbar es sticky y dark en todas las páginas autenticadas. Las páginas de auth no tienen navbar.

## Content Hierarchy

### Feed de Recetas (`/recipes/`)
1. Filtros rápidos (método de extracción) — permiten reducir el feed antes de leer
2. Grid de Recipe Cards — el contenido principal
3. Botón "Nueva Receta" (sticky o en navbar) — acción frecuente del usuario

### Detalle de Receta (`/recipes/detail.html`)
1. Imagen hero a ancho completo — establece la identidad visual de la receta
2. Título + badge de método + autor — quién hizo qué con qué
3. Parámetros técnicos (dosis, ratio, temperatura, tiempo, punto de molienda) — el dato central
4. Notas y descripción — contexto narrativo
5. Acciones: Guardar en bitácora, Compartir — secundarias

### Conversor de Molienda (`/tools/grind-converter.html`)
1. Selector de molino origen + punto de molienda — input del usuario
2. Selector de molino destino — segundo input
3. Resultado: punto equivalente + micrones — output inmediato
4. Tabla de equivalencias completa (colapsable) — referencia extendida

### Calculadora de Ratio (`/tools/ratio-calculator.html`)
1. Inputs: gramos de café / volumen de agua (se calculan mutuamente)
2. Ratio resultante expresado como 1:X
3. Cronómetro con tiempo objetivo según método seleccionado

### Mi Bitácora (`/journal/`)
1. Botón "Nueva cata" — acción principal
2. Lista de entradas ordenadas por fecha desc — el historial
3. Filtros: por grano, por puntaje, por fecha

### Nueva Entrada de Cata (`/journal/create.html`)
1. Nombre del grano + origen + tostador
2. Parámetros de preparación (vinculable a una receta existente)
3. Puntuación (1-100, tipo SCA)
4. Notas: aroma, sabor, textura, retrogusto
5. ¿Recomendarías este grano? (toggle)

## User Flows

### Usuario nuevo — Registro y primera receta
1. Llega a `/auth/login.html`
2. Hace clic en tab "Registrarse"
3. Completa el formulario (username, email, password)
4. Acepta términos → submit
5. Redirige a `/recipes/` (feed vacío con CTA "Explorá recetas")
6. Puede crear su primera receta con "Nueva Receta"

### Usuario existente — Encontrar receta y convertir molienda
1. Login → llega al feed `/recipes/`
2. Filtra por método "V60"
3. Abre el detalle de una receta
4. Ve que la receta pide molienda 20 en Comandante — él tiene 1Zpresso
5. Navega a `/tools/grind-converter.html`
6. Selecciona Comandante (origen, punto 20) + 1Zpresso (destino)
7. Obtiene el punto equivalente al instante
8. Vuelve a la receta y prepara el café

### Usuario — Registrar una cata
1. Después de preparar, va a `/journal/create.html`
2. Ingresa nombre del grano, origen, tostador
3. Vincula la receta usada (opcional)
4. Asigna puntaje y escribe notas
5. Guarda → redirige a `/journal/` donde ve la entrada nueva al tope

## Naming Conventions

| Concepto | Label en UI | Notas |
|---|---|---|
| Preparación de café | Receta | No "brew", no "preparación" |
| Punto de molienda | Punto de molienda | No "grind setting", no "clicks" |
| Registro personal | Bitácora | No "diario", no "journal" (en UI en español) |
| Entrada en la bitácora | Cata | No "registro", no "nota" |
| Puntuación de la cata | Puntaje | Escala 1-100 estilo SCA |
| Café de especialidad | Café de especialidad | No "specialty coffee" en la UI |

## Component Reuse Map

| Componente | Usado en | Variaciones |
|---|---|---|
| Navbar | Todas las páginas post-login | — |
| Recipe Card | /recipes/, /profile/ | Sin acciones de edición en el feed público |
| Badge de método | Recipe Card, Recipe Detail | Solo cambia el texto |
| Parámetros técnicos | Recipe Detail, Journal Entry Form | En el form son inputs; en el detail son texto |
| Botón primario (.btn-primary) | Todas las páginas | Tamaño full-width en forms de auth |

## Content Growth Plan

- **Recetas**: crecen indefinidamente → se pagina con "Cargar más" (lazy load simulado con JS)
- **Bitácora**: crecen por usuario → se ordena por fecha, se filtra por grano/puntaje
- **Molinos en el conversor**: lista estática inicial (~15 modelos) → campo de búsqueda cuando supera 20

## URL Strategy

- Archivos estáticos `.html` — sin servidor backend real
- Parámetros simulados con query string (`?id=1`) leídos por JS
- Estructura: `/seccion/accion.html` — plana, sin nesting profundo
- Sin hash routing: cada página es un archivo HTML independiente
