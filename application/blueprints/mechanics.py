from flask import Blueprint, request, jsonify
from application.extensions import db
from application.models import Mechanic

mechanics_bp = Blueprint('mechanics', __name__)

@mechanics_bp.route('/', methods=['GET'])
def list_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify([m.to_dict() for m in mechanics]), 200

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'name': ['Missing data for required field.']}), 400

    m = Mechanic(name=name)
    db.session.add(m)
    db.session.commit()
    return jsonify(m.to_dict()), 201

@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'name': ['Missing data for required field.']}), 400

    m = Mechanic.query.get(id)
    if not m:
        return jsonify({'message': 'Mechanic not found'}), 404

    m.name = name
    db.session.commit()
    return jsonify(m.to_dict()), 200

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    m = Mechanic.query.get(id)
    if not m:
        return jsonify({'message': 'Mechanic not found'}), 404

    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': f'Mechanic {id} deleted successfully.'}), 200
