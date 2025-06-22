import pytest
from fastapi.testclient import TestClient
from main import app
from base64 import b64encode
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

def get_basic_auth(username, password):
    credentials = f"{username}:{password}"
    return "Basic " + b64encode(credentials.encode()).decode()

@pytest.fixture
def auth_header():
    return {"Authorization": get_basic_auth("subham", "qwerty123")}

def test_fund_wallet(auth_header):
    response = client.post("/wallet/Fund", json={"amount": 1000}, headers=auth_header)
    assert response.status_code == 200
    assert "Deposit Successful" in response.json()["message"]

def test_get_balance(auth_header):
    response = client.get("/wallet/balance", headers=auth_header)
    assert response.status_code == 200
    assert "balance" in response.json()

def test_pay_user(auth_header):
    response = client.post("/wallet/pay", json={"to": "udipta", "amt": 500}, headers=auth_header)
    assert response.status_code == 200 or response.status_code == 400  # 400 if insufficient balance or invalid user

def test_transaction_history(auth_header):
    response = client.get("/stmt", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
