"""
config.py — Configuración central de la aplicación Flask.

Acá definimos los parámetros que Flask y sus extensiones necesitan.
Mantenerlos en un solo lugar facilita cambiarlos sin tocar el resto del código.
"""

import os

# Carpeta raíz del proyecto (donde está este archivo).
# Sirve para construir rutas absolutas sin importar desde dónde se ejecute.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base de la aplicación."""

    # SECRET_KEY: clave que Flask usa para firmar las cookies de sesión.
    # En producción debería venir de una variable de entorno y ser secreta.
    # Para la cursada, un valor fijo de desarrollo está bien.
    SECRET_KEY = os.environ.get("SECRET_KEY", "brewlog-clave-de-desarrollo-cambiar-en-produccion")

    # URI de la base de datos. Usamos SQLite: un único archivo (brewlog.db)
    # que se crea solo, sin necesidad de instalar un servidor de base de datos.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "brewlog.db"),
    )

    # Desactiva un sistema de notificaciones de SQLAlchemy que no usamos
    # y que solo gastaría memoria. Recomendado dejarlo en False.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
