from app import app, db
from models import User, Maintenance

# ** python init_db.py
with app.app_context():
    print("🔧 Yritetään luoda taulut...")
    db.create_all()
    print("✅ Tietokantataulut luotu onnistuneesti.")