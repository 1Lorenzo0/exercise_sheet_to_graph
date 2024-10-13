# district_exercise_mapper.py
from typing import List, Optional
from exercise_sheet_to_graph.utils import get_logger

logger = get_logger("sheet_to_graph")


class DistrictExerciseMapper:
    def __init__(self):
        self.district_to_exercises = {}
        self.exercises_to_district = {}

    def get_exercise_by_district(self, district: str) -> Optional[List[str]]:
        """
        Retrieves a list of exercises for a given district.

        :param district: The name of the district.
        :return: A list of exercises in the district, or None if the district does not exist.
        """
        try:
            return self.district_to_exercises[district]
        except KeyError:
            logger.error(f"District '{district}' does not exist.")
            return None

    def get_district_by_exercise(self, exercise: str) -> Optional[str]:
        """
        Retrieves the district for a given exercise.

        :param exercise: The name of the exercise.
        :return: The district name, or None if the exercise does not exist.
        """
        try:
            return self.exercises_to_district[exercise]
        except KeyError:
            logger.error(f"Exercise '{exercise}' does not exist.")
            return None

    def add_exercise_to_district(self, district: str, exercise: str) -> None:
        """
        Adds an exercise to a district.

        :param district: The name of the district.
        :param exercise: The name of the exercise.
        """
        try:
            self.district_to_exercises[district] = self.district_to_exercises.get(district, []) + [exercise]
            self.exercises_to_district[exercise] = district
            logger.info(f"Added exercise '{exercise}' to district '{district}'.")
        except Exception as e:
            logger.error(f"Error adding exercise to district: {e}")

    def remove_exercise_from_district(self, district: str, exercise: str) -> None:
        """
        Removes an exercise from a district.

        :param district: The name of the district.
        :param exercise: The name of the exercise.
        """
        try:
            if exercise in self.district_to_exercises[district]:
                self.district_to_exercises[district].remove(exercise)
            self.exercises_to_district.pop(exercise, None)
            logger.info(f"Removed exercise '{exercise}' from district '{district}'.")
        except KeyError:
            logger.error(f"Error: District '{district}' or exercise '{exercise}' does not exist.")
        except Exception as e:
            logger.error(f"Error removing exercise from district: {e}")
