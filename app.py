from flask import Flask, render_template

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

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/synth")
def synth():
    return render_template("synth.html")
