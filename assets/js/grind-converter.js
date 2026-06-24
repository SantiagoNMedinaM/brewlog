/* ============================================================
   BrewLog — grind-converter.js
   Lógica del Conversor de Molienda entre marcas de molinos.

   PROBLEMA QUE RESUELVE:
   Cada molino usa su propia escala de "puntos" (clicks). El
   punto 20 de un Comandante NO equivale al punto 20 de un
   1Zpresso. Lo único comparable entre marcas es el tamaño
   real de partícula, medido en MICRONES (µm).

   ESTRATEGIA DE CONVERSIÓN:
   1. Cada molino tiene una relación lineal aproximada entre
      su número de punto y los micrones resultantes:
         micrones = micronesPorPunto * punto
   2. Para convertir de un molino A a uno B:
         a) puntoA  ->  micrones   (con la tabla del molino A)
         b) micrones ->  puntoB    (con la tabla del molino B, al revés)

   NOTA: Son valores aproximados de referencia comunitaria, no
   medidas de laboratorio. Por eso el resultado se redondea y
   se muestra como "punto aproximado".
   ============================================================ */

(function () {
  'use strict';

  /* ----------------------------------------------------------
     BASE DE DATOS DE MOLINOS (mock estático)
     micronesPorPunto = cuántos micrones agrega cada click/punto.
     pasos = cantidad máxima de puntos del molino (para el max del input).
     ---------------------------------------------------------- */
  const MOLINOS = {
    comandante: { nombre: 'Comandante C40',      micronesPorPunto: 30,  pasos: 40 },
    '1zpresso-jx': { nombre: '1Zpresso JX',       micronesPorPunto: 12.5, pasos: 80 },
    '1zpresso-k': { nombre: '1Zpresso K-Plus',    micronesPorPunto: 22,  pasos: 90 },
    baratza:     { nombre: 'Baratza Encore',      micronesPorPunto: 38,  pasos: 40 },
    niche:       { nombre: 'Niche Zero',          micronesPorPunto: 11,  pasos: 100 },
    timemore:    { nombre: 'Timemore C2',         micronesPorPunto: 28,  pasos: 36 },
    fellow:      { nombre: 'Fellow Ode Gen 2',    micronesPorPunto: 30,  pasos: 31 },
  };

  /* ----------------------------------------------------------
     Referencias al DOM
     ---------------------------------------------------------- */
  const selOrigen  = document.getElementById('molino-origen');
  const selDestino = document.getElementById('molino-destino');
  const inputPunto = document.getElementById('punto-origen');
  const resultValue = document.getElementById('result-value');
  const resultMicrones = document.getElementById('result-micrones');
  const resultBox = document.getElementById('converter-result');

  /* ----------------------------------------------------------
     Poblar los dos <select> con la lista de molinos.
     Se hace por JS para no repetir el HTML y para que agregar
     un molino nuevo sea cambiar solo el objeto MOLINOS de arriba.
     ---------------------------------------------------------- */
  function poblarSelects() {
    Object.entries(MOLINOS).forEach(([clave, datos]) => {
      // Creamos una opción idéntica para ambos selects
      const optA = new Option(datos.nombre, clave);
      const optB = new Option(datos.nombre, clave);
      selOrigen.add(optA);
      selDestino.add(optB);
    });

    // Valores por defecto para que el usuario vea un ejemplo al entrar
    selOrigen.value  = 'comandante';
    selDestino.value = '1zpresso-jx';
  }

  /* ----------------------------------------------------------
     Conversión núcleo (la fórmula explicada arriba).
     Devuelve { punto, micrones } o null si falta algún dato.
     ---------------------------------------------------------- */
  function convertir() {
    const claveOrigen  = selOrigen.value;
    const claveDestino = selDestino.value;
    const punto = parseFloat(inputPunto.value);

    // Validación: necesitamos los tres datos para calcular
    if (!claveOrigen || !claveDestino || isNaN(punto)) {
      return null;
    }

    const molinoOrigen  = MOLINOS[claveOrigen];
    const molinoDestino = MOLINOS[claveDestino];

    // Paso a) punto del molino origen  ->  micrones
    const micrones = punto * molinoOrigen.micronesPorPunto;

    // Paso b) micrones  ->  punto del molino destino (operación inversa)
    const puntoDestino = micrones / molinoDestino.micronesPorPunto;

    return {
      punto: puntoDestino,
      micrones: Math.round(micrones),
    };
  }

  /* ----------------------------------------------------------
     Pintar el resultado en pantalla.
     Se ejecuta en TIEMPO REAL ante cualquier cambio, sin botón
     de "calcular" (decisión de UX del brief: feedback inmediato).
     ---------------------------------------------------------- */
  function actualizarResultado() {
    const resultado = convertir();

    if (!resultado) {
      // Falta algún dato: mostramos estado vacío atenuado
      resultBox.classList.add('is-empty');
      resultValue.textContent = '—';
      resultMicrones.textContent = 'Completá los tres campos para ver la equivalencia';
      return;
    }

    resultBox.classList.remove('is-empty');

    // Redondeamos a 0.5 porque la mayoría de los molinos tienen
    // medios puntos como granularidad práctica.
    const puntoRedondeado = Math.round(resultado.punto * 2) / 2;
    resultValue.textContent = puntoRedondeado;

    const nombreDestino = MOLINOS[selDestino.value].nombre;
    resultMicrones.textContent =
      `≈ ${resultado.micrones} µm  ·  punto aproximado en ${nombreDestino}`;
  }

  /* ----------------------------------------------------------
     Actualizar el atributo max del input según el molino origen
     elegido (no tiene sentido permitir punto 90 en un Comandante
     que solo llega a 40).
     ---------------------------------------------------------- */
  function actualizarMaxPunto() {
    const molino = MOLINOS[selOrigen.value];
    if (molino) inputPunto.max = molino.pasos;
  }

  /* ----------------------------------------------------------
     Wiring de eventos: cualquier cambio recalcula al instante.
     ---------------------------------------------------------- */
  function init() {
    poblarSelects();
    actualizarMaxPunto();
    actualizarResultado();

    selOrigen.addEventListener('change', () => {
      actualizarMaxPunto();
      actualizarResultado();
    });
    selDestino.addEventListener('change', actualizarResultado);
    inputPunto.addEventListener('input', actualizarResultado);
  }

  init();
})();
