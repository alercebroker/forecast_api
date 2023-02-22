from flask_restx import Namespace
from src.adapters.controller import controller_parametric_response
from src.frameworks.input_model import parametric_parser
from src.frameworks.response_model import parametric_response, forecast_model

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
