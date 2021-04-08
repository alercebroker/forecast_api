import datetime
import numpy as np

from flask_restx import Namespace, Resource, abort
from numba import jit
from astropy.time import Time
from alerce.core import Alerce
from alerce.exceptions import ObjectNotFoundError
from lc_classifier.features.extractors import SNParametricModelExtractor

from .models import parametric_response, forecast_model
from .parsers import parametric_parser


api = Namespace("parametric", description="Parametric Forecasts Module")
api.models[parametric_response.name] = parametric_response
api.models[forecast_model.name] = forecast_model

MODEL_PARAMS = [
    'SPM_t0',
    'SPM_chi',
    'SPM_gamma',
    'SPM_beta',
    'SPM_A',
    'SPM_tau_rise',
    'SPM_tau_fall'
]

def flux_to_mag(flux):
    return 16.4 - 2.5 * np.log10(flux)

@jit(nopython=True)
def model_inference(times, A, t0, gamma, f, t_rise, t_fall):
    # f in this function is SPM_beta
    beta = 1.0 / 3.0
    t1 = t0 + gamma

    sigmoid = 1.0 / (1.0 + np.exp(-beta * (times - t1)))
    den = 1 + np.exp(-(times - t0) / t_rise)
    flux = (A * (1 - f) * np.exp(-(times - t1) / t_fall) / den
            * sigmoid
            + A * (1. - f * (times - t0) / gamma) / den
            * (1 - sigmoid))
    return flux

@api.route('/sn')
@api.response(200, "Success")
@api.response(404, "Not found")
@api.response(400, "Bad Request")
class SNParametricForecast(Resource):
    """
        Supernova Parametric Model.
    """
    client = Alerce()
    extractor = SNParametricModelExtractor()

    def check_object(self, oid):
        try:
            object = self.client.query_object(oid, format="pandas")
            object = object.iloc[0]
            return object
        except ObjectNotFoundError as e:
            return abort(404,'Not Found', errors='Object ID not found in ALeRCE database')

    def mjd_now(self):
        now_datetime = datetime.datetime.utcnow()
        astro_time = Time(now_datetime)
        return astro_time.mjd

    def shift_mjd(self,mjd,days=0):
        mjd += days
        return mjd

    def fit_parameters(self, oid):
        detections = self.client.query_detections(oid,format="pandas")
        detections["oid"] = oid
        detections.set_index("oid",inplace=True)
        params = self.extractor.compute_features(detections)
        return params

    def clean_response(self, values):
        new_values = []
        for value in values:
            if np.isnan(value):
                new_values.append(value)
            else:
                new_values.append(value)
        return new_values

    def get_parameters(self, oid):
        try:
            features = self.client.query_features(oid, format="pandas")
            if len(features) == 0:
                raise Exception("Features not found, fitting model")
            params = features[features.name.isin(MODEL_PARAMS)]
            return True, params
        except Exception as e:
            #TODO: Calculate features on demand
            # Fitting model and getting params
            params = self.fit_parameters(oid).iloc[0]

            # Renaming index and getting fid
            fids = [int(i.rsplit("_",1)[1]) for i in params.index]
            params.index = [i.rsplit("_",1)[0] for i in params.index]

            # Transforming to dataframe and resetting index
            params = params.to_frame()
            params.reset_index(inplace = True)
            # Setting new column names
            params.columns = ["name", "value"]

            # Adding fid
            params["fid"] = fids
            return False, params

    def infer(self, params, mjd):
        flux_forecast = model_inference(
                mjd,
                params.SPM_A,
                params.SPM_t0,
                params.SPM_gamma,
                params.SPM_beta,
                params.SPM_tau_rise,
                params.SPM_tau_fall
            )
        magnitude_forecast = flux_to_mag(flux_forecast)
        return magnitude_forecast

    @api.marshal_with(parametric_response)
    @api.expect(parametric_parser)
    def get(self):
        args = parametric_parser.parse_args()
        object = self.check_object(args.oid)
        min_mjd = object["firstmjd"]
        if not args.mjd:
            forecast_mjd = np.array([self.mjd_now()])
        else:
            forecast_mjd = np.array(args.mjd)
        shifted_mjd = forecast_mjd - min_mjd
        features_on_db, parameters = self.get_parameters(args.oid)
        print(features_on_db,parameters)
        message = "Forecast based on modified Villar et al. 2019. analytic model (see [https://arxiv.org/abs/1905.07422] and [https://arxiv.org/abs/2008.03311]). "
        if features_on_db:
            message += "Using precomputed ALeRCE [http://alerce.science] parameters."
        else:
            message += "On-demand parameters computed in ALeRCE [http://alerce.science] API. Warning: This forecast was made with few points."

        forecasts = []
        for fid in parameters.fid.unique():
            fid_params = parameters[parameters.fid == fid]
            fid_params.set_index("name", inplace=True)
            fid_params = fid_params.value
            magpsf = self.infer(fid_params, shifted_mjd)
            forecasts.append({
                'magpsf': self.clean_response(magpsf),
                'mjd': forecast_mjd,
                'fid': fid,
            })

        return {
                'oid': args.oid,
                "forecast": forecasts,
                "comment": message
            }
