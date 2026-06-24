"""
tools.py — Rutas de las herramientas (conversor y calculadora).

Estas dos herramientas funcionan ENTERAMENTE en el navegador con JavaScript
(no necesitan la base de datos). El servidor solo entrega la plantilla HTML;
toda la lógica de cálculo está en los archivos .js de static/js/.
"""

from flask import Blueprint, render_template
from flask_login import login_required

tools_bp = Blueprint("tools", __name__, url_prefix="/herramientas")


@tools_bp.route("/conversor")
@login_required
def grind_converter():
    """Conversor de molienda entre marcas de molinos."""
    return render_template("tools/grind_converter.html")


@tools_bp.route("/calculadora")
@login_required
def ratio_calculator():
    """Calculadora de ratio café:agua con cronómetro de extracción."""
    return render_template("tools/ratio_calculator.html")
