#qui metto classi per field e base model per validazione parametri
from pydantic import BaseModel, Field
from typing import List, Dict

from pydantic_settings import BaseSettings

class LiteralValue(BaseModel):
    type: str
    value: str

class SearchResult(BaseModel):
    name: LiteralValue
    titolo: LiteralValue

class SearchResponse(BaseModel):
    results: List[SearchResult]

# Modelli Pydantic per il file YML
class Entity(BaseModel):
    label: str
    rel: str

class LeftConfig(BaseModel):
    entitytype: str  

class Namespace(BaseModel):
    left: LeftConfig
    right: Dict[str, Entity]

class Config(BaseSettings):
    name: str
    endpoint: str
    namespace: Namespace
    prefix: Dict[str, str]
