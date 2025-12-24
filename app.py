from flask import Flask, jsonify
from models import db
from routes import register_blueprints
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
import time
import os

app = Flask(__name__)

metrics = PrometheusMetrics(app)

# DB config - use environment variables with fallback
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'bookmeup')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
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

# Health check endpoint for Kubernetes
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    try:
        # Check if database is accessible
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
