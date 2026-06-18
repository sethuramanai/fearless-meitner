Django Todo Application with CI/CD
This plan outlines the architecture and implementation details for a beautiful, fully functional Django-based Todo application. It includes user authentication, task search and categorization, a modern Glassmorphism web interface with a dark mode toggle, Docker integration, and a CI/CD pipeline using GitHub Actions.

User Review Required
IMPORTANT

Python Version: The system is running Python 3.13.5. We will target Python 3.12 or 3.13 in our Docker/CI environments.
Database: For simplicity and ease of setup, we will use SQLite for development/testing, but package it with Docker so that it is production-ready.
CI/CD Target: We will set up a GitHub Actions workflow that automatically runs linting (black and flake8), runs django tests, and builds a Docker image to verify container integrity.
Proposed Architecture
1. Backend: Django (Python 3.13)
Authentication: Native Django Auth system for User signup, login, and logout.
Models:
Task: Title, Description, Created date, Due date, Completion status, Priority (Low, Medium, High), Category (Work, Personal, etc.), Owner (ForeignKey to User).
Forms: Django ModelForm for tasks and custom user creation/authentication forms.
Views: CBVs (Class-Based Views) or neat FBVs (Function-Based Views) with login decorators.
2. Frontend: Django Templates + Vanilla CSS + JS
UI Design: Modern Glassmorphism aesthetic. Transparent panels with backdrop filters, vibrant neon accents, custom gradients, interactive task cards with hover animations, and a responsive grid layout.
Theme: Dark/Light mode toggle persisted via localStorage and system preference detection.
Features:
Task progress visualization (completion rate donut/progress bar).
Search and filter bar (filter by category, priority, status).
Quick toggle for task completion (AJAX-based for seamless UX).
Form validation with beautiful toast notifications.
3. CI/CD & Devops
Docker:
Dockerfile: Multi-stage build for production-ready Django runtime.
docker-compose.yml: For containerized orchestration.
CI/CD Workflow:
.github/workflows/django-ci.yml: Triggers on push/PR. Runs code formatting tests (black), linting (flake8), unit tests (manage.py test), and verifies the Docker build.
