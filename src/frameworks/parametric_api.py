from fastapi import APIRouter, Depends
from src.adapters.controller import controller_parametric_response
from src.frameworks.input_model import SNInput
from src.frameworks.response_model import ParametricResponse

router = APIRouter()


@router.get(
    "/sn",
    response_model=ParametricResponse,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found"},
        400: {"description": "Bad Request"},
    },
)
def get_parametric_forecast(params: SNInput = Depends()):
    return controller_parametric_response(params)
