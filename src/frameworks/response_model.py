from pydantic import BaseModel
from fastapi import Query
from typing import List


class ForecastModel(BaseModel):
    magpsf: List[float] = Query(description="Forecast Apparent Magnitude")
    mjd: List[float] = Query(description="MJD associated to forecast")
    fid: int = Query(description="Filter ID (1=g; 2=r; 3=i)")


class ParametricResponse(BaseModel):
    oid: str = Query(description="Object identifier")
    forecast: List[ForecastModel]
    comment: str = Query(description="Metadata from forecast")
