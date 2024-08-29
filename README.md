# Planetarium API Service

## Description

Planetarium API Service is a Django project that provides functionality for managing astronomical shows in a planetarium. The project includes models for shows, show themes, planetarium domes, reservations, show sessions, and tickets.

## Requirements

- Python 3.10
- PostgreSQL 14
- Docker (for containerization)

## Installation Instructions

1. **Clone the repository:**

   ```bash
   git clone <REPOSITORY-URL>
   cd <REPOSITORY-DIRECTORY>
2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
3. **Install dependencies:**

    ```dash
    pip install -r requirements.txt

4. **Configure the database:**

Create a .env file in the root directory and add settings for PostgreSQL database.

5. **Apply migrations:**
    
    ```bash
    python manage.py migrate

6. **Run the server:**

    ```bash
    python manage.py runserver


## Usage

The API supports the following endpoints:

- **ShowTheme**
  - **GET** `/show-themes/` - Retrieve a list of show themes.
  - **POST** `/show-themes/` - Create a new show theme.

- **AstronomyShow**
  - **GET** `/astronomy-shows/` - Retrieve a list of astronomy shows.
  - **POST** `/astronomy-shows/` - Create a new show.
  - **POST** `/astronomy-shows/{id}/upload-image/` - Upload an image for a show.

- **PlanetariumDome**
  - **GET** `/planetarium-domes/` - Retrieve a list of planetarium domes.
  - **POST** `/planetarium-domes/` - Create a new dome.

- **Reservation**
  - **GET** `/reservations/` - Retrieve a list of reservations (authenticated users only).
  - **POST** `/reservations/` - Create a new reservation.

- **ShowSession**
  - **GET** `/show-sessions/` - Retrieve a list of show sessions.
  - **POST** `/show-sessions/` - Create a new show session.


## Docker
To run the project with Docker:

1. **Build the Docker image:**

    ```bash
    docker build -t planetarium-api-service .
   

2. **Start the containers:**

    ```bash
    docker-compose up

## Contribution
If you want to contribute to the project, please create a pull request. For reporting bugs or feature requests, use the Issues section.

## Authors
Viktor Shveda
