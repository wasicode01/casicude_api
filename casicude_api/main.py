#gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from typing import List
from casicude_api.data import groups, exercises
from casicude_api.schemas import Routine
from . import models, database

app = FastAPI(title="Gym Personal API")
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para obtener sesión
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/routines", response_model=List[Routine])
def get_routines(db: Session = Depends(get_db)):
    return db.query(models.Routine).all()

#@app.get("/routines/{routine_id}", response_model=Routine)
#def get_routine(routine_id: int, db: Session = Depends(get_db)):
#    routine = db.query(models.Routine).filter(models.Routine.id == routine_id).first()
#    if not routine:
#        raise HTTPException(status_code=404, detail="Routine not found")
#    return routine*/

@app.get("/routines/{routine_id}")
def get_routine(routine_id: int, db: Session = Depends(get_db)):
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