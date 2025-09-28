from datetime import date

groups = [
    {"id": 1, "name": "Pecho", "description": "Ejercicios de pecho"},
    {"id": 2, "name": "Piernas", "description": "Ejercicios de piernas"},
    {"id": 3, "name": "Espalda", "description": "Ejercicios de espalda"},
]

exercises = [
    {"id": 1, "group_id": 1, "name": "Press de banca", "sets": 3, "reps": 10, "weight": 50, "date": date.today()},
    {"id": 2, "group_id": 2, "name": "Sentadillas", "sets": 4, "reps": 12, "weight": 60, "date": date.today()},
]