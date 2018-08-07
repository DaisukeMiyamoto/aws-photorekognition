# -*- coding: utf-8 -*-

import json
import pytest
from helloworld.application import application
from helloworld.application import dynamodb_scan

@pytest.fixture
def client():
    return application.test_client()

def test_response(client):
    result = client.get('/api')
    response_body = json.loads(result.get_data())
    assert result.status_code == 200
    assert result.headers['Content-Type'] == 'application/json'
    assert response_body['Output'] == 'Hello World'


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # assert response.data == '<h1>hello!</h1>'


def test_search_error(client):
    response = client.get('/?search=hogehoge')
    assert response.status_code == 200

    response = client.get('/?search=')
    assert response.status_code == 200

    response = client.get('/?search=日本語')
    assert response.status_code == 200

    response = client.get('/?search=!<>')
    assert response.status_code == 200


def test_dynamodb_scan():
    scan_result = dynamodb_scan()

    scan_result = dynamodb_scan('Food')
