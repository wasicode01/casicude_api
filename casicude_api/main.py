#gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from typing import List
from casicude_api.data import groups, exercises
from casicude_api.schemas import Routine, ExerciseRepetitionCreate, ExerciseRepetition, UserCreate, UserOut, Token
from fastapi.security import OAuth2PasswordRequestForm
from . import models, database
from .security import (
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_current_active_user,
    oauth2_scheme,
)

app = FastAPI(title="Gym Personal API")
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para obtener sesión
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/routines", response_model=List[Routine])
def get_routines(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return db.query(models.Routine).all()

#@app.get("/routines/{routine_id}", response_model=Routine)
#def get_routine(routine_id: int, db: Session = Depends(get_db)):
#    routine = db.query(models.Routine).filter(models.Routine.id == routine_id).first()
#    if not routine:
#        raise HTTPException(status_code=404, detail="Routine not found")
#    return routine*/

@app.get("/routines/{routine_id}")
def get_routine(routine_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    routine = db.query(models.Routine).filter(models.Routine.id == routine_id).first()
    if not routine:
        return {"error": "Rutina no encontrada"}
    return {
        "id": routine.id,
        "name": routine.name,
        "exercises": [
            {"id": e.id, "name": e.name, "restTime": e.rest_time, "minRepetition": e.min_repetition, "maxRepetition": e.max_repetition, "numRep": e.num_rep}
            for e in routine.exercises
        ]
    }


@app.post("/repetitions", response_model=ExerciseRepetition)
def create_repetition(rep: ExerciseRepetitionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Verificar que el ejercicio existe
    exercise = db.query(models.Exercise).filter(models.Exercise.id == rep.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # (Opcional) verificar rutina si se proporcionó
    if rep.routine_id is not None:
        routine = db.query(models.Routine).filter(models.Routine.id == rep.routine_id).first()
        if not routine:
            raise HTTPException(status_code=404, detail="Routine not found")

    db_rep = models.ExerciseRepetition(
        exercise_id=rep.exercise_id,
        routine_id=rep.routine_id,
        num_reps=rep.num_reps,
        weight=rep.weight,
        notes=rep.notes,
    )
    db.add(db_rep)
    db.commit()
    db.refresh(db_rep)
    return db_rep