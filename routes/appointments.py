from flask import Blueprint, request, jsonify
from models import db, Appointment

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/appointments", methods=["GET"])
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify([
        {
            "id": a.id,
            "user_id": a.user_id,
            "service": {
                "id": a.service.id,
                "name": a.service.name
            },
            "date": a.date,
            "time": a.time
        }
        for a in appointments
    ])

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["GET"])
def get_appointment_by_id(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    return jsonify({
        "id": appointment.id,
        "user_id": appointment.user_id,
        "service_id": appointment.service_id,
        "date": appointment.date,
        "time": appointment.time
    }), 200

@appointments_bp.route("/appointments/user/<int:user_id>", methods=["GET"])
def get_appointments_by_user(user_id):
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": a.id,
            "service": {
                "id": a.service.id,
                "name": a.service.name
            },
            "date": a.date,
            "time": a.time
        }
        for a in appointments
    ])

@appointments_bp.route("/appointments/date/<date>", methods=["GET"])
def get_appointments_by_date(date):
    appointments = Appointment.query.filter_by(date=date).all()
    return jsonify([
        {
            "id": a.id,
            "user_id": a.user_id,
            "service": {
                "id": a.service.id,
                "name": a.service.name
            },
            "date": a.date,
            "time": a.time
        }
        for a in appointments
    ])

@appointments_bp.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    new_appointment = Appointment(
        user_id=data["user_id"],
        service_id=data["service_id"],
        date=data["date"],
        time=data["time"]
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({
        "message": "Appointment booked",
        "object_id": new_appointment.id
    }), 201

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.json
    if "date" in data:
        appointment.date = data["date"]
    if "time" in data:
        appointment.time = data["time"]

    db.session.commit()
    return jsonify({"message": "Appointment updated"}), 200

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment canceled"})
    return jsonify({"error": "Appointment not found"}), 404
