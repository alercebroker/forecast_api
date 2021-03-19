from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS

from .modules.parametric import api as parametric_api

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_namespace(parametric_api, path="/parametric")


if __name__ == '__main__':
    app.run(debug=True)
