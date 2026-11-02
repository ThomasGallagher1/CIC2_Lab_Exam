import pytest
def loan_payload(equipment_id= 1,borrower_name="Tom", loan_days= 7, purpose= "Insurance"):
    return{"equipment_id": equipment_id, "borrower_name": borrower_name, "loan_days":loan_days, "purpose":purpose}

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_add(client):
    r = client.post("/api/loans", json=loan_payload())
    assert r.status_code==201
    assert r.json()["id"] == 1
    assert r.json()["equipment_id"] == 1

@pytest.mark.parametrize("bad", [0,15])
def test_bad_loan_day(client,bad):
    r = client.post("/api/loans", json=loan_payload(loan_days=bad))
    assert r.status_code==422
