# FlashDeck Backend

FlashDeck is a spaced-repetition flashcard application built with Django REST Framework. Users can create private study decks, manage flashcards, review due cards, and track study statistics.

## Features

- JWT authentication
- User-owned decks and flashcards
- Deck and card CRUD operations
- Search, filtering, ordering, and pagination
- Five-box spaced-repetition scheduling
- Due-card study endpoint
- Study statistics
- Admin interface

## Technology Stack

- Python 3.10+
- Django
- Django REST Framework
- Simple JWT
- django-cors-headers
- django-filter
- SQLite
- python-decouple

## Backend Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-NAME-flashdeck-backend.git
cd YOUR-NAME-flashdeck-backend
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and set your local values. Do not commit `.env`.

Example `.env`:

```env
SECRET_KEY=replace-with-a-local-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Run migrations

```powershell
python manage.py migrate
```

### 6. Create an administrator (optional)

```powershell
python manage.py createsuperuser
```

### 7. Start the server

```powershell
python manage.py runserver
```

The development API is available at `http://127.0.0.1:8000/`.

## Environment Variables

| Variable          | Purpose                            |
| ----------------- | ---------------------------------- |
| `SECRET_KEY`    | Django secret key                  |
| `DEBUG`         | Enables/disables Django debug mode |
| `ALLOWED_HOSTS` | Comma-separated allowed host names |

## Spaced-Repetition Intervals

| Box | Next review after a correct answer |
| --- | ---------------------------------- |
| 1   | 0 days                             |
| 2   | 1 day                              |
| 3   | 3 days                             |
| 4   | 7 days                             |
| 5   | 16 days                            |

Incorrect answers return a card to Box 1 and make it due immediately. The box is managed by the backend.

## API Endpoints

| Method             | Endpoint                    | Authentication |
| ------------------ | --------------------------- | -------------- |
| POST               | `/api/register/`          | Public         |
| POST               | `/api/token/`             | Public         |
| POST               | `/api/token/refresh/`     | Refresh token  |
| GET, POST          | `/api/decks/`             | Required       |
| GET, PATCH, DELETE | `/api/decks/<id>/`        | Required       |
| GET, POST          | `/api/cards/`             | Required       |
| GET, PATCH, DELETE | `/api/cards/<id>/`        | Required       |
| POST               | `/api/cards/<id>/review/` | Required       |
| GET                | `/api/study/`             | Required       |
| GET                | `/api/stats/`             | Required       |

Authenticated requests use the header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Frontend Repository

[FlashDeck Frontend](https://github.com/YOUR-USERNAME/YOUR-NAME-flashdeck-frontend)

## Security Notes

- User data is scoped to the authenticated owner.
- Card review fields are managed by the backend.
- Keep `.env` and production secrets out of version control.
- Use `DEBUG=False` and configure production settings before deployment.
