# QuizWhiz Flashcard Application


## Description

QuizWhiz is a web-based flashcard application that will allow users to create, edit, and review flashcards. The application will be built using Django with Django REST Framework, and will be deployed to Google Cloud Run.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Testing](#testing)


## Features

- None yet

## Technologies

- RESTful API
  - Django REST framework
  - Django REST framework SimpleJWT (for JWT authentication)
  - Django REST Swagger (for API documentation)
- Database
  - PostgreSQL (local in development, Google Cloud SQL in production)
- CI/CD
  - Containerization with Docker
  - Continuous Integration with GitHub Actions
  - Continuous Deployment to Google Cloud Run with the Google Cloud CLI
- Deployment
  - Google Cloud Run

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Docker (if using setting up with Docker Compose)

### Setup

There are two ways to run this application: using Docker Compose or running the Django development server directly.


#### Using Docker Compose (Recommended)
1. Clone the repository:
    ```sh
    git clone https://github.com/EAdibi/SWE-Project-3-Backend.git
    cd SWE-Project-3-Backend
    ```
   
2. Set up the environment variables:
    ```sh
    cp .env.example .env
    # Edit the .env file to include your database connection string and other settings
    ```

3. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```
    - The application will be accessible at `http://127.0.0.1:8080/`.
    - The Django development server will be running in a Docker container, and a local PostgreSQL instance will be running in another container.
    - The application will automatically reload when changes are made to the source code.
    - To stop the application, press `Ctrl+C` in the terminal where `docker-compose up` is running.
    - To stop and remove the containers, run `docker-compose down`.

With that, you should have the application up and running. You can now access the API endpoints. 

##### Note:
- If a database migration is required, you can run the following command:
    ```sh
    docker-compose run api python manage.py migrate
    ```

<br>

#### Running the Django Development Server (with a local PostgreSQL database)
1. Clone the repository:
    ```sh
    git clone https://github.com/EAdibi/SWE-Project-3-Backend.git
    cd SWE-Project-3-Backend
    ```
   - Ensure that you have PostgreSQL installed and running on your local machine. Create a new database for the application.

    <br>
   
2. Create and activate a virtual environment:
    ```sh
    python -m venv .venv # MacOS: python3 -m venv .venv
    .venv\Scripts\activate  # MacOS: `source .venv/bin/activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt #MacOS: pip3 install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    # Edit the .env file to include your database connection string and other settings
    ```

5. Apply database migrations (when applicable):
    ```sh
    python manage.py migrate # MacOS: python3 manage.py migrate
    ```

6. Run the development server:
    ```sh
    python manage.py runserver # MacOS: python3 manage.py runserver
    ```

## Usage

Once the development server is running, you can access the application at `http://127.0.0.1:8000/`. Use the provided API endpoints to manage users, flashcards and lessons.

## Testing

To run the tests, use the following command:
```sh
python manage.py test
```