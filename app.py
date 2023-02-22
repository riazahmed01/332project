from flask import Flask, render_template, redirect, url_for, Markup
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"