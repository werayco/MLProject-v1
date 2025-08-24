from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modelLoad import second_workflow

microServiceDemo = APIRouter(prefix="/api/v1")

class requestModel(BaseModel):
    x: int
    y: int

class requestModelV2(BaseModel):
    query: str

@microServiceDemo.get("/")
async def main():
    return {"status": "successful", "response": "this microservice is working"}

@microServiceDemo.post("/model")
async def sample(request: Request, body: requestModelV2):
    payload = body.dict()
    if "query" in payload: 
        query: str = payload.get("query", "")
        
        modelResponse: str = second_workflow(
            text=query, 
            vectorizer=request.app.state.vectorizer, 
            model=request.app.state.model, 
            encoder=request.app.state.encoder
        )[0]

        return JSONResponse(
            {"status": "successful", "response": f"Your email is: {modelResponse}. Thanks for stopping by"},
            status_code=200
        )
    
    return JSONResponse(
        {"status": "failed", "response": "WRONG PAYLOAD! 'query' is required and must be a string."},
        status_code=400
    )

@microServiceDemo.post("/upload")
async def mlModel(body: requestModel):
    payload = body.dict()
    if "x" in payload and "y" in payload:
        x: int = payload.get("x", 0)
        y: int = payload.get("y", 0)
        return JSONResponse(
            {"status": "successful", "response": f"Your Answer is: {x + y}. Thanks for stopping by"},
            status_code=200
        )
    
    return JSONResponse(
        {"status": "failed", "response": "WRONG PAYLOAD! x and y are required and must be integers."},
        status_code=400
    )
