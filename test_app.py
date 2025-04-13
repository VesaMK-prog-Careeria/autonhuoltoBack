import unittest
import json
from app import app, db
from models import Maintenance

# ** python test_app.py

class MaintenanceTestCase(unittest.TestCase):
    def setUp(self):
        # Aseta sovellus testaus-tilaan ja luo testitietokanta (ei käytetä tuotantotietokantaa)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # Käytetään SQLitea nopeaan testaukseen
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Poista tietokanta jokaisen testin jälkeen
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_empty_maintenance(self):
        # Testaa, että aluksi maintenance-lista on tyhjä
        response = self.app.get("/api/maintenance")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_post_maintenance(self):
        # Testaa uuden huollon lisääminen
        payload = {
            "car": "Honda Civic",
            "description": "Jarrupalojen vaihto",
            "date": "2025-04-02"
        }
        response = self.app.post("/api/maintenance", 
                                 data=json.dumps(payload),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Added successfully")

        # Testaa että huolto näkyy nyt GET-kutsussa
        response = self.app.get("/api/maintenance")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["car"], "Honda Civic")

if __name__ == '__main__':
    unittest.main()
