from datetime import date


def _create_category(client, headers):
    resp = client.post("/api/v1/categories", headers=headers, json={
        "name": "Test Cat", "type": "expense", "icon": "🛒", "color": "#ff0000",
    })
    return resp.json()["id"]


def test_create_budget(client, auth_headers):
    cat_id = _create_category(client, auth_headers)
    today = date.today()
    resp = client.post("/api/v1/budgets", headers=auth_headers, json={
        "category_id": cat_id,
        "amount": 500.0,
        "month": today.month,
        "year": today.year,
        "alert_threshold": 80.0,
    })
    assert resp.status_code == 201
    assert float(resp.json()["amount"]) == 500.0


def test_duplicate_budget(client, auth_headers):
    cat_id = _create_category(client, auth_headers)
    today = date.today()
    payload = {"category_id": cat_id, "amount": 200.0, "month": today.month, "year": today.year}
    client.post("/api/v1/budgets", headers=auth_headers, json=payload)
    resp = client.post("/api/v1/budgets", headers=auth_headers, json=payload)
    assert resp.status_code == 409


def test_list_budgets_with_spending(client, auth_headers):
    resp = client.get("/api/v1/budgets", headers=auth_headers)
    assert resp.status_code == 200
    for b in resp.json():
        assert "spent" in b
        assert "percentage" in b
        assert "is_over_budget" in b
