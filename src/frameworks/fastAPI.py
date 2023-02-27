from src.frameworks.parametric_api import router
import uvicorn
from fastapi import FastAPI

with open("description.md") as f:
    description = f.read()

app = FastAPI(
    description=description,
    version="1.0.1",
    title="ALeRCE Forecast API",
)

app.include_router(router, prefix="/parametric")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
