import unittest
from app import create_app
from application.extensions import db
from application.models import ServiceTicket, Customer, Mechanic
from datetime import date

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # create a customer and mechanic for FKs
            cust = Customer(name="Test Cust", email="tc@example.com")
            mech = Mechanic(name="Test Mech")
            db.session.add_all([cust, mech])
            db.session.commit()
            self.cust_id = cust.id
            self.mech_id = mech.id
        self.client = self.app.test_client()

    def test_list_empty(self):
        resp = self.client.get('/service-tickets/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_create_ticket_success(self):
        payload = {
            'description': 'Engine check',
            'customer_id': self.cust_id
        }
        resp = self.client.post('/service-tickets/', json=payload)
        data = resp.get_json()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['description'], 'Engine check')
        self.assertEqual(data['customer_id'], self.cust_id)
        self.assertEqual(data['status'], 'open')

    def test_create_ticket_missing_field(self):
        resp = self.client.post('/service-tickets/', json={'customer_id': self.cust_id})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('description', resp.get_json())

    def test_update_ticket_success(self):
        r1 = self.client.post('/service-tickets/', json={
            'description': 'Oil change',
            'customer_id': self.cust_id
        })
        tid = r1.get_json()['id']
        r2 = self.client.put(f'/service-tickets/{tid}', json={
            'status': 'closed',
            'assigned_mechanic_id': self.mech_id
        })
        d2 = r2.get_json()
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(d2['status'], 'closed')
        self.assertEqual(d2['assigned_mechanic_id'], self.mech_id)

    def test_update_ticket_not_found(self):
        resp = self.client.put('/service-tickets/999', json={'status': 'x'})
        self.assertEqual(resp.status_code, 404)

    def test_delete_ticket_success(self):
        r1 = self.client.post('/service-tickets/', json={
            'description': 'Brake fix',
            'customer_id': self.cust_id
        })
        tid = r1.get_json()['id']
        r2 = self.client.delete(f'/service-tickets/{tid}')
        self.assertEqual(r2.status_code, 200)
        self.assertIn('message', r2.get_json())

    def test_delete_ticket_not_found(self):
        resp = self.client.delete('/service-tickets/999')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
