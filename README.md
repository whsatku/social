# Youniversity

## Setup

1. Setup virtual environment: `virtualenv venv; source venv/bin/activate`
2. Setup requirements: `pip install -r requirements.txt`
3. Sync database: `python manage.py migrate`
4. Add user: `python manage.py createsuperuser`
5. Run webserver: `python manage.py runserver`
6. Visit the admin page at `http://localhost:8000/admin/`
7. Fix the first site name from example.com to localhost:8000
8. Add a new social app, using your Facebook app ID and secret

## Development

- Run webserver: `python manage.py runserver`
- Enter the front page at http://localhost:8000/static/index.html