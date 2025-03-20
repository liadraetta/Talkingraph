import requests
from fastapi import FastAPI, HTTPException, Query, APIRouter
from SPARQLWrapper import SPARQLWrapper, JSON
import yaml
import os,json
from internal.schemas import SearchResponse, FindResult, SearchResultURI
from internal.config import config as config 
from scripts.retrieval import Retriever

retriever = Retriever()


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


    

@query.get("/find", response_model=FindResult)
def search(rel: str, o: str) -> FindResult:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    # Controllo se il prefisso urw è disponibile
    urw_prefix = config.prefix["urw"]
    if not urw_prefix:
        raise HTTPException(status_code=500, detail="Prefix is missing in configuration")

    
    entity_key = f"entità{rel}"  # Nome chiave da cercare
    
    # Controllo se esiste l'entità richiesta
    if entity_key not in config.namespace.right:
        raise HTTPException(status_code=400, detail=f"Entity {entity_key} not found in config")

    configEntity = config.namespace.right[entity_key].rel  

    # Costruzione della query SPARQL con validazione
    query = f"""
    PREFIX urw: {urw_prefix}
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?s, ?sogg WHERE {{
      ?s {configEntity} {o}.
      ?s rdfs:label ?sogg.
      
    }}
    """
    print(query)
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Query Error: {str(e)}")

    # Trasforma la risposta per Pydantic
    bindings = results["results"]["bindings"]
    formatted_results = [{"s": item["s"], "sogg": item["sogg"]} for item in bindings]

    return {"results": formatted_results}


@query.get("/search_typeEntity", response_model=SearchResultURI)
def search(entitytype: str) -> SearchResultURI:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    # Controllo se il prefisso urw è disponibile
    urw_prefix = config.prefix["urw"]
    if not urw_prefix:
        raise HTTPException(status_code=500, detail="Prefix is missing in configuration")

    
    entity_key = f"entitytype{entitytype}"  # Nome chiave da cercare
    
    # Controllo se esiste l'entità richiesta
    if entity_key not in config.namespace.left:
        raise HTTPException(status_code=400, detail=f"Entity {entity_key} not found in config")

    prefix_type = config.namespace.left[entity_key].prefix
    entity_type = config.namespace.left[entity_key].type  

    # Costruzione della query SPARQL con validazione
    query = f"""
    PREFIX urw: {urw_prefix}
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    {prefix_type}

    SELECT DISTINCT ?s, ?name WHERE {{
      ?s  rdf:type {entity_type}.
      ?s rdfs:label ?name.
    }}

    """
    print(query)
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Query Error: {str(e)}")

    # Trasforma la risposta per Pydantic
    bindings = results["results"]["bindings"]
    formatted_results = [{"s": item["s"], "name": item["name"]} for item in bindings]

    return {"results": formatted_results}

@query.get("/graphrag")
def retrieve(template:str,text:str,type:str,k:int):
    template = eval(template)
    my_res = []
    result = retriever.extract_knowledge(template=template,text=text)
    result = json.loads(result)

    for res in result['entities'][type]:

        linked = retriever.link(res,type,k)
        
    
        my_res.extend(linked)

    results = search(1,f"urw:{my_res[0][0]['entity']}")
    return results

def search(rel: str, o: str) -> FindResult:
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    # Controllo se il prefisso urw è disponibile
    urw_prefix = config.prefix["urw"]
    if not urw_prefix:
        raise HTTPException(status_code=500, detail="Prefix is missing in configuration")

    
    entity_key = f"entità{rel}"  # Nome chiave da cercare
    
    # Controllo se esiste l'entità richiesta
    if entity_key not in config.namespace.right:
        raise HTTPException(status_code=400, detail=f"Entity {entity_key} not found in config")

    configEntity = config.namespace.right[entity_key].rel  

    # Costruzione della query SPARQL con validazione
    query = f"""
    PREFIX urw: {urw_prefix}
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?s, ?sogg WHERE {{
      ?s {configEntity} {o}.
      ?s rdfs:label ?sogg.
      
    }}
    """
    print(query)
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Query Error: {str(e)}")

    # Trasforma la risposta per Pydantic
    bindings = results["results"]["bindings"]
    formatted_results = [{"s": item["s"], "sogg": item["sogg"]} for item in bindings]

    return {"results": formatted_results}


    