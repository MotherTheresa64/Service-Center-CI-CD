from .extensions import db
from datetime import date

class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    def to_dict(self): return {"id": self.id, "name": self.name}

class Customer(db.Model):
    __tablename__ = 'customers'
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    def to_dict(self): return {"id": self.id, "name": self.name, "email": self.email}

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id       = db.Column(db.Integer, primary_key=True)
    product  = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    def to_dict(self): return {"id": self.id, "product": self.product, "quantity": self.quantity}

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'
    id                   = db.Column(db.Integer, primary_key=True)
    description          = db.Column(db.String(256), nullable=False)
    customer_id          = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    assigned_mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=True)
    status               = db.Column(db.String(32), nullable=False, default='open')
    created_on           = db.Column(db.Date, nullable=False, default=date.today)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "customer_id": self.customer_id,
            "assigned_mechanic_id": self.assigned_mechanic_id,
            "status": self.status
        }
