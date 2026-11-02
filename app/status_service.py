import os
import httpx
URL=os.getenv("Loan_Service_URL", "http://127.0.0.1:8001")

def fetch_loan(status:str) -> dict:
    r = httpx.get(f"{URL}/loans/{status}", timeout=3.0)
    r.raise_for_status()
    return r.json()

def get_loan_fetcher():
    return fetch_loan