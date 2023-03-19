# import libraries
from flask import Flask, render_template, Markup

# create flask app
app = Flask(__name__)

# route home/index page
@app.route("/")
def index():
    return render_template("index.html")

# route custom builds page
@app.route("/custombuilds/")
def custombuild():
    return render_template("custombuild.html")

# route cpu page
@app.route("/cpu/")
def cpu():
    return render_template("cpu.html")

# route cart page
@app.route("/cart/")
def cart():
    return render_template("cart.html")

# route login page
@app.route("/login/")
def login():
    return render_template("login.html")

# route user page
@app.route("/user/")
def user():
    return render_template("user.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
