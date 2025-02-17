#qui metto classi per field e base model per validazione parametri
from pydantic import BaseModel, Field
from typing import List, Dict

class LiteralValue(BaseModel):
    type: str
    value: str

class SearchResult(BaseModel):
    name: LiteralValue
    titolo: LiteralValue

class SearchResponse(BaseModel):
    results: List[SearchResult]
