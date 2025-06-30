from flask import Blueprint, request, jsonify
from application.extensions import db
from application.models import ServiceTicket

service_ticket_bp = Blueprint('service_tickets', __name__)

@service_ticket_bp.route('/', methods=['GET'])
def list_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify([t.to_dict() for t in tickets]), 200

@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json() or {}
    missing = [f for f in ('description','customer_id') if not data.get(f)]
    if missing:
        return jsonify({ missing[0]: ['Missing data for required field.'] }), 400

    try:
        cid = int(data['customer_id'])
    except (ValueError, TypeError):
        return jsonify({'customer_id': ['Must be an integer.']}), 400

    t = ServiceTicket(
        description=data['description'],
        customer_id=cid,
        assigned_mechanic_id=data.get('assigned_mechanic_id'),
        status=data.get('status', 'open')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@service_ticket_bp.route('/<int:id>', methods=['PUT'])
def update_ticket(id):
    data = request.get_json() or {}
    t = ServiceTicket.query.get(id)
    if not t:
        return jsonify({'message': 'Service ticket not found'}), 404

    if data.get('description'): t.description = data['description']
    if data.get('customer_id') is not None:
        try:
            t.customer_id = int(data['customer_id'])
        except (ValueError, TypeError):
            return jsonify({'customer_id': ['Must be an integer.']}), 400
    if data.get('assigned_mechanic_id') is not None:
        t.assigned_mechanic_id = data['assigned_mechanic_id']
    if data.get('status'): t.status = data['status']

    db.session.commit()
    return jsonify(t.to_dict()), 200

@service_ticket_bp.route('/<int:id>', methods=['DELETE'])
def delete_ticket(id):
    t = ServiceTicket.query.get(id)
    if not t:
        return jsonify({'message': 'Service ticket not found'}), 404

    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': f'Service ticket {id} deleted successfully.'}), 200
