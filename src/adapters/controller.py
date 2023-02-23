from src.use_cases.get_parametric_response import get
from src.domain.domain_methods import check_object, mjd_now
from src.adapters.presenter import parse_to_json
import numpy as np

from lc_classifier.features.extractors import SNParametricModelExtractor
from alerce.core import Alerce


client = Alerce()
extractor = SNParametricModelExtractor(bands=[1, 2])


def controller_parametric_response(parametric_parser):
    args = parametric_parser.parse_args()
    print("antes del check\n")
    object = check_object(args.oid, client)
    print("despues del check\n")
    min_mjd = object["firstmjd"]
    if not args.mjd:
        forecast_mjd = np.array([mjd_now()])
    else:
        forecast_mjd = np.array(args.mjd)
    shifted_mjd = forecast_mjd - min_mjd

    parametric_response = get(args.oid, forecast_mjd, shifted_mjd, client, extractor)

    print("TY" * 10)
    print(parametric_response)
    print("TY" * 10)
    print("\n")

    return parse_to_json(parametric_response)
