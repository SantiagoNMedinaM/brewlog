"""
extensions.py — Instancias de las extensiones de Flask.

Creamos los objetos de las extensiones (base de datos, login) ACÁ, separados
de la app, para evitar "importaciones circulares". Después, en el app factory
(__init__.py), los conectamos a la aplicación con .init_app(app).

Este patrón es estándar en proyectos Flask medianos.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# db: el objeto ORM. Con él definimos modelos y hacemos consultas a la BD.
db = SQLAlchemy()

# login_manager: gestiona las sesiones de usuario (quién está logueado).
login_manager = LoginManager()

# Si un usuario no logueado intenta entrar a una página protegida,
# Flask-Login lo redirige a esta vista (el endpoint 'auth.login').
login_manager.login_view = "auth.login"

# Mensaje que se muestra al redirigir por falta de sesión.
login_manager.login_message = "Iniciá sesión para acceder a esta página."
login_manager.login_message_category = "warning"
