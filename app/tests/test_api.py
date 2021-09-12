# -*- coding: utf-8 -*-
from starlette.testclient import TestClient
from app.main import app


def test_docs_redirect():
    client = TestClient(app)
    response = client.get("/")
    assert response.history[0].status_code == 307
    assert response.status_code == 200
    assert response.url == "http://testserver/docs"


def test_api():
    client = TestClient(app)

    text = """
    Secretary of State Mike Pompeo and Defense Secretary Mark T. Esper met with 
    President Trump at the White House following the attack. The president said 
    he will make a statement Wednesday morning...""".replace(
        "\n", ""
    )
    example_request = {"text": text}

    response = client.post("/entities", json=example_request)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["doc_id"], str) and len(data["doc_id"]) == 32
    assert list(data["entities"]) == [
        "0-PERSON-Pompeo",
        "0-PERSON-Esper",
        "0-PERSON-Trump",
    ]
