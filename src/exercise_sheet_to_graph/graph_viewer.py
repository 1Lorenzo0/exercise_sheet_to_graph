from exercise_sheet_to_graph.graph_creator import GraphCreator
from exercise_sheet_to_graph.district_exercise_mapper import DistrictExerciseMapper
from exercise_sheet_to_graph.models import Exercise


class GraphViewer:
    def __init__(self, mapper: DistrictExerciseMapper):
        self.mapper = mapper
        self.graph_creator = GraphCreator(mapper)

    def show_volume_graph(self, exercise: Exercise) -> None:
        """
        Displays the graph showing the volume (Reps x Kg) over time for a given exercise.

        :param exercise: The Exercise object containing volume data.
        """
        fig = self.graph_creator.create_volume_graph(exercise)
        fig.show()

    def show_weight_per_reps_graph(self, exercise, reps) -> None:
        """
        Displays the graph showing the weight over time for a given exercise.

        :param exercise: The Exercise object containing weight data.
        :param reps: The specific number of reps to filter the data.
        """

        fig = self.graph_creator.create_weight_per_reps_graph(exercise, reps)
        fig.show()

    def show_reps_per_weight_graph(self, exercise, weight) -> None:
        """
        Displays the graph showing the reps over time for a given exercise.

        :param exercise: The Exercise object containing reps data.
        :param weight: The specific weight to filter the data.
        """
        fig = self.graph_creator.create_reps_per_weight_graph(exercise, weight)
        fig.show()
