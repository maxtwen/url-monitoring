# coding:utf-8
import json
import logging
import urllib.parse
from datetime import datetime

from celery import Celery
import requests
from celery import current_app
logger = logging.getLogger(__name__)
app = Celery('tasks')
app.config_from_object('celeryconfig')


DB_API_HOST = urllib.parse.urljoin(current_app.conf.DB_API_HOST, '/api/v1/latest_url_page/')


@app.task
def report(url):
    page = json.loads(requests.get('http://{}?url={}'.format(DB_API_HOST, url)).content)
    logger.info((page['url'], page['page']))

