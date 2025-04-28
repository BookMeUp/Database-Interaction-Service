from flask import Blueprint, request, jsonify
from models import db, Availability

availability_bp = Blueprint("availability", __name__)

@availability_bp.route("/availability/id/<int:availability_id>", methods=["GET"])
def get_availability_by_id(availability_id):
    availability = Availability.query.get(availability_id)
    if not availability:
        return jsonify({"error": "Availability not found"}), 404

    return jsonify({
        "id": availability.id,
        "date": availability.date,
        "start_time": availability.start_time,
        "end_time": availability.end_time
    }), 200

@availability_bp.route("/availability/<date>", methods=["GET"])
def get_availability_by_date(date):
    slots = Availability.query.filter_by(date=date).all()
    return jsonify([
        {
            "id": s.id,
            "date": s.date,
            "start_time": s.start_time,
            "end_time": s.end_time
        }
        for s in slots
    ])

@availability_bp.route("/availability", methods=["POST"])
def add_availability():
    data = request.json
    new_slot = Availability(
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"]
    )
    db.session.add(new_slot)
    db.session.commit()
    return jsonify({
        "message": "Availability added",
        "object_id": new_slot.id
    }), 201

@availability_bp.route("/availability/<int:availability_id>", methods=["DELETE"])
def delete_availability(availability_id):
    availability = Availability.query.get(availability_id)
    if not availability:
        return jsonify({"error": "Availability not found"}), 404

    db.session.delete(availability)
    db.session.commit()
    return jsonify({"message": "Availability deleted"}), 200
