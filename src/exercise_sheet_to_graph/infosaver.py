import json
from pathlib import Path
from typing import Union
from exercise_sheet_to_graph.models import SheetPerson, Exercise
from exercise_sheet_to_graph.utils import get_logger

logger = get_logger("sheet_to_graph")


def find_exercise_by_name(person: SheetPerson, exercise_name: str) -> Union[Exercise, None]:
    """
    Finds an exercise by name in a given SheetPerson's exercises.

    :param person: The SheetPerson object containing exercises.
    :param exercise_name: The name of the exercise to find.
    :return: The Exercise object if found, otherwise None.
    """
    for exercise in person.exercises:
        if exercise.name == exercise_name:
            return exercise
    return None


class InfoSaver:
    def __init__(self, base_dir: Path):
        """
        Initializes the InfoSaver with a base directory.

        :param base_dir: The base directory where data will be saved.
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_person(self, info_person: SheetPerson) -> None:
        """
        Saves a SheetPerson's information to a JSON file.

        :param info_person: The SheetPerson object to save.
        """
        if not info_person or not info_person.name:
            logger.error("No person inserted")
            return

        name_to_save = info_person.name.replace(" ", "_")
        file_path = self.base_dir / f"{name_to_save}.json"

        if file_path.exists():
            info_person = self._merge_data(info_person) or info_person

        with open(file_path, 'w') as to_write:
            json.dump(info_person.model_dump(), to_write)

        logger.info(f"Person {info_person.name} saved")

    def load_person(self, name: str) -> Union[SheetPerson, None]:
        """
        Loads a SheetPerson's information from a JSON file.

        :param name: The name of the person to load.
        :return: The SheetPerson object if found, otherwise None.
        """
        if not name:
            logger.error("No name inserted")
            return None

        name_to_save = name.replace(" ", "_")
        file_path = self.base_dir / f"{name_to_save}.json"

        if file_path.exists() and file_path.stat().st_size > 0:
            with open(file_path, 'r') as read_file:
                data = json.load(read_file)
                return SheetPerson.model_validate(data)
        else:
            logger.error(f"File for {name} not found, check the name of the person")
            return None

    def _merge_data(self, person_to_save: SheetPerson) -> Union[SheetPerson, None]:
        """
        Merges new exercise data with existing data for a SheetPerson.

        :param person_to_save: The SheetPerson object with new data to merge.
        :return: The merged SheetPerson object if successful, otherwise None.
        """
        saved_person = self.load_person(person_to_save.name)

        if not saved_person or not saved_person.name:
            logger.error(f"{person_to_save.name} not found")
            return None

        not_founded = []

        for exercise in person_to_save.exercises:
            matching_exercise = find_exercise_by_name(saved_person, exercise.name)
            if matching_exercise:
                matching_exercise.volumes.append(exercise.volumes[0])
                logger.info(f"{exercise.name} found in {saved_person.name}")
            else:
                not_founded.append(exercise)

        saved_person.exercises.extend(not_founded)

        return saved_person
