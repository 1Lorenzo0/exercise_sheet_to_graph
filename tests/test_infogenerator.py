import unittest
from pathlib import Path
from exercise_sheet_to_graph.infogenerator import InfoGenerator


class TestInfoGenerator(unittest.TestCase):

    def test_getinformations(self):
        file = Path("./tests/data/esempio.txt")
        info_generator = InfoGenerator()

        info = info_generator.get_informations("Lorenzo", file)

        self.assertEqual(info.name, "Lorenzo")
        self.assertIsNotNone(info.exercises)
        self.assertEqual(len(info.exercises), 3)

        for exercise in info.exercises:
            self.assertIsNotNone(exercise.volumes)
            self.assertIsNot(exercise.volumes[0].weight, 0)
            self.assertIsNot(exercise.volumes[0].reps, 0)
