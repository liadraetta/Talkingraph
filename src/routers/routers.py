import requests
from fastapi import FastAPI, HTTPException, Query, APIRouter
from SPARQLWrapper import SPARQLWrapper, JSON
import yaml
import os
from routers.schemas import SearchResponse

# Ottieni il percorso assoluto basato sulla posizione attuale
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yml")

def load_config(filepath: str = CONFIG_PATH):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)  # Carica i dati YAML in un dizionario

router = APIRouter(
    prefix="/router",
    tags=["router"],
    responses={404: {"description": "Not found"}},
)


# Carica la configurazione
config = load_config()
# Configura endpoint 
SPARQL_ENDPOINT = config["progetto"]["endpoint"]


@router.get("/search", response_model=SearchResponse)
def search(label: str) -> SearchResponse:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    query = f"""
    PREFIX : <https://purl.archive.org/urwriters#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?name ?titolo WHERE {{
      ?author :wasAttributedTo ?books.
      ?books rdfs:label ?titolo.
      ?author rdfs:label ?name.
      
      FILTER(regex(?titolo, "{label}", "i") || regex(?name, "{label}", "i"))
    }}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    return {"results": results["results"]["bindings"]}
