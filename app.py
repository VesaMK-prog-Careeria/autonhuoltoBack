#region Importit
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Maintenance, User
from config import Config
from sqlalchemy import text
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
#endregion

app = Flask(__name__)
app.config.from_object(Config)
#app.config['JWT_SECRET_KEY'] = 'salainenavain123' #Muutettu config.py-tiedostoon
jwt = JWTManager(app)

#* Kuvien tallennuskansio
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Luo kansio, jos ei ole olemassa
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#* Tietokannan alustaminen paikallinen sekä Netlify
db.init_app(app)
# CORS(app)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://precious-praline-353513.netlify.app"]}}, supports_credentials=True)

#region Reitit
@app.route("/")
def hello():
    return "Flask toimii"

@app.route("/test-db")
def test_db():
    result = db.session.execute(text("SELECT DB_NAME()")).scalar()
    return f"Ollaan yhteydessä tietokantaan: {result}"


#* Tämä on reitti, joka palauttaa kaikki käyttäjät
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    print("DEBUG data:", data)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
            return jsonify({"error": "Anna käyttäjätunnus ja salasana"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Käyttäjätunnus on jo olemassa"}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Rekisteröinti onnistui"}), 201

#* Tämä on reitti, joka palauttaa kaikki käyttäjät
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Virheellinen käyttäjätunnus tai salasana"}), 401

    token = create_access_token(identity=str(user.id))  # 🔧 TÄRKEÄ MUUTOS
    return jsonify({"token": token, "username": user.username})

#* Tämä on reitti, joka palauttaa kaikki käyttäjät
@app.route("/api/users", methods=["GET"])
@jwt_required()
def list_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username
    } for u in users])

#* Tämä on reitti, joka palauttaa yksittäisen käyttäjän
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Käyttäjää ei löytynyt"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Käyttäjä poistettu"})

#* Lisää käyttäjä (vain sisäänkirjautuneille)
@app.route("/api/users", methods=["POST"])
@jwt_required()
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Anna käyttäjätunnus ja salasana"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Käyttäjätunnus on jo olemassa"}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Käyttäjä lisätty"}), 201


# Tämä on uusi reitti, joka palauttaa kaikki huollot
@app.route("/api/maintenance", methods=["GET"])
#@jwt_required()
def get_maintenance():
    #user_id = get_jwt_identity()
    #print("✅ GET user_id:", user_id)  # 🐞 tulostus
    #maintenances = Maintenance.query.filter_by(user_id=user_id).all()
    maintenances = Maintenance.query.all()  #TODO 🔓 Ei enää suodatusta koska suodatus ei toiminut
    return jsonify([{
        "id": m.id,
        "car": m.car,
        "description": m.description,
        "km": m.km,
        "date": m.date,
        "image_path": m.image_path  # Lisää kuva polku
    } for m in maintenances])

#* Lisää huolto ja kuva
@app.route("/api/maintenance", methods=["POST"])
@jwt_required()
def add_maintenance():
    try:
        user_id = get_jwt_identity()
        #* Hae käyttäjätunnus JWT:stä
        car = request.form.get("car")
        description = request.form.get("description")
        km = request.form.get("km")
        date = request.form.get("date")

        file = request.files.get("image")
        filename = None

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        m = Maintenance(car=car, description=description, date=date, user_id=user_id)
        if km:
            try:
                m.km = int(km)  # Muuta km kokonaisluvuksi, jos se on annettu
            except ValueError:
                m.km = None  # Jos ei onnistu, aseta None
        # Tallenna kuva tiedostoon ja polku tietokantaan
        if filename:
            m.image_path = filename # Tallenna tiedostonimi tietokantaan

        # Tallenna huolto tietokantaan
        db.session.add(m)
        db.session.commit()

        return jsonify({"message": "Added successfully"}), 201

    except Exception as e:
        print("❌ Virhe POSTissa:", e)
        return jsonify({"error": str(e)}), 500


#* Tämä on uusi reitti, joka päivittää yksittäisen huollon
#TODO tämä ei vielä käytössä koska kuvat ei toimi
@app.route("/api/maintenance/<int:id>", methods=["PUT"])
def update_maintenance(id):
    data = request.get_json()
    m = Maintenance.query.get(id)
    if not m:
        return jsonify({"error": "Not found"}), 404
    m.car = data["car"]
    m.description = data["description"]
    m.km = data["km"]
    m.date = data["date"]
    db.session.commit()
    return jsonify({"message": "Updated successfully"})

#* Tämä on uusi reitti, joka poistaa yksittäisen huollon
@app.route("/api/maintenance/<int:id>", methods=["DELETE"])
def delete_maintenance(id):
    m = Maintenance.query.get(id)
    if not m:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(m)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})

#* Palauta kuva tiedostosta
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#* Palauta kaikki huollot tietyn auton mukaan
@app.route("/api/cars", methods=["GET"])
def get_unique_cars():
    cars = db.session.query(Maintenance.car).distinct().all()
    car_list = [c[0] for c in cars if c[0]]  # poista mahdolliset None-arvot
    return jsonify(car_list)
#endregion

#! Tärkeä: tämä viimeiseksi! Tämä siirretty init_db.py-tiedostosta tänne
if __name__ == "__main__":
    with app.app_context():
        try:
            print("🔧 Yritetään luoda taulut...")
            db.create_all()
            print("✅ Tietokantataulut luotu onnistuneesti.")
        except Exception as e:
            print("❌ Virhe tietokantayhteydessä:")
            print(e)

    app.run(debug=False)
    #? debug=True ei saa olla käytössä tuotannossa, koska se voi paljastaa tietoturva-aukkoja

    #? tietokannan ja taulujen luonti
    #? db.create_all() tai db.init_app(app) ja db.create_all() app.runin jälkeen
    #? db.create_all() luo taulut vain, jos niitä ei ole olemassa
    # ❌ ✅ 🔓 🐞 🔧