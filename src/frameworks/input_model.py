from fastapi import Query
from pydantic.dataclasses import dataclass


@dataclass
class SNInput:
    oid: str = Query(description="ZTF Object ID")
    mjd: float | None = Query(None, description="Modified julian date to next forecast")
