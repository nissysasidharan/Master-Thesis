from flask import Flask, render_template, redirect, session, request, flash
from database import db, init_db, create_user, Users
import secrets
from config import DATABASE_CONFIG



app = Flask(__name__)
# Set the SQLALCHEMY_DATABASE_URI using the configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)


# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

# Initialize the database with the app
init_db(app)

@app.route('/')
def index():
    return render_template('home.html')

def create_user(username, email, password):
    try:
        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return True  # User created successfully
    except Exception as error:
        print(f"Error creating user: {error}")
        return False  # Error creating user


@app.route("/create_user", methods=["GET", "POST"])
def create_user_route():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database
        if create_user(username, email, password):
            # If user creation is successful, redirect to the dashboard
            session['username'] = username
            return redirect('/dashboard')
        else:
            # If user creation fails, show an error message
            flash("Error creating user")

    return render_template("home.html")
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect("/")

#Main Execution
if __name__ == "__main__":
    app.run(port=5001)
