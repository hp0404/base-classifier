# -*- coding: utf-8 -*-
import json
from pathlib import Path

import spacy
from fastapi import FastAPI, Body
from starlette.responses import RedirectResponse

from app.models import InputDocument, ModelResponse
from app.classifier import NER


root = Path(__file__).resolve().parent

nlp = spacy.load(root / "models")
app = FastAPI(title="MENA policies PERSON classifier", version="1.0")

text = """
Secretary of State Mike Pompeo and Defense Secretary Mark T. Esper met with 
President Trump at the White House following the attack. The president said 
he will make a statement Wednesday morning...""".replace(
    "\n", ""
)
example_request = json.dumps({"text": text})


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")


@app.post("/entities", response_model=ModelResponse, tags=["NER"])
async def extract_entities(body: InputDocument = Body(..., example=example_request)):
    """Extract Named Entities from an InputDocument."""
    ner = NER(nlp=nlp, document=body)
    return ner.extract_entities()
