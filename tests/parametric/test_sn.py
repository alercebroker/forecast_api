import pytest
from src.frameworks.flask import app

import pandas as pd
from alerce.exceptions import ObjectNotFoundError

forecast_route = "/parametric/sn"


@pytest.fixture
def tester():
    with app.test_client() as tester:
        yield tester


def test_index(tester):
    print("un test bueno\n")
    response = tester.get("/", content_type="html/text")
    assert "swagger" in response.data.decode("utf-8").lower()
    assert response.status_code == 200


def test_not_found(tester, mocker):
    print("segundo test bueno\n")
    params = {"oid": "not_in_db"}

    mocker.patch("alerce.core.Alerce.query_object", side_effect=ObjectNotFoundError())

    response = tester.get(forecast_route, content_type="html/text", query_string=params)
    assert response.status_code == 404


def test_already_on_db(tester, mocker):
    params = {"oid": "ZTF21aaqfrxz"}

    mocker.patch(
        "src.adapters.controller.check_object",
        return_value={"firstmjd": 58000},
    )
    mocker.patch(
        "src.use_cases.get_parametric_response.get_parameters",
        return_value=(
            True,
            pd.DataFrame(
                [
                    {"name": "SPM_A", "fid": 1, "value": 2},
                    {"name": "SPM_tau_rise", "fid": 1, "value": 2},
                    {"name": "SPM_tau_fall", "fid": 1, "value": 2},
                    {"name": "SPM_t0", "fid": 1, "value": 2},
                    {"name": "SPM_beta", "fid": 1, "value": 2},
                    {"name": "SPM_gamma", "fid": 1, "value": 2},
                ]
            ),
        ),
    )

    print("tercer tests problemas\n")
    response = tester.get(forecast_route, content_type="html/text", query_string=params)
    print(response.status_code)
    assert response.status_code == 200
    assert "precomputed" in response.data.decode("utf-8").lower()


def test_fit_parameters(tester, mocker):
    params = {"oid": "ZTF21aaqfrxz"}

    mocker.patch(
        "src.adapters.controller.check_object",
        return_value={"firstmjd": 58000},
    )
    mocker.patch(
        "src.use_cases.get_parametric_response.get_parameters",
        return_value=(
            False,
            pd.DataFrame(
                [
                    {"name": "SPM_A", "fid": 1, "value": 2},
                    {"name": "SPM_tau_rise", "fid": 1, "value": 2},
                    {"name": "SPM_tau_fall", "fid": 1, "value": 2},
                    {"name": "SPM_t0", "fid": 1, "value": 2},
                    {"name": "SPM_beta", "fid": 1, "value": 2},
                    {"name": "SPM_gamma", "fid": 1, "value": 2},
                ]
            ),
        ),
    )

    print("cuarto test problemas\n")
    response = tester.get(forecast_route, content_type="html/text", query_string=params)
    assert response.status_code == 200
    assert "demand" in response.data.decode("utf-8").lower()
