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
    if request.method == "POST":
        load = False
        if "postpatch" in request.form:
            print("post patch test")
            # DB set up
            db = sqlite3.connect("wavewall.db")
            ex = db.cursor()
            # Patch name
            name = request.form.get("patchname")
            # Oscillator waveform
            waveform = request.form.get("wave")
            # Oscilator type and modulation if appliable
            wavetype = request.form.get("type")
            if wavetype == "fm":
                modulation = request.form.get("fm")
            elif wavetype == "am":
                modulation = request.form.get("am")
            else:
                modulation = ""
            # Filter section
            filterpass = request.form.get("filter")
            rolloff = request.form.get("roll")
            cutoff = request.form.get("cutoff")
            # Envelopes
            # Amplitude
            ampa = request.form.get("attacka")
            ampd = request.form.get("decaya")
            amps = request.form.get("sustaina")
            ampr = request.form.get("releasea")
            # Filter
            fila = request.form.get("attackf")
            fild = request.form.get("decayf")
            fils = request.form.get("sustainf")
            filr = request.form.get("releasef")
            # Effects
            # Chorus
            chorus = request.form.get("choruscheck")
            depthchorus = request.form.get("depthchorus")
            freqchorus = request.form.get("freqchorus")
            delaychorus = request.form.get("delaychorus")
            amountchorus = request.form.get("wetchorus")
            # Reverb
            reverb = request.form.get("reverbcheck")
            decayreverb = request.form.get("decayreverb")
            amountreverb = request.form.get("wetreverb")
            # Vibrato
            vibrato = request.form.get("vibratocheck")
            depthvibrato = request.form.get("depthvibrato")
            freqvibrato = request.form.get("freqvibrato")
            amountvibrato = request.form.get("wetvibrato")
            # Transposer
            transposer = request.form.get("transposer")
            # Volume
            volume = request.form.get("vol")

            # Patch must have a name
            if not request.form.get("patchname"):
                return error("must provide patch name", 403)

            rows = ex.execute("SELECT * FROM patches WHERE name=?",
                            (name, ))

            #  Patch name needs to be unique
            list_rows = rows.fetchall()
            name_check = empty(list_rows)
            if name_check == False:
                return error("Patch name is taken", 403)

            ex.execute("INSERT INTO patches (user_id, name, waveform, type, modulation, filter, rolloff, \
                        cutoff, ampa, ampd, amps, ampr, fila, fild, fils, filr, choruscheck, cdepth, cfreq, \
                        cdelay, camount, reverbcheck, rdecay, ramount, vibratocheck, vdepth, vfreq, vamount, transposer, volume) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
                        (session["user_id"], name, waveform, wavetype, modulation, filterpass, rolloff, cutoff, ampa, ampd, amps, ampr, \
                        fila, fild, fils, filr, chorus, depthchorus, freqchorus, delaychorus, amountchorus, reverb, decayreverb, amountreverb, \
                        vibrato, depthvibrato, freqvibrato, amountvibrato, transposer, volume))
            db.commit()
            db.close()
            return redirect(request.url)
        
        # Patch recovery
        if "getpatch" in request.form:
            load = True
            # DB set up
            db = sqlite3.connect("wavewall.db")
            ex = db.cursor()
            db.row_factory = sqlite3.Row
            # Patch name
            currentpatch = request.form.get("patches")
            if currentpatch == "":
                return redirect(request.url)
            else:
                # shows patch list with render_template
                row = ex.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
                r = row.fetchone()
                username = r[0]
                patchesload = ex.execute("SELECT name FROM patches WHERE user_id = ?", (session["user_id"],))
                p = patchesload.fetchall()
                patches = []
                for item in p:
                    for patch in item:
                        patches.append(patch)

                patchcall = ex.execute("SELECT waveform, type, modulation, filter, rolloff, \
                        cutoff, ampa, ampd, amps, ampr, fila, fild, fils, filr, choruscheck, cdepth, cfreq, \
                        cdelay, camount, reverbcheck, rdecay, ramount, vibratocheck, vdepth, vfreq, vamount, transposer, volume\
                        FROM patches WHERE name=?", (currentpatch,))
                patch = patchcall.fetchone()
            
                # Oscillator waveform
                waveform = patch[0]
                if waveform == "square":
                    square = True
                elif waveform == "sawtooth":
                    sawtooth = True
                elif waveform == "triangle":
                    triangle = True
                else:
                    sine = True
                # Oscilator type and modulation if appliable
                wavetype = patch[1] # can be empty
                if wavetype == "":
                    plain = True
                elif wavetype == "fat":
                    fat = True
                elif wavetype == "fm":
                    fm = True
                else:
                    am = True   
                modulation = patch[2] # can be empty
                if modulation == "square":
                    modsquare = True
                elif modulation == "sawtooth":
                    modsawtooth = True
                elif modulation == "triangle":
                    modtriangle = True
                else:
                    modsine = True
                # Filter section
                filterpass = patch[3]
                if filterpass == "lowpass":
                    lowpass = True
                elif filterpass == "bandpass":
                    bandpass = True
                else:
                    highpass = True

                rolloff = patch[4]
                if rolloff == "-12":
                    r12 = True
                elif rolloff == "-24":
                    r24 = True
                elif rolloff == "-48":
                    r48 = True
                else:
                    r96 = True

                cutoff = patch[5]
                # Envelopes
                # Amplitude
                ampa = patch[6]
                ampd = patch[7]
                amps = patch[8]
                ampr = patch[9]
                # Filter
                fila = patch[10]
                fild = patch[11]
                fils = patch[12]
                filr = patch[13]
                # Effects
                # Chorus
                chorus = patch[14]
                depthchorus = patch[15]
                freqchorus = patch[16]
                delaychorus = patch[17]
                amountchorus = patch[18]
                # Reverb
                reverb = patch[19]
                decayreverb = patch[20]
                amountreverb = patch[21]
                # Vibrato
                vibrato = patch[22]
                depthvibrato = patch[23]
                freqvibrato = patch[24]
                amountvibrato = patch[25]
                # Transposer
                transposer = patch[26]
                # Volume
                volume = patch[27]

                # Close db
                db.close()
                return render_template("synth.html", **locals())
    else:
        try:
            if session["user_id"]:
                db = sqlite3.connect("wavewall.db")
                db.row_factory = sqlite3.Row
                ex = db.cursor()
                row = ex.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
                r = row.fetchone()
                r.keys()
                username = r["username"]
                patchesload = ex.execute("SELECT name FROM patches WHERE user_id = ?", (session["user_id"],))
                p = patchesload.fetchall()
                patches = []
                for item in p:
                    for patch in item:
                        patches.append(patch)
                
                db.close()
                return render_template("synth.html", **locals())
        except:
            return render_template("synth.html")


@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        try:
            if session["user_id"]:
                patchname = request.form.get("patch")
                db = sqlite3.connect("wavewall.db")
                db.row_factory = sqlite3.Row
                ex = db.cursor()
                ex.execute("DELETE FROM patches WHERE user_id = ? AND name=?", (session["user_id"], patchname))
                db.commit()
                db.close()
                return redirect(request.url)
        except:
            return render_template("user.html")
        
    
    else:
        try:
            if session["user_id"]:
                db = sqlite3.connect("wavewall.db")
                db.row_factory = sqlite3.Row
                ex = db.cursor()
                row = ex.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
                r = row.fetchone()
                r.keys()
                username = r["username"]
                patchesload = ex.execute("SELECT name FROM patches WHERE user_id = ?", (session["user_id"],))
                p = patchesload.fetchall()
                patches = []
                for item in p:
                    for patch in item:
                        patches.append(patch)
                db.close()
                return render_template("user.html", **locals())
        except:
            return render_template("user.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Open db
        db = sqlite3.connect("wavewall.db")
        db.row_factory = sqlite3.Row
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
        rows = ex.execute("SELECT * FROM users WHERE username =?",
                          (username,))

        # Ensure username exists and password is correct
        r = rows.fetchone()
        r.keys()

        if r["username"] != username or check_password_hash(r["hash"], request.form.get("password")) == False:
            return error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = r["id"]
        db.close()
        # Redirect user to home page
        return redirect("/synth")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/synth")


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
    try:
        if session["user_id"]:
            db = sqlite3.connect("wavewall.db")
            db.row_factory = sqlite3.Row
            ex = db.cursor()
            row = ex.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
            r = row.fetchone()
            r.keys()
            username = r["username"]
            db.close()
            return render_template("about.html", **locals())
    except:
        return render_template("about.html")
    