# import libraries
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import re

# create flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/ComputerStore'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

db = SQLAlchemy(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_registered = db.Column(db.Date, default=datetime.date.today()) 
    def __repr__(self):
        return '<Name %r>' %self.id
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(10), default="CU")
    banned = db.Column(db.Boolean, default=False)
    date_registered = db.Column(db.Date, default=datetime.date.today())
    compliments = db.Column(db.Integer, default=0)
    warnings = db.Column(db.Integer, default=0)
    balance = db.Column(db.Float, default=0.00)
    #shopping_cart = db.relationship('Product')
    def __repr__(self):
        return '<Name %r>' %self.f_name

class Banned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_registered = db.Column(db.Date, default=datetime.date.today())

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable =False)
    discounts = db.Column(db.Float, nullable=False, default=0.0)
    #comments = db.relationship('Comments')
    type_name = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.Date, default=datetime.date.today())

class Taboo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False) 
 
  
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

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    try:
        logout_user()
        session.clear()
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return "An error occurred while logging out."

# route login page
@app.route("/login/", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email_in = request.form['email']
        password_in = request.form['password']

        user = User.query.filter_by(email=email_in, password=password_in).first()
        banned = Banned.query.filter_by(email=email_in).first()
        if banned:
            return "Log In failed. Your account has been banned."
        elif user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Log In failed. Invalid Credentials."
    else:
        return render_template("login.html")

# route signup page

@app.route("/signup/",methods=['POST','GET'])
def signup():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        rg_email = request.form['email']
        rg_password1 = request.form['password1']
        rg_password2 = request.form['password2']
        new_address = request.form['address']
        new_phonenumber = request.form['phonenumber']
        email_validate_pattern = "^\S+@\S+\.\S+$"

        #handling post request
        if rg_password1 != rg_password2:
            return 'Passwords do not match'
        elif len(rg_password1) < 8:
            return 'Password must be at least 8 characters'
        #elif len(rg_email) < 4:
        elif not (bool(re.match(email_validate_pattern, rg_email))):
        #   return 'Email must be at least 3 characters'
            return 'Invalid format of email'
        elif len(new_phonenumber) > 10:
            return 'Invalid format of phone number'
        else:
            new_user = User(email = rg_email, password=rg_password1, f_name = first_name, l_name = last_name, 
                                address = new_address, phone_number=new_phonenumber)
            existing_user = User.query.filter_by(email=rg_email).first()
            if existing_user:
                return "You are already registered"
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
            except:
                return "Something went wrong with registration. Please, try again."
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
        texts = Comments.query.order_by(Comments.date_registered)
        return render_template("product.html", texts = texts)
# route user page
@app.route("/user/", methods=['POST','GET'])
@login_required
def user():    
    if current_user.user_type == "CU":
        if request.method == 'POST':
            new_email = request.form['email']
            new_password1 = request.form['password1']
            new_password2 = request.form['password2']
            new_address = request.form['address']
            new_phonenumber = request.form['phone']
            if new_email:
                if len(new_email) < 4:
                    return 'Email must be at least 3 characters'
                else: current_user.email = new_email
            if new_password1 and new_password2:
                if (new_password1 != new_password2):
                    return 'Passwords do not match'
                elif len(new_password1) < 8:
                    return 'Password must be at least 8 characters'
                else: current_user.password = new_password1
            if new_address:
                current_user.address = new_address
            if new_phonenumber:
                if len(new_phonenumber) > 10:
                    return 'Invalid format of phone number'
                else: current_user.phone_number = new_phonenumber
            try:
               db.session.commit()
               return "Information updated succesfully"
            except:
                return "Something went wrong. Try again!"
        else:
            # display page for regular customers
            return render_template("user.html", user=current_user)
        
    elif current_user.user_type == "EMPLY":
            # display page for admin users
        return render_template("employee.html", user=current_user)
    elif current_user.user_type == "SU":
            # display page for admin users
        return render_template("superuser.html", user=current_user)
    # if user is not logged in, redirect to login page
    return redirect(url_for('login'))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

