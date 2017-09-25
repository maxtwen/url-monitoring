import json
import urllib.parse

import celery.schedules
import datetime

import requests
from celery.beat import Scheduler, ScheduleEntry
from celery import current_app

if hasattr(current_app.conf, "CELERY_REST_SCHEDULER_TASK"):
    TASK = current_app.conf.CELERY_REST_SCHEDULER_TASK
else:
    raise Exception('CELERY_REST_SCHEDULER_TASK does not exists')


class RestApiSchedulerEntry(ScheduleEntry):

    def __init__(self, task):
        self._task = task
        self.app = current_app._get_current_object()
        self.name = self._task['name']
        self.task = TASK
        self.is_active = self._task['is_active']

        self.schedule = celery.schedules.schedule(datetime.timedelta(seconds=self._task['params']['interval']))
        self.options = {}
        self.args = (self._task['params']['url'],)
        self.total_run_count = self._task['total_run_count']
        self.last_run_at = self._task['last_run_at']

    def _default_now(self):
        return self.app.now()

    def next(self):
        self._task['last_run_at'] = self.app.now()
        self._task['total_run_count'] += 1
        self._task['is_active'] = self.is_active
        self._task['run_immediately'] = False
        return self.__class__(self._task)

    __next__ = next

    def is_due(self):
        if not self.is_active:
            return False, 1.0
        return self.schedule.is_due(self.last_run_at)


class RestApiScheduler(Scheduler):

    #: how often should we sync in schedule information
    UPDATE_INTERVAL = datetime.timedelta(seconds=5)

    Entry = RestApiSchedulerEntry

    def __init__(self, *args, **kwargs):
        if hasattr(current_app.conf, "CELERY_REST_SCHEDULER_TASKS_API_HOST"):
            self.api_url = urllib.parse.urljoin(current_app.conf.CELERY_REST_SCHEDULER_TASKS_API_HOST,
                                                '/api/v1/reporter_task/')
        else:
            raise Exception('CELERY_REST_SCHEDULER_API_HOST does not exists')
        self._schedule = {}
        self._last_updated = None
        Scheduler.__init__(self, *args, **kwargs)
        self.max_interval = (kwargs.get('max_interval')
                             or self.app.conf.CELERYBEAT_MAX_LOOP_INTERVAL or 5)

    def setup_schedule(self):
        pass

    def requires_update(self):
        """check whether we should pull an updated schedule
        from the backend database"""
        if not self._last_updated:
            return True
        return self._last_updated + self.UPDATE_INTERVAL < datetime.datetime.now()

    def get_tasks(self):
        tasks = json.loads(requests.get(self.api_url).content)
        d = {}
        for task in tasks:
            task_name = (task['params']['url'], task['params']['interval'])
            if task_name in self._schedule:
                _task = self._schedule.pop(task_name)
                task['last_run_at'] = _task.last_run_at
                task['total_run_count'] = _task.total_run_count
            else:
                task['last_run_at'] = self._default_now()
                task['total_run_count'] = 0
            task['name'] = task_name
            d[task_name] = self.Entry(task)
        return d

    @property
    def schedule(self):
        if self.requires_update():
            self._schedule = self.get_tasks()
            self._last_updated = datetime.datetime.now()
        return self._schedule

    def sync(self):
        pass

    def _default_now(self):
        return self.app.now()

    def reserve(self, entry):
        prev_entry = self.schedule[entry.name]
        new_entry = self.schedule[entry.name] = next(entry)
        new_entry.is_active = prev_entry.is_active
        return new_entry
