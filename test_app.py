import pytest
from app import app
import json

@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    res = client.get("/home")
    assert res.status_code == 200