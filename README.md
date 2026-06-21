# 🚀 Django Todo Application with CI/CD

A modern, production-ready Todo application built with Django, featuring user authentication, task management, search and filtering, Glassmorphism UI, dark/light themes, Docker containerization, and automated CI/CD using GitHub Actions.

---

# 📋 Project Overview

This project demonstrates modern full-stack web development practices using Django and DevOps tooling.

## Key Features

### 🔐 Authentication

* User Registration
* User Login
* User Logout
* Secure Session Management
* User-specific Tasks

### ✅ Task Management

* Create Tasks
* Edit Tasks
* Delete Tasks
* Mark Tasks as Complete
* Task Due Dates
* Task Priorities
* Task Categories

### 🔍 Search & Filtering

* Search Tasks by Title
* Filter by Category
* Filter by Priority
* Filter by Status
* Combined Search & Filters

### 🎨 Modern UI

* Glassmorphism Design
* Responsive Layout
* Hover Animations
* Gradient Backgrounds
* Toast Notifications
* Interactive Task Cards

### 🌙 Dark Mode

* Dark Theme
* Light Theme
* Theme Persistence using LocalStorage
* Automatic System Preference Detection

### 📊 Dashboard Features

* Task Completion Percentage
* Progress Bar Visualization
* Task Statistics
* Category Breakdown

### ⚡ AJAX Features

* Instant Task Completion Toggle
* Dynamic UI Updates
* Improved User Experience

---

# 🏗️ Architecture

## Backend

### Framework

* Django 5.x
* Python 3.12 / 3.13

### Database

* SQLite (Development)
* Dockerized Deployment Ready

### Models

#### Task Model

| Field       | Type             |
| ----------- | ---------------- |
| title       | CharField        |
| description | TextField        |
| created_at  | DateTimeField    |
| due_date    | DateField        |
| completed   | BooleanField     |
| priority    | CharField        |
| category    | CharField        |
| owner       | ForeignKey(User) |

### Authentication

* Django Authentication System
* LoginRequiredMixin
* User Creation Form
* Authentication Form

### Forms

* Task ModelForm
* User Registration Form
* Login Form

### Views

* List View
* Create View
* Update View
* Delete View
* Detail View

---

# 🎨 Frontend

## Technologies

* HTML5
* CSS3
* JavaScript
* Django Templates

## UI Design

### Glassmorphism Components

* Transparent Cards
* Blur Effects
* Frosted Glass Panels
* Modern Shadows
* Smooth Animations

### Responsive Design

* Desktop
* Tablet
* Mobile

---

# 🐳 Docker Configuration

## Dockerfile

Features:

* Multi-stage Build
* Lightweight Runtime
* Production Ready
* Security Optimized

## Docker Compose

Services:

* Django Application
* SQLite Storage Volume

Run:

```bash
docker-compose up --build
```

---

# 🔄 CI/CD Pipeline

GitHub Actions workflow automatically performs:

## Code Quality

### Black

```bash
black .
```

### Flake8

```bash
flake8 .
```

## Testing

```bash
python manage.py test
```

## Docker Verification

```bash
docker build -t django-todo .
```

---

# 📂 Project Structure

```text
django-todo-app/
│
├── .github/
│   └── workflows/
│       └── django-ci.yml
│
├── todo_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── task_list.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

# 🚀 Local Setup

## Clone Repository

```bash
git clone https://github.com/yourusername/django-todo-app.git
cd django-todo-app
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Start Server

```bash
python manage.py runserver
```

Application URL:

```text
http://127.0.0.1:8000
```

---

# 🧪 Running Tests

```bash
python manage.py test
```

---

# 🐳 Running with Docker

Build Image:

```bash
docker build -t django-todo .
```

Run Container:

```bash
docker run -p 8000:8000 django-todo
```

Or

```bash
docker-compose up --build
```

---

# 🔒 Future Enhancements

* PostgreSQL Support
* Redis Caching
* Celery Background Jobs
* Email Notifications
* REST API using Django REST Framework
* JWT Authentication
* Kubernetes Deployment
* AWS ECS/EKS Deployment
* Monitoring with Prometheus & Grafana

---

# 👨‍💻 Tech Stack

* Python 3.13
* Django 5.x
* SQLite
* HTML5
* CSS3
* JavaScript
* Docker
* GitHub Actions
* Git
* Linux

---

# 📜 License

MIT License

---

Built with ❤️ using Django, Docker, and GitHub Actions.
