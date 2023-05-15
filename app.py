# import libraries
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import re

from sqlalchemy import or_

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
        return '<Name %r>' % self.text


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
    payment_methods = db.relationship('PaymentMethod', backref='product', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.f_name


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
    model = db.Column(db.String(100), nullable=False)
    type_name = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(250), unique=True, nullable=False)
    image = db.Column(db.String(250))
    price = db.Column(db.Float, nullable =False)
    power = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    discounts = db.Column(db.Float, default=0.0)
    in_stock = db.Column(db.Boolean, default = True)
    form_factor = db.Column(db.String(50))
    date_registered = db.Column(db.Date, default=datetime.date.today())
    comments = db.relationship('Comments', backref='product', lazy=True)
    rating = db.relationship('Rating', backref='product', lazy=True)


class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    card_type = db.Column(db.String(20), nullable=False)
    expiration_date = db.Column(db.String(7), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f'<PaymentMethod {self.card_type} {self.card_number}>'

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1)

class Purchased(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    cb_id = db.Column(db.Integer)
    date_purchased = db.Column(db.Date, default=datetime.date.today())


class Taboo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False) 


class Specs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    cpu_support = db.Column(db.Text)
    bios_update = db.Column(db.Text)
    m2_support = db.Column(db.Integer)
    ssd_hard_drive_support = db.Column(db.Integer)
    pclex16_slots = db.Column(db.Integer)
    memory_type = db.Column(db.String(20))
    memory_slots = db.Column(db.Integer)


class CustomBuild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    build_type = db.Column(db.String(50))
    cpu_id = db.Column(db.Integer)
    cooler_id = db.Column(db.Integer)
    motherboard_id = db.Column(db.Integer)
    RAM_id = db.Column(db.Integer)
    m2_id = db.Column(db.Integer)
    GPU_id = db.Column(db.Integer)
    PSU_id = db.Column(db.Integer)
    case_id = db.Column(db.Integer)
    price = db.Column(db.Float, default = 0)
    power_supply = db.Column(db.Integer)
    ssd_hdd_drive_id = db.Column(db.Integer)
    m2_quantity = db.Column(db.Integer)
    ssd_hdd_drive_quantity = db.Column(db.Integer)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

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
    cpu_products = Product.query.filter_by(type_name = 'cpu')
    return render_template("pcproducts.html", products=cpu_products)

# route cooling page
@app.route("/cooling/")
def cooling():
    cooling_products = Product.query.filter_by(type_name='cooler')
    return render_template("pcproducts.html", products=cooling_products)

# route gpu page
@app.route("/gpu/")
def gpu():
    gpu_products = Product.query.filter_by(type_name='GPU')
    return render_template("pcproducts.html", products=gpu_products)


# route motherboard page
@app.route("/motherboard/")
def motherboard():
    motherboard_products = Product.query.filter_by(type_name='motherboard')
    return render_template("pcproducts.html", products=motherboard_products)


# route memory page
@app.route("/memory/")
def memory():
    memory_products = Product.query.filter_by(type_name='RAM')
    return render_template("pcproducts.html", products=memory_products)

# route storage page
@app.route("/storage/")
def storage():
    storage_products = Product.query.filter(or_(Product.type_name == 'm2', Product.type_name == 'ssd_hard_drive')).all()
    return render_template("pcproducts.html", products=storage_products)
  
# route psu page
@app.route("/psu/")
def psu():
    psu_products = Product.query.filter_by(type_name='PSU')
    return render_template("pcproducts.html", products=psu_products)

# route case page
@app.route("/case/")
def case():
    case_products = Product.query.filter_by(type_name ='case')
    return render_template("pcproducts.html", products=case_products)

@app.route("/laptops/")
def laptops():
    laptop_products = Product.query.filter_by(type_name ='laptop')
    return render_template("pcproducts.html", products=laptop_products)

@app.route("/other/")
def other():
    other_products = Product.query.filter_by(type_name = 'other')
    return render_template("pcproducts.html", products=other_products)

# route cart page
@app.route("/cart/", methods=['GET', 'POST'])
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id)
    product_ids = [item.product_id for item in cart_items]
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    
    prices = [product.price for product in products]
    tprice = 0.00
    for price in prices:
        tprice+=price
    
    cart_dict = {}
    for item in cart_items:
        for product in products:
            if item.product_id == product.id:
                cart_dict[product] = item
    return render_template("cart.html", cart=cart_dict, total=tprice)

@app.route("/changecart/<int:id>/", methods=['GET', 'POST'])
def changecart(id):
    item = Cart.query.filter_by(user_id=current_user.id, product_id=id).first()
    if request.method == 'POST':
        option = request.form.get('change-q')
        if option == 'add1':
            item.quantity += 1
        elif option == 'remove1' and item.quantity >= 1:
            item.quantity -= 1  
        if item.quantity==0:
            db.session.delete(item)  
        try:
            db.session.commit()
            return redirect('/cart/')
        except:
            return 'Something went wrong modifying the cart'
    else:
        return 'Invalid request method'

@app.route("/deletecart/<int:id>/", methods=['GET', 'POST'])
def deletecart(id):
    item = Cart.query.get(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/cart/')
    except:
        return 'Something went wrong deleting the product'

# route logout page
@app.route('/logout', methods=['GET', 'POST'])
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
@app.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email_in = request.form['email']
        password_in = request.form['password']
        user = User.query.filter_by(email=email_in, password=password_in).first()
        if user.user_type == "CU" and user.warnings == 3:
            banned_user = Banned(
                email=user.email,
                f_name=user.f_name,
                l_name=user.l_name
            )
            db.session.add(banned_user)
            db.session.commit()
        if user.user_type == "EMPLY" and user.warnings >=6:
            banned_user = Banned(
                email=user.email,
                f_name=user.f_name,
                l_name=user.l_name
            )
            db.session.add(banned_user)
            db.session.commit()
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
@app.route("/signup/", methods=['POST', 'GET'])
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

        # handling post request
        if rg_password1 != rg_password2:
            return 'Passwords do not match'
        elif len(rg_password1) < 8:
            return 'Password must be at least 8 characters'
        # elif len(rg_email) < 4:
        elif not (bool(re.match(email_validate_pattern, rg_email))):
            #   return 'Email must be at least 3 characters'
            return 'Invalid format of email'
        elif len(new_phonenumber) > 10:
            return 'Invalid format of phone number'
        else:
            new_application = Application(email=rg_email, password=rg_password1, f_name=first_name, l_name=last_name, address=new_address, phone_number=new_phonenumber)
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
    

# route add_payment_method page
@app.route('/add_payment_method', methods=['GET', 'POST'])
@login_required
def add_payment():
    if request.method == 'POST':
        user_id = current_user.id
        card_number = request.form['card_number']
        card_type = request.form['card_type']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']

        payment_method = PaymentMethod(
            user_id=user_id,
            card_number=card_number,
            card_type=card_type,
            expiration_date=expiration_date,
            cvv=cvv
        )

        db.session.add(payment_method)
        db.session.commit()

        return redirect(url_for('user'))

    else:
        return render_template('payment_methods.html')

# route delete_payment_method page
@app.route('/delete_payment_method/<int:payment_method_id>', methods=['POST'])
@login_required
def delete_payment_method(payment_method_id):
    payment_method = PaymentMethod.query.get(payment_method_id)
    if payment_method and payment_method.user_id == current_user.id:
        db.session.delete(payment_method)
        db.session.commit()
    return redirect(url_for('user'))

# route deposit page
@app.route("/deposit/", methods=['POST', 'GET'])
@login_required
def deposit():
    if request.method == 'POST':
        amount = request.form['amount']
        current_user.balance += float(amount)
        db.session.commit()
        success = f"You have successfully deposited ${amount}!"
        return render_template("deposit.html", success=success)
    else:
        return render_template("deposit.html")

# route withdraw page
@app.route("/withdraw/", methods=['POST', 'GET'])
@login_required
def withdraw():
    if request.method == 'POST':
        amount = request.form['amount']
        if float(amount) > current_user.balance:
            current_user.warnings += 1  # increment warning counter
            db.session.commit()
            error = f"You do not have enough balance to withdraw ${amount}"
            return render_template("withdraw.html", error=error)
        else:
            current_user.balance -= float(amount)
            db.session.commit()
            success = f"Your balance has been updated to ${current_user.balance:.2f}"
            return render_template("withdraw.html", success=success)
    else:
        return render_template("withdraw.html")

  
# route balance page
@app.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    if request.method == 'POST':
        if 'deposit' in request.form:
            return redirect(url_for('deposit', next=request.full_path))
        elif 'withdraw' in request.form:
            return redirect(url_for('withdraw', next=request.full_path))
    payment_methods = PaymentMethod.query.filter_by(user_id=current_user.id).all()
    next_url = request.args.get('next')
    if next_url:
        return redirect(next_url)

    return render_template('balance.html', balance=current_user.balance, payment_methods=payment_methods)

# route product page
@app.route("/product/<int:id>", methods=['POST', 'GET'])
def product(id):
    product = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        if "comment-submit" in request.form:
            new_text = request.form['comment']
            if current_user.is_authenticated:
                new_comment = Comments(
                    text=new_text, user_id=current_user.id, product_id=id)
            else:
                new_comment = Comments(text=new_text, product_id=id)
            try:
                db.session.add(new_comment)
                db.session.commit()
                return redirect(url_for('product', id=id))
            except:
                return "Comment was longer than 300 characters"
        elif "add-product" in request.form:
            q = request.form['amount']
            new_c = Cart(user_id=current_user.id, product_id=id, quantity=q)
            try:
                db.session.add(new_c)
                db.session.commit()
                return redirect('/cart')
            except:
                return "Invalid product"

        # Add product retrieves the product ID value in Prodcuts
        # Then it creates a new column in Shopping and sets the product atrribute in shapping to the product atrribute
        # in Produts 
    else:
        texts = Comments.query.filter_by(
            product_id=id).order_by(Comments.date_registered)
        return render_template("product.html", texts=texts, product=product)

############################# SU functions ######################################
@app.route('/manage_builds/', methods=["POST",'GET'])
def manage_builds():
    
    builds = CustomBuild.query.all()
    return render_template('managebuilds.html', builds)

# Delete one particular costumer from database
@app.route("/delete_costumer/<int:id>")
def delete_costumer(id):
    to_be_deleted = User.query.filter_by(id=id).first()
    banned_user = Banned(email=to_be_deleted.email, f_name=to_be_deleted.f_name,
                         l_name=to_be_deleted.l_name)
    try:
        db.session.add(banned_user)
        db.session.delete(to_be_deleted)
        db.session.commit()
        return redirect('/manage_costumer')
    except:
        return "Costumer wasnt found"

# Displays all the customer
@app.route("/manage_costumer/", methods=['POST', 'GET'])
def manage_costumers():
    costumers = User.query.filter_by(
        user_type='CU').order_by(User.date_registered)
    return render_template("managecostumer.html", costumers=costumers)

# Displays all the employees
@app.route("/manage_emply/", methods=['POST', 'GET'])
def manage_emply():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        rg_email = request.form['email']
        rg_password = request.form['password']
        new_address = request.form['address']
        new_phonenumber = request.form['phonenumber']
        new_user = User(email=rg_email, password=rg_password, f_name=first_name,
                        l_name=last_name, address=new_address, phone_number=new_phonenumber,
                        user_type='EMPLY')
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/manage_emply/')
        except:
            return "Employee could not be added"
    employees = User.query.filter_by(
        user_type="EMPLY").order_by(User.date_registered)
    return render_template("manageemply.html", employees=employees)

# Delete an emply from database
@app.route("/deleteemply/<int:id>", methods=['POST', 'GET'])
def deleteemply(id):
    fired = User.query.filter_by(id=id).first()
    banned_user = Banned(email=fired.email, f_name=fired.f_name,
                         l_name=fired.l_name)
    try:
        db.session.add(banned_user)
        db.session.delete(fired)
        db.session.commit()
        return redirect('/manage_emply')
    except:
        return "Employee wasnt found"

# Display information of a particular product
@app.route("/reviewprod/<int:id>", methods=['POST', "GET"])
def reviewprod(id):
    product = Product.query.filter_by(id=id).first()
    specs = Specs.query.filter_by(product_id=product.id).first()
    if request.method == 'POST':
        if 'update' in request.form:
            new_name = request.form['name']
            new_price = request.form['price']
            new_q = request.form['quantity']
            new_d = request.form['discounts']
            new_desc = request.form['description']
            if new_name:
                product.name = new_name
            if new_price:
                product.price = new_price
            if new_q:
                product.quantity = new_q
            if new_desc:
                product.description = new_desc
            if new_d:
                product.discounts = new_d
            try:
                db.session.commit()
                return redirect('/manage_product')
            except:
                "Something went wrong deleting the product"
    return render_template("reviewprod.html", product=product, specs=specs)

# Displays all the products
@app.route("/manage_product/", methods=['POST', 'GET'])
def manage_product():
    products = Product.query.order_by(Product.date_registered)
    if request.method == 'POST':
        new_name = request.form['name']
        new_model = request.form['model']
        power = request.form['power']
        formfactor = request.form['form-factor']
        new_descrp = request.form['description']
        new_price = request.form['price']
        new_type_prod = request.form['type-name']
        existing_product = Product.query.filter_by(name=new_name).first()
        new_prod = Product(name=new_name, model=new_model, power=power,form_factor=formfactor, description=new_descrp,
                           price=new_price, type_name=new_type_prod,
                           discounts=0)
        cpu_support = request.form['cpu-support']
        bios_update = request.form['bios-update']
        m2_support = request.form['m2_support']
        ssd_hard = request.form['ssd/hard-drive']
        pclex16_slots = request.form['pclex16_slots']
        memory_type = request.form['memory_type']
        memory_slots = request.form['memory_slots']
        fan_size = request.form['fan_size']
        if existing_product:
            return "This product already exists. Try a new one."
        try:
            db.session.add(new_prod)
            db.session.commit()
            try:
                new_specs = Specs(product_id = new_prod.id,cpu_support=cpu_support, bios_update=bios_update,m2_support=m2_support,
                          ssd_hard_drive_support=ssd_hard,pclex16_slots=pclex16_slots,memory_type=memory_type,memory_slots=memory_slots, fan_size=fan_size)
                db.session.add(new_specs)
                db.session.commit()
                return redirect('/manage_product/')
            except:
                'something wrong with adding specs'
        except:
            return "Something went wrong when adding the product"
    return render_template("manageproduct.html", products=products)

################ User page #########################
# route user page
@app.route("/user/", methods=['POST', 'GET'])
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
                else:
                    current_user.email = new_email
            if new_password1 and new_password2:
                if (new_password1 != new_password2):
                    return 'Passwords do not match'
                elif len(new_password1) < 8:
                    return 'Password must be at least 8 characters'
                else:
                    current_user.password = new_password1
            if new_address:
                current_user.address = new_address
            if new_phonenumber:
                if len(new_phonenumber) > 10:
                    return 'Invalid format of phone number'
                else:
                    current_user.phone_number = new_phonenumber
            try:
                db.session.commit()
                return "Information updated succesfully"
            except:
                return "Something went wrong. Try again!"
        else:
            # display page for regular customers
            return render_template("user.html", user=current_user)

    elif current_user.user_type == "EMPLY":
        curr_applications = Application.query.order_by( Application.date_registered)
        # display page for admin users
        if request.method == 'POST':
            if 'product' in request.form:
                return redirect('/manage_product/')
            elif 'costumer' in request.form:
                return redirect('/manage_costumer/')
            elif 'builds' in request.form:
                return redirect('/manage_builds/')
        curr_applications = Application.query.order_by( Application.date_registered)
        # display page for employee users
        return render_template("employee.html", applications=curr_applications)
    # if user is not logged in, redirect to login page

    elif current_user.user_type == "SU":
        if request.method == 'POST':
            if 'product' in request.form:
                return redirect('/manage_product/')
            elif 'emply' in request.form:
                return redirect('/manage_emply/')
            elif 'costumer' in request.form:
                return redirect('/manage_costumer/')
            elif 'builds' in request.form:
                return redirect('/manage_builds/')
        rejected_applications = Application.query.order_by(
            Application.rejected == 1)
        # display page for admin users
        return render_template("superuser.html", applications=rejected_applications)
    # if user is not logged in, redirect to login page
    return redirect(url_for('login'))

############ Common User application functionality ###########################
# Rejects the application
@app.route("/reject/<int:id>", methods=['POST', 'GET'])
def reject(id):
    if request.method == 'POST':
        to_be_rejected = Application.query.filter_by(id=id).first()
        to_be_rejected.memo = request.form['memo']
        to_be_rejected.rejected = 1
        try:
            db.session.commit()
            return redirect('/user')
        except:
            return "Something went wrong rejecting the user."
    return render_template("memo.html")

# Reviews the applicationD
@app.route("/review/<int:id>", methods=['POST', 'GET'])
def review(id):
    if request.method == 'POST':
        if "accept-EMPLY" in request.form or "reject-EMPLY" in request.form:
            if "accept-EMPLY" in request.form:
                to_be_added = Application.query.get(id)
                new_user = User(email=to_be_added.email, password=to_be_added.password, f_name=to_be_added.f_name, l_name=to_be_added.l_name, address=to_be_added.address, phone_number=to_be_added.phone_number)
                try:
                    db.session.add(new_user)
                    db.session.delete(to_be_added)
                    db.session.commit()
                    return redirect('/user')
                except:
                    return "Something went wrong adding the user."
            elif "reject-EMPLY" in request.form:
                return redirect(url_for('reject', id=id))
        if "aprove-SU" in request.form or "disaprove-SU" in request.form:
            if "aprove-SU" in request.form:
                to_be_banned = Application.query.filter_by(id=id).first()
                banned_user = Banned(email=to_be_banned.email, f_name=to_be_banned.f_name, l_name=to_be_banned.l_name)
                try:
                    db.session.add(banned_user)
                    db.session.delete(to_be_banned)
                    db.session.commit()
                    return redirect('/user')
                except:
                    return "Something went wrong aproving the rejection"
            elif "disaprove-SU" in request.form:
                to_be_added = Application.query.filter_by(id=id).first()
                new_user = User(email=to_be_added.email, password=to_be_added.password, f_name=to_be_added.f_name, l_name=to_be_added.l_name, address=to_be_added.address, phone_number=to_be_added.phone_number)
                try:
                    db.session.add(new_user)
                    db.session.delete(to_be_added)
                    db.session.commit()
                    return redirect('/user')
                except:
                    return "Something went wrong adding the user."
    return redirect('/user')

####################### Costum Builds #############################
@app.route("/initcb/", methods=["GET", "POST"])
def initcb():
    if request.method == "POST":
        category = request.form["option"]
        name = request.form["title"]
        new_cb = CustomBuild(
            creator_id=current_user.id, name=name, build_type=category
        )
        try:
            db.session.add(new_cb)
            db.session.commit()
            return redirect(url_for("createbuild", id=new_cb.id))
        except:
            return "Something went wrong"
    return render_template("initcb.html")

@app.route('/deletepart/<int:id>/<string:type>', methods=['POST', 'GET'])
def deletepart(id,type):
        cb = CustomBuild.query.get(id)
        if type=='cpu':
            cb.cpu_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='cooler':
            cb.cooler_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='motherboard':
            cb.motherboard_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='RAM':
            cb.RAM_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='m2':
            cb.m2_id = None
            cb.m2_quantity = 0
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='ssd_hdd_drive':
            cb.ssd_hdd_drive_id = None
            cb.ssd_hdd_drive_quantity = 0
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='GPU':
            cb.GPU_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='PSU':
            cb.PSU_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
        elif type=='case':
            cb.case_id = None
            try:
                db.session.commit()
                return redirect(url_for('createbuild', id=id))
            except: return'Something went wrong'
@app.route('/addpart/<int:id>/<string:type>', methods=['POST', 'GET'])
def addpart(id, type):
    cb = CustomBuild.query.get(id)

    # Retrieve the already selected parts for the build
    selected_parts = {
        'cpu': cb.cpu_id,
        'cooler': cb.cooler_id,
        'motherboard': cb.motherboard_id,
        'RAM': cb.RAM_id,
        'm2': cb.m2_id,
        'ssd_hdd_drive': cb.ssd_hdd_drive_id,
        'GPU': cb.GPU_id,
        'PSU': cb.PSU_id,
        'case': cb.case_id
    }

    # Filter products based on the selected parts and compatibility
    products = Product.query.filter_by(type_name=type).all()
    compatible_products = []
    if type=='cpu':
        for product in products:
            if check_cpu_compatibility(product, selected_parts['motherboard']) == 'Okay':
                compatible_products.append(product)

    if type=='motherboard':
        if not selected_parts['cpu'] and not selected_parts['RAM'] and not selected_parts['case']:
            compatible_products = products
        else:
            cpu_compatible = []
            memory_compatible =[]
            case_compatible=[]
            for product in products:
                if cb.cpu_id:
                    if 'Okay' == check_motherboard_cpu(product, selected_parts['cpu']):
                        cpu_compatible.append(product)
                if selected_parts['RAM']:
                    if 'Okay' == check_motherboard_memory(product, selected_parts['RAM']):
                        memory_compatible.append(product)
                if selected_parts['case']:
                    if 'Okay' == check_motherboard_case(product, selected_parts['case']):
                        case_compatible.append(product)
            temp = cpu_compatible+memory_compatible+case_compatible
            compatible_products = set(temp)
    if type=='RAM':
        for product in products:
            if check_memory_compatibility(product, selected_parts['motherboard']) == 'Okay':
                compatible_products.append(product)
    if type=='GPU':
        for product in products:
            if check_gpu_compatibility(product, selected_parts['case']) == 'Okay':
                compatible_products.append(product)
    if type == 'cooler':
        for product in products:
            if check_cooler_compatibility(product, selected_parts['case']) == 'Okay':
                compatible_products.append(product)
    if type=='PSU':
        for product in products:
            if check_psu_compatibility(product, selected_parts['case']) == 'Okay':
                compatible_products.append(product)
    if type=='case':
        if not selected_parts['cooler'] and not selected_parts['GPU'] and not selected_parts['motherboard']:
            compatible_products = products
        else:
            cooler_compatible = []
            gpu_compatible =[]
            motherboard_compatible=[]
            
            for product in products:
                if selected_parts['motherboard']:
                    if 'Okay' == check_case_motherboard(product, selected_parts['motherboard']):
                        motherboard_compatible.append(product)
                if selected_parts['GPU']:
                    if 'Okay' == check_case_gpu(product, selected_parts['GPU']):
                        gpu_compatible.append(product)
                if selected_parts['cooler']:
                    if 'Okay' == check_case_cooler(product, selected_parts['cooler']):
                        cooler_compatible.append(product)
            temp = cooler_compatible + gpu_compatible + motherboard_compatible
            compatible_products = set(temp)
    if type=='m2' or type=='ssd_hdd_drive':
        compatible_products = products

    if request.method == 'POST':
        product_id = request.form['product_id']
        product = Product.query.get(product_id)
        if product:
            type = product.type_name
            if type=='m2':
                if type in selected_parts:
                    setattr(cb, type + '_id', product_id)
                    setattr(cb, type + '_quantity', 1)
                    try:
                        db.session.commit()
                        return redirect(url_for('createbuild', id=id))
                    except:
                        return 'Something went wrong'
            elif type=='ssd_hdd_drive':
                if type in selected_parts:
                    setattr(cb, type + '_id', product_id)
                    setattr(cb, type + '_quantity', 1)
                    try:
                        db.session.commit()
                        return redirect(url_for('createbuild', id=id))
                    except:
                        return 'Something went wrong'
            else:
                if type in selected_parts:
                    # Update the selected part in the custom build
                    setattr(cb, type + '_id', product_id)
                    try:
                        db.session.commit()
                        return redirect(url_for('createbuild', id=id))
                    except:
                        return 'Something went wrong'

    return render_template('pickproduct.html', products=compatible_products)
@app.route('/addcart/<int:cb_id>', methods=['POST','GET'])
def addcart(cb_id):
    cb = CustomBuild.query.get(cb_id)
     # create a new Cart object for each product in the custom build
    cart_items = [
        Cart(product_id=cb.cpu_id, user_id=current_user.id),
        Cart(product_id=cb.cooler_id, user_id=current_user.id),
        Cart(product_id=cb.motherboard_id, user_id=current_user.id),
        Cart(product_id=cb.RAM_id, user_id=current_user.id),
        Cart(product_id=cb.m2_id, user_id=current_user.id),
        Cart(product_id=cb.ssd_hdd_drive_id, user_id=current_user.id),
        Cart(product_id=cb.GPU_id, user_id=current_user.id),
        Cart(product_id=cb.PSU_id, user_id=current_user.id),
        Cart(product_id=cb.case_id, user_id=current_user.id)
    ]

    # add each cart item to the database session
    try:
        for item in cart_items:
            db.session.add(item)

        db.session.commit()
    except:
        return "Something went wrong adding the build"
    return redirect('/cart')

@app.route("/createbuild/<int:id>", methods=['POST','GET'])
def createbuild(id):
    if current_user.is_authenticated:
        if request.method=='POST':
            post = request.form['option']
            if 'yes' == post:
                return redirect(url_for('addcart', cb_id=id))
            elif 'no' == post:
                #add it to the shopping cart and delete the custom build
                return 'something'

        cb = CustomBuild.query.get(id)
        cpu = Product.query.get(cb.cpu_id)
        cooling = Product.query.get(cb.cooler_id)
        mb=Product.query.get(cb.motherboard_id)
        memory = Product.query.get(cb.RAM_id)
        m2 = Product.query.get(cb.m2_id)
        ssd_hdd = Product.query.get(cb.ssd_hdd_drive_id)
        gpu=Product.query.get(cb.GPU_id)
        psu = Product.query.get(cb.PSU_id)
        case= Product.query.get(cb.case_id)
        lst_prod = [cpu,cooling,mb,memory,m2,ssd_hdd,gpu,psu,case]
        price = get_price(lst_prod)
        power = get_power(lst_prod,psu)
        compatibility='Not Done'
        if cpu and cooling and mb and memory and storage and gpu and psu and case:
            compatibility = check_comp(cpu,cooling,mb,memory,storage,gpu,psu,case, power)
        return render_template("createbuild.html", build=cb, cpu=cpu,cooling=cooling,
                               motherboard=mb,memory=memory,m2=m2,ssd_hdd=ssd_hdd,gpu = gpu, psu=psu,
                               case=case, power=power, price = price, compatibility=compatibility)
    return redirect('/login')

def check_comp(cpu,cooling,mb,memory,storage,gpu,psu,case, power):
    '''mb_specs = Specs.query.filter_by(product_id=mb.id).first()
    memory_specs = Specs.query.filter_by(product_id=memory.id).first()
    storage_specs = Specs.query.filter_by(product_id=storage.id).first()
    cooling_specs = Specs.query.filter_by(product_id=cooling.id).first()
    case_specs = Specs.query.filter_by(product_id=case.id).first()
    if mb_specs.memory_type!=memory_specs.memory_type:
        return 'Error'
    elif mb_specs.memory_slots<memory_specs.memory_slots:
        return 'Error'
    elif storage_specs.m2_support > mb_specs.m2_support:
        return 'Error'
    elif storage_specs.ssd_hard_drive_support:
        if storage_specs.ssd_hard_drive_support > mb_specs.ssd_hard_drive_support:
            return 'Error'
    elif cpu.model not in mb_specs.cpu_support:
        return "Error"
    elif mb_specs.bios_update:
        if cpu.model in mb_specs.bios_update:
            return "BIOS"
    elif case.form_factor not in mb.form_factor and case.form_factor not in psu.form_factor:
        return "Error"
    elif cooling_specs.fan_size[:-2] > case_specs.fan_size[:-2]:
        return "Error"
    elif cpu.model not in cooling_specs.cpu_support:
        return "Error"
    elif power>psu.power:
        return "Error"
    else:
        return 'Okay'''
    return 'Error'
def get_power(products,psu):
    power = 0
    for product in products:
        if product and product!=psu and product.power:
            power += product.power
    return power
def get_price(products):
    price = 0.0
    for product in products:
        if product and product.price:
            price += product.price
    return price
# route recommended custombuilds page
@app.route("/recbuild/")
def recbuild():
    return render_template("recbuild.html")

# route user custombuilds page
@app.route("/userbuild/")
def userbuild():
    return render_template("userbuild.html")


def check_cpu_compatibility(cpu, motherboard):
    if motherboard:
        motherboard_specs = Specs.query.filter_by(product_id=motherboard).first()

        if cpu.model in motherboard_specs.cpu_support:
            return 'Okay'
        elif motherboard_specs.bios_update: 
            if cpu.model in motherboard_specs.bios_update:
                return 'Okay'
        else:
            return 'Error'
    else:
        return 'Okay'

def check_motherboard_cpu(motherboard, cpu):
    if cpu:
        CPU = Product.query.get(cpu)
        motherboard_specs = Specs.query.filter_by(product_id=motherboard.id).first()
        if CPU.model in motherboard_specs.cpu_support:
            return "Okay"
        elif motherboard_specs.bios_update:
            if CPU.model in motherboard_specs.bios_update:
                return 'Okay'
        else:
            return 'Error'
    else:
        return 'Okay'

def check_motherboard_memory(motherboard, memory):
    if memory:
        motherboard_specs = Specs.query.filter_by(product_id=motherboard).first()
        memory_specs = Specs.query.filter_by(product_id=memory).first()
        if motherboard_specs.memory_type == memory_specs.memory_type and motherboard_specs.memory_slots >= memory_specs.memory_slots:
            return "Okay"
        else:
            return 'Error'
    else:
        return 'Okay'

def check_motherboard_storage(motherboard, storage, quantity):
    ''''if storage:
        Storage = Product.query.get(storage)
        motherboard_specs = Specs.query.filter_by(product_id=motherboard).first()
        if Storage.type_name=='m2':
            if motherboard_specs.m2_support >= .m2_support:
                return "Okay"
            else:
                return "Error"
        elif Storage.model=='ssd':
            return 1
        elif Storage.model=='hdd':
            return 2
    else:'''
    return 'Okay'
    
def check_motherboard_case(motherboard, case):
    if case:
        Case = Product.query.get(case)
        if Case.form_factor in motherboard.form_factor:
            return "Okay"
        else:
            return 'Error'
    else:
        return 'Okay'
    
def check_memory_compatibility(memory, motherboard):
    if motherboard:
        motherboard_specs = Specs.query.filter_by(product_id=motherboard).first()
        memory_specs = Specs.query.filter_by(product_id=memory.id).first()
        if (memory_specs.memory_slots <= motherboard_specs.memory_slots
            and memory_specs.memory_type == motherboard_specs.memory_type):
            return 'Okay'
        else:
            return 'Error'
    else:
        return 'Okay'


def check_storage_compatibility(storage, motherboard):
    if motherboard:
        motherboard_specs = Specs.query.filter_by(product_id=motherboard).first()
        storage_specs = Specs.query.filter_by(product_id=storage.id).first()
        if storage_specs.m2_support <= motherboard_specs.m2_support and storage_specs.ssd_hard_drive_support <= motherboard_specs.ssd_hard_drive_support:
            return 'Okay'
        else:
            return 'Error'
    else:
        return 'Okay'


def check_gpu_compatibility(gpu, case):
    if case:
        if case.form_factor in gpu.form_factor:
            return 'Okay'
        else:
            return 'Error'
    else:
        return 'Okay'

def check_cooler_compatibility(cooler, case):
    if case:
        if case.form_factor in cooler.form_factor:
            return 'Okay'
        else:
            return 'Error'
    else:
        return 'Okay'


def check_psu_compatibility(psu, case):
    if case:
        case_specs = Specs.query.filter_by(product_id=case).first()

        if psu.form_factor in case_specs.form_factor:
            return 'Okay'
        else:
            return 'Error'
    else: return 'Okay'

def check_case_motherboard(case, motherboard):
    if motherboard:
        MB = Product.query.get(motherboard)
        if MB.form_factor == case.form_factor:
            return 'Okay'
        else: return 'Error'
    else:
        return 'Okay'

def check_case_gpu(case,gpu):
    if gpu:
        GPU = Product.query.get(gpu)
        if GPU.form_factor == case.form_factor:
            return 'Okay'
        else: return 'Error'
    else:
        return 'Okay'

def check_case_cooler(case, cooler):
    if cooler:
        Cooler = Product.query.get(cooler)
        if Cooler.form_factor == case.form_factor:
            return 'Okay'
        else: return 'Error'
    else:
        return 'Okay'    

### Run application ###
if __name__ == "__main__":
    app.run(debug=True)
