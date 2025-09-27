#gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

from fastapi import FastAPI, HTTPException
from typing import List
from data import groups, exercises
from schemas import Group, GroupCreate, Exercise, ExerciseCreate

app = FastAPI(title="Gym Personal API")

# -------------------- GROUPS --------------------
@app.get("/groups", response_model=List[Group])
def get_groups():
    return groups

@app.get("/groups/{group_id}", response_model=Group)
def get_group(group_id: int):
    for g in groups:
        if g["id"] == group_id:
            return g
    raise HTTPException(status_code=404, detail="Group not found")

@app.post("/groups", response_model=Group)
def create_group(group: GroupCreate):
    new_id = max([g["id"] for g in groups]) + 1 if groups else 1
    new_group = group.dict()
    new_group["id"] = new_id
    groups.append(new_group)
    return new_group

@app.put("/groups/{group_id}", response_model=Group)
def update_group(group_id: int, group: GroupCreate):
    for i, g in enumerate(groups):
        if g["id"] == group_id:
            updated = group.model_dump()
            updated["id"] = group_id
            groups[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Group not found")

@app.delete("/groups/{group_id}")
def delete_group(group_id: int):
    for i, g in enumerate(groups):
        if g["id"] == group_id:
            groups.pop(i)
            return {"detail": "Group deleted"}
    raise HTTPException(status_code=404, detail="Group not found")

# -------------------- EXERCISES --------------------
@app.get("/exercises", response_model=List[Exercise])
def get_exercises():
    return exercises

@app.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id: int):
    for ex in exercises:
        if ex["id"] == exercise_id:
            return ex
    raise HTTPException(status_code=404, detail="Exercise not found")

@app.post("/exercises", response_model=Exercise)
def create_exercise(exercise: ExerciseCreate):
    new_id = max([ex["id"] for ex in exercises]) + 1 if exercises else 1
    new_ex = exercise.dict()
    new_ex["id"] = new_id
    exercises.append(new_ex)
    return new_ex

@app.put("/exercises/{exercise_id}", response_model=Exercise)
def update_exercise(exercise_id: int, exercise: ExerciseCreate):
    for i, ex in enumerate(exercises):
        if ex["id"] == exercise_id:
            updated = exercise.dict()
            updated["id"] = exercise_id
            exercises[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Exercise not found")

@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    for i, ex in enumerate(exercises):
        if ex["id"] == exercise_id:
            exercises.pop(i)
            return {"detail": "Exercise deleted"}
    raise HTTPException(status_code=404, detail="Exercise not found")
