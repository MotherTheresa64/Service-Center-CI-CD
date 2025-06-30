import unittest
from app import create_app
from application.extensions import db
from application.models import Mechanic

class TestMechanics(unittest.TestCase):
    def setUp(self):
        # spin up app in testing mode
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_list_empty(self):
        resp = self.client.get('/mechanics/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_create_mechanic_success(self):
        resp = self.client.post('/mechanics/', json={'name': 'Jane Mechanic'})
        data = resp.get_json()
        self.assertEqual(resp.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Jane Mechanic')

    def test_create_mechanic_missing_field(self):
        resp = self.client.post('/mechanics/', json={})
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)
        self.assertIn('name', data)

    def test_update_mechanic_success(self):
        # first create one
        r1 = self.client.post('/mechanics/', json={'name': 'Alice'})
        mech_id = r1.get_json()['id']

        r2 = self.client.put(f'/mechanics/{mech_id}', json={'name': 'Alicia'})
        data = r2.get_json()
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(data['name'], 'Alicia')

    def test_update_mechanic_not_found(self):
        resp = self.client.put('/mechanics/999', json={'name': 'NoOne'})
        self.assertEqual(resp.status_code, 404)

    def test_delete_mechanic_success(self):
        r1 = self.client.post('/mechanics/', json={'name': 'Bob'})
        mech_id = r1.get_json()['id']

        r2 = self.client.delete(f'/mechanics/{mech_id}')
        data = r2.get_json()
        self.assertEqual(r2.status_code, 200)
        self.assertIn('message', data)

    def test_delete_mechanic_not_found(self):
        resp = self.client.delete('/mechanics/999')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
