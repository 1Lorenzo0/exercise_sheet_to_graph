from typing import List
from datetime import datetime
import pydantic


class Volume(pydantic.BaseModel):
    weight: int = 0
    reps: int = 0
    ts: str = str(datetime.now())


class Exercise(pydantic.BaseModel):
    name: str = ""
    district: str = ""
    volumes: List[Volume] = []


class SheetPerson(pydantic.BaseModel):
    name: str = ""
    exercises: List[Exercise] = []


class SheetPeople(pydantic.BaseModel):
    people: List[SheetPerson] = []
