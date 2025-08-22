from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from random import choice
from time import time
from serviceDemo.demo import microServiceDemo
from contextlib import asynccontextmanager
import pyfiglet
import boto3
import os

bucket_name = "bucket-practice-rayco"
s3_folder = "ml_models"
local_download = "."

@asynccontextmanager
async def lifespan(app: FastAPI):
    ascii_art = pyfiglet.figlet_format("WELCOME TO RAYCO'S CABAL")
    print(ascii_art)

    print("Starting app... downloading models from S3")
    s3 = boto3.client("s3")
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder)
    for obj in objects.get("Contents", []):
        s3_key = obj["Key"]
        local_path = os.path.join(local_download, os.path.relpath(s3_key, s3_folder))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading {s3_key} to {local_path}")
        s3.download_file(bucket_name, s3_key, local_path)

    yield

    print("Shutting down app... cleanup here if needed")
    ascii_art = pyfiglet.figlet_format("BYE, SEE YOU NEXT TIME!")
    print(ascii_art)



app = FastAPI(version="0.0.0.1", description="this is just a sample app i am testing", lifespan=lifespan)
app.include_router(microServiceDemo)
@app.middleware("http")
async def userAgent(req: Request, call_next):
    if req.headers.get("jwt") == "1234":
        response = await call_next(req)
        return response
    else:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "response": "Sorry we couldn't verify your identity"}
        )

@app.middleware("http")
async def timeCalculator(req: Request, call_next):
    startTime = time()
    response: Response = await call_next(req)
    endTime = time()
    process_time = endTime - startTime
    response.headers["X-Process-Time"] = str(process_time)  # Add custom header
    return response

class responseModel(BaseModel):
    status: str
    response: str

class requestModel(BaseModel):
    query: str

@app.post("/poster", response_model=responseModel, status_code=200)
def posterHander(payLoad: requestModel):
    greetings = [
        f"Hello, Mr {payLoad.query}. It's nice to meet you!",  
        f"Hi there, Mr {payLoad.query}! Great to meet you.",
        f"Good day, Mr {payLoad.query}! Pleasure to meet you.",
        f"Hey, Mr {payLoad.query}! How's it going?",
        f"Greetings, Mr {payLoad.query}! Nice to see you.",
        f"Hello, Mr {payLoad.query}! I've been looking forward to meeting you.",
        f"Hi, Mr {payLoad.query}! Hope you're doing well.",
        f"Salutations, Mr {payLoad.query}! Nice to make your acquaintance.",
        f"Hey there, Mr {payLoad.query}! Pleasure to meet you.",
        f"Good to see you, Mr {payLoad.query}! How are you!"
    ]
    greet = choice(greetings)
    return {"status": "success", "response": greet}

@app.get("/{item}")
def homeRoute(item: str):
    return {"status": "this app is ready to go!", "number": item}