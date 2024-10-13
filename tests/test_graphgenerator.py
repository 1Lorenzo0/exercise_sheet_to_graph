import unittest
from datetime import datetime
from exercise_sheet_to_graph.models import Exercise, Volume
from exercise_sheet_to_graph.graph_creator import GraphCreator


class TestGraphCreator(unittest.TestCase):
    def setUp(self):
        # Create a sample exercise with volumes
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
        self.graph_creator = GraphCreator()

    def test_create_volume_graph(self):
        # Create the graph
        fig = self.graph_creator.create_volume_graph(self.exercise)

        # Check if the figure is created
        self.assertIsNotNone(fig)
        self.assertEqual(fig.data[0].name, "Bench Press")
        self.assertEqual(len(fig.data[0].x), 5)
        self.assertEqual(len(fig.data[0].y), 5)
        self.assertEqual(fig.layout.title.text, "Volume Over Time for Bench Press")
        self.assertEqual(fig.layout.xaxis.title.text, "Time")
        self.assertEqual(fig.layout.yaxis.title.text, "Volume (Reps x Kg)")

    def test_create_weight_per_reps_graph(self):
        # Create the graph
        fig = self.graph_creator.create_weight_per_reps_graph(self.exercise, 10)

        # Check if the figure is created
        self.assertIsNotNone(fig)
        self.assertEqual(fig.data[0].name, "Bench Press - 10 Reps")
        self.assertEqual(len(fig.data[0].x), 3)
        self.assertEqual(len(fig.data[0].y), 3)
        self.assertEqual(fig.layout.title.text, "Weight Over Time for Bench Press - 10 Reps")
        self.assertEqual(fig.layout.xaxis.title.text, "Time")
        self.assertEqual(fig.layout.yaxis.title.text, "Weight (Kg)")

    def test_create_reps_per_weight_graph(self):
        # Create the graph
        fig = self.graph_creator.create_reps_per_weight_graph(self.exercise, 100)

        # Check if the figure is created
        self.assertIsNotNone(fig)
        self.assertEqual(fig.data[0].name, "Bench Press - 100 Kg")
        self.assertEqual(len(fig.data[0].x), 3)
        self.assertEqual(len(fig.data[0].y), 3)
        self.assertEqual(fig.layout.title.text, "Reps Over Time for Bench Press - 100 Kg")
        self.assertEqual(fig.layout.xaxis.title.text, "Time")
        self.assertEqual(fig.layout.yaxis.title.text, "Reps")

    def test_show_weight_per_reps_graph(self):
        # Check if the method runs without errors
        self.graph_creator.show_weight_per_reps_graph(self.exercise, 10)

    def test_show_volume_graph(self):
        # Check if the method runs without errors
        self.graph_creator.show_volume_graph(self.exercise)

    def test_show_reps_per_weight_graph(self):
        # Check if the method runs without errors
        self.graph_creator.show_reps_per_weight_graph(self.exercise, 100)