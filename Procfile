release: python manage.py migrate
web: gunicorn crypto_ledger.wsgi
beat: celery -A crypto_ledger beat -l INFO
worker: celery -A crypto_ledger worker -l INFO