import requests
from fastapi import FastAPI, HTTPException, Query, APIRouter
from SPARQLWrapper import SPARQLWrapper, JSON
import yaml
import os,json
from internal.schemas import SearchResponse, FindResult, SearchResultURI
from internal.config import config as config 


# Configura endpoint 
SPARQL_ENDPOINT = config.endpoint


def searchExactly(label: str, configEntity: str, urw_prefix:str) :
    
    # Costruzione della query SPARQL 
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
    return query
    

def searchRegex(label: str, configEntity:str, urw_prefix:str) :
    
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
    return query


def finder(urw_prefix:str, configEntity:str, o:str):

    # Costruzione della query SPARQL con validazione
    query = f"""
    PREFIX urw: {urw_prefix}
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?s, ?sogg WHERE {{
      ?s {configEntity} {o}.
      ?s rdfs:label ?sogg.
      
    }}
    """
    return query

def searchTypeEntity(urw_prefix:str, entity_type:str, prefix_type:str) :

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
    return query