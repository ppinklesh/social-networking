Sure! Below is the `README.md` file for your project.

```markdown
# Social Network API

This is a social networking application API built using Django Rest Framework. The application includes user signup, login, search, friend requests, and friend listing functionalities.

## Features

- User Signup
- User Login
- Search Users by Email or Name
- Send/Accept/Reject Friend Requests
- List Friends
- List Pending Friend Requests
- Rate Limiting for Friend Requests (max 3 requests per minute)

## Technologies Used

- Django
- Django Rest Framework
- PostgreSQL
- Redis
- Docker
- JWT for Authentication

## Prerequisites

- Docker and Docker Compose installed on your machine

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/social_network_api.git
cd social_network_api
```

### 3. Build and Run the Docker Containers

```bash
docker-compose up --build
```

This command will build the Docker images and start the containers for the Django application, PostgreSQL database, and Redis.

### 4. Create a Superuser

After the containers are up, create a superuser to access the Django admin interface:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application

- The Django application will be running at `http://localhost:8000`.
- The Django admin interface will be accessible at `http://localhost:8000/admin`.

## API Endpoints

You can use Postman to test the API endpoints. Import the provided Postman collection to get started quickly.

### Postman Collection

Import the `SocialNetworkAPI.postman_collection.json` file into Postman to get all the configured endpoints.

### Endpoints

#### User Signup

- **URL**: `http://localhost:8000/api/signup/`
- **Method**: POST
- **Body**: 
  ```json
  {
    "email": "testuser@example.com",
    "password": "testpassword"
  }
  ```

#### User Login

- **URL**: `http://localhost:8000/api/login/`
- **Method**: POST
- **Body**: 
  ```json
  {
    "email": "testuser@example.com",
    "password": "testpassword"
  }
  ```

#### Search Users

- **URL**: `http://localhost:8000/api/search/?q=searchterm`
- **Method**: GET
- **Headers**: 
  ```
  Authorization: Bearer <access_token>
  ```

#### Send Friend Request

- **URL**: `http://localhost:8000/api/friend-request/`
- **Method**: POST
- **Headers**: 
  ```
  Authorization: Bearer <access_token>
  ```
- **Body**:
  ```json
  {
    "to_user": "otheruser@example.com"
  }
  ```

#### Accept Friend Request

- **URL**: `http://localhost:8000/api/friend-request/accept/`
- **Method**: POST
- **Headers**: 
  ```
  Authorization: Bearer <access_token>
  ```
- **Body**:
  ```json
  {
    "from_user": "otheruser@example.com"
  }
  ```

#### Reject Friend Request

- **URL**: `http://localhost:8000/api/friend-request/reject/`
- **Method**: POST
- **Headers**: 
  ```
  Authorization: Bearer <access_token>
  ```
- **Body**:
  ```json
  {
    "from_user": "otheruser@example.com"
  }
  ```

#### List Friends

- **URL**: `http://localhost:8000/api/friends/`
- **Method**: GET
- **Headers**: 
  ```
  Authorization: Bearer <access_token>
  ```

#### List Pending Friend Requests

- **URL**: `http://localhost:8000/api/friend-requests/pending/`
- **Method**: GET
- **Headers**: 
  ```
  Authorization: Bearer <access_token>
  ```

## Containerize the Application

The application is containerized using Docker. The Docker setup includes a web service for the Django application, a database service for PostgreSQL, and a Redis service.

### Docker Setup

- **Dockerfile**: Defines the image for the Django application.
- **docker-compose.yml**: Configures the services and networking.

## Rate Limiting

Friend requests are rate-limited to a maximum of 3 requests per minute.
