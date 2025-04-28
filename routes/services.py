from flask import Blueprint, request, jsonify
from models import db, Service

services_bp = Blueprint("services", __name__)

@services_bp.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "price": s.price, "duration": s.duration}
        for s in services
    ])

@services_bp.route("/services/<int:service_id>", methods=["GET"])
def get_service_by_id(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "[db-service: get_service_by_id()] Service not found"}), 404

    return jsonify({
        "id": service.id,
        "name": service.name,
        "price": service.price,
        "duration": service.duration
    }), 200

@services_bp.route("/services", methods=["POST"])
def create_service():
    data = request.json
    new_service = Service(
        name=data["name"],
        price=data["price"],
        duration=data["duration"]
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({
        "message": "Service added",
        "object_id": new_service.id
    }), 201

@services_bp.route("/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    data = request.json
    if "name" in data:
        service.name = data["name"]
    if "price" in data:
        service.price = data["price"]
    if "duration" in data:
        service.duration = data["duration"]

    db.session.commit()
    return jsonify({"message": "Service updated"}), 200

@services_bp.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted"}), 200
