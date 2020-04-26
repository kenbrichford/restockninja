web: gunicorn restockninja.wsgi --log-file -
worker: celery -A restockninja worker --log-file -
beat: celery -A restockninja beat --log-file -