from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'customer' or 'staff'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False) # e.g. "50 RON"
    duration = db.Column(db.Integer, nullable=False)  # in minutes

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date = db.Column(db.String, nullable=False)  # e.g., "2025-04-25"
    time = db.Column(db.String, nullable=False)  # e.g., "09:00"

    service = db.relationship("Service", backref="appointments")

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)  # e.g., "2025-04-25"
    start_time = db.Column(db.String, nullable=False)  # e.g., "09:00"
    end_time = db.Column(db.String, nullable=False)    # e.g., "17:00"
