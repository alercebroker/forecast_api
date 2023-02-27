from fastapi import APIRouter
from src.adapters.controller import controller_parametric_response
from src.frameworks.input_model import parametric_parser
from src.frameworks.response_model import parametric_response

router = APIRouter()


@router.get(
    "/sn",
    response_model=parametric_response,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found"},
        400: {"description": "Bad Request"},
    },
)
def get_parametric_forecast(params: parametric_parser):
    return controller_parametric_response(params)
