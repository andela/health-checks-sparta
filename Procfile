release: python manage.py makemigrations accounts api front payments && python manage.py migrate
web: gunicorn hc.wsgi:application
