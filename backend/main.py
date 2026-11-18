from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
from auth import router as auth_router
from loans import router as loans_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit Risk Analyst API")
app.include_router(auth_router)
app.include_router(loans_router)

@app.get("/")
def root():
    return {"message": "Credit Risk API jalan"}

@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "database connected"}