# Tupange Web App

## Overview
Tupange is a robust healthcare appointment scheduling system designed to efficiently manage patient data and enable seamless appointment scheduling with healthcare providers. This system provides backend functionality for patient and doctor management, appointment scheduling, and optional features like medical records management.

## Features
- **Patient Management**: Register and manage patient profiles with personal and insurance information
- **Doctor Management**: Maintain doctor profiles with specializations and availability schedules
- **Appointment Scheduling**: Create appointments with conflict prevention and status management
- **Medical Records (Bonus)**: Basic medical records storage linked to appointments with access controls
- **Secure API**: Role-based authentication and authorization for all endpoints


## Technology Stack
- **Backend**: Python with FastAPI
- **Database**: MySQL
- **Authentication**: OAuth 2.0 with JWT
- **Message Queue**: RabbitMQ for asynchronous processing
- **Caching**: Redis
- **API Documentation**: OpenAPI/Swagger
- **Testing**: Pytest
- **CI/CD**: GitHub Actions

## Setup Instructions

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- RabbitMQ
- Redis

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/its-kios09/tupange.git
   cd tupange
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

### Running the Application
Start the development server:
```bash
uvicorn app.main:app --reload
```

The API documentation will be available at `http://localhost:8000/docs`

### Running Tests
```bash
pytest
```

## API Documentation
Interactive API documentation is available via Swagger UI at `/docs` when the application is running. The OpenAPI specification is available at `/openapi.json`.


## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request


## The UI is still under development: Demo
![demoTupange](https://github.com/user-attachments/assets/f00eb8ca-4b68-47f6-8ea8-62197cad1d1a)


