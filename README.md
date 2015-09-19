# Youniversity

## Setup

1. Setup virtual environment: `virtualenv venv; source venv/bin/activate`
2. Setup requirements: `pip install -r requirements.txt`
3. Sync database: `python manage.py migrate`

## Development

- Run webserver: `python manage.py runserver`
- Enter the front page at http://localhost:8000/static/index.html