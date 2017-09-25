# coding:utf-8

from mongoengine import DynamicDocument, StringField, DateTimeField
from mongoengine import connect
import os
connect('app', host=os.environ['MONGO_HOST'])


class UrlPages(DynamicDocument):
    url = StringField()
    page = StringField()
    datetime = DateTimeField()
