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
  - Django REST framework SimpleJWT
- Database
  - Undecided
- CI/CD
  - Containerization with Docker
  - Continuous Integration with GitHub Actions
  - Continuous Deployment to Google Cloud Run with the Google Cloud CLI
- Deployment
  - Google Cloud Run

## Setup Instructions

### Prerequisites

- Python 3.8 or higher

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/EAdibi/SWE-Project-3-Backend.git
    cd SWE-Project-3-Backend
    ```

2. Create a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    # Edit the .env file to include your database connection string and other settings
    ```

5. Apply database migrations (when applicable):
    ```sh
    python manage.py migrate
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

Once the development server is running, you can access the application at `http://127.0.0.1:8000/`. Use the provided API endpoints to manage flashcards and decks.

## Testing

To run the tests, use the following command:
```sh
python manage.py test
```