Getting started
====================

1. Setup virtual environment::
   
      virtualenv venv
      source venv/bin/activate

2. Setup requirements::

      pip install -r requirements.txt

3. Sync database::

      python manage.py migrate

4. Add user::
   
      python manage.py createsuperuser

5. Run webserver::

      python manage.py runserver

Starting the web server
-------------------------

1. Run webserver::

      python manage.py runserver

2. Enter the front page at `http://localhost:8000/static/index.html <http://localhost:8000/static/index.html>`_


Configure Facebook login
-----------------------------

1. Enter Django administration page at `http://localhost:8000/admin/ <http://localhost:8000/admin/>`_
2. Click *Sites* then fix the first site name from ``example.com`` to ``localhost:8000``
3. Go back to front page and click *Social applications*
4. Add new social application. Enter the following information:

   * Name: Facebook
   * Client ID, Secret Key: As given by Facebook (`Register a new Facebook application <https://developers.facebook.com/apps/>`_)
   * Sites: Add ``localhost:8000`` to the list