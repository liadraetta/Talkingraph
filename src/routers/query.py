import requests
from fastapi import FastAPI, HTTPException, Query, APIRouter
from SPARQLWrapper import SPARQLWrapper, JSON
import yaml
import os
from routers.schemas import SearchResponse
from config import config as config 


query = APIRouter(
    prefix="/query",
    tags=["query"],
    responses={404: {"description": "Not found"}},
)



# Configura endpoint 
SPARQL_ENDPOINT = config.endpoint


@query.get("/search_exactly", response_model=SearchResponse)
def search(label: str, numberEntity: int) -> SearchResponse:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    entity_key = f"entità{numberEntity}"  # Nome chiave da cercare
    
    # Controllo se esiste l'entità richiesta
    if entity_key not in config.namespace.right:
        raise HTTPException(status_code=400, detail=f"Entity {entity_key} not found in config")

    configEntity = config.namespace.right[entity_key].rel  

    # Controllo se il prefisso urw è disponibile
    urw_prefix = config.prefix["urw"]
    if not urw_prefix:
        raise HTTPException(status_code=500, detail="Prefix is missing in configuration")

    # Costruzione della query SPARQL con validazione
    query = f"""
    PREFIX urw: {urw_prefix}
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?name ?titolo WHERE {{
      ?author {configEntity} ?books.
      ?books rdfs:label ?titolo.
      ?author rdfs:label ?name.
      
      FILTER((?titolo = "{label}") || (?name = "{label}"))
    }}
    LIMIT 10
    """
    print(query)
    
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Query Error: {str(e)}")

    return {"results": results["results"]["bindings"]}



@query.get("/search_regex", response_model=SearchResponse)
def search(label: str, numberEntity: int) -> SearchResponse:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    entity_key = f"entità{numberEntity}"  # Nome chiave da cercare
    
    # Controllo se esiste l'entità richiesta
    if entity_key not in config.namespace.right:
        raise HTTPException(status_code=400, detail=f"Entity {entity_key} not found in config")

    configEntity = config.namespace.right[entity_key].rel  

    # Controllo se il prefisso urw è disponibile
    urw_prefix = config.prefix["urw"]
    if not urw_prefix:
        raise HTTPException(status_code=500, detail="Prefix is missing in configuration")

    # Costruzione della query SPARQL con validazione
    query = f"""
    PREFIX urw: {urw_prefix}
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?name ?titolo WHERE {{
      ?author {configEntity} ?books.
      ?books rdfs:label ?titolo.
      ?author rdfs:label ?name.
      
      FILTER(regex(?titolo, "{label}", "i") || regex(?name, "{label}", "i"))
    }}
    LIMIT 10
    """
    
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Query Error: {str(e)}")

    return {"results": results["results"]["bindings"]}