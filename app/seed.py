"""
seed.py — Carga de datos iniciales en la base de datos.

Se ejecuta con 'flask init-db'. Llena las tablas de catálogo (molinos y
equipamiento) y crea un usuario demo con algunas recetas de ejemplo, para
que la app no se vea vacía la primera vez.

Es idempotente: si los datos ya existen, no los duplica.
"""

from .extensions import db
from .models import Usuario, Molino, Equipamiento, Receta


def sembrar_datos():
    # --- MOLINOS ---
    # micrones_por_punto: cuántos micrones agrega cada punto de molienda.
    # Es el dato que usa el conversor para traducir entre marcas.
    molinos = [
        ("Comandante", "C40", "manual", 40, 30.0),
        ("1Zpresso", "JX", "manual", 80, 12.5),
        ("1Zpresso", "K-Plus", "manual", 90, 22.0),
        ("Baratza", "Encore", "electrico", 40, 38.0),
        ("Niche", "Zero", "electrico", 100, 11.0),
        ("Timemore", "C2", "manual", 36, 28.0),
        ("Fellow", "Ode Gen 2", "electrico", 31, 30.0),
    ]
    if Molino.query.count() == 0:
        for marca, modelo, tipo, pasos, micrones in molinos:
            db.session.add(Molino(
                marca=marca, modelo=modelo, tipo=tipo,
                pasos_totales=pasos, micrones_por_punto=micrones
            ))

    # --- EQUIPAMIENTO ---
    equipos = [
        ("Hario V60 02", "cafetera", "Hario"),
        ("Chemex 6 tazas", "cafetera", "Chemex"),
        ("Aeropress", "cafetera", "Aeropress"),
        ("Prensa francesa", "cafetera", "Bodum"),
        ("Balanza Acaia Pearl", "balanza", "Acaia"),
        ("Pava cuello de ganso", "kettle", "Fellow"),
    ]
    if Equipamiento.query.count() == 0:
        for nombre, tipo, marca in equipos:
            db.session.add(Equipamiento(nombre=nombre, tipo=tipo, marca=marca))

    db.session.commit()

    # --- USUARIO DEMO + RECETAS DE EJEMPLO ---
    # Solo si no existe todavía, para no duplicar al re-ejecutar.
    if not Usuario.query.filter_by(username="demo").first():
        demo = Usuario(username="demo", email="demo@brewlog.com",
                       bio="Cuenta de demostración de BrewLog.")
        demo.set_password("demo1234")   # contraseña de prueba
        db.session.add(demo)
        db.session.commit()

        # Buscamos referencias para las FK de las recetas.
        comandante = Molino.query.filter_by(marca="Comandante").first()
        v60 = Equipamiento.query.filter_by(nombre="Hario V60 02").first()

        recetas_demo = [
            dict(titulo="Etiopía Yirgacheffe en V60 — Floral y brillante",
                 metodo="v60", dosis_cafe=18, volumen_agua=288, ratio="1:16",
                 temp_agua=92, tiempo_extraccion="3:30", punto_molienda=20,
                 imagen_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80",
                 descripcion="Receta pensada para resaltar la acidez brillante y las notas florales del Yirgacheffe."),
            dict(titulo="Espresso clásico — Colombia Huila con perfil dulce",
                 metodo="espresso", dosis_cafe=18, volumen_agua=40, ratio="1:2.2",
                 temp_agua=93, tiempo_extraccion="0:28", punto_molienda=10,
                 imagen_url="https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=800&q=80",
                 descripcion="Un espresso equilibrado con notas de caramelo y manzana roja."),
            dict(titulo="Chemex 6 tazas — Guatemala Huehuetenango",
                 metodo="chemex", dosis_cafe=40, volumen_agua=600, ratio="1:15",
                 temp_agua=90, tiempo_extraccion="4:00", punto_molienda=23,
                 imagen_url="https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&q=80",
                 descripcion="Cuerpo limpio y dulzor prolongado, ideal para compartir."),
        ]
        for datos in recetas_demo:
            db.session.add(Receta(
                usuario_id=demo.id,
                molino_id=comandante.id if comandante else None,
                equipamiento_id=v60.id if v60 else None,
                es_publica=True,
                **datos
            ))
        db.session.commit()
