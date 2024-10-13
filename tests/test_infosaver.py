from pathlib import Path
import os
from exercise_sheet_to_graph.infosaver import InfoSaver
from exercise_sheet_to_graph.infogenerator import InfoGenerator
import unittest


class TestInfoSaver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.info_generator = InfoGenerator()
        cls.name_person = "Lorenzo"

        cls.info = cls.info_generator.load_sheet_person_from_exercises_file("Lorenzo", Path("./tests/data/esempio.txt"))
        cls.key = "12345678".encode()
        cls.saver = InfoSaver(Path("./tests/data/db"))

    @classmethod
    def tearDownClass(cls):
        os.remove(Path("./tests/data/db/Lorenzo.json"))

    def test_saveperson(self):
        self.saver.save_person(info_person=self.info)

        new_info = self.info_generator.load_sheet_person_from_exercises_file("Lorenzo",
                                                                             Path("./tests/data/esempio2.txt"))

        self.saver.save_person(info_person=new_info)
        self.assertTrue(True)

    def test_loadperson(self):
        self.saver.save_person(info_person=self.info)
        person = self.saver.load_person(name=self.info.name)
        self.assertIsNotNone(person)

        self.assertEqual(person.name, "Lorenzo")
        self.assertEqual(person.exercises[0].name, "Panca piana")
        print(person)
        self.assertEqual(person.exercises[0].volumes[0].weight, 60)
        print(person)
