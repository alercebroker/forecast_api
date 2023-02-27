from src.use_cases.get_parametric_response import get
from src.domain.domain_methods import check_object, mjd_now
import numpy as np

from lc_classifier.features.extractors import SNParametricModelExtractor
from alerce.core import Alerce


client = Alerce()
extractor = SNParametricModelExtractor(bands=[1, 2])


def controller_parametric_response(params):

    object = check_object(params.oid, client)
    min_mjd = object["firstmjd"]

    forecast_mjd = params.mjd

    if forecast_mjd is None:
        forecast_mjd = np.array([mjd_now()])

    shifted_mjd = forecast_mjd - min_mjd
    parametric_response = get(params.oid, forecast_mjd, shifted_mjd, client, extractor)

    return parametric_response
