import unittest
from app import create_app
from application.extensions import db
from application.models import Customer

class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all(); db.create_all()
        self.client = self.app.test_client()

    def test_list_empty(self):
        resp = self.client.get('/customers/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_create_customer_success(self):
        payload = {'name': 'Alice Smith', 'email': 'alice@example.com'}
        resp = self.client.post('/customers/', json=payload)
        data = resp.get_json()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['name'], 'Alice Smith')
        self.assertEqual(data['email'], 'alice@example.com')

    def test_create_customer_missing(self):
        resp = self.client.post('/customers/', json={'name': 'Bob'})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('email', resp.get_json())

    def test_create_customer_duplicate_email(self):
        p = {'name': 'X', 'email': 'dup@ex.com'}
        self.client.post('/customers/', json=p)
        resp = self.client.post('/customers/', json=p)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('email', resp.get_json())

    def test_update_customer_success(self):
        r1 = self.client.post('/customers/', json={'name':'Joe','email':'joe@x.com'})
        cid = r1.get_json()['id']
        r2 = self.client.put(f'/customers/{cid}', json={'email':'joe2@x.com'})
        data = r2.get_json()
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(data['email'], 'joe2@x.com')

    def test_update_customer_not_found(self):
        resp = self.client.put('/customers/999', json={'name':'Nope'})
        self.assertEqual(resp.status_code, 404)

    def test_delete_customer_success(self):
        r1 = self.client.post('/customers/', json={'name':'Sue','email':'sue@x.com'})
        cid = r1.get_json()['id']
        r2 = self.client.delete(f'/customers/{cid}')
        self.assertEqual(r2.status_code, 200)
        self.assertIn('message', r2.get_json())

    def test_delete_customer_not_found(self):
        resp = self.client.delete('/customers/999')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
