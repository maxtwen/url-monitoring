# coding:utf-8
import datetime
import json

from flask import Flask
from flask import make_response
from flask_restful import Api
from resources import LatestUrlPage, UrlPage
from bson import ObjectId

app = Flask(__name__)
api = Api(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


@api.representation('application/json')
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data, cls=JSONEncoder), code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(UrlPage, '/api/v1/url_page/', endpoint='url_page_resource',
                 strict_slashes=False)
api.add_resource(LatestUrlPage, '/api/v1/latest_url_page/', endpoint='latest_url_page_list_resource',
                 strict_slashes=False)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
