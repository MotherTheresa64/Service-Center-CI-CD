import unittest
from app import create_app
from application.extensions import db
from application.models import Inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_list_empty(self):
        resp = self.client.get('/inventory/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_create_inventory_success(self):
        payload = {'product': 'Brake Pad', 'quantity': 50}
        resp = self.client.post('/inventory/', json=payload)
        data = resp.get_json()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['product'], 'Brake Pad')
        self.assertEqual(data['quantity'], 50)

    def test_create_inventory_missing_field(self):
        resp = self.client.post('/inventory/', json={'product': 'Brake Pad'})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('quantity', resp.get_json())

    def test_create_inventory_bad_quantity(self):
        resp = self.client.post('/inventory/', json={'product': 'Pads', 'quantity': 'lots'})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('quantity', resp.get_json())

    def test_update_inventory_success(self):
        r1 = self.client.post('/inventory/', json={'product': 'Oil', 'quantity': 10})
        iid = r1.get_json()['id']
        r2 = self.client.put(f'/inventory/{iid}', json={'quantity': 20})
        data = r2.get_json()
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(data['quantity'], 20)

    def test_update_inventory_not_found(self):
        resp = self.client.put('/inventory/999', json={'product': 'X'})
        self.assertEqual(resp.status_code, 404)

    def test_delete_inventory_success(self):
        r1 = self.client.post('/inventory/', json={'product': 'Filter', 'quantity': 5})
        iid = r1.get_json()['id']
        r2 = self.client.delete(f'/inventory/{iid}')
        self.assertEqual(r2.status_code, 200)
        self.assertIn('message', r2.get_json())

    def test_delete_inventory_not_found(self):
        resp = self.client.delete('/inventory/999')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
