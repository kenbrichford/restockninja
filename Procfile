web: gunicorn restockninja.wsgi
worker: celery -A restockninja worker
beat: celery -A restockninja beat