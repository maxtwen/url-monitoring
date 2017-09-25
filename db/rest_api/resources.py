# coding:utf-8

from flask_restful import Resource, reqparse
from models import UrlPages


class LatestUrlPage(Resource):

    @property
    def query_string_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, location='args')
        return parser

    def get(self):
        args = self.query_string_parser.parse_args()
        obj = UrlPages.objects(**args).order_by('-datetime').first()
        if not obj:
            return '', 404
        return obj.to_mongo()


class UrlPage(Resource):
    @property
    def body_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True, type=str)
        parser.add_argument('page', required=True, type=str)
        parser.add_argument('datetime', required=True, type=str)
        return parser

    def post(self):
        args = self.body_parser.parse_args()
        UrlPages(**args).save()
        return '', 204
