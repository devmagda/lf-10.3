from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

# App Configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


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
    return get_user("id", user_id)


def get_user_by_username(username):
    return get_user("username", username)


def get_user(identifier, identity):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_users WHERE %s = %s", (identifier, identity))
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
    """, (owner_id, title_short, title, description))
    db.commit()
    cursor.close()
    db.close()


def get_selectable_roles():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ref_roles where role_id in (1, 2)")
    events = cursor.fetchall()
    cursor.close()
    db.close()
    return events


def get_event_by_id(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_events WHERE id = %s", (event_id,))
    event = cursor.fetchone()
    cursor.close()
    db.close()
    return event

@app.route('/')
def outer():
    # Simulate a condition for the value of x
    x = False  # or False depending on the condition
    return render_template('outer.html', x=x)


@app.route('/login', methods=['GET', 'POST'])
def get_post_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password_hash(user[2], password):
            user = User(user[0], user[1], user[3])
            login_user(user)
            return redirect(url_for('dashboard'))

        return "Login failed. Please try again."

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def get_post_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']

        if user_exists(username):
            return "User already exists."

        create_user(username, password, role_id)
        return redirect(url_for('login'))

    selectable_roles = get_selectable_roles()
    return render_template('register.html', selectable_roles=selectable_roles)


def get_register():
    return render_template('register.html')


@app.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
def get_logout():
    if request.method == 'POST':
        logout_user()
    return redirect(url_for('login'))


@app.route('/events/create', methods=['GET', 'POST'])
@login_required
def get_post_create_event():
    if request.method == 'POST':
        title_short = request.form['title_short']
        title = request.form['title']
        description = request.form['description']
        owner_id = current_user.id

        create_event(title_short, title, description, owner_id)

        return redirect(url_for('get_all_events'))

    return render_template('create_event.html')


@app.route('/events/get_all', methods=['GET'])
def get_get_all_events():
    events = get_all_events()

    return render_template('all_events.html', events=events)


@app.route('/roles', methods=['GET'])
def get_get_roles():
    events = get_all_roles()

    return events


@app.route('/events/get/<int:event_id>', methods=['GET'])
def get_get_event(event_id):
    event = get_event_by_id(event_id)

    if event:
        return render_template('event_detail.html', event=event)
    else:
        return "Event not found", 404


@app.route('/event-list', methods=['GET'])
def get_event_list():
    return render_template('event_list.html')


@app.route('/event/<string:event_name>', methods=['GET'])
def get_event_detail(event_name):
    return render_template('event_detail.html', event_name=event_name)


@app.route('/team', methods=['GET'])
def get_team():
    return render_template('team.html')


@app.route('/imprint', methods=['GET'])
def get_imprint():
    return render_template('imprint.html')


@app.route('/terms-and-conditions', methods=['GET'])
def get_terms_and_conditions():
    return render_template('terms_and_conditions.html')


if __name__ == '__main__':
    app.run(debug=True)
