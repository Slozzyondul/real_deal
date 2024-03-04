# app.py
from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin
from flask import jsonify
from models import CartItem


from models import db, Fruit, Vegetable, BestsellerProduct
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Adjust this based on your database setup

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


with app.app_context():
    db.create_all()

    bestseller_data = [
        {"name": "Organic Tomato", "image_url": "img/best-product-1.jpg", "rating": 4.5, "price": 3.12},
        {"name": "Fresh Apple", "image_url": "img/best-product-2.jpg", "rating": 4.2, "price": 4.99},
        {"name": "Exotic Vegetable", "image_url": "img/best-product-3.jpg", "rating": 4.7, "price": 5.99},
        # Add more bestseller data as needed
    ]

    for product_info in bestseller_data:
        # Check if the product already exists in the database
        existing_product = BestsellerProduct.query.filter_by(name=product_info["name"]).first()
        if not existing_product:
            product = BestsellerProduct(
                name=product_info["name"],
                image_url=product_info["image_url"],
                rating=product_info["rating"],
                price=product_info["price"]
            )
            db.session.add(product)

    # Sample data for fruits
    fruit_data = [
        {"name": "Fresh Apples", "discount": "20% OFF", "image": "img/featur-1.jpg"},
        {"name": "Tasty Fruits", "discount": "Free delivery", "image": "img/featur-2.jpg"},
        {"name": "Exotic Vegitable", "discount": "Discount 30$", "image": "img/featur-3.jpg"},
    ]

    for fruit_info in fruit_data:
        # Check if the fruit already exists in the database
        existing_fruit = Fruit.query.filter_by(name=fruit_info["name"]).first()
        if not existing_fruit:
            fruit = Fruit(name=fruit_info["name"], discount=fruit_info["discount"], image=fruit_info["image"])
            db.session.add(fruit)

    # Sample data for vegetables
    vegetable_data = [
        {"name": "Parsely", "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit", "price": 4.99, "image": "img/vegetable-item-6.jpg"},
        {"name": "Bell Papper", "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit", "price": 7.99, "image": "img/vegetable-item-4.jpg"},
        {"name": "Potatoes", "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit", "price": 7.99, "image": "img/vegetable-item-5.jpg"},
    ]

    for vegetable_info in vegetable_data:
        # Check if the vegetable already exists in the database
        existing_vegetable = Vegetable.query.filter_by(name=vegetable_info["name"]).first()
        if not existing_vegetable:
            vegetable = Vegetable(
                name=vegetable_info["name"],
                description=vegetable_info["description"],
                price=vegetable_info["price"],
                image=vegetable_info["image"]
            )
            db.session.add(vegetable)

    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    # Query all fruits and vegetables from the respective tables
    fruits = Fruit.query.all()
    vegetables = Vegetable.query.all()
    bestsellers = BestsellerProduct.query.all()
    return render_template('index.html', fruits=fruits, vegetables=vegetables, bestsellers=bestsellers)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    if request.method == 'POST':
        data = request.json
        product_name = data.get('product_name')
        price = data.get('price')

        # Create or update the cart item
        cart_item = CartItem.query.filter_by(user=current_user, product_name=product_name).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user=current_user, product_name=product_name, price=price)

        db.session.add(cart_item)
        db.session.commit()

        return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Invalid request'})



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)
