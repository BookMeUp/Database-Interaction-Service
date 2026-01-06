# Database Service

The Database Service is the data persistence layer for the Slotify application. It provides a RESTful API for managing users, services, appointments, and availability data using PostgreSQL with SQLAlchemy ORM.

## Features

- **User Management**: Create, read, and update user records
- **Service Management**: CRUD operations for business services
- **Appointment Management**: Complete appointment lifecycle management
- **Availability Management**: Schedule and manage provider availability
- **PostgreSQL Integration**: Robust relational database with SQLAlchemy ORM
- **Connection Retry Logic**: Automatic retry mechanism for database connections
- **Prometheus Metrics**: Built-in monitoring and metrics exposure
- **Health Check Endpoint**: Kubernetes-ready health checks
- **Blueprint Architecture**: Modular route organization

## Tech Stack

- **Framework**: Flask 2.3.2
- **ORM**: Flask-SQLAlchemy
- **Database**: PostgreSQL (via psycopg2-binary)
- **Monitoring**: Prometheus Flask Exporter
- **Runtime**: Python 3.13

## Prerequisites

- Python 3.13+
- PostgreSQL database server

## Installation

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export POSTGRES_USER="user"
export POSTGRES_PASSWORD="password"
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="slotify"
```

3. Ensure PostgreSQL is running and accessible

4. Run the service:
```bash
python app.py
```

The service will start on `http://localhost:5003`

### Docker

Build and run using Docker:

```bash
docker build -t db-service .
docker run -p 5003:5003 \
  -e POSTGRES_USER="user" \
  -e POSTGRES_PASSWORD="password" \
  -e POSTGRES_HOST="postgres" \
  -e POSTGRES_PORT="5432" \
  -e POSTGRES_DB="slotify" \
  db-service
```

Or pull from Docker Hub:

```bash
docker pull alexnv67/db-service
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | PostgreSQL username | `user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `password` |
| `POSTGRES_HOST` | PostgreSQL host address | `postgres` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | PostgreSQL database name | `slotify` |

## Database Models

### User
```python
{
  "id": Integer (Primary Key),
  "name": String(120),
  "email": String(120) - Unique,
  "password": String(128) - Hashed,
  "role": String(20) - 'customer' or 'staff'
}
```

### Service
```python
{
  "id": Integer (Primary Key),
  "name": String(100),
  "price": String(100) - e.g., "50 RON",
  "duration": Integer - Duration in minutes
}
```

### Appointment
```python
{
  "id": Integer (Primary Key),
  "user_id": Integer,
  "service_id": Integer (Foreign Key -> Service),
  "date": String - Format: "YYYY-MM-DD",
  "time": String - Format: "HH:MM"
}
```

### Availability
```python
{
  "id": Integer (Primary Key),
  "date": String - Format: "YYYY-MM-DD",
  "start_time": String - Format: "HH:MM",
  "end_time": String - Format: "HH:MM"
}
```

## API Endpoints

### Health Check
```http
GET /health
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "database-interaction"
}
```

---

## User Endpoints

### Create User
```http
POST /users
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "hashed_password_here",
  "role": "customer"
}
```

**Response:** `201 Created`
```json
{
  "message": "User created",
  "object_id": 1
}
```

### Get User by ID
```http
GET /users/<user_id>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "customer"
}
```

### Get User by Email
```http
GET /users/email/<email>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "password": "hashed_password_here",
  "role": "customer"
}
```

**Note:** Password is included for authentication purposes.

### Update User
```http
PUT /users/<user_id>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "newemail@example.com",
  "password": "new_hashed_password"
}
```

**Response:** `200 OK`

---

## Service Endpoints

### Get All Services
```http
GET /services
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Haircut",
    "price": "25 RON",
    "duration": 30
  }
]
```

### Get Service by ID
```http
GET /services/<service_id>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Haircut",
  "price": "25 RON",
  "duration": 30
}
```

### Create Service
```http
POST /services
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Haircut",
  "price": "25 RON",
  "duration": 30
}
```

**Response:** `201 Created`
```json
{
  "message": "Service added",
  "object_id": 1
}
```

### Update Service
```http
PUT /services/<service_id>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Premium Haircut",
  "price": "35 RON",
  "duration": 45
}
```

**Response:** `200 OK`

### Delete Service
```http
DELETE /services/<service_id>
```

**Response:** `200 OK`

---

## Appointment Endpoints

### Get All Appointments
```http
GET /appointments
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "service": {
      "id": 1,
      "name": "Haircut"
    },
    "date": "2026-01-15",
    "time": "10:00"
  }
]
```

### Get Appointment by ID
```http
GET /appointments/<appointment_id>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "service_id": 1,
  "date": "2026-01-15",
  "time": "10:00"
}
```

### Get Appointments by User
```http
GET /appointments/user/<user_id>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "service": {
      "id": 1,
      "name": "Haircut"
    },
    "date": "2026-01-15",
    "time": "10:00"
  }
]
```

### Get Appointments by Date
```http
GET /appointments/date/<date>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "service": {
      "id": 1,
      "name": "Haircut"
    },
    "date": "2026-01-15",
    "time": "10:00"
  }
]
```

### Create Appointment
```http
POST /appointments
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": 1,
  "service_id": 1,
  "date": "2026-01-15",
  "time": "10:00"
}
```

**Response:** `201 Created`
```json
{
  "message": "Appointment booked",
  "object_id": 1
}
```

### Update Appointment
```http
PUT /appointments/<appointment_id>
Content-Type: application/json
```

**Request Body:**
```json
{
  "date": "2026-01-16",
  "time": "11:00"
}
```

**Response:** `200 OK`

### Delete Appointment
```http
DELETE /appointments/<appointment_id>
```

**Response:** `200 OK`

---

## Availability Endpoints

### Get Availability by ID
```http
GET /availability/id/<availability_id>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "date": "2026-01-15",
  "start_time": "09:00",
  "end_time": "17:00"
}
```

### Get Availability by Date
```http
GET /availability/<date>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "date": "2026-01-15",
    "start_time": "09:00",
    "end_time": "17:00"
  }
]
```

### Create Availability
```http
POST /availability
Content-Type: application/json
```

**Request Body:**
```json
{
  "date": "2026-01-15",
  "start_time": "09:00",
  "end_time": "17:00"
}
```

**Response:** `201 Created`
```json
{
  "message": "Availability added",
  "object_id": 1
}
```

### Delete Availability
```http
DELETE /availability/<availability_id>
```

**Response:** `200 OK`

---

## Architecture

The Database Service is the foundation layer of the Slotify microservices architecture:

```
Auth Service (5001) ─────┐
                          │
Business Service (5002) ──┼──> Database Service (5003) ──> PostgreSQL
                          │
Other Services ───────────┘
```

- **Data Layer**: Direct PostgreSQL interaction via SQLAlchemy
- **Stateless API**: RESTful endpoints for data operations
- **Single Source of Truth**: All persistent data flows through this service
- **Connection Pooling**: SQLAlchemy manages database connections efficiently

## Project Structure

```
database-service/
├── app.py                  # Main Flask application
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container image definition
├── routes/
│   ├── __init__.py        # Blueprint registration
│   ├── users.py           # User CRUD operations
│   ├── services.py        # Service CRUD operations
│   ├── appointments.py    # Appointment management
│   └── availability.py    # Availability management
└── .github/
    └── workflows/
        └── docker-publish.yml  # CI/CD pipeline
```

## Connection Retry Logic

The service implements robust database connection handling:

- **Max Retries**: 10 attempts
- **Retry Delay**: 3 seconds between attempts
- **Automatic Table Creation**: Creates all tables on successful connection
- **Failure Handling**: Exits with error code 1 if connection fails

This makes the service resilient in orchestrated environments (Docker Swarm, Kubernetes) where the database may not be immediately available.

## Metrics

Prometheus metrics are automatically exposed at:
```
GET /metrics
```

Includes standard HTTP metrics for all endpoints.

## CI/CD

The service uses GitHub Actions for continuous deployment:

- **Trigger**: Push to `main` branch
- **Action**: Builds Docker image and pushes to Docker Hub
- **Image**: `alexnv67/db-service`
- **Workflow**: `.github/workflows/docker-publish.yml`

## Development Notes

- **No Authentication**: This service does NOT validate JWT tokens - authentication is handled by upstream services
- **Direct Database Access**: Provides raw CRUD operations without business logic
- **Foreign Key Relationships**: Service relationship in Appointment model enables joined queries
- **String-based Dates/Times**: Uses string format for flexibility (YYYY-MM-DD, HH:MM)
- **Debug Mode**: Disabled in production (`debug=False`)
- **SQLALCHEMY_TRACK_MODIFICATIONS**: Disabled for performance

## Security Considerations

⚠️ **Important:**

- **Internal Service Only**: Should NOT be exposed directly to the internet
- **No Input Validation**: Assumes upstream services validate input
- **No Authentication**: Trusts all incoming requests
- **Network Isolation**: Should only be accessible within the service network
- **Password Storage**: Stores passwords as received (hashing done by Auth Service)
- **Database Credentials**: Use strong passwords and secure environment variable management

## Production Recommendations

1. **Network Policies**: Restrict access to Auth and Business services only
2. **Database Backups**: Implement regular automated backups
3. **Connection Pooling**: Configure SQLAlchemy pool size for production load
4. **Monitoring**: Set up alerts for connection failures and query performance
5. **Migrations**: Use Alembic for database schema migrations
6. **Logging**: Implement comprehensive logging for debugging
7. **Read Replicas**: Consider read replicas for scaling queries
8. **Index Optimization**: Add indexes on frequently queried columns (email, date, etc.)

## Error Handling

The service returns appropriate HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Database or server errors

## Testing Considerations

When testing:
- Ensure PostgreSQL is running and accessible
- Use a separate test database
- Test connection retry logic by delaying database startup
- Verify foreign key constraints (Appointment → Service)
- Test edge cases (duplicate emails, invalid IDs)

## Database Initialization

On startup, the service:
1. Attempts to connect to PostgreSQL
2. Retries up to 10 times if connection fails
3. Creates all tables defined in `models.py`
4. Registers all blueprint routes
5. Starts the Flask server

## Related Services

- **Authentication Service**: Creates users and validates credentials
- **Business Logic Service**: Implements business rules and validation

## License

Part of the Slotify platform.
