# About this repository

The "exercise" app is a Django-based web application designed to help users explore and manage exercises for their
workout
routines. The application provides a user-friendly interface to browse exercises by muscle groups, filter exercises
based on specific criteria, and view detailed information about each exercise. It also includes various API for
programmatic access and creation of data.

This project was built as part of my portfolio to showcase skills in Python (OOP), Django development, Database design,
REST API design, Docker containerization and frontend development and integration.

The app is currently up at: ...........................................................

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

- **Backend**: Django 5.2.6 (Python)
- **Frontend**: Bootstrap 5.3.8 for responsive design, combined with JavaScript (OOP) for asynchronous data handling,
  ensuring a smooth and responsive user experience.
- **Database**: PostgreSQL.
- **API**: Django REST Framework (DRF) with OpenAPI documentation via `drf-spectacular`
- **Testing**: `pytest`, `pytest-django`, and `factory_boy`
- **Containerization**: Docker for deployment

---

## Features

- **Homepage**: A welcoming landing page with links to browse muscle groups and all exercises;
- **Muscle Groups**: View muscle groups with images and descriptions, and explore exercises associated with each group;
- **Exercise List**: A paginated and filterable list of exercises, with options to filter by name, description, workout
  type, muscle group, muscle, and muscle part;
- **Exercise Details**: View detailed information about each exercise, including its name, description, workout type,
  and associated muscle parts;
- **Dynamic Filtering**: Filters that dynamically update based on user selections;
- **REST API**: Provides endpoints to retrieve and create exercises programmatically;
- **Admin Panel**: Manage exercises, muscle groups, and related data through Django's admin interface;
- **Test Suite**: Comprehensive test coverage for models, views, serializers, and filters using `pytest`.

---

## Usage

### Web Interface

- Homepage: Navigate to the homepage to start exploring.
- Muscle Groups: Browse muscle groups available to view associated exercises.
- Exercises: Use the filterable list to find exercises that match your criteria.
- API
    - Swagger UI: Explore the API documentation at /api/schema/docs/.
    - To use the APIs the user must authenticate himself. If you want to try them for yourself, contact me at
      "https://www.linkedin.com/in/daniel-carapinha-oliveira" and I'll send you some credentials as soon as I can.

---

## Main Project Structure

- apps/core: Core utilities, to handle app wide logic.
- apps/exercises: Main app for managing exercises and related data.
- static: Static files, including JavaScript and CSS.
- templates: HTML templates for the frontend.
- tests: Comprehensive test suite for all components.

---

## Prerequisites

1. **To run the development server**

- **Python 3.13.7**
- **pip** (usually bundled with Python)
- **virtualenv** or **venv** (highly recommended)
- **PostgreSQL**

2. **To Deploy:**

- **Docker**

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

---

## Running the Development Server or Deploying the app

### Running the Development Server

1. **Run the development server with python:**
    - **Install project dependencies (files in requirements folder):**
        - **Project:**
            - **pip install -r requirements\base.txt**
        - **Project and tests:**
            - **pip install -r requirements\tests.txt**

- python manage.py runserver
- After running, the project will be available at: http://localhost:8000

### Deploying the app

**To deploy the project with docker:**

- Go to \env and remove .example from "exercise.env.example" and "exercise_db.env.example".
    - Set up the variables inside:
        - exercise.env:
            - SECRET_KEY: A chosen secret key;
            - ALLOWED_HOSTS....................................................................................
            - DB_PASSWORD: choose a password for your database.
        - exercise_db.env:
            - POSTGRES_PASSWORD: must be exactly the same as "DB_PASSWORD" in file "exercise.env";

- Use the following command in CMD: **docker-compose build && docker-compose up -d**
- The app comes preloaded with data via fixtures that get loaded via the docker-compose process, so you can jump right
  into testing the app.

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