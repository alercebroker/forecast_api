from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_restx import Namespace
from src.adapters.controller import controller_parametric_response
from src.frameworks.input_model import parametric_parser
from src.frameworks.response_model import parametric_response, forecast_model


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1, x_prefix=1)
CORS(app)

description = open("description.md")


# Deberia mover parametric_api a su propio archivo
parametric_api = Namespace("parametric", description="Parametric Forecasts Module")
parametric_api.models[parametric_response.name] = parametric_response
parametric_api.models[forecast_model.name] = forecast_model


@parametric_api.route("/sn")
@parametric_api.response(200, "Success")
@parametric_api.response(404, "Not found")
@parametric_api.response(400, "Bad Request")
@parametric_api.marshal_with(parametric_response)
@parametric_api.expect(parametric_parser)
def get_SNParametricForecast():
    return controller_parametric_response(parametric_parser)


api = Api(
    app, version="1.0.1", title="ALeRCE Forecast API", description=description.read()
)
api.add_namespace(parametric_api, path="/parametric")


if __name__ == "__main__":
    app.run(debug=True)
