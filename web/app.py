from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS

from .modules.parametric import api as parametric_api

app = Flask(__name__)
CORS(app)

description = open("description.md")
api = Api(app,
        version = "1.0",
        title = "ALeRCE Supernova Forecast API",
        description = description.read())
api.add_namespace(parametric_api, path="/parametric")


if __name__ == '__main__':
    app.run(debug=True)
