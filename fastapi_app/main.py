from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/Login/")
def login_for_user(user_from_fe : schemas.UserCreate, db: Session = Depends(get_db)):
    if not user_from_fe:
        return {"Message":"Jwt Token Not provided"}
    pass_check = crud.check_user(db=db, user=user_from_fe)
    if pass_check: 
        return {"Messsage":"login Success"}
    else: 
        return {"Message":"Invalid Credentials"}