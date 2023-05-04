# import libraries
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime 
import smtplib
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    def __repr__(self):
        return '<Name %r>' %self.text
    
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
    comments = db.relationship('Comments', backref='user', lazy=True)
    def __repr__(self):
        return '<Name %r>' %self.f_name

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    rejected = db.Column(db.Boolean)
    date_registered = db.Column(db.Date, default=datetime.date.today())
    memo = db.Column(db.String(300))
    def __repr__(self):
        return '<Name %r>' %self.email

class Banned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_registered = db.Column(db.Date, default=datetime.date.today())

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable =False)
    discounts = db.Column(db.Float, nullable=False, default=0.0)
    type_name = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.Date, default=datetime.date.today())
    comments = db.relationship('Comments', backref='product', lazy=True)

class Shopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer)
    #purchased = db.Column(db.Boolean, default=False)
    

class Purchased(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    product = db.Column(db.String(250), unique=True, nullable=False)
    #date_purchased = db.Column(db.Date, default=datetime.date.today())


class Taboo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False) 


#class Specs(db.Model)


    




 
  
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
    cpu_products = Product.query.order_by(Product.type_name=='cpu')
    return render_template("cpu.html", products=cpu_products)

@app.route("/cooling/")
def cooling():
    cpu_products = Product.query.order_by(Product.type_name=='cooling')
    return render_template("cooling.html", products=cpu_products)

@app.route("/gpu/")
def gpu():
    cpu_products = Product.query.order_by(Product.type_name=='gpu')
    return render_template("gpu.html", products=cpu_products)

@app.route("/motherboard/")
def cpu():
    cpu_products = Product.query.order_by(Product.type_name=='motherboard')
    return render_template("motherboard.html", products=cpu_products)

@app.route("/memory/")
def cpu():
    cpu_products = Product.query.order_by(Product.type_name=='memory')
    return render_template("memory.html", products=cpu_products)

@app.route("/storage/")
def cpu():
    cpu_products = Product.query.order_by(Product.type_name=='storage')
    return render_template("storage.html", products=cpu_products)

@app.route("/psu/")
def cpu():
    cpu_products = Product.query.order_by(Product.type_name=='psu')
    return render_template("psu.html", products=cpu_products)

@app.route("/case/")
def cpu():
    cpu_products = Product.query.order_by(Product.type_name=='case')
    return render_template("case.html", products=cpu_products)



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
            new_application = Application(email = rg_email, password=rg_password1, f_name = first_name, l_name = last_name, 
                                address = new_address, phone_number=new_phonenumber)
            existing_user = Application.query.filter_by(email=rg_email).first()
            if existing_user:
                return "You are already registered"
            try:
                db.session.add(new_application)
                db.session.commit()
                return redirect('/login')
            except:
                return "Something went wrong with registration. Please, try again."
    else:
        return render_template("signup.html")

# route product page
@app.route("/product/<int:id>", methods=['POST','GET'])
def product(id):
    product = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        if "comment-submit" in request.form:
            new_text = request.form['comment']
            if current_user.is_authenticated:
                new_comment = Comments(text=new_text, user_id=current_user.id,product_id = id)
            else:
                new_comment = Comments(text=new_text,product_id = id)
            try:
                db.session.add(new_comment)
                db.session.commit()
                return redirect(url_for('product',id=id))
            except:
                return "Comment was longer than 300 characters"
        elif "add-product" in request.form:
            #productTable = Product.query.filter_by(id = NULL).first()
            #new_product = Shopping(product = productTable)
            product = request.form['product']
            try:
                #db.session.add(new_product)
                db.session.commit()
                return "Added to cart"
            except:
                return "Invalid product"
            
        # Add product retrieves the product ID value in Prodcuts
        # Then it creates a new column in Shopping and sets the product atrribute in shapping to the product atrribute
        # in Produts 


    else:
        texts = Comments.query.filter_by(product_id=id).order_by(Comments.date_registered)
        return render_template("product.html", texts = texts, product=product)

@app.route("/add_product/", methods=['POST', 'GET'])
def add_product():
    if request.method=='POST':
        new_name = request.form['name']
        new_descrp = request.form['description']
        new_price = request.form['price']
        new_type_prod = request.form['type-name']
        existing_product = Product.query.filter_by(name = new_name).first()
        new_prod = Product(name=new_name, description=new_descrp, price=new_price, type_name=new_type_prod, discounts=0)
        if existing_product:
            return "This product already exists. Try a new one."
        try:
            db.session.add(new_prod)
            db.session.commit()
            return redirect('/user')
        except:
            return "Something went wrong when adding the product"
    return render_template("addproduct.html")
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
        curr_applications = Application.query.order_by(Application.date_registered)
            # display page for admin users
        return render_template("employee.html", applications=curr_applications)
    elif current_user.user_type == "SU":
        if request.method == 'POST':
            if 'add-product' in request.form:
                return redirect('/add_product/')
            elif 'delete-product' in request.form:
                return "Not available right now"
        rejected_applications = Application.query.order_by(Application.rejected==1)
            # display page for admin users
        return render_template("superuser.html", applications=rejected_applications)
    # if user is not logged in, redirect to login page
    return redirect(url_for('login'))

@app.route("/reject/<int:id>", methods=['POST','GET'])
def reject(id):
    if request.method =='POST':
        to_be_rejected = Application.query.filter_by(id=id).first()
        to_be_rejected.memo = request.form['memo']
        to_be_rejected.rejected = 1
        try:
            db.session.commit()
            return redirect('/user')
        except:
            return "Something went wrong rejecting the user."
    return render_template("memo.html")

@app.route("/review/<int:id>", methods=['POST','GET'])
def review(id):
    if request.method == 'POST':
        if "accept-EMPLY" in request.form or "reject-EMPLY" in request.form:
            if "accept-EMPLY" in request.form:
                to_be_added = Application.query.filter_by(id=id).first()
                new_user = User(email = to_be_added.email, password=to_be_added.password, f_name = to_be_added.f_name,
                                    l_name = to_be_added.l_name, address = to_be_added.address, phone_number=to_be_added.phone_number)
                try:
                    db.session.add(new_user)
                    db.session.delete(to_be_added)
                    db.session.commit()
                    return redirect('/user')
                except:
                    return "Something went wrong adding the user."
            elif "reject-EMPLY" in request.form:
                return redirect(url_for('reject', id =id))
        if "aprove-SU" in request.form or "disaprove-SU" in request.form:
            if "aprove-SU" in request.form:
                to_be_banned = Application.query.filter_by(id=id).first()
                banned_user = Banned(email = to_be_banned.email, f_name = to_be_banned.f_name,
                           l_name = to_be_banned.l_name)
                try:
                    db.session.add(banned_user)
                    db.session.delete(to_be_banned)
                    db.session.commit()
                    return redirect('/user')
                except:
                    return "Something went wrong aproving the rejection"
            elif "disaprove-SU" in request.form:
                to_be_added = Application.query.filter_by(id=id).first()
                new_user = User(email = to_be_added.email, password=to_be_added.password, f_name = to_be_added.f_name,
                                    l_name = to_be_added.l_name, address = to_be_added.address, phone_number=to_be_added.phone_number)
                try:
                    db.session.add(new_user)
                    db.session.delete(to_be_added)
                    db.session.commit()
                    return redirect('/user')
                except:
                    return "Something went wrong adding the user."
    return redirect('/user') 

# route create custombuilds page
@app.route("/createbuild/")
def createbuild():
    return render_template("createbuild.html")

# route recommended custombuilds page
@app.route("/recbuild/")
def recbuild():
    return render_template("recbuild.html")

# route user custombuilds page
@app.route("/userbuild/")
def userbuild():
    return render_template("userbuild.html")

# Run the app

@app.route("/createbuild/")
def createbuild():
    return render_template("createbuild.html")

# route recommended custombuilds page
@app.route("/recbuild/")
def recbuild():
    return render_template("recbuild.html")

# route user custombuilds page
@app.route("/userbuild/")
def userbuild():
    return render_template("userbuild.html")

if __name__ == "__main__":
    app.run(debug=True)



