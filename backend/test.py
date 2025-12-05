import unittest
import os
import sys

# DB test módba állítása
os.environ['FLASK_ENV'] = 'testing'

# Main megtalálása
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from main import app, db, AppUser, VacationEntry

class TestVacationApp(unittest.TestCase):
    # Minden teszt előtt DB/app setup, utánuk teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    #Test user készítés
    def create_standard_user(self):
        user_data = {
            "email": "test@example.com",
            "password_hash": "test123",
            "full_name": "Test User",
            "base_vacation_days": 20
        }
        self.client.post('/register', json=user_data)
        return user_data

    # TEST CASEK
    # Regisztráció teszt
    def test_register_user(self):
        response = self.client.post('/register', json={
            "email": "new@example.com",
            "password_hash": "pass123",
            "full_name": "New User",
            "base_vacation_days": 25
        })
        self.assertEqual(response.status_code, 201)
        user = AppUser.query.filter_by(email="new@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.unique_key, "UKEY-001")

    # Duplicate email teszt
    def test_register_duplicate_email(self):
        self.create_standard_user()
        response = self.client.post('/register', json={
            "email": "test@example.com",
            "password_hash": "test1234",
            "full_name": "Test Userr",
            "base_vacation_days": 10
        })
        self.assertEqual(response.status_code, 400)

    # Sikeres login teszt
    def test_login_success(self):
        user_data = self.create_standard_user()
        response = self.client.post('/login', json={
            "email": user_data['email'],
            "password_hash": user_data['password_hash']
        })
        self.assertEqual(response.status_code, 200)

    # Sikertelen login teszt
    def test_login_failure(self):
        user_data = self.create_standard_user()
        response = self.client.post('/login', json={
            "email": user_data['email'],
            "password_hash": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)

    # Szabadság foglalás teszt
    def test_add_vacation_success(self):
        user_data = self.create_standard_user()
        response = self.client.post('/vacations', json={
            "email": user_data['email'],
            "vacation_date": "2025-12-25",
            "days": 5
        })
        self.assertEqual(response.status_code, 201)

    # Szabadság limit túllépés teszt
    def test_add_vacation_exceeds_limit(self):
        user_data = self.create_standard_user()  # 20 days
        response = self.client.post('/vacations', json={
            "email": user_data['email'],
            "vacation_date": "2025-12-01",
            "days": 21
        })
        self.assertEqual(response.status_code, 400)

    # Szabadság számolás teszt
    def test_get_vacations_calculation(self):
        user_data = self.create_standard_user()
        self.client.post('/vacations', json={
            "email": user_data['email'],
            "vacation_date": "2025-01-01",
            "days": 5
        })
        self.client.post('/vacations', json={
            "email": user_data['email'],
            "vacation_date": "2025-02-01",
            "days": 3
        })

        response = self.client.get(f"/vacations?email={user_data['email']}")
        data = response.get_json()

        self.assertEqual(data['base_vacation_days'], 20)
        self.assertEqual(data['used_vacation_days'], 8)
        self.assertEqual(data['available_vacation_days'], 12)

    # Szabadság törlés teszt
    def test_delete_vacation(self):
        user_data = self.create_standard_user()
        self.client.post('/vacations', json={
            "email": user_data['email'],
            "vacation_date": "2025-05-01",
            "days": 5
        })

        vacation = VacationEntry.query.first()
        response = self.client.delete(f'/vacations/{vacation.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(VacationEntry.query.count(), 0)

    # Szabadság módosítás teszt
    def test_modify_vacation_success(self):
        user_data = self.create_standard_user()
        self.client.post('/vacations', json={
            "email": user_data['email'],
            "vacation_date": "2025-06-01",
            "days": 5
        })

        vac_id = VacationEntry.query.first().id
        response = self.client.put(f'/vacations/{vac_id}', json={
            "days": 10,
            "vacation_date": "2025-06-05"
        })

        self.assertEqual(response.status_code, 200)

        response_get = self.client.get(f"/vacations?email={user_data['email']}")
        data = response_get.get_json()
        self.assertEqual(data['used_vacation_days'], 10)

if __name__ == '__main__':
    unittest.main()