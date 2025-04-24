📦 Backend – Autonhuolto API
Tämä on Flask-pohjainen REST API autonhuoltosovellukseen. API tarjoaa rekisteröitymisen, kirjautumisen, huoltotietojen hallinnan ja käyttäjien hallinnan. Käyttää PostgreSQL-tietokantaa Render-palvelussa.

🔧 Teknologiat
    Python / Flask
    PostgreSQL
    SQLAlchemy
    Flask-JWT-Extended (JWT-autentikointi)
    Render (hostaus)

🚀 Käynnistys paikallisesti
1. Luo virtuaaliympäristö ja asenna riippuvuudet:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Lisää .env-tiedosto (tai määritä environment-variabelit Renderiin):

DATABASE_URL=postgresql://<käyttäjä>:<salasana>@<host>/<tietokanta>
JWT_SECRET_KEY=salainenavain123

3. Käynnistä sovellus:

flask run

🔐 Reitit
    POST /api/register – rekisteröi uusi käyttäjä
    POST /api/login – kirjaudu sisään ja saa JWT-token
    GET /api/maintenance – hae huollot (JWT vaaditaan)
    POST /api/maintenance – lisää uusi huolto (JWT vaaditaan)
    GET /api/cars – palauttaa kaikki tallennetut autot
    GET /api/users – listaa käyttäjät (admin)
    POST /api/users – lisää käyttäjä (admin)
    DELETE /api/users/:id – poistaa käyttäjän (admin)