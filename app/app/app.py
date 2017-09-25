# coding:utf-8
import json

from flask import Flask
from flask import make_response
from flask_restful import Api
from resources import WorkerTask, ReporterTask
from bson import ObjectId

app = Flask(__name__)
api = Api(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@api.representation('application/json')
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data, cls=JSONEncoder), code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(WorkerTask, '/api/v1/worker_task/<string:task_id>', endpoint='worker_task_resource',
                 strict_slashes=False)
api.add_resource(WorkerTask, '/api/v1/worker_task/', endpoint='worker_task_list_resource', strict_slashes=False)

api.add_resource(ReporterTask, '/api/v1/reporter_task/<string:task_id>', endpoint='reporter_task_resource',
                 strict_slashes=False)
api.add_resource(ReporterTask, '/api/v1/reporter_task/', endpoint='reporter_task_list_resource', strict_slashes=False)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
