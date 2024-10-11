from pathlib import Path
import exercise_sheet_to_graph.models as gm
from typing import Union, Tuple
import re
from exercise_sheet_to_graph.utils import get_logger

logger = get_logger("sheet_to_graph")


class InfoGenerator():
    def __init__(self):
        pass

    # create the informations from the input, you need to do operations for comparing what u saved (timestamp of exercise is important)
    def get_informations(self, name: str, file: Union[Path, str]) -> gm.SheetPerson:
        file = Path(file)
        if name == "":
            logger.error("No Person name in input")
            return None

        if file == None or not (file.is_file()):
            logger.error("No file in input")
            return None

        person = gm.SheetPerson()
        with open(file, "r") as read_file:
            for line in read_file:
                exercise = self._get_exercise(line)
                person.exercises.append(exercise)

        person.name = name

        return person

    # no compare name of exercise because is relative to the same day in a different period
    def _get_exercise(self, line: str) -> gm.Exercise:
        exercise = gm.Exercise()
        exercise_info = self._parse_line_extended(line)
        exercise.name = exercise_info[0]
        exercise.volumes.append(gm.Volume(
            weight=exercise_info[1], reps=exercise_info[2]))
        return exercise

    def _parse_line_extended(self, line) -> Tuple[str, int, int]:
        if line == "":
            return

        pattern = r'(?P<exercise>[\w\s]+)\s+(?P<weight>\d+)kg\s*x\s*(?P<reps>\d+)'
        match = re.match(pattern, line)

        if match:
            return match.group('exercise'), int(match.group('weight')), int(match.group('reps'))
        return None, None, None
