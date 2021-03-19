import pytest
from web.app import app

forecast_route = "/parametric/sn"

@pytest.fixture
def tester():
    with app.test_client() as tester:
        yield tester

def test_index(tester):
    response = tester.get("/", content_type = "html/text")

    assert "swagger" in response.data.decode("utf-8").lower()
    assert response.status_code == 200

def test_parameters(tester):
    param_list = [
        ({},400),
        ({
            "oid": "test",
            "days": "three"
        }, 400),
        ({
            "oid": "ZTF18aavrmcg",
            "days": "3"
        }, 200),
        ({
            "oid": "ZTF18aavrmcg"
        }, 200),
        ({
            "oid": "ZTF18aavrmcg",
            "days": 3
        }, 200),
    ]

    for param, code in param_list:
        response = tester.get(forecast_route,
                        content_type = "html/text",
                        query_string=param)
        assert response.status_code == code

def test_not_found(tester):
    params = {
        "oid": "not_in_db"
    }
    response = tester.get(forecast_route,
                        content_type= "html/text",
                        query_string=params)
    assert response.status_code == 404

def test_already_on_db():
    pass

def test_fit_parameters(tester):
    params = {
        "oid" : "ZTF21aaqfrxz"
    }
    response = tester.get(forecast_route,
                        content_type= "html/text",
                        query_string=params)
    assert response.status_code == 200
    print(response.data)
    raise

def test_fit_error():
    pass
