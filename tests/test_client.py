import json

import requests

from app.api.client import APIClient


class DummyResponse:
    def __init__(self, status_code=200, data=None):
        self.status_code = status_code
        self._data = data or {}

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError(f"Status {self.status_code}")

    def json(self):
        return self._data


def test_chamar_endpoint_github(monkeypatch):
    called = {}

    def fake_get(url, headers=None):
        called['url'] = url
        called['headers'] = headers
        print("fake_get called")
        return DummyResponse(200, {'tag_name': 'v1.2.3'})

    monkeypatch.setattr('requests.get', fake_get)

    client = APIClient()
    res = client.chamar_endpoint('repos/owner/repo/releases/latest', {}, use_github=True)

    assert 'api.github.com' in called['url']
    assert 'Accept' in called['headers']
    assert res['tag_name'] == 'v1.2.3'


def test_chamar_endpoint_nexus(monkeypatch):
    called = {}

    def fake_get(url, headers=None):
        called['url'] = url
        called['headers'] = headers
        return DummyResponse(200, {'name': 'mod name'})

    monkeypatch.setattr('requests.get', fake_get)

    client = APIClient()
    res = client.chamar_endpoint('v1/games/eldenring/mods/1', {})

    assert 'api.nexusmods.com' in called['url']
    assert 'apikey' in called['headers']
    assert res['name'] == 'mod name'