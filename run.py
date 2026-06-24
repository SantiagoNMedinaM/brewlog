"""
run.py — Punto de entrada de la aplicación.

Ejecutá:  python run.py
y la app queda disponible en http://localhost:5000

Internamente llama al app factory (create_app) y arranca el servidor de
desarrollo de Flask. debug=True recarga la app al guardar cambios y muestra
errores detallados (NO usar en producción).
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
