import plotly.graph_objects as go
from typing import List
from exercise_sheet_to_graph.models import Exercise


class GraphCreator:
    def __init__(self):
        pass

    def create_weight_per_reps_graph(self, exercise: Exercise, target_reps: int) -> go.Figure:
        """
        Creates a graph showing the weight used for a specific number of reps over time for a given exercise.

        :param exercise: The Exercise object containing weight and reps data.
        :param target_reps: The specific number of reps to filter the data.
        :return: A Plotly Figure object.
        """
        # Extract data
        times = [volume.ts for volume in exercise.volumes if volume.reps == target_reps]
        weights = [volume.weight for volume in exercise.volumes if volume.reps == target_reps]

        # Create the figure
        fig = go.Figure()

        # Add trace
        fig.add_trace(
            go.Bar(x=times, y=weights, name=f"{exercise.name} - {target_reps} Reps"))

        # Update layout
        fig.update_layout(
            title=f"Weight Over Time for {exercise.name} - {target_reps} Reps",
            xaxis_title="Time",
            yaxis_title="Weight (Kg)",
            xaxis=dict(
                type='category',
                tickmode='array',
                tickvals=times,
                ticktext=times
            ),
            yaxis=dict(
                tickmode='auto',
                nticks=40  # Adjust this value to control the number of ticks
            ),
            template="plotly_dark"
        )

        return fig

    def create_reps_per_weight_graph(self, exercise: Exercise, target_weight: int) -> go.Figure:
        """
        Creates a graph showing the reps performed for a specific weight over time for a given exercise.

        :param exercise: The Exercise object containing weight and reps data.
        :param target_weight: The specific weight to filter the data.
        :return: A Plotly Figure object.
        """
        # Extract data
        times = [volume.ts for volume in exercise.volumes if volume.weight == target_weight]
        reps = [volume.reps for volume in exercise.volumes if volume.weight == target_weight]

        # Create the figure
        fig = go.Figure()

        # Add trace
        fig.add_trace(
            go.Bar(x=times, y=reps, name=f"{exercise.name} - {target_weight} Kg"))

        # Update layout
        fig.update_layout(
            title=f"Reps Over Time for {exercise.name} - {target_weight} Kg",
            xaxis_title="Time",
            yaxis_title="Reps",
            xaxis=dict(
                type='category',
                tickmode='array',
                tickvals=times,
                ticktext=times
            ),
            yaxis=dict(
                tickmode='auto',
                nticks=40  # Adjust this value to control the number of ticks
            ),
            template="plotly_dark"
        )

        return fig

    def create_volume_graph(self, exercise: Exercise) -> go.Figure:
        """
        Creates a graph showing the volume (Reps x Kg) over time for a given exercise.

        :param exercise: The Exercise object containing volume data.
        :return: A Plotly Figure object.
        """
        # Extract data
        times = [volume.ts for volume in exercise.volumes]
        volumes = [volume.weight * volume.reps for volume in exercise.volumes]

        # Create the figure
        fig = go.Figure()

        # Add trace
        fig.add_trace(go.Scatter(x=times, y=volumes, mode='lines+markers', name=exercise.name))

        # Update layout
        fig.update_layout(
            title=f"Volume Over Time for {exercise.name}",
            xaxis_title="Time",
            yaxis_title="Volume (Reps x Kg)",
            template="plotly_dark"
        )

        return fig

    def show_volume_graph(self, exercise: Exercise) -> None:
        """
        Displays the graph showing the volume (Reps x Kg) over time for a given exercise.

        :param exercise: The Exercise object containing volume data.
        """
        fig = self.create_volume_graph(exercise)
        fig.show()

    def show_weight_per_reps_graph(self, exercise, reps):
        """
        Displays the graph showing the weight over time for a given exercise.

        :param exercise: The Exercise object containing weight data.
        :param reps: The specific number of reps to filter the data.
        """
        fig = self.create_weight_per_reps_graph(exercise, reps)
        fig.show()

    def show_reps_per_weight_graph(self, exercise, weight):
        """
        Displays the graph showing the reps over time for a given exercise.

        :param exercise: The Exercise object containing reps data.
        :param weight: The specific weight to filter the data.
        """
        fig = self.create_reps_per_weight_graph(exercise, weight)
        fig.show()
