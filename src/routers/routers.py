import requests
from fastapi import FastAPI, HTTPException, Query, APIRouter
from SPARQLWrapper import SPARQLWrapper, JSON

router = APIRouter(
    prefix="/router",
    tags=["router"],
    responses={404: {"description": "Not found"}},
)

# Configura endpoint 
SPARQL_ENDPOINT = "https://kgccc.di.unito.it/sparql/wl-kg"

@router.get("/query1")
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


@router.get("/query2")
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

@router.get("/search")
def search(label: str):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    
    query = f"""
    PREFIX : <https://purl.archive.org/urwriters#>
    PREFIX urb: <https://purl.archive.org/urbooks#>
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
