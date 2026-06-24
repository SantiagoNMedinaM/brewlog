"""
auth.py — Rutas de autenticación: registro, login y logout.

Un "blueprint" agrupa rutas relacionadas. Este maneja todo lo referido
a las cuentas de usuario. Las contraseñas se guardan hasheadas (ver models.py)
y las sesiones las maneja Flask-Login.
"""

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..models import Usuario

# Creamos el blueprint. Todas sus rutas cuelgan de /auth (url_prefix).
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    GET  -> muestra la pantalla de login/registro.
    POST -> procesa el formulario de INICIO DE SESIÓN.
    """
    # Si ya está logueado, no tiene sentido mostrarle el login.
    if current_user.is_authenticated:
        return redirect(url_for("recipes.feed"))

    if request.method == "POST":
        # Tomamos los datos enviados por el formulario.
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Buscamos un usuario con ese email.
        usuario = Usuario.query.filter_by(email=email).first()

        # Verificamos que exista Y que la contraseña coincida con el hash.
        if usuario and usuario.check_password(password):
            login_user(usuario)   # crea la sesión: el usuario queda logueado
            flash(f"¡Bienvenido de nuevo, {usuario.username}!", "success")
            # 'next' permite volver a la página que intentaba visitar antes.
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("recipes.feed"))

        # Si algo falló, avisamos sin revelar si fue el email o la contraseña
        # (buena práctica de seguridad).
        flash("Email o contraseña incorrectos.", "error")

    # GET, o POST fallido: mostramos la pantalla con el tab de login activo.
    return render_template("auth/login.html", tab_activo="login")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Procesa el formulario de REGISTRO (crear cuenta nueva).
    Solo acepta POST porque el formulario vive en la misma pantalla de login.
    """
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")

    # --- Validaciones del lado del servidor ---
    # (El frontend ya valida, pero NUNCA hay que confiar solo en el cliente.)
    errores = []

    if len(username) < 3:
        errores.append("El nombre de usuario debe tener al menos 3 caracteres.")
    if "@" not in email:
        errores.append("Ingresá un email válido.")
    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres.")
    if password != password_confirm:
        errores.append("Las contraseñas no coinciden.")

    # Verificamos que el usuario/email no estén ya tomados.
    if Usuario.query.filter_by(username=username).first():
        errores.append("Ese nombre de usuario ya está en uso.")
    if Usuario.query.filter_by(email=email).first():
        errores.append("Ya existe una cuenta con ese email.")

    # Si hubo errores, los mostramos y volvemos al tab de registro.
    if errores:
        for e in errores:
            flash(e, "error")
        return render_template("auth/login.html", tab_activo="register")

    # --- Crear el usuario ---
    nuevo = Usuario(username=username, email=email)
    nuevo.set_password(password)   # guarda el HASH, no la contraseña
    db.session.add(nuevo)
    db.session.commit()

    # Lo logueamos automáticamente tras registrarse.
    login_user(nuevo)
    flash(f"¡Cuenta creada! Bienvenido a BrewLog, {username}.", "success")
    return redirect(url_for("recipes.feed"))


@auth_bp.route("/logout")
@login_required          # solo accesible si hay sesión iniciada
def logout():
    """Cierra la sesión del usuario actual."""
    logout_user()
    flash("Cerraste sesión. ¡Hasta la próxima!", "success")
    return redirect(url_for("auth.login"))
