from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Maintenance(db.Model):
    __tablename__ = "Maintenance"
    id = db.Column(db.Integer, primary_key=True)
    car = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    km = db.Column(db.Integer)
    image_path = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))  # 🔐 liittyy käyttäjään
    