# -*- coding: utf-8 -*-
from pathlib import Path

import spacy
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.models import InputDocument, ModelResponse
from app.classifier import NER


root = Path(__file__).resolve().parent

nlp = spacy.load(root / "models")
app = FastAPI(title="MENA policies NER classifier", version="1.0")


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")

@app.post("/entities", response_model=ModelResponse, tags=["NER"])
async def extract_entities(body: InputDocument):
    """Extract Named Entities from an InputDocument."""
    ner = NER(nlp=nlp, document=body)
    return ner.extract_entities()
