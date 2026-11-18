from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models

Base.metadata.create_all(bind=engine)  # tabel yang sudah ada tidak akan dibuat ulang

app = FastAPI(title="Credit Risk Analyst API")

@app.get("/")
def root():
    return {"message": "Credit Risk API jalan"}

@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "database connected"}