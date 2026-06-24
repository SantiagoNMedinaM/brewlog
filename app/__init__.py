"""
__init__.py — "App Factory" de BrewLog.

Patrón de fábrica: en vez de crear la app como una variable global, la
construimos dentro de una función create_app(). Esto facilita testear,
configurar distintos entornos y evita importaciones circulares.

Al importar el paquete 'app', Flask llama a create_app() para armar todo:
  1. Crea la aplicación y le carga la configuración.
  2. Conecta las extensiones (base de datos, login).
  3. Registra los blueprints (los módulos de rutas).
  4. Define un comando para inicializar la base de datos.
"""

from flask import Flask

from config import Config
from .extensions import db, login_manager


def create_app(config_class=Config):
    # Creamos la aplicación Flask.
    app = Flask(__name__)
    # Cargamos la configuración desde la clase Config (config.py).
    app.config.from_object(config_class)

    # --- Conectar extensiones a esta app concreta ---
    db.init_app(app)
    login_manager.init_app(app)

    # --- Registrar blueprints (cada uno agrupa rutas de una sección) ---
    # Se importan acá adentro para evitar importaciones circulares.
    from .routes.auth import auth_bp
    from .routes.recipes import recipes_bp
    from .routes.journal import journal_bp
    from .routes.tools import tools_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(tools_bp)

    # --- Comando de consola: "flask init-db" crea las tablas y carga datos ---
    register_cli_commands(app)

    return app


def register_cli_commands(app):
    """
    Registra comandos personalizados que se ejecutan con 'flask <comando>'.
    Acá definimos 'init-db' para crear las tablas y sembrar datos iniciales.
    """
    import click

    @app.cli.command("init-db")
    def init_db():
        """Crea las tablas de la base de datos y carga datos de ejemplo."""
        from .seed import sembrar_datos
        db.create_all()           # crea todas las tablas definidas en models.py
        sembrar_datos()           # carga molinos, equipos y recetas demo
        click.echo("Base de datos inicializada y poblada con datos de ejemplo.")
