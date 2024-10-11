# Definisco file per ogni persona in modo da immagazzinare i
# dati e accedo al file tramite la persona (devo crittografare i nomi)
# Quando faccio il backup avro' bisogno di creare una cartella backup della cartella principale.
from pathlib import Path
import json
from typing import List, Union
from exercise_sheet_to_graph.models import SheetPerson, Exercise
from exercise_sheet_to_graph.utils import get_logger

logger = get_logger("sheet_to_graph")


class InfoSaver():
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_person(self, info_person: SheetPerson):  # if exists, u need to update
        to_save = info_person

        if info_person == None or info_person.name == "":
            logger.error("No person inserted")
            return

        file_path = self.base_dir / f"{info_person.name}.json"

        if file_path.exists():
            to_save = self._merge_data(info_person)

            if to_save is None:
                to_save = info_person

        with open(file_path, 'w') as to_write:
            json.dump(to_save.model_dump(), to_write)

        logger.info(f"Person {info_person.name} saved")

    def load_person(self, name: str):
        if name == None or name == "":
            logger.error("No name inserted")
            return None

        file_path = self.base_dir / f"{name}.json"

        if file_path.exists() and not (file_path.stat().st_size == 0):
            with open(file_path, 'r') as read_file:
                data = json.load(read_file)
                return SheetPerson.model_validate(data)
        else:
            logger.error(
                f"File for {name} not found, check the name of the person")
            return None

    def _merge_data(self, person_to_save: SheetPerson):
        saved_person = self.load_person(person_to_save.name)
        print("ciao")

        if saved_person is None or saved_person.name == "":
            logger.error(f"{person_to_save.name} not found")
            return None

        not_founded = []
        # controllo se tra gli esercizi da salvare c'e' un matching di nome
        for exercise in person_to_save.exercises:
            matching_exercise = self.find_exercise_by_name(
                saved_person, exercise.name)
            if matching_exercise:
                matching_exercise.volumes.append(exercise.volumes[0])
                logger.info(f"{exercise.name} founded in {saved_person.name}")
            else:
                not_founded.append(exercise)

        for new_exercise in not_founded:
            saved_person.exercises.append(new_exercise)

        return saved_person

    def find_exercise_by_name(self, person, exercise_name) -> Union[Exercise, None]:
        for exercise in person.exercises:
            if exercise.name == exercise_name:
                return exercise
        return None
