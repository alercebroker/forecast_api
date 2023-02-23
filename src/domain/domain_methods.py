from astropy.time import Time
import datetime
from alerce.exceptions import ObjectNotFoundError
from flask_restx import abort
from src.domain.SN_model import SNModel, MODEL_PARAMS


def check_object(oid, client):
    try:
        object = client.query_object(oid, format="pandas")
        object = object.iloc[0]
        return object
    except ObjectNotFoundError:
        return abort(404, "Not Found", errors="Object ID not found in ALeRCE database")


def mjd_now():
    now_datetime = datetime.datetime.utcnow()
    astro_time = Time(now_datetime)
    return astro_time.mjd


def infer(params, mjd):
    model = SNModel()

    flux_forecast = model.model_inference_jit(
        mjd,
        params.SPM_A,
        params.SPM_t0,
        params.SPM_gamma,
        params.SPM_beta,
        params.SPM_tau_rise,
        params.SPM_tau_fall,
    )
    magnitude_forecast = model.flux_to_mag(flux_forecast)
    return magnitude_forecast
