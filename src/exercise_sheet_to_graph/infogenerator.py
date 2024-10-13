import re
from pathlib import Path
from typing import Union, Tuple, Optional
import exercise_sheet_to_graph.models as gm
from exercise_sheet_to_graph.utils import get_logger

logger = get_logger("sheet_to_graph")


class InfoGenerator:
    def __init__(self):
        pass

    def get_informations(self, name: str, file: Union[Path, str]) -> Optional[gm.SheetPerson]:
        """
        Creates information from the input, performing operations to compare what has been saved
        (the exercise timestamp is important).

        :param name: Name of the person
        :param file: Path to the file containing exercise data
        :return: An instance of SheetPerson with the loaded exercises
        """
        file = Path(file)
        if not name:
            logger.error("No Person name in input")
            return None

        if not file.is_file():
            logger.error("No file in input")
            return None

        person = gm.SheetPerson(name=name, exercises=[])
        with open(file, "r") as read_file:
            for line in read_file:
                exercise = InfoGenerator._get_exercise(line=line)
                if exercise:
                    person.exercises.append(exercise)

        return person

    @staticmethod
    def _get_exercise(line: str) -> Optional[gm.Exercise]:
        """
        Extracts exercise information from a line of text.

        :param line: Line of text containing exercise data
        :return: An instance of Exercise with the extracted data
        """
        exercise_info = InfoGenerator._parse_line_extended(line)
        if not exercise_info:
            return None

        exercise = gm.Exercise(name=exercise_info[0], volumes=[
            gm.Volume(weight=exercise_info[1], reps=exercise_info[2])
        ])
        return exercise

    @staticmethod
    def _parse_line_extended(line: str) -> Optional[Tuple[str, int, int]]:
        """
        Parses a line of text to extract the exercise name, weight, and repetitions.

        :param line: Line of text to parse
        :return: A tuple containing the exercise name, weight, and repetitions
        """
        if not line:
            return None

        pattern = r'(?P<exercise>[\w\s]+)\s+(?P<weight>\d+)kg\s*x\s*(?P<reps>\d+)'
        match = re.match(pattern, line)

        if match:
            return match.group('exercise'), int(match.group('weight')), int(match.group('reps'))
        return None
