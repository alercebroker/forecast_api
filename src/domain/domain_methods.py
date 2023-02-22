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


def fit_parameters(oid, client, extractor):
    detections = client.query_detections(oid, format="pandas")
    detections["oid"] = oid
    detections.set_index("oid", inplace=True)
    params = extractor.compute_features(detections)
    return params


def rename_and_get_fit(params):
    fids = [int(i.rsplit("_", 1)[1]) for i in params.index]
    params.index = [i.rsplit("_", 1)[0] for i in params.index]
    return fids


def params_to_dataframe(params, fids):
    params = params.to_frame()
    params.reset_index(inplace=True)
    # Setting new column names
    params.columns = ["name", "value"]

    # Adding fid
    params["fid"] = fids
    return params


def get_parameters(oid, client, extractor):
    features = client.query_features(oid, format="pandas")
    if len(features) > 0:
        params = features[features.name.isin(MODEL_PARAMS)]
        return True, params
    else:
        # Fitting model and getting params
        params = fit_parameters(oid, client, extractor).iloc[0]

        # Renaming index and getting fid
        fids = rename_and_get_fit(params)

        # Transforming to dataframe and resetting index
        params = params_to_dataframe(params, fids)

        return False, params


def infer(params, mjd):
    model = SNModel()
    print("#" * 10)
    print(f"el mjd es:\n{mjd}")
    print("#" * 10)
    print("#" * 10)
    print(f"los params son:\n{params}")
    print("#" * 10)

    flux_forecast = model.model_inference(
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


def get_features_message(features_on_db: bool):
    message = "Forecast based on modified Villar et al. 2019. analytic model"
    message += " (see [https://arxiv.org/abs/1905.07422] and [https://arxiv.org/abs/2008.03311]). "
    if features_on_db:
        message += "Using precomputed ALeRCE [http://alerce.science] parameters."
    else:
        message += (
            "On-demand parameters computed in ALeRCE [http://alerce.science] API."
        )
        message += " Warning: This forecast was made with few points."
