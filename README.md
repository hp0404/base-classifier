# base-classifier

This repository contains REST API powered by `FastAPI` that
uses custom `spacy` model (trained with `prodigy`) to extract entities
from a given document.  

## Usage
```console
$ git clone https://github.com/hp0404/base-classifier.git
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ uvicorn app.main:app --host 0.0.0.0 --reload --debug
```