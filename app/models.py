"""
models.py — Modelos de datos (las tablas de la base de datos).

Cada clase es una tabla. SQLAlchemy (el ORM) traduce estas clases Python
a tablas SQL, y nos deja crear/consultar registros como si fueran objetos,
sin escribir SQL a mano.

Refleja el modelo entidad-relación diseñado en la Primera Etapa:
Usuario, Receta, Molino, Equipamiento, BitacoraCata.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db, login_manager


# ============================================================
#  USUARIO
# ============================================================
class Usuario(UserMixin, db.Model):
    """
    Representa una cuenta de usuario.

    Hereda de UserMixin (Flask-Login) para obtener gratis los métodos que
    el sistema de sesiones necesita (is_authenticated, get_id, etc.).
    """
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # Guardamos SOLO el hash de la contraseña, nunca la contraseña real.
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones: una forma cómoda de acceder a los registros asociados.
    # 'usuario.recetas' devuelve todas las recetas de ese usuario.
    # backref crea el camino inverso: 'receta.autor' devuelve el Usuario.
    recetas = db.relationship("Receta", backref="autor", lazy=True,
                              cascade="all, delete-orphan")
    catas = db.relationship("BitacoraCata", backref="autor", lazy=True,
                            cascade="all, delete-orphan")

    # --- Métodos para manejar la contraseña de forma segura ---
    def set_password(self, password):
        """Genera y guarda el hash de la contraseña dada."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Devuelve True si la contraseña coincide con el hash guardado."""
        return check_password_hash(self.password_hash, password)

    # Iniciales para el avatar (ej: "juan_perez" -> "JU")
    @property
    def iniciales(self):
        return self.username[:2].upper()

    def __repr__(self):
        return f"<Usuario {self.username}>"


# Flask-Login necesita saber cómo recuperar un usuario a partir de su id
# (que guarda en la sesión). Esta función se lo indica.
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


# ============================================================
#  MOLINO
# ============================================================
class Molino(db.Model):
    """
    Catálogo de modelos de molinos. Usado por las recetas (qué molino se usó)
    y por el conversor de molienda.
    """
    __tablename__ = "molino"

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(20))            # 'manual' o 'electrico'
    pasos_totales = db.Column(db.Integer)      # cantidad máxima de puntos
    # Micrones que agrega cada punto de molienda (clave para el conversor).
    micrones_por_punto = db.Column(db.Float)

    # Una receta apunta a un molino; desde el molino accedemos a sus recetas.
    recetas = db.relationship("Receta", backref="molino", lazy=True)

    @property
    def nombre_completo(self):
        return f"{self.marca} {self.modelo}"

    def __repr__(self):
        return f"<Molino {self.nombre_completo}>"


# ============================================================
#  EQUIPAMIENTO
# ============================================================
class Equipamiento(db.Model):
    """
    Catálogo de equipos de preparación (V60, Chemex, Aeropress, balanzas...).
    Una receta referencia el equipo principal utilizado.
    """
    __tablename__ = "equipamiento"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(30))   # 'cafetera', 'balanza', 'kettle', etc.
    marca = db.Column(db.String(100))

    recetas = db.relationship("Receta", backref="equipamiento", lazy=True)

    def __repr__(self):
        return f"<Equipamiento {self.nombre}>"


# ============================================================
#  RECETA
# ============================================================
class Receta(db.Model):
    """
    Entidad central: una receta de café con todos sus parámetros técnicos.
    """
    __tablename__ = "receta"

    id = db.Column(db.Integer, primary_key=True)

    # Claves foráneas: vinculan la receta con su autor, molino y equipo.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    molino_id = db.Column(db.Integer, db.ForeignKey("molino.id"))
    equipamiento_id = db.Column(db.Integer, db.ForeignKey("equipamiento.id"))

    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    metodo = db.Column(db.String(30), nullable=False)  # v60, espresso, etc.

    # Parámetros de extracción
    dosis_cafe = db.Column(db.Float)        # gramos de café
    volumen_agua = db.Column(db.Float)      # gramos/ml de agua
    ratio = db.Column(db.String(10))        # ej: "1:16"
    temp_agua = db.Column(db.Float)         # °C
    tiempo_extraccion = db.Column(db.String(10))  # "MM:SS"
    punto_molienda = db.Column(db.Integer)  # punto en el molino elegido

    imagen_url = db.Column(db.String(500))
    es_publica = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Receta {self.titulo}>"


# ============================================================
#  BITÁCORA DE CATA
# ============================================================
class BitacoraCata(db.Model):
    """
    Registro personal de una cata: el usuario evalúa un grano que probó.
    Puede vincularse opcionalmente a una receta de la plataforma.
    """
    __tablename__ = "bitacora_cata"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # FK opcional (nullable): la cata puede no estar atada a una receta.
    receta_id = db.Column(db.Integer, db.ForeignKey("receta.id"), nullable=True)

    nombre_grano = db.Column(db.String(150), nullable=False)
    origen = db.Column(db.String(100))
    tostador = db.Column(db.String(100))
    metodo = db.Column(db.String(30))
    puntaje = db.Column(db.Integer)         # escala 1-100 (estilo SCA)

    # Notas sensoriales
    notas_aroma = db.Column(db.Text)
    notas_sabor = db.Column(db.Text)
    notas_textura = db.Column(db.Text)
    retrogusto = db.Column(db.Text)

    recomendaria = db.Column(db.Boolean, default=True)
    fecha_cata = db.Column(db.DateTime, default=datetime.utcnow)

    # Acceso cómodo a la receta vinculada (si existe)
    receta = db.relationship("Receta", lazy=True)

    def __repr__(self):
        return f"<BitacoraCata {self.nombre_grano} ({self.puntaje})>"
