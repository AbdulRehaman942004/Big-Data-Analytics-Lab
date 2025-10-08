# CRUD API with MongoDB and Docker

A complete CRUD (Create, Read, Update, Delete) application built with FastAPI, MongoDB, and Docker.

## Features

- ✅ Complete CRUD operations for user management
- ✅ MongoDB integration with async operations
- ✅ Docker containerization
- ✅ Environment variable configuration
- ✅ Input validation with Pydantic
- ✅ Error handling and HTTP status codes
- ✅ CORS support
- ✅ Health check endpoints
- ✅ API documentation with FastAPI

## Project Structure

```
BDA lab 3/
├── crud.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker services setup
├── mongo-init.js       # MongoDB initialization script
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Quick Start

### 1. Create Environment File
Copy the example environment file:
```bash
copy .env.example .env
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```

### 3. Access the Application
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Health & Info
- `GET /` - Root endpoint
- `GET /health` - Health check with database status
- `GET /stats` - Application statistics

### User Operations
- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `GET /users/search/email/{email}` - Get user by email
- `PUT /users/{user_id}` - Update user by ID
- `DELETE /users/{user_id}` - Delete user by ID
- `DELETE /users/` - Delete all users (use with caution)

## Sample API Usage

### Create User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "phone": "+1234567890",
    "address": "123 Main St"
  }'
```

### Get All Users
```bash
curl -X GET "http://localhost:8000/users/"
```

### Update User
```bash
curl -X PUT "http://localhost:8000/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "age": 31
  }'
```

### Delete User
```bash
curl -X DELETE "http://localhost:8000/users/{user_id}"
```

## Development

### Run Locally (without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start MongoDB locally or use MongoDB Atlas

3. Update `.env` file with your MongoDB connection string

4. Run the application:
   ```bash
   python crud.py
   ```

### Docker Commands
```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (careful - deletes data)
docker-compose down -v
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://mongo:27017` |
| `MONGODB_DATABASE` | Database name | `crud_app` |
| `MONGODB_COLLECTION` | Collection name | `users` |
| `APP_HOST` | Application host | `0.0.0.0` |
| `APP_PORT` | Application port | `8000` |
| `DEBUG` | Debug mode | `True` |

## Data Model

### User Schema
```json
{
  "id": "ObjectId",
  "name": "string",
  "email": "string (unique)",
  "age": "integer",
  "phone": "string (optional)",
  "address": "string (optional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Features Implemented

- ✅ **Create**: Add new users with validation
- ✅ **Read**: Get users by ID, email, or all users with pagination
- ✅ **Update**: Update user information with partial updates
- ✅ **Delete**: Delete single user or all users
- ✅ **Validation**: Email uniqueness, required fields, data types
- ✅ **Error Handling**: Comprehensive error messages and HTTP status codes
- ✅ **Database**: MongoDB with async operations
- ✅ **Containerization**: Docker with multi-service setup
- ✅ **Configuration**: Environment variables for all settings
- ✅ **Documentation**: Auto-generated API docs with FastAPI

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `docker-compose logs mongo`
- Check connection string in `.env` file
- Verify network connectivity between containers

### Port Conflicts
- Change ports in `docker-compose.yml` if 8000 or 27017 are in use
- Update `.env` file accordingly

### Permission Issues
- On Windows, ensure Docker Desktop has proper permissions
- On Linux/Mac, ensure user is in docker group

## Production Considerations

1. **Security**: Change default passwords and secret keys
2. **Environment**: Set `DEBUG=False` in production
3. **Database**: Use MongoDB Atlas or secure MongoDB instance
4. **SSL**: Add HTTPS/TLS certificates
5. **Monitoring**: Add logging and monitoring solutions
6. **Backup**: Implement database backup strategy
