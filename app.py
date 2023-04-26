# import libraries
from flask import Flask, redirect, render_template, Markup, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
# create flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/ComputerStore'

db = SQLAlchemy(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Name %r>' %self.id
registered_users = dict()
  
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
@app.route("/login/", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email_in = request.form['email']
        password_in = request.form['password']
        if (email_in in registered_users.keys()) and (registered_users[email_in] == password_in):
            username = email_in
            return render_template("index.html")
        else:
            return "Log In failed. You are not registered."
    else:
        return render_template("login.html")

# route signup page

@app.route("/signup/",methods=['POST','GET'])
def signup():
    if request.method == "POST":
        rg_email = request.form['email']
        rg_password = request.form['password']
        
        if rg_email not in registered_users.keys():
            registered_users[rg_email] = rg_password
            return redirect('/login')
        else:
            return "Email already registered"
    else:
        return render_template("signup.html")

# route product page
@app.route("/product/", methods=['POST','GET'])
def product():
    if request.method == "POST":
        guest_text = request.form['comment']
        new_text = Comments(text=guest_text)

        try:
            db.session.add(new_text)
            db.session.commit()
            return redirect('/product')
        except:
            return "Comment was longer than 300 characters"
    else:
        texts = Comments.query.order_by(Comments.date_created)
        return render_template("product.html", texts = texts)
# route user page
@app.route("/user/")
def user():
    return render_template("user.html")

# route employee page
@app.route("/employee/")
def employee():
    return render_template("employee.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
