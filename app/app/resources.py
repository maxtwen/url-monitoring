# coding:utf-8

from flask_restful import Resource, reqparse
from models import WorkerTasksModel, ReporterTasksModel, Params


class Task(Resource):

    MODEL = None

    @staticmethod
    def filter_none_value_args(args):
        return {k: v for k, v in args.items() if v is not None}

    @staticmethod
    def process_url(url):
        return url.replace("www.", "").replace("http://", "")

    @property
    def get_request_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('is_active', type=bool, required=False)
        return parser

    def get(self, task_id=None):
        args = self.filter_none_value_args(self.get_request_params.parse_args())
        if task_id:
            obj = self.MODEL.objects(pk=task_id).get()
            return obj.to_mongo()
        else:
            queryset = self.MODEL.objects(**args)
            return list(queryset.as_pymongo())

    @property
    def post_request_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('interval', type=int, required=True)
        parser.add_argument('url', type=str, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        return parser

    def post(self):
        args = self.post_request_params.parse_args()
        is_active = args.pop('is_active')
        args['url'] = self.process_url(args['url'])
        self.MODEL.objects(params=Params(**args)).update_one(is_active=is_active, upsert=True)
        return '', 204

    @property
    def patch_request_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('interval', type=int)
        parser.add_argument('url', type=str)
        parser.add_argument('is_active', type=bool)
        return parser

    def patch(self, task_id):
        args = self.filter_none_value_args(self.patch_request_params.parse_args())
        if self.MODEL.objects(id=task_id).update_one() is 0:
            return '', 404
        return '', 204


class WorkerTask(Task):
    MODEL = WorkerTasksModel


class ReporterTask(Task):
    MODEL = ReporterTasksModel
