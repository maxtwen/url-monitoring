# coding:utf-8
import urllib.parse
from datetime import datetime

from celery import Celery
import requests
from celery import current_app

app = Celery('tasks')
app.config_from_object('celeryconfig')


RESULT_API_URL = urllib.parse.urljoin(current_app.conf.RESULT_API_HOST, '/api/v1/url_page/')
TASKS_API_URL = urllib.parse.urljoin(current_app.conf.CELERY_REST_SCHEDULER_TASKS_API_HOST, '/api/v1/worker_task/')


@app.task
def get_url_page(url):
    page = requests.get('http://{}'.format(url)).text
    requests.post(RESULT_API_URL, data=dict(
        url=url,
        page=page,
        datetime=datetime.utcnow().isoformat()
    ))
