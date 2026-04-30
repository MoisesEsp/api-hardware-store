from app import create_app
from app.modelos import db, Categoria, Producto, Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tablas verificadas en PostgreSQL.")

    # --- Seeding del Administrador ---
    if not Usuario.query.first():
        print("⏳ Creando usuario administrador...")
        hash_pass = generate_password_hash("admin123")
        admin = Usuario(username="admin", password_hash=hash_pass)
        db.session.add(admin)
        db.session.commit()
        print("✅ Administrador creado con éxito.")
    else:
        print("ℹ️ El usuario administrador ya existe.")

    # --- Seeding de Categorías y Productos ---
    if not Categoria.query.first():
        print("⏳ Insertando datos de prueba (Seeding)...")
        cat1 = Categoria(nombre="Periféricos y Accesorios")
        cat2 = Categoria(nombre="Componentes Internos")
        cat3 = Categoria(nombre="Redes y Conectividad")
        
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

        prod1 = Producto(nombre="Mouse Logitech G203", especificaciones="8000 DPI, RGB", precio=25.50, stock=15, categoria_id=cat1.id)
        prod2 = Producto(nombre="Teclado Mecánico Redragon", especificaciones="Switches Outemu Red", precio=45.00, stock=8, categoria_id=cat1.id)
        prod3 = Producto(nombre="Router TP-Link Archer C7", especificaciones="Doble banda, Gigabit", precio=60.00, stock=5, categoria_id=cat3.id)
        
        db.session.add_all([prod1, prod2, prod3])
        db.session.commit()
        print("✅ Datos guardados correctamente.")
    else:
        print("ℹ️ La base de datos ya contiene productos. Seeding omitido.")