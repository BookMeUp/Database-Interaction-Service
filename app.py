from flask import Flask
from models import db
from routes import register_blueprints
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
import time

app = Flask(__name__)

metrics = PrometheusMetrics(app)

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

# Register blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
