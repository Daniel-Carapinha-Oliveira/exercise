# About this repository

The application is live and accessible at https://thebestexerciseapp.com/. Feel free to explore its features.

The "exercise" app is a Django-based web application that helps users explore exercises for their workout
routines. It provides a user-friendly interface to browse exercises by muscle group, filter by criteria, and view
detailed information. The app also provides REST APIs for access and data creation.

This project demonstrates skills in Python (OOP), Django development, project design, database design, REST API design,
Docker containerization, frontend development (html, javascript) and integration, as well as proficiency in working with 
Linux servers and understanding their underlying logic and operations. I built a production-ready web application fully 
containerized with Docker and orchestrated using Docker Compose. It connects to a PostgreSQL database and is served 
through Caddy, which handles static file serving, reverse proxying, and HTTPS. The project demonstrates expertise in 
CI/CD practices, including version control (Git/GitHub), containerization (Docker), and automated testing frameworks.

Key production features include:

- Persistent volumes for static, media files, and logging files;
- Secure non-root user setup, as well as other security features;
- Service separation for app, database, and web server/reverse proxy;
- Manage secrets securely.
- Logging and deployment readiness.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Features](#features)
3. [Usage](#usage)
4. [Main Project Structure](#main-project-structure)
5. [Prerequisites](#prerequisites)
6. [Installation and setup to run the development server](#installation-and-setup-to-run-the-development-server)
7. [Running the Development Server or Deploying the app](#running-the-development-server-or-deploying-the-app)
8. [Running tests](#running-tests)

---

## Tech Stack

The tech stack used for this project is the following:

- **Backend**: Django 5.2.6 with Python (object-oriented programming) for scalable and maintainable server-side logic.
- **Frontend**: Bootstrap 5.3.8 for responsive UI design, enhanced with JavaScript (OOP) for asynchronous data handling
  and a smooth, dynamic user experience.
- **Database**: PostgreSQL for robust relational data storage and efficient querying.
- **API**: Django REST Framework (DRF) with OpenAPI documentation using drf-spectacular for well-documented,
  standards-compliant APIs.
- **Testing**: `pytest`, `pytest-django`, and `factory_boy` for comprehensive unit and integration testing, ensuring
  reliability and maintainability. Comprehensive test coverage for models, views, serializers, and filters.
- **Containerization**: Docker and Docker Compose for consistent development, testing, and deployment environments.
- **version control**: Git and GitHub for source code management, and version tracking.

---

## Web app features

- **Homepage**: A welcoming landing page with links to browse muscle groups and all exercises;
- **Muscle Groups**: View muscle groups with images and descriptions, and explore exercises associated with each group;
- **Exercise List**: A paginated and filterable list of exercises, with options to filter by name, description, workout
  type, muscle group, muscle, and muscle part;
- **Exercise Details**: View detailed information about each exercise, including its name, description, workout type,
  and associated muscle parts;
- **Dynamic Filtering**: Filters that dynamically update based on user selections;
- **REST API**: Provides endpoints to retrieve and create exercises;
- **Admin Panel**: Manage exercises, muscle groups, and related data through Django's admin interface
  https://thebestexerciseapp.com/admin.

### Interface and Usage

- Homepage: Navigate to the homepage to start exploring.
- Muscle Groups: Browse muscle groups available to view associated exercises.
- Exercises: Use the filters available to find exercises that match your criteria.
- API
    - Swagger UI: Explore the API documentation at https://thebestexerciseapp.com/api/schema/docs/.
    - To use the APIs the user must authenticate himself. If you want to try them for yourself, contact me at
      "https://www.linkedin.com/in/daniel-carapinha-oliveira" and I'll send you some credentials as soon as I can.

---

## Main Project Structure

- apps/core – Contains core utilities and services that handle application-wide logic and shared functionality.
- apps/exercises – Primary app responsible for managing exercises, related data, and associated business logic.
- static – Stores static assets such as JavaScript, CSS, images, and other frontend resources.
- templates – Holds HTML templates used to render frontend pages dynamically.
- tests – Comprehensive test suite covering all components of the project, ensuring correctness and stability.

---

## Prerequisites to run and deploy the app

1. **To run the development server**

- **Python 3.13.7**;
- **pip** (usually bundled with Python);
- **virtualenv** or **venv** (highly recommended);
- **PostgreSQL**.

2. **To Deploy with a private domain:**

- **Docker**;
- **A private domain**.

---

## Installation and setup to run the development server

1. **Clone the repository.**

2. **Create PostgreSQL database**
    - Create a PostgreSQL database.

3. **Setup ".env" file:**
    - **Remove `.example` from the file `.env.example` in the root of the project.**
        - **Generate new secret key:**
            - Activate your virtual environment, navigate to the project’s root directory, and run the following
              commands:
                - python manage.py shell
                - from django.core.management.utils import get_random_secret_key
                - print(get_random_secret_key())
                - Copy the secret key and paste it after `SECRET_KEY=`
        - **Set up the rest of the environment variables:**
            - DEBUG: "True" or "False" depending on what you want, but for development is it recommended to leave it at
              "True".
            - DB_NAME: choose exactly the same name of the database you created in point 2.
            - DB_USER: your database user (default postgres)
            - DB_PASSWORD: your database password
            - DB_HOST: your database host (default localhost)
            - DB_PORT: your database port (default 5432)
            - ALLOWED_HOSTS:localhost,127.0.0.1.

### Running the Development Server

1. **Run the development server with python:**

- **Install project dependencies (files in requirements folder):**
    - **Project:**
        - **pip install -r requirements\base.txt**
    - **Project and tests:**
        - **pip install -r requirements\tests.txt**

- **python manage.py runserver**
- **After running, the project will be available at:** http://localhost:8000

---

## Deploying the app

**To deploy the project**

- Go to \env and remove .example from "exercise.env.example", "exercise_db.env.example" and "caddy.env.example".
    - Set up the variables inside:
        - exercise.env:
            - SECRET_KEY: A chosen secret key;
            - ALLOWED_HOSTS: your domain name;
            - DB_PASSWORD: choose a password for your database.
        - exercise_db.env:
            - POSTGRES_PASSWORD: must be exactly the same as "DB_PASSWORD" in file "exercise.env";
        - caddy.env:
            - DOMAIN_NAME= your domain name.

- Use the following command in CMD: **docker compose build && docker compose up -d**

- Note: The app comes preloaded with sample data that you can use immediately after deployment. To load the fixtures,
  simply run the following command in the "exercise" docker container:

**python manage.py loaddata user_fixture.json muscle_group_fixture.json muscle_fixture.json muscle_part_fixture.json
exercise_fixture.json**

---

## Running tests

1. **All tests:**

- pytest

2. **Specific test file (in this example test_models.py for the exercises app):**

- pytest apps/exercises/tests/test_models.py

3. **Specific class:**

- pytest apps/exercises/tests/test_models.py::TestMuscleGroupModel

4. **Specific test:**

- pytest apps/exercises/tests/test_models.py::TestMuscleGroupModel::test_name_max_length

### Test Coverage

- Models: Validates field constraints, relationships, and methods.
- Views: Ensures correct rendering of templates and API responses.
- Serializers: Validates data serialization and deserialization.
- Filters: Tests dynamic filtering logic.

---

# Contacts

- https://www.linkedin.com/in/daniel-carapinha-oliveira;