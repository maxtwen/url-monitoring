# coding:utf-8
import os

RESULT_API_HOST = os.environ['RESULT_API_HOST']
CELERY_REST_SCHEDULER_TASKS_API_HOST = os.environ['CELERY_REST_SCHEDULER_TASKS_API_HOST']
CELERY_REST_SCHEDULER_TASK = 'tasks.get_url_page'

broker_url = os.environ['BROKER_URL']
