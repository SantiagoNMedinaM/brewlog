/* BrewLog — auth.js
   Maneja tabs, validación inline y toggle de contraseña */

(function () {
  'use strict';

  /* --- Tabs --- */
  const tabs = document.querySelectorAll('.auth-tab');
  const forms = document.querySelectorAll('.auth-form');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.target;

      tabs.forEach(t => t.classList.remove('active'));
      forms.forEach(f => f.classList.remove('active'));

      tab.classList.add('active');
      document.getElementById(target)?.classList.add('active');
    });
  });

  /* --- Toggle contraseña --- */
  document.querySelectorAll('.btn-toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.closest('.input-password-wrapper').querySelector('input');
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';

      const icon = btn.querySelector('svg use, svg path');
      btn.setAttribute('aria-label', isPassword ? 'Ocultar contraseña' : 'Mostrar contraseña');

      /* Rotar el icono para dar feedback visual */
      btn.style.opacity = isPassword ? '1' : '0.5';
    });
  });

  /* --- Validación inline al blur --- */
  function validateField(input) {
    input.classList.remove('is-valid', 'is-invalid');

    if (!input.checkValidity()) {
      input.classList.add('is-invalid');
      return false;
    }

    /* Validación extra: coincidencia de contraseñas */
    if (input.id === 'reg-password-confirm') {
      const original = document.getElementById('reg-password');
      if (original && input.value !== original.value) {
        input.classList.add('is-invalid');
        const feedback = input.nextElementSibling;
        if (feedback?.classList.contains('invalid-feedback')) {
          feedback.textContent = 'Las contraseñas no coinciden.';
        }
        return false;
      }
    }

    input.classList.add('is-valid');
    return true;
  }

  document.querySelectorAll('.auth-form .form-control').forEach(input => {
    input.addEventListener('blur', () => validateField(input));
    input.addEventListener('input', () => {
      if (input.classList.contains('is-invalid')) validateField(input);
    });
  });

  /* --- Fortaleza de contraseña --- */
  const passwordInput = document.getElementById('reg-password');
  const strengthFill  = document.querySelector('.password-strength-bar__fill');

  if (passwordInput && strengthFill) {
    passwordInput.addEventListener('input', () => {
      const val = passwordInput.value;
      let score = 0;

      if (val.length >= 8)                          score++;
      if (/[A-Z]/.test(val))                        score++;
      if (/[0-9]/.test(val))                        score++;
      if (/[^A-Za-z0-9]/.test(val))                 score++;

      strengthFill.dataset.strength = score > 0 ? score : '';
    });
  }

  /* --- Submit con validación completa --- */
  document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      let valid = true;
      form.querySelectorAll('.form-control').forEach(input => {
        if (!validateField(input)) valid = false;
      });

      if (!valid) {
        e.preventDefault();
        form.querySelector('.is-invalid')?.focus();
      }
    });
  });

})();
