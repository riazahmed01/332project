# import libraries
from flask import Flask, render_template, Markup

# create flask app
app = Flask(__name__)

# route home/index page
@app.route("/")
def index():
    return render_template("index.html")

# route login page
@app.route("/login/")
def login():
    return render_template("login.html")

# route user page
@app.route("/user/")
def user():
    return render_template("user.html")