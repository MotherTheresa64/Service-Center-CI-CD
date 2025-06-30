from flask import Blueprint, request, jsonify
from application.extensions import db
from application.models import Customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/', methods=['GET'])
def list_customers():
    all_c = Customer.query.all()
    return jsonify([c.to_dict() for c in all_c]), 200

@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json() or {}
    missing = [f for f in ('name','email') if not data.get(f)]
    if missing:
        return jsonify({ missing[0]: ['Missing data for required field.'] }), 400

    c = Customer(name=data['name'], email=data['email'])
    db.session.add(c)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'email': ['Email must be unique.']}), 400

    return jsonify(c.to_dict()), 201

@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json() or {}
    if not data.get('name') and not data.get('email'):
        return jsonify({'message': 'Nothing to update'}), 400

    c = Customer.query.get(id)
    if not c:
        return jsonify({'message': 'Customer not found'}), 404

    if data.get('name'):  c.name = data['name']
    if data.get('email'): c.email = data['email']
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'email': ['Email must be unique.']}), 400

    return jsonify(c.to_dict()), 200

@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    c = Customer.query.get(id)
    if not c:
        return jsonify({'message': 'Customer not found'}), 404

    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': f'Customer {id} deleted successfully.'}), 200
