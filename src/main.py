from fastapi import FastAPI, HTTPException, Query
import requests
from routers.routers import router
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

# Configura endpoint 
SPARQL_ENDPOINT = "https://kgccc.di.unito.it/sparql/wl-kg"

@app.get("/query1")
def execute_sparql_query():
    sparql = get_example_query()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query": sparql
    }
    
    try:
        response = requests.post(SPARQL_ENDPOINT, data=data, headers=headers)
        print("SPARQL Response:", response.text)  # Debug della risposta

        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Errore nella richiesta SPARQL: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Errore nel parsing della risposta SPARQL")

    return data

# Query di esempio 
def get_example_query():
    example_query = """
  PREFIX : <https://purl.archive.org/urwriters#>
PREFIX urb: <https://purl.archive.org/urbooks#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?book ?bookTitle WHERE { 
  ?book urb:wasWrittenBy ?author .
  ?book rdfs:label ?bookTitle .
  ?author rdfs:label ?authorName .
  
  FILTER(LCASE(?authorName) = "orwell")  
} 
LIMIT 10

    """
    return example_query

@app.get("/")
async def root():
    return {"message": "Benvenuto nell'API FastAPI"}


@app.get("/query2")
def execute_sparql_query():
    sparql = get_example_query2()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "query": sparql
    }
    
    try:
        response = requests.post(SPARQL_ENDPOINT, data=data, headers=headers)
        print("SPARQL Response:", response.text)  # Debug della risposta

        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Errore nella richiesta SPARQL: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Errore nel parsing della risposta SPARQL")

    return data

# Query di esempio 
def get_example_query2():
    example_query = """
  prefix :<https://purl.archive.org/urwriters#>

    prefix urw:<https://purl.archive.org/urwriters#>

    prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#>

    prefix geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>


    select distinct ?work ?name where {?w urw:wasAttributedTo ?pl. ?w rdfs:label ?work.  ?pl rdfs:label ?name.

} limit 10

    """
    return example_query




