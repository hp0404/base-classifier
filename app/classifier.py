# -*- coding: utf-8 -*-
import uuid
import spacy
from app.models import InputDocument, ModelResponse


class NER:
    """Pipe Document through a spacy model and return entities.


    Usage
    -----
    >>> nlp = spacy.load("path/to/model")
    >>> snippet = '''
    Secretary of State Mike Pompeo and Defense Secretary Mark T. Esper met with
    President Trump at the White House following the attack. The president said
    he will make a statement Wednesday morning...
    '''
    >>> document = InputDocument(text=snippet)
    >>> ner = NER(nlp=nlp, document=document)
    >>> ner.extract_entities()
    {
        "doc_id": "a3a32917aa49455b8b117a01806c75ed",
        "text": "Secretary of State Mike Pompeo and Defense Secretary Mark...",
        "entities": {
            "0-PERSON-Pompeo": {
                "name": "Pompeo",
                "label": "PERSON",
                "matches": [
                    {
                        "start": 24,
                        "end": 30,
                        "text": "Pompeo"
                    }
                ]
            },
            "0-PERSON-Esper": {
                "name": "Esper",
                "label": "PERSON",
                "matches": [
                    {
                        "start": 61,
                        "end": 66,
                        "text": "Esper"
                    }
                ]
            },
            "0-PERSON-Trump": {
                "name": "Trump",
                "label": "PERSON",
                "matches": [
                    {
                        "start": 86,
                        "end": 91,
                        "text": "Trump"
                    }
                ]
            }
        }
    }
    """

    def __init__(self, nlp: spacy.language.Language, document: InputDocument) -> None:
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
                    "matches": [],
                }
            entities[ent_id]["matches"].append(
                {"start": ent.start_char, "end": ent.end_char, "text": ent.text}
            )
        return {"doc_id": self.doc_id.hex, "text": self.document.text, "entities": entities}
