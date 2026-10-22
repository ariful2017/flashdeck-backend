# **FlashDeck Backend**

A spaced-repetition flashcard application built with Django
and Django REST Framework.

## Tech Stack

- Python
- Django
- Django REST Framework
- JWT authentication
- SQLite
- django-filter

## Local Setup

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create `.env` using `.env.example` as a reference.
4. Run `python manage.py migrate`.
5. Run `python manage.py createsuperuser`.
6. Start the server with `python manage.py runserver`.

## Environment Variables

| Variable      | Purpose                   |
| ------------- | ------------------------- |
| SECRET_KEY    | Django secret key         |
| DEBUG         | Development debug setting |
| ALLOWED_HOSTS | Allowed hostnames         |

## Review Intervals

| Box | Interval after a correct answer |
| --- | ------------------------------- |
| 1   | 0 days                          |
| 2   | 1 day                           |
| 3   | 3 days                          |
| 4   | 7 days                          |
| 5   | 16 days                         |

## Frontend

Frontend repository: Add your frontend GitHub URL here.
