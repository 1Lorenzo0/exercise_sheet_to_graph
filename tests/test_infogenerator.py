import unittest
from pathlib import Path
from exercise_sheet_to_graph.infogenerator import InfoGenerator


class TestInfoGenerator(unittest.TestCase):

    def test_loadsheetpersonfromyaml(self):
        file = Path("./tests/data/db/data_20241013_183717_giorgio_finizio.yaml")
        info_generator = InfoGenerator()

        info = info_generator.load_sheet_person_from_yaml(file)
        self.assertEqual(info.name, "giorgio finizio")
        self.assertIsNotNone(info.exercises)
        self.assertEqual(len(info.exercises), 2)
        self.assertEqual(info.exercises[0].name, "croci al cavo basso")
        self.assertEqual(info.exercises[1].name, "curl con manubri in piedi")
        self.assertEqual(info.exercises[0].volumes[0].weight, 10)
        self.assertEqual(info.exercises[0].volumes[0].reps, 10)
        self.assertEqual(info.exercises[1].volumes[0].weight, 10)
        self.assertEqual(info.exercises[1].volumes[0].reps, 10)

    def test_getinformations(self):
        file = Path("./tests/data/esempio.txt")
        info_generator = InfoGenerator()

        info = info_generator.load_sheet_person_from_exercises_file("Lorenzo", file)

        self.assertEqual(info.name, "Lorenzo")
        self.assertIsNotNone(info.exercises)
        self.assertEqual(len(info.exercises), 3)

        for exercise in info.exercises:
            self.assertIsNotNone(exercise.volumes)
            self.assertIsNot(exercise.volumes[0].weight, 0)
            self.assertIsNot(exercise.volumes[0].reps, 0)
