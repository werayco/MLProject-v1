from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from http import HTTPStatus
microServiceDemo = APIRouter(prefix="/api/v1",)

class requestModel(BaseModel):
    x: int
    y: int

@microServiceDemo.get("/")
async def main():
    return {"status": "successful", "response":"this microservice is working"}

@microServiceDemo.post("/upload")
async def sample(request: requestModel):
    payload = request.dict()
    if isinstance(payload,dict):
        if "x" or "y" in payload: 
            x: int = payload.get("x", 0)
            y: int = payload.get("y", 0)
            return JSONResponse({"status": "successful", "response":f"Your Answer is: {x + y}. Thanks for stopping by"}, status_code=200)
        else:
            return JSONResponse({"status": "failed", "response":"WRONG PAYLOAD! x and y are the required payload--Both having a datatype of 'int',"}, status_code=400)
    return {"status": "failed", "response":"this microservice is working"}