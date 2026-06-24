/* ============================================================
   BrewLog — ratio-calculator.js
   Dos features independientes en una misma página:

   1) CALCULADORA DE RATIO
      El ratio café:agua es la relación entre gramos de café y
      gramos (≈ ml) de agua. Ej: 18 g de café + 288 g de agua = 1:16.
      Los tres valores (café, agua, ratio) están ligados: si
      conocés dos, el tercero queda determinado. Implementamos
      recálculo bidireccional para que sea cómodo de usar.

   2) CRONÓMETRO DE EXTRACCIÓN
      Mide el tiempo de preparación en formato MM:SS. Cada
      método tiene un tiempo objetivo recomendado; al alcanzarlo,
      el display da feedback visual (y vibración en mobile).
   ============================================================ */

(function () {
  'use strict';

  /* ==========================================================
     PARTE 1 — CALCULADORA DE RATIO
     ========================================================== */

  const inputCafe  = document.getElementById('input-cafe');
  const inputAgua  = document.getElementById('input-agua');
  const inputRatio = document.getElementById('input-ratio');
  const ratioDisplay = document.getElementById('ratio-display-value');

  /* Flag para evitar bucles infinitos: cuando el código actualiza
     un input mediante JS, dispara su evento 'input', que volvería
     a llamar al cálculo. Con este flag ignoramos esos disparos
     "programáticos". */
  let actualizandoInterno = false;

  /* Recalcula a partir de café + ratio  ->  agua.
     Es el flujo más natural: "tengo 18 g y quiero ratio 16". */
  function calcularDesdeRatio() {
    const cafe  = parseFloat(inputCafe.value);
    const ratio = parseFloat(inputRatio.value);
    if (isNaN(cafe) || isNaN(ratio)) return;

    const agua = cafe * ratio;            // 18 * 16 = 288 g de agua
    actualizandoInterno = true;
    inputAgua.value = Math.round(agua);
    actualizandoInterno = false;
    pintarRatio(ratio);
  }

  /* Recalcula a partir de café + agua  ->  ratio.
     Útil si el usuario ya sabe cuánta agua puso. */
  function calcularDesdeAgua() {
    const cafe = parseFloat(inputCafe.value);
    const agua = parseFloat(inputAgua.value);
    if (isNaN(cafe) || isNaN(agua) || cafe === 0) return;

    const ratio = agua / cafe;            // 288 / 18 = 16
    actualizandoInterno = true;
    inputRatio.value = ratio.toFixed(1);
    actualizandoInterno = false;
    pintarRatio(ratio);
  }

  /* Muestra el ratio en grande como "1 : X" */
  function pintarRatio(ratio) {
    if (isNaN(ratio) || !isFinite(ratio)) {
      ratioDisplay.textContent = '1 : —';
      return;
    }
    // Quita el ".0" innecesario (16.0 -> 16) pero conserva 16.5
    const limpio = Number.isInteger(ratio) ? ratio : ratio.toFixed(1);
    ratioDisplay.textContent = `1 : ${limpio}`;
  }

  /* Wiring de los tres inputs.
     - Cambiar CAFÉ o RATIO  -> recalcula AGUA
     - Cambiar AGUA          -> recalcula RATIO  */
  inputCafe.addEventListener('input', () => {
    if (actualizandoInterno) return;
    calcularDesdeRatio();
  });
  inputRatio.addEventListener('input', () => {
    if (actualizandoInterno) return;
    calcularDesdeRatio();
  });
  inputAgua.addEventListener('input', () => {
    if (actualizandoInterno) return;
    calcularDesdeAgua();
  });

  // Cálculo inicial con los valores por defecto del HTML
  calcularDesdeRatio();


  /* ==========================================================
     PARTE 2 — CRONÓMETRO DE EXTRACCIÓN
     ========================================================== */

  const display    = document.getElementById('timer-display');
  const targetText = document.getElementById('timer-target');
  const btnPlay    = document.getElementById('timer-play');
  const btnReset   = document.getElementById('timer-reset');
  const iconPlay   = document.getElementById('icon-play');
  const iconPause  = document.getElementById('icon-pause');
  const selectMetodo = document.getElementById('timer-metodo');

  /* Tiempo objetivo recomendado por método, en segundos.
     Cuando el cronómetro lo alcanza, avisa visualmente. */
  const TIEMPOS_OBJETIVO = {
    espresso: 28,    // 0:28
    v60: 210,        // 3:30
    chemex: 240,     // 4:00
    aeropress: 120,  // 2:00
    prensa: 240,     // 4:00
  };

  let segundos = 0;          // tiempo transcurrido
  let intervalo = null;      // referencia al setInterval (null = pausado)
  let objetivoActual = TIEMPOS_OBJETIVO.v60;

  /* Convierte segundos a "MM:SS" con ceros a la izquierda */
  function formatear(seg) {
    const m = Math.floor(seg / 60);
    const s = seg % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  /* Refresca el display y, si se alcanzó el objetivo, avisa */
  function pintarTiempo() {
    display.textContent = formatear(segundos);

    if (segundos === objetivoActual && objetivoActual > 0) {
      // Feedback visual: clase que dispara la animación de pulso
      display.classList.add('is-target-reached');
      // Feedback háptico en dispositivos que lo soporten (mobile)
      if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
    }
  }

  /* Alterna entre iniciar y pausar el cronómetro */
  function togglePlay() {
    if (intervalo) {
      // Está corriendo -> pausar
      clearInterval(intervalo);
      intervalo = null;
      iconPlay.style.display = 'block';
      iconPause.style.display = 'none';
    } else {
      // Está pausado -> arrancar. Tick cada 1000 ms.
      intervalo = setInterval(() => {
        segundos++;
        pintarTiempo();
      }, 1000);
      iconPlay.style.display = 'none';
      iconPause.style.display = 'block';
    }
  }

  /* Reinicia el cronómetro a 00:00 y lo detiene */
  function reset() {
    clearInterval(intervalo);
    intervalo = null;
    segundos = 0;
    display.classList.remove('is-target-reached');
    display.textContent = formatear(0);
    iconPlay.style.display = 'block';
    iconPause.style.display = 'none';
  }

  /* Actualiza el tiempo objetivo cuando cambia el método */
  function actualizarObjetivo() {
    objetivoActual = TIEMPOS_OBJETIVO[selectMetodo.value] || 0;
    targetText.textContent = `Objetivo: ${formatear(objetivoActual)}`;
  }

  btnPlay.addEventListener('click', togglePlay);
  btnReset.addEventListener('click', reset);
  selectMetodo.addEventListener('change', actualizarObjetivo);

  // Estado inicial del cronómetro
  actualizarObjetivo();
  pintarTiempo();
})();
