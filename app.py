from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from tempfile import mkdtemp
from helpers import empty

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren"t cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/")
def main():
    return render_template("main.html")

@app.route("/error")
def error(message,number):
    return render_template("error.html")


@app.route("/synth", methods=["GET", "POST"])
def synth():
    return render_template("synth.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Open db
        db = sqlite3.connect("wavewall.db")
        ex = db.cursor()
        username = request.form.get("username")
        hashpass = generate_password_hash(request.form.get("password"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username =?",
                          (username,))

        # Ensure username exists and password is correct
        print(rows.fetchall()[1])
        #checker = rows.fe
        #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    return error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/synth")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    #Register user
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        db = sqlite3.connect("wavewall.db")
        ex = db.cursor()
        username = request.form.get("username")
        hashpass = generate_password_hash(request.form.get("password"))
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Password must match password confirmation
        elif request.form.get("password") != request.form.get("confirmpassword"):
            return error("passwords must match", 403)
        
        rows = ex.execute("SELECT * FROM users WHERE username=?",
                          (username, ))

        # -- username needs to be unique
        list_rows = rows.fetchall()
        username_check = empty(list_rows)
        if username_check == False:
            print("error")
            print(list_rows)
            return error("username is taken", 403)
            

        else:
            # -- password needs to be hashed and saved in the users table
            ex.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashpass))
            db.commit()
            db.close()
            return redirect("/synth")
    else:
    # when requested via GET display form similar to login.html + password confirmation
        return render_template("register.html")
    

@app.route("/about")
def about():
    return render_template("about.html")