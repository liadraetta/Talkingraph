from fastapi import FastAPI
import requests
from routers.routers import router #dare un nome specifico anhe al file
from pydantic import BaseModel, Field


app = FastAPI(
    title= "API FastAPI wlkg",
    description="API FastAPI wlkg",
    version="0.1",
    openapi_tags=[
        {  
            "name": "wlkg",
        }
    ]
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Benvenuto nell'API di EWLKG!"}




