from flask import Blueprint, request, jsonify
from application.extensions import db
from application.models import Inventory

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/', methods=['GET'])
def list_inventory():
    items = Inventory.query.all()
    return jsonify([i.to_dict() for i in items]), 200

@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json() or {}
    missing = [f for f in ('product','quantity') if data.get(f) is None]
    if missing:
        return jsonify({ missing[0]: ['Missing data for required field.'] }), 400

    try:
        qty = int(data['quantity'])
    except (ValueError, TypeError):
        return jsonify({'quantity': ['Quantity must be an integer.']}), 400

    item = Inventory(product=data['product'], quantity=qty)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    data = request.get_json() or {}
    item = Inventory.query.get(id)
    if not item:
        return jsonify({'message': 'Inventory item not found'}), 404

    if data.get('product'):
        item.product = data['product']
    if data.get('quantity') is not None:
        try:
            item.quantity = int(data['quantity'])
        except (ValueError, TypeError):
            return jsonify({'quantity': ['Quantity must be an integer.']}), 400

    db.session.commit()
    return jsonify(item.to_dict()), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    item = Inventory.query.get(id)
    if not item:
        return jsonify({'message': 'Inventory item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Inventory {id} deleted successfully.'}), 200
