from flask import Flask, request, jsonify
from models import db, User, Service, Appointment
from sqlalchemy.exc import OperationalError
import time

app = Flask(__name__)

# DB config (matches docker-compose setup)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@postgres:5432/bookmeup'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Retry logic for waiting on the DB (Swarm-safe)
MAX_RETRIES = 10
RETRY_DELAY = 3  # seconds

with app.app_context():
    for attempt in range(MAX_RETRIES):
        try:
            db.create_all()
            print("✅ Successfully connected to and initialized the database.")
            break
        except OperationalError as e:
            print(f"⏳ Waiting for DB... attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            time.sleep(RETRY_DELAY)
    else:
        print("❌ Could not connect to the database after several retries.")
        exit(1)

@app.route("/db/health", methods=["GET"])
def health_check():
    return "Database Interaction Service is running", 200

# ---------------- USERS ---------------- #

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })
    return jsonify({"error": "User not found"}), 404

@app.route("/users/email/<email>", methods=["GET"])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "role": user.role
        })
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]

    db.session.commit()
    return jsonify({"message": "User updated"}), 200

# ---------------- SERVICES ---------------- #

@app.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "price": s.price, "duration": s.duration}
        for s in services
    ])

@app.route("/services", methods=["POST"])
def create_service():
    data = request.json
    new_service = Service(
        name=data["name"],
        price=data["price"],
        duration=data["duration"]
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service added"}), 201

@app.route("/services/<int:service_id>", methods=["PUT"])
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

@app.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted"}), 200

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
            "service": {
                "id": a.service.id,
                "name": a.service.name
            },
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
            "service": {
                "id": a.service.id,
                "name": a.service.name
            },
            "date": a.date,
            "time": a.time
        }
        for a in appointments
    ])

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
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
