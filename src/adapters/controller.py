from src.use_cases.get_parametric_response import get
from src.domain.domain_methods import check_object, mjd_now
from src.adapters.presenter import parse_to_json
from flask_restx import Namespace
import numpy as np

from lc_classifier.features.extractors import SNParametricModelExtractor
from alerce.core import Alerce


client = Alerce()
extractor = SNParametricModelExtractor(bands=[1, 2])

# comentario


def controller_parametric_response(parametric_parser):
    args = parametric_parser.parse_args()
    object = check_object(args.oid, client)
    min_mjd = object["firstmjd"]
    if not args.mjd:
        forecast_mjd = np.array([mjd_now()])
    else:
        forecast_mjd = np.array(args.mjd)
    shifted_mjd = forecast_mjd - min_mjd

    parametric_response = get(args.oid, forecast_mjd, shifted_mjd, client, extractor)

    return parse_to_json(parametric_response)
