from enum import Enum

import psycopg2
import sass
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# App Configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


# Define the paths for SCSS and CSS files
scss_file = 'static/scss/styles.scss'
css_file = 'static/css/styles.css'


def compile_scss():
    try:
        # Compile SCSS to CSS
        css = sass.compile(filename=scss_file)

        # Write the compiled CSS to a file
        with open(css_file, 'w') as file:
            file.write(css)

        print('SCSS compiled to CSS successfully.')
    except Exception as e:
        print(f'Error compiling SCSS: {e}')


class Event:
    def __init__(self, id, owner_username, title, title_short, description, subscriptions=None):
        self.id = id
        self.owner_username = owner_username
        self.title = title
        self.title_short = title_short
        self.description = description
        self.subscriptions = subscriptions if subscriptions is not None else []

    def get_subscriptions(self):
        return ', '.join(self.subscriptions)

    @classmethod
    def from_sql_data(cls, event, subscriptions):
        id = event[0]
        owner_username = event[5]  # Owner's username is now in event[5] due to the LEFT JOIN
        title_short = event[2]
        title = event[3]
        description = event[4]

        # Convert the subscriptions tuples into a flat list of usernames
        subscription_list = [sub[0] for sub in subscriptions]

        return cls(id, owner_username, title, title_short, description, subscription_list)

    @classmethod
    def from_id(cls, event_id):
        # Fetch event data by event_id
        event_data = get_event_by_id(event_id)

        # Fetch subscriptions for the event
        subscriptions_data = get_event_subscriptions(event_id)

        # Use from_sql_data to return a new Event object
        return cls.from_sql_data(event_data, subscriptions_data)


class UserRole(Enum):
    ADMIN = 3
    CREATOR = 2
    USER = 1
    GUEST = 0

    @staticmethod
    def get_by_id(role_id):
        for role in UserRole:
            if role.value == role_id:
                return role
        raise ValueError(f"Invalid role ID: {role_id}")


class View(Enum):
    HOME = 'home'
    LOGIN = 'login'
    REGISTER = 'register'
    TERMS = 'terms-and-conditions'
    IMPRINT = 'imprint'
    TEAM = 'team'
    EVENT_ALL = 'all-events'
    EVENT_SINGLE = 'single-event'
    EVENT_CREATE = 'event-create'


class SessionManager:
    @staticmethod
    def set_focused_event_id(event_id):
        session['focused_event_id'] = event_id

    @staticmethod
    def get_focused_event_id():
        view_value = session.get('focused_event_id', None)
        return view_value

    @staticmethod
    def set_view(view: View):
        session['view'] = view.value  # Store only the value of the enum

    @staticmethod
    def get_view():
        view_value = session.get('view', View.HOME.value)  # Default to HOME if 'view' is not set
        return View(view_value)  # Convert the stored value back to a View enum

    @staticmethod
    def get_user_role():
        return UserRole.get_by_id(session.get('role', UserRole.GUEST.value))

    @staticmethod
    def set_user_role(role: UserRole):
        session['role'] = role.value


# Login Configurations
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    user_row = get_user_by_id(user_id)
    if user_row:
        return User(user_row[0], user_row[1], user_row[3])
    return None


# Database Functions
def get_db():
    return psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        database="dbdev"
    )


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_users WHERE id = %s", (user_id,))
    user_row = cursor.fetchone()
    cursor.close()
    db.close()
    return user_row


def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_users WHERE username = %s", (username,))
    user_row = cursor.fetchone()
    cursor.close()
    db.close()
    return user_row


def user_exists(username):
    user = get_user_by_username(username)
    return user is not None


def create_user(username, password, role_id):
    hashed_password = generate_password_hash(password)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tbl_users (username, password, role_id) VALUES (%s, %s, %s)",
                   (username, hashed_password, role_id))
    db.commit()
    cursor.close()
    db.close()


def get_all_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_events")
    events = cursor.fetchall()
    cursor.close()
    db.close()
    return events


def get_all_events_with_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT e.*, u.username FROM tbl_events e LEFT JOIN tbl_users u ON e.owner = u.id")
    events_users = cursor.fetchall()
    cursor.close()
    db.close()
    return events_users


def get_all_roles():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ref_roles")
    events = cursor.fetchall()
    cursor.close()
    db.close()
    return events


def create_event(title_short, title, description, owner_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO tbl_events (owner, title_short, title, description) 
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (owner_id, title_short, title, description))

    # Fetch the ID of the newly created event
    event_id = cursor.fetchone()[0]

    db.commit()
    cursor.close()
    db.close()

    return event_id


def subscribe(event_id, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO tbl_event_subscriptions (event_id, user_id) 
        VALUES (%s, %s)
    """, (event_id, user_id))
    db.commit()
    cursor.close()
    db.close()


def get_event_subscriptions(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "select u.username from tbl_event_subscriptions s left join tbl_users u on s.user_id = u.id where s.event_id = %s",
        (event_id,))
    subscriptions = cursor.fetchall()
    cursor.close()
    db.close()
    return subscriptions


def get_selectable_roles():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ref_roles where id in (1, 2)")
    events = cursor.fetchall()
    cursor.close()
    db.close()
    return events


def get_event_by_id(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT e.*, u.username FROM tbl_events e LEFT JOIN tbl_users u ON e.owner = u.id WHERE e.id = %s",
                   (event_id,))
    event = cursor.fetchone()
    cursor.close()
    db.close()
    return event


def get_event_ids():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM tbl_events ORDER BY id DESC")
    events = cursor.fetchall()
    cursor.close()
    db.close()
    return events


def get_combined_events():
    all_event_ids = get_event_ids()
    all_events = []
    for event_id in all_event_ids:
        event = Event.from_id(event_id)
        all_events.append(event)
    return all_events


@app.route('/')
def index():
    view_name = SessionManager.get_view().name
    role_id = SessionManager.get_user_role().value
    events = None
    focused_event_id = SessionManager.get_focused_event_id()
    focused_event = None

    if role_id >= UserRole.USER.value:
        events = get_combined_events()

    if view_name == View.EVENT_SINGLE.name and focused_event_id is not None:
        focused_event = Event.from_id(focused_event_id)

    return render_template('index.html', view=view_name, role=role_id, event_list=events, focused_event=focused_event)


@app.route('/outer')
def outer():
    # Simulate a condition for the value of x
    x = False  # or False depending on the condition
    return render_template('outer.html', x=x)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password_hash(user[2], password):
            user = User(user[0], user[1], user[3])
            login_user(user)
            SessionManager.set_user_role(UserRole.get_by_id(user.role))
            SessionManager.set_view(View.HOME)
            return redirect(url_for('index'))

        return "Login failed. Please try again.", 500

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']

        if user_exists(username):
            return "User already exists."

        create_user(username, password, role_id)

        SessionManager.set_view(View.LOGIN)

        return redirect(url_for('index'))

    selectable_roles = get_selectable_roles()
    return render_template('register.html', selectable_roles=selectable_roles)


@app.route('/subscribe', methods=['POST'])
@login_required
def post_subscribe():
    try:
        # Get event_id and user_id from the form
        event_id = request.form.get('event_id')
        user_id = request.form.get('user_id')

        # Check if event_id and user_id are provided
        if not event_id or not user_id:
            return "event_id and user_id are required", 400

        # Call the function to subscribe
        subscribe(event_id, user_id)

        return "Subscription successful", 200
    except Exception as e:
        return str(e), 500


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    SessionManager.set_user_role(UserRole.GUEST)
    SessionManager.set_view(View.HOME)
    return redirect(url_for('index'))


@app.route('/events/create', methods=['POST'])
@login_required
def get_post_create_event():
    title_short = request.form['title_short']
    title = request.form['title']
    description = request.form['description']
    owner_id = current_user.id

    event_id = create_event(title_short, title, description, owner_id)

    SessionManager.set_view(View.EVENT_SINGLE)
    SessionManager.set_focused_event_id(event_id)

    return redirect(url_for('index'))


@app.route('/events/get_all', methods=['GET'])
def get_get_all_events():
    events = get_all_events()

    return render_template('all_events.html', events=events)


@app.route('/roles', methods=['GET'])
def get_get_roles():
    events = get_all_roles()

    return events


@app.route('/events/<int:event_id>', methods=['POST'])
@login_required
def get_event(event_id):
    SessionManager.set_focused_event_id(event_id)
    SessionManager.set_view(View.EVENT_SINGLE)
    return redirect(url_for('index'))


@app.route('/event-list', methods=['GET'])
def get_event_list():
    return render_template('event_list.html')


@app.route('/team', methods=['GET'])
def get_team():
    return render_template('team.html')


@app.route('/imprint', methods=['GET'])
def get_imprint():
    return render_template('imprint.html')


@app.route('/terms-and-conditions', methods=['GET'])
def get_terms_and_conditions():
    return render_template('terms_and_conditions.html')


@app.route('/view/<view_name>', methods=['POST'])
def set_view(view_name):
    try:
        view = View(view_name)
        SessionManager.set_view(view)
    except ValueError:
        return "Invalid view", 404  # Handle invalid view names

    # Redirect to a default page or a page based on the view
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
