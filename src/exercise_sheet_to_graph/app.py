from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from pydantic import ValidationError
from datetime import timedelta  # Importa timedelta per il timeout della sessione
from exercise_sheet_to_graph.district_exercise_mapper import DistrictExerciseMapper
from exercise_sheet_to_graph.infosaver import InfoSaver
from exercise_sheet_to_graph.models import Exercise, Volume, SheetPerson

app = Flask(__name__)
app.secret_key = 'to_a_better_key'

# Configura il database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Configura il timeout della sessione (esempio: 30 minuti)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return str(self.id)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        session.permanent = True  # Rende la sessione permanente per rispettare il timeout configurato
    return user


# Load the district and exercise mapper, load the info saver
exercise_mapper = DistrictExerciseMapper(config_path='../../config/district_and_exercise_italian.yaml')
info_saver = InfoSaver(base_dir=Path('../../db'))


class RegistrationForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Cognome', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Nome Utente', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrati')


class LoginForm(FlaskForm):
    username = StringField('Nome Utente', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Verifica se l'username è già in uso
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            error = 'Nome utente già in uso. Scegli un altro.'
            return render_template('register.html', form=form, error=error)

        # Crea un nuovo utente
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password_hash=hashed_password,
            name=form.name.data,
            surname=form.surname.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Cerca l'utente nel database
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            session.permanent = True  # Rende la sessione permanente al login
            return redirect(url_for('index'))
        else:
            error = 'Credenziali non valide. Riprova.'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Modifica della rotta '/' per mostrare il messaggio di benvenuto e le opzioni
@app.route('/', methods=['GET'])
@login_required
def index():
    name = current_user.name
    return render_template('home.html', name=name)


@app.route('/add_exercises', methods=['GET'])
@login_required
def add_exercises():
    districts = list(exercise_mapper.district_to_exercises.keys())
    exercises = list(exercise_mapper.exercises_to_district.keys())
    district_to_exercises = exercise_mapper.district_to_exercises
    exercises_to_district = exercise_mapper.exercises_to_district
    weights = [round(i * 2.5, 1) for i in range(1, 81)]  # Da 2.5 a 200 con incrementi di 2.5
    return render_template('index.html', districts=districts,
                           exercises=exercises,
                           district_to_exercises=district_to_exercises,
                           exercises_to_district=exercises_to_district,
                           weights=weights)


# Nuova rotta per il pannello di visualizzazione grafici
@app.route('/graphs', methods=['GET'])
@login_required
def graphs():
    return render_template('graphs.html')


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    try:
        name = current_user.name
        surname = current_user.surname

        exercise_list = []

        index = 1
        while f'exercises[{index}][name]' in request.form:
            exercise_name = request.form.get(f'exercises[{index}][name]')
            district = request.form.get(f'exercises[{index}][district]')
            reps = request.form.get(f'exercises[{index}][reps]')
            weight = request.form.get(f'exercises[{index}][weight]')

            volume = Volume(
                weight=float(weight),
                reps=int(reps)
            )

            exercise = Exercise(
                name=exercise_name,
                district=district,
                volumes=[volume]
            )

            exercise_list.append(exercise)
            index += 1

        person = SheetPerson(
            name=f"{name} {surname}",
            exercises=exercise_list
        )

        info_saver.save_person(person)

        return render_template('success.html', name=person.name)

    except ValidationError as e:
        return f'Errore di validazione dei dati: {e}', 400
    except Exception as e:
        return f'Si è verificato un errore inaspettato: {e}', 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
