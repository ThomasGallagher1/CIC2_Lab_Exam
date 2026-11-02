from fastapi import Depends, FastAPI, HTTPException, status
import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, LoanDB
from app.schemas import loanCreate, loanRead
from app.status_service import get_loan_fetcher

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Example template")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.post("/api/loans", response_model=loanRead, status_code=status.HTTP_201_CREATED)
def add_loans(loan: loanCreate, db: Session=Depends(get_db)):
    db_loan = LoanDB(**loan.model_dump())
    db.add(db_loan)
    try:
        db.commit()
        db.refresh(db_loan)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Loam already exists")
    return db_loan

@app.get("/api/loans/{loan_id}", response_model=loanRead)
def get_loan(loan_id: int, db:Session=Depends(get_db)):
    db_loan=db.get(LoanDB, loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan does not exist")
    return db_loan

@app.delete("/api/loans/{loan_id}", status_code=204)
def delete_loan(loan_id: int, db:Session=Depends(get_db)):
    db_loan=db.get(LoanDB, loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan does not exist")
    db.delete(db_loan)
    db.commit()


@app.get("/api/remote/{status}")
def get_remote(status:str, fetcher=Depends(get_loan_fetcher)):
    try:
        return fetcher(status)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404)from exc
        raise HTTPException(status_code=502) from exc
    except httpx.ReadError as exc:
        raise HTTPException(status_code=503)from exc