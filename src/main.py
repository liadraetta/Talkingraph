import yaml
import os
from fastapi import FastAPI
from routers.query import query as query_router 
from config import config as config



app = FastAPI(
    title= f"API FastAPI wlkg",
    description="API FastAPI wlkg",
    version="0.1",
    openapi_tags=[
        {  
            "name": "wlkg",
        }
    ]
)

app.include_router(query_router)


@app.get("/")
async def root():
    return {"message": f"Benvenuto nell'API di {config.name}!"}


@app.get("/1")
async def root():

    return {
        "app_name": config.name,
        "endpoint": config.endpoint,
        "namespace_left": config.namespace.left.entitytype,  
        "namespace_right": config.namespace.right["entità1"].label,
        "prefix": config.prefix["urw"]
    }

