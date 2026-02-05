# E-Commerce Backend 

This project is a backend system for an e-commerce application built using **Django REST Framework**, containerized with **Docker**, and integrated with **MySQL**, **Redis**, and **Celery** for background task processing.

---

##  Features

- Django REST API
- MySQL Database
- Redis for Caching & Celery Broker
- Celery for Background Tasks
- Automatic Database Migration
- Automatic Fake Data Seeding (Faker)
- Fully Containerized using Docker

---

## 🛠️ Tech Stack

- Python 3.11
- Django 4.2
- Django REST Framework
- MySQL 8
- Redis 7
- Celery 5
- Docker & Docker Compose


---

##  Prerequisites

Make sure you have installed:

- Docker
- Docker Compose
- Git

Download from: https://www.docker.com/products/docker-desktop/

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RheaTiwari01/ecom_website.git
cd ecom_website
Add your username and password to the setting.py
2️⃣ Build and Start Containers
docker-compose down -v
docker-compose build --no-cache
docker-compose up
This will start:

Django Server

MySQL Database

Redis Server

Celery Worker

3️ Apply Migrations (First Time Only)
Open a new terminal and run:

docker-compose exec web python manage.py migrate
4️ (Optional) Create Admin User
docker-compose exec web python manage.py createsuperuser
Admin Panel:

http://localhost:8000/admin
🌐 Accessing the Application
Service	URL
API Server	http://localhost:8000
Admin Panel	http://localhost:8000/admin
Redis	localhost:6380
MySQL	localhost:3307
🔄 Automatic Seeding
Fake data is generated automatically using Faker during container startup.

Command used:

python manage.py seed
You can also run manually:

docker-compose exec web python manage.py seed
⚡ Background Tasks (Celery)
Celery is used for asynchronous tasks such as:

Sending order confirmations

Background processing

Worker runs automatically using:

celery -A aforro_project worker -l info
 Environment Configuration
Database and Redis connections are configured in:

aforro_project/settings.py
Using Docker service names:

HOST = "db"
REDIS = "redis"
🧪 API Testing
You can test APIs using:

Postman

Thunder Client (VS Code)

Browser (GET requests)

Example:

GET /api/orders/
POST /api/orders/
🧹 Stop Containers
To stop everything:

docker-compose down
To remove all data:

docker-compose down -v
⚠️ Common Issues
MySQL Connection Error
Fix: Wait for database or restart containers.

Redis Connection Error
Fix: Check Redis service is running.

Migration Warning
Run:

docker-compose exec web python manage.py migrate
📈 Future Improvements
Add JWT Authentication

Add Frontend (React/Angular)

Add CI/CD Pipeline

Improve Logging

Deploy on Cloud (AWS / Azure)