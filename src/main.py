import yaml
import os
from fastapi import FastAPI
import requests
from routers.routers import router #dare un nome specifico anhe al file
from pydantic import BaseModel, Field
from config import config as config1

#todo eliminare questa parte
# Ottieni il percorso assoluto basato sulla posizione attuale
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yml")

def load_config(filepath: str = CONFIG_PATH):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)  # Carica i dati YAML in un dizionario
    
# Carica la configurazione
config = load_config()
#### creare file a parte per la configurazione e importarlo
#todo fino qui e poi rinominare import config1 in config e basta 

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

app.include_router(router)


@app.get("/")
async def root():
    return {"message": f"Benvenuto nell'API di {config['app']['name']}!"}


@app.get("/1")
async def root():
    return {
        "app_name": config1.name,
        "endpoint": config1.endpoint,
        "namespace_left": config1.namespace.left,
        "namespace_right": config1.namespace.right,
        "prefix": config1.prefix.urw
    }

