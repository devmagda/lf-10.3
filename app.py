from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Example function to handle database connection
def get_db():
    return psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        database="dbdev"
    )

# User model
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Correct usage of @login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_users WHERE id = %s", (user_id,))
    user_row = cursor.fetchone()
    if user_row:
        return User(user_row[0], user_row[1], user_row[3])
    return None

# Function to check if a user exists
def user_exists(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_users WHERE username = %s", (username,))
    return cursor.fetchone() is not None

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE username = %s", (username,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row[2], password):
            user = User(user_row[0], user_row[1], user_row[3])
            login_user(user)
            return redirect(url_for('dashboard'))

        return "Login failed. Please try again."

    return render_template('login.html')

# Route for Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']

        if user_exists(username):
            return "User already exists."

        hashed_password = generate_password_hash(password)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tbl_users (username, password, role_id) VALUES (%s, %s, %s)",
                       (username, hashed_password, role_id))
        db.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for Dashboard (Requires login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Route for Logging Out
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title_short = request.form['title_short']
        title = request.form['title']
        description = request.form['description']
        owner = current_user.id  # Assuming the current user is the event owner

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO tbl_events (owner, title_short, title, description) 
            VALUES (%s, %s, %s, %s)
        """, (owner, title_short, title, description))
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('get_all_events'))

    return render_template('create_event.html')  # Create a form in 'create_event.html' for event creation

@app.route('/events/get_all', methods=['GET'])
def get_all_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_events")
    events = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('all_events.html', events=events)  # Create 'all_events.html' to list events

@app.route('/events/get/<int:event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbl_events WHERE id = %s", (event_id,))
    event = cursor.fetchone()
    cursor.close()
    db.close()

    if event:
        return render_template('event_detail.html', event=event)  # Create 'event_detail.html' to show event details
    else:
        return "Event not found", 404


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
