from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from src.frameworks.parametric_api import api as parametric_api


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1, x_prefix=1)
CORS(app)

description = open("description.md")


api = Api(
    app, version="1.0.1", title="ALeRCE Forecast API", description=description.read()
)
api.add_namespace(parametric_api, path="/parametric")


if __name__ == "__main__":
    app.run(debug=True)
