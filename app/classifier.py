# -*- coding: utf-8 -*-
import uuid
import spacy
from app.models import InputDocument, ModelResponse


class NER:
    """Pipe document through a spacy model and return entities.
    
    
    Usage
    -----
    >>> nlp = spacy.load("path/to/model")
    >>> document = "Margarita Simonyan, editor-in-chief of Russia's overseas propaganda channel, RT, had ..."
    >>> ner = NER(nlp=nlp, document=document)
    >>> ner.extract_entities()
    {
        "doc_id": "439d2be6c8bf421c8cf74d8f8d070f69", 
        "document": "Margarita Simonyan, editor-in-chief of Russia's overseas propaganda channel, RT, had ...",
        "entities": {
            "0": {
                "name": "Simonyan", 
                "label": "PERSON", 
                "matches": [
                    {"start": 10, "end": 18, "text": "Simonyan"}
                ]
            }
        }
    }
    """
    def __init__(self, nlp: spacy.language.Language, document: InputDocument):
        self.nlp = nlp
        self.document = self.nlp(document.text)
        self.doc_id = uuid.uuid4()

    def extract_entities(self) -> ModelResponse:
        entities = {}
        for ent in self.document.ents:
            ent_id = f"{ent.kb_id}-{ent.label_}-{ent.text}"
            if ent_id not in entities:
                entities[ent_id] = {
                    "name": ent.text,
                    "label": ent.label_,
                    "matches": []
                }
            entities[ent_id]["matches"].append(
                {"start": ent.start_char, "end": ent.end_char, "text": ent.text}
            )
        return {"doc_id": self.doc_id.hex, "text": self.document.text, "entities": entities}

