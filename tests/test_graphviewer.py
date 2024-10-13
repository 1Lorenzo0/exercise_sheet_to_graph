import unittest
from datetime import datetime

from exercise_sheet_to_graph.GraphViewer import GraphViewer
from exercise_sheet_to_graph.models import Volume, Exercise


class TestGraphViewer(unittest.TestCase):

    def setUp(self):
        self.exercise = Exercise(
            name="Bench Press",
            volumes=[
                Volume(ts=str(datetime(2023, 1, 1)), weight=100, reps=10),
                Volume(ts=str(datetime(2023, 2, 1)), weight=105, reps=10),
                Volume(ts=str(datetime(2023, 3, 1)), weight=110, reps=10),
                Volume(ts=str(datetime(2023, 4, 1)), weight=100, reps=12),
                Volume(ts=str(datetime(2023, 5, 1)), weight=100, reps=14),
            ]
        )
        self.graph_viewer = GraphViewer()

    def test_show_weight_per_reps_graph(self):
        # Check if the method runs without errors
        self.graph_viewer.show_weight_per_reps_graph(self.exercise, 10)

    def test_show_volume_graph(self):
        # Check if the method runs without errors
        self.graph_viewer.show_volume_graph(self.exercise)

    def test_show_reps_per_weight_graph(self):
        # Check if the method runs without errors
        self.graph_viewer.show_reps_per_weight_graph(self.exercise, 100)
