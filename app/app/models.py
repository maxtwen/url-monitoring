# coding:utf-8
import os

from mongoengine import DynamicDocument, BooleanField, StringField, IntField, EmbeddedDocumentField, \
    EmbeddedDocument

from mongoengine import connect

connect('app', host=os.environ['MONGO_HOST'])


class Params(EmbeddedDocument):
    url = StringField()
    interval = IntField()


class Tasks(DynamicDocument):
    meta = {
        'abstract': True,
    }

    status = StringField()
    is_active = BooleanField(default=True)
    params = EmbeddedDocumentField(Params, unique=True)


class WorkerTasksModel(Tasks):
    pass


class ReporterTasksModel(Tasks):
    pass
