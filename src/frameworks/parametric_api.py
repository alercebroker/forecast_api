from flask_restx import Namespace, Resource
from src.adapters.controller import controller_parametric_response
from src.frameworks.input_model import parametric_parser
from src.frameworks.response_model import parametric_response, forecast_model

api = Namespace("parametric", description="Parametric Forecasts Module")
api.models[parametric_response.name] = parametric_response
api.models[forecast_model.name] = forecast_model


@api.route("/sn")
@api.response(200, "Success")
@api.response(404, "Not found")
@api.response(400, "Bad Request")
class SNParametricForecast(Resource):
    @api.marshal_with(parametric_response)
    @api.expect(parametric_parser)
    def get(self):
        return controller_parametric_response(parametric_parser)
