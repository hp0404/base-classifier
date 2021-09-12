# -*- coding: utf-8 -*-
from typing import Dict, List
from pydantic import BaseModel

class InputDocument(BaseModel):
    text: str

class Matches(BaseModel):
    start: int
    end: int
    text: str

class SingeEntitiy(BaseModel):
    name: str
    label: str
    matches: List[Matches]

class ModelResponse(BaseModel):
    doc_id: str
    text: str
    entities: Dict[str, SingeEntitiy]
