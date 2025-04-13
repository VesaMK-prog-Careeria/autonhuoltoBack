from app import app, db

# ** python init_db.py
with app.app_context():
    print("🔧 Yritetään luoda taulut...")
    db.create_all()
    print("✅ Tietokantataulut luotu onnistuneesti.")