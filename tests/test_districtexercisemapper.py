import unittest
from unittest.mock import patch, mock_open
from exercise_sheet_to_graph.district_exercise_mapper import DistrictExerciseMapper


class TestDistrictExerciseMapper(unittest.TestCase):
    config_data = '''
        {
            "district_to_exercises": {
                "district1": ["exercise1", "exercise2"],
                "district2": ["exercise3"]
            },
            "exercises_to_district": {
                "exercise1": "district1",
                "exercise2": "district1",
                "exercise3": "district2"
            }
        }
        '''

    def setUp(self):
        self.config_data = '''
        {
            "district_to_exercises": {
                "district1": ["exercise1", "exercise2"],
                "district2": ["exercise3"]
            },
            "exercises_to_district": {
                "exercise1": "district1",
                "exercise2": "district1",
                "exercise3": "district2"
            }
        }
        '''
        self.mapper = None

    @patch("builtins.open", new_callable=mock_open,
           read_data='{"district_to_exercises": {}, "exercises_to_district": {}}')
    def test_init_empty_config(self, mock_file):
        self.mapper = DistrictExerciseMapper("dummy_path")
        self.assertEqual(self.mapper.district_to_exercises, {})
        self.assertEqual(self.mapper.exercises_to_district, {})

    @patch("builtins.open", new_callable=mock_open, read_data=config_data)
    def test_init_with_config(self, mock_file):
        self.mapper = DistrictExerciseMapper("dummy_path")
        self.assertEqual(self.mapper.district_to_exercises["district1"], ["exercise1", "exercise2"])
        self.assertEqual(self.mapper.exercises_to_district["exercise3"], "district2")

    @patch("builtins.open", new_callable=mock_open, read_data=config_data)
    def test_get_exercise_by_district(self, mock_file):
        self.mapper = DistrictExerciseMapper("dummy_path")
        self.assertEqual(self.mapper.get_exercise_by_district("district1"), ["exercise1", "exercise2"])
        self.assertIsNone(self.mapper.get_exercise_by_district("nonexistent_district"))

    @patch("builtins.open", new_callable=mock_open, read_data=config_data)
    def test_get_district_by_exercise(self, mock_file):
        self.mapper = DistrictExerciseMapper("dummy_path")
        self.assertEqual(self.mapper.get_district_by_exercise("exercise1"), "district1")
        self.assertIsNone(self.mapper.get_district_by_exercise("nonexistent_exercise"))

    @patch("builtins.open", new_callable=mock_open, read_data=config_data)
    def test_add_exercise_to_district(self, mock_file):
        self.mapper = DistrictExerciseMapper("dummy_path")
        self.mapper.add_exercise_to_district("district1", "exercise4")
        self.assertIn("exercise4", self.mapper.district_to_exercises["district1"])
        self.assertEqual(self.mapper.exercises_to_district["exercise4"], "district1")

    @patch("builtins.open", new_callable=mock_open, read_data=config_data)
    def test_remove_exercise_from_district(self, mock_file):
        self.mapper = DistrictExerciseMapper("dummy_path")
        self.mapper.remove_exercise_from_district("district1", "exercise1")
        self.assertNotIn("exercise1", self.mapper.district_to_exercises["district1"])
        self.assertNotIn("exercise1", self.mapper.exercises_to_district)


if __name__ == "__main__":
    unittest.main()
