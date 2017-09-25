# coding:utf-8
import os

DB_API_HOST = os.environ['RESULT_API_HOST']
CELERY_REST_SCHEDULER_TASKS_API_HOST = os.environ['CELERY_REST_SCHEDULER_TASKS_API_HOST']
CELERY_REST_SCHEDULER_TASK = 'tasks.report'

broker_url = os.environ['BROKER_URL']
