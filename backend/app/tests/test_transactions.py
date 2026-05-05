import pytest
from datetime import date


def test_create_transaction(client, auth_headers):
    resp = client.post("/api/v1/transactions", headers=auth_headers, json={
        "amount": 49.99,
        "type": "expense",
        "description": "Supermarché",
        "date": str(date.today()),
        "tags": ["courses"],
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["amount"] == "49.99"
    assert data["type"] == "expense"


def test_list_transactions(client, auth_headers):
    resp = client.get("/api/v1/transactions", headers=auth_headers)
    assert resp.status_code == 200
    assert "items" in resp.json()
    assert "total" in resp.json()


def test_filter_by_type(client, auth_headers):
    # Create income tx
    client.post("/api/v1/transactions", headers=auth_headers, json={
        "amount": 2000.0, "type": "income", "description": "Salaire", "date": str(date.today()),
    })
    resp = client.get("/api/v1/transactions?type=income", headers=auth_headers)
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert all(t["type"] == "income" for t in items)


def test_delete_transaction(client, auth_headers):
    create_resp = client.post("/api/v1/transactions", headers=auth_headers, json={
        "amount": 10.0, "type": "expense", "description": "Test delete", "date": str(date.today()),
    })
    tx_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
