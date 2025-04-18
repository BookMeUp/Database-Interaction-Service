from flask import Flask, request, jsonify
from models import db, User, Service, Appointment

app = Flask(__name__)

# DB config (matches docker-compose setup)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@postgres:5432/bookmeup'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/db/health", methods=["GET"])
def health_check():
    return "Database Interaction Service is running", 200

# ---------------- USERS ---------------- #

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(email=data["email"], password=data["password"], role=data["role"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route("/users/email/<email>", methods=["GET"])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "role": user.role
        })
    return jsonify({"error": "User not found"}), 404

# ---------------- SERVICES ---------------- #

@app.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "duration": s.duration}
        for s in services
    ])

@app.route("/services", methods=["POST"])
def create_service():
    data = request.json
    new_service = Service(name=data["name"], duration=data["duration"])
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service added"}), 201

# ---------------- APPOINTMENTS ---------------- #

@app.route("/appointments", methods=["POST"])
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
    return jsonify({"message": "Appointment booked"}), 201

@app.route("/appointments", methods=["GET"])
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify([
        {
            "id": a.id,
            "user_id": a.user_id,
            "service_id": a.service_id,
            "date": a.date,
            "time": a.time
        }
        for a in appointments
    ])

@app.route("/appointments/user/<int:user_id>", methods=["GET"])
def get_appointments_by_user(user_id):
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": a.id,
            "service_id": a.service_id,
            "date": a.date,
            "time": a.time
        }
        for a in appointments
    ])

@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment canceled"})
    return jsonify({"error": "Appointment not found"}), 404

# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
