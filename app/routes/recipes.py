"""
recipes.py — Rutas de recetas: feed, detalle y creación.

Casi todas requieren sesión iniciada (@login_required). El feed muestra las
recetas públicas de toda la comunidad; "nueva" crea una receta asociada al
usuario logueado.
"""

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash, abort
)
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Receta, Molino, Equipamiento

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/")
@login_required
def feed():
    """
    Página principal: muestra todas las recetas públicas, más nuevas primero.
    Acepta ?metodo=v60 para filtrar por método de extracción.
    """
    metodo = request.args.get("metodo")   # filtro opcional desde la URL

    # Construimos la consulta. SQLAlchemy permite encadenar condiciones.
    consulta = Receta.query.filter_by(es_publica=True)
    if metodo and metodo != "all":
        consulta = consulta.filter_by(metodo=metodo)

    # order_by descendente por fecha = las más recientes arriba.
    recetas = consulta.order_by(Receta.fecha_creacion.desc()).all()

    return render_template("recipes/feed.html", recetas=recetas, metodo_activo=metodo or "all")


@recipes_bp.route("/recetas/<int:receta_id>")
@login_required
def detail(receta_id):
    """Muestra el detalle completo de una receta."""
    # get_or_404: si no existe esa receta, devuelve una página 404.
    receta = db.get_or_404(Receta, receta_id)
    return render_template("recipes/detail.html", receta=receta)


@recipes_bp.route("/recetas/nueva", methods=["GET", "POST"])
@login_required
def create():
    """
    GET  -> formulario de nueva receta.
    POST -> guarda la receta nueva en la base de datos.
    """
    if request.method == "POST":
        # Leemos los campos del formulario.
        titulo = request.form.get("titulo", "").strip()
        metodo = request.form.get("metodo", "").strip()

        # Validación mínima: título y método son obligatorios.
        if not titulo or not metodo:
            flash("El título y el método son obligatorios.", "error")
            return redirect(url_for("recipes.create"))

        # Creamos la receta asociada al usuario logueado (current_user).
        receta = Receta(
            usuario_id=current_user.id,
            titulo=titulo,
            metodo=metodo,
            descripcion=request.form.get("descripcion", "").strip(),
            dosis_cafe=_a_float(request.form.get("dosis_cafe")),
            volumen_agua=_a_float(request.form.get("volumen_agua")),
            ratio=request.form.get("ratio", "").strip(),
            temp_agua=_a_float(request.form.get("temp_agua")),
            tiempo_extraccion=request.form.get("tiempo_extraccion", "").strip(),
            punto_molienda=_a_int(request.form.get("punto_molienda")),
            molino_id=_a_int(request.form.get("molino_id")) or None,
            equipamiento_id=_a_int(request.form.get("equipamiento_id")) or None,
            # Si no se sube imagen, usamos una por defecto.
            imagen_url=request.form.get("imagen_url", "").strip()
                       or "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80",
            es_publica=True,
        )
        db.session.add(receta)
        db.session.commit()

        flash("¡Receta publicada con éxito!", "success")
        return redirect(url_for("recipes.detail", receta_id=receta.id))

    # GET: pasamos molinos y equipos para poblar los <select> del formulario.
    molinos = Molino.query.order_by(Molino.marca).all()
    equipos = Equipamiento.query.order_by(Equipamiento.nombre).all()
    return render_template("recipes/create.html", molinos=molinos, equipos=equipos)


# --- Helpers internos para convertir texto del formulario a números ---
# Los formularios siempre mandan texto; estas funciones lo convierten de
# forma segura (devuelven None si el campo está vacío o mal escrito).
def _a_float(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def _a_int(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None
