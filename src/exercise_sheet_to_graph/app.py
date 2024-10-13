from flask import Flask, request, render_template, url_for, redirect, session
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from exercise_sheet_to_graph.district_exercise_mapper import DistrictExerciseMapper
from exercise_sheet_to_graph.infosaver import InfoSaver
from exercise_sheet_to_graph.models import Exercise, Volume, SheetPerson
from exercise_sheet_to_graph.utils import normalize_string

app = Flask(__name__)
app.secret_key = "not_forever_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SqLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)


# with app.app_context():
#    db.create_all()

# Load the district and exercise mapper, load the info saver
exercise_mapper = DistrictExerciseMapper(config_path='../../config/district_and_exercise_italian.yaml')
info_saver = InfoSaver(base_dir=Path('../../db'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = normalize_string(request.form.get('username'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = normalize_string(request.form.get('name'))
        surname = normalize_string(request.form.get('surname'))

        if not username or not password or not name or not surname:
            error = 'Compila tutti i campi.'
            return render_template('register.html', error=error)

        if confirm_password != password:
            error = 'Le password non corrispondono.'
            return render_template('register.html', error=error)

        # Check if the username is already taken
        user = User.query.filter_by(username=username).first()
        if user:
            error = 'Username già in uso. Scegline un altro.'
            return render_template('register.html', error=error)

        # Create a new User instance
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            name=name,
            surname=surname
        )

        # Save the new user
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = normalize_string(request.form.get('username'))
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            error = 'Credenziali non valide. Riprova.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user = User.query.get(session.get('user_id'))

    districts = list(exercise_mapper.district_to_exercises.keys())
    exercises = list(exercise_mapper.exercises_to_district.keys())

    return render_template('index.html', districts=districts, exercises=exercises,
                           district_to_exercises=exercise_mapper.district_to_exercises,
                           exercises_to_district=exercise_mapper.exercises_to_district, user=user)


@app.route('/submit', methods=['POST'])
def submit():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        # Get data from form
        user = User.query.get(session['user_id'])
        name = user.name
        surname = user.surname

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

        # Save the data using InfoSaver
        info_saver.save_person(person)

        return f'Data saved for {person.name}'

    except ValidationError as e:
        return f'Data validation error: {e}', 400
    except Exception as e:
        return f'An unexpected error occurred: {e}', 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
