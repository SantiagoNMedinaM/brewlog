"""
journal.py — Rutas de la Bitácora de Catas.

La bitácora es PRIVADA: cada usuario solo ve y crea sus propias catas.
Por eso todas las consultas filtran por current_user.id.
"""

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)
from flask_login import login_required, current_user

from ..extensions import db
from ..models import BitacoraCata, Receta

journal_bp = Blueprint("journal", __name__, url_prefix="/bitacora")


@journal_bp.route("/")
@login_required
def index():
    """Lista las catas del usuario logueado, más recientes primero."""
    catas = (BitacoraCata.query
             .filter_by(usuario_id=current_user.id)
             .order_by(BitacoraCata.fecha_cata.desc())
             .all())

    # Calculamos el puntaje promedio para mostrarlo en el encabezado.
    if catas:
        promedio = round(sum(c.puntaje or 0 for c in catas) / len(catas))
    else:
        promedio = 0

    return render_template("journal/index.html", catas=catas, promedio=promedio)


@journal_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def create():
    """
    GET  -> formulario de nueva cata.
    POST -> guarda la cata en la base de datos (asociada al usuario).
    """
    if request.method == "POST":
        nombre_grano = request.form.get("nombre_grano", "").strip()

        # El nombre del grano es el único campo obligatorio.
        if not nombre_grano:
            flash("Ingresá el nombre del grano.", "error")
            return redirect(url_for("journal.create"))

        # El puntaje viene como texto del slider; lo convertimos a entero.
        try:
            puntaje = int(request.form.get("puntaje", 85))
        except ValueError:
            puntaje = 85

        cata = BitacoraCata(
            usuario_id=current_user.id,
            nombre_grano=nombre_grano,
            origen=request.form.get("origen", "").strip(),
            tostador=request.form.get("tostador", "").strip(),
            metodo=request.form.get("metodo", "").strip(),
            puntaje=puntaje,
            notas_aroma=request.form.get("notas_aroma", "").strip(),
            notas_sabor=request.form.get("notas_sabor", "").strip(),
            notas_textura=request.form.get("notas_textura", "").strip(),
            retrogusto=request.form.get("retrogusto", "").strip(),
            # Un checkbox manda "on" si está tildado, o nada si no.
            recomendaria=request.form.get("recomendaria") == "on",
            # Receta vinculada (opcional): vacío -> None.
            receta_id=_a_int(request.form.get("receta_id")) or None,
        )
        db.session.add(cata)
        db.session.commit()

        flash("¡Cata registrada en tu bitácora!", "success")
        return redirect(url_for("journal.index"))

    # GET: ofrecemos las recetas del usuario para poder vincular la cata.
    recetas = Receta.query.filter_by(usuario_id=current_user.id).all()
    return render_template("journal/create.html", recetas=recetas)


def _a_int(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None
