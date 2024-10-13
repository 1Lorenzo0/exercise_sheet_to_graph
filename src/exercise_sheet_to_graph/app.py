from flask import Flask, request, render_template
import yaml
from datetime import datetime
from pydantic import ValidationError
from exercise_sheet_to_graph.district_exercise_mapper import DistrictExerciseMapper
from exercise_sheet_to_graph.models import Exercise, Volume, SheetPerson
from exercise_sheet_to_graph.utils import normalize_string

app = Flask(__name__)

# Load the district and exercise mapper
exercise_mapper = DistrictExerciseMapper(config_path='../../config/district_and_exercise_italian.yaml')

@app.route('/', methods=['GET'])
def index():
    districts = list(exercise_mapper.district_to_exercises.keys())
    exercises = list(exercise_mapper.exercises_to_district.keys())

    return render_template('index.html', districts=districts, exercises=exercises,
                           district_to_exercises=exercise_mapper.district_to_exercises,
                           exercises_to_district=exercise_mapper.exercises_to_district)


@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get data from form
        name = normalize_string(request.form.get('name'))
        surname = normalize_string(request.form.get('surname'))

        exercise_list = []

        index = 1
        while f'exercises[{index}][name]' in request.form:
            exercise_name = request.form.get(f'exercises[{index}][name]')
            district = request.form.get(f'exercises[{index}][district]')
            reps = request.form.get(f'exercises[{index}][reps]')
            weight = request.form.get(f'exercises[{index}][weight]')

            # Create an instance of Volume
            volume = Volume(
                weight=int(weight),
                reps=int(reps)
            )

            # Create an instance of Exercise
            exercise = Exercise(
                name=exercise_name,
                district=district,
                volumes=[volume]
            )

            exercise_list.append(exercise)
            index += 1

        # Create an instance of SheetPerson
        person = SheetPerson(
            name=f"{name} {surname}",
            exercises=exercise_list
        )

        # Serialize data to YAML
        yaml_data = yaml.safe_dump(person.dict(), allow_unicode=True)

        # Save the data to a YAML file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'../db/data_{timestamp}_{name}_{surname}.yaml'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(yaml_data)

        return f'Data saved successfully in file {filename}'

    except ValidationError as e:
        return f'Data validation error: {e}', 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
