from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

from pydantic import BaseModel

DEFAULT_THRESHOLDS = {
    "gpu_util": 80,
    "memory_util": 90,
    "power_draw": 1000,
    "temp": 100,
    "interval_time": 5
}
current_thresholds = DEFAULT_THRESHOLDS.copy()

class ThresholdRequest(BaseModel):
    gpu_util: float | None = None
    memory_util: float | None = None
    power_draw: float | None = None
    temp: float | None = None
    interval_time: float | None = None


@app.get("/sample_API")
async def sample_API():
    return {"message":"Called the Sample API....."}


@app.post("/set_thresholds")
async def set_thresholds(data: ThresholdRequest):
    updated = {}
    for key, val in data.dict(exclude_unset=True).items():
        current_thresholds[key] = float(val)
        updated[key] = current_thresholds[key]
    return {"message": "Thresholds updated", "thresholds": updated}


@app.get("/check_setting_values")
async def check_metrics():
    mock_metrics = {"gpu_util":82,"memory_util":88,"power_draw":310,"temp":81}
    status = {k:("OK" if mock_metrics[k] <= current_thresholds[k] else "HIGH")
              for k in mock_metrics}
    return {"metrics": mock_metrics, "thresholds": current_thresholds, "status": status}


@app.post("/reset_thresholds")
async def reset_thresholds():
    global current_thresholds
    current_thresholds = DEFAULT_THRESHOLDS.copy()
    return {"message": "Thresholds reset to default", "thresholds": current_thresholds}



if __name__ == "__main__":
   uvicorn.run("app:app", host="127.0.0.1", port=2000, reload=True)