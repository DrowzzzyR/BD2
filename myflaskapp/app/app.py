from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

# mysql = MySQL(app)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from models import *

# from auth import bp as auth_bp
# app.register_blueprint(auth_bp)

# Маршрут для корневой страницы
@app.route('/')
def index():
    return render_template('index.html')


# Функция для проверки авторизации пользователя
def login_required(role='operator'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'user_id' in session:
                user_id = session['user_id']
                user = User.query.filter_by(id=int(user_id)).first()
                user_role = user.role
                if user_role == role or user_role == 'admin':
                    return fn(*args, **kwargs)
                flash('Недостаточно прав для доступа', 'danger')
                return redirect(url_for('login'))
            flash('Необходима авторизация', 'danger')
            return redirect(url_for('login'))
        return decorated_view
    return wrapper

@app.route('/dashboard')
@login_required()  # Предполагается, что это эндпоинт, доступный только авторизованным пользователям
def dashboard():
    # Ваш код для отображения дашборда
    return render_template('dashboard.html')


from flask import request


@app.route('/add_product', methods=['POST'])
@login_required(role='admin')
def add_product():
    if request.method == 'POST':
        params= {
        "name": request.form['product_name'],
        "description": request.form['description'],
        "price": request.form['price'],
        }
        try:
            product_item = Product(**params)
            db.session.add(product_item)
            db.session.commit()
            flash('Product added successfully', 'success')
        except Exception as e:
            db.connection.rollback()
            flash('Error adding product: {}'.format(str(e)), 'danger')


    return redirect(url_for('dashboard'))


@app.route('/add_supply', methods=['POST'])
@login_required(role='admin')
def add_supply():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        supply_date = request.form['supply_date']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO supplies (product_id, quantity, supply_date) VALUES (%s, %s, %s)",
                           (product_id, quantity, supply_date))
            mysql.connection.commit()
            flash('Supply added successfully', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error adding supply: {}'.format(str(e)), 'danger')
        finally:
            cursor.close()

    return redirect(url_for('dashboard'))


@app.route('/products')
def products():
    products_data = Product.query.all()
    supplies_data = Supply.query.all()

    # Передача данных в шаблон и отображение страницы
    return render_template('products.html', products=products_data, supplies=supplies_data)


# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Используем pbkdf2_sha256 для хэширования

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                       (username, hashed_password, role))
        mysql.connection.commit()
        cursor.close()

        flash('Регистрация прошла успешно', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username="admin").first() 

        if user and check_password_hash(user.password_hash, password):  
            session['user_id'] = user.id
            flash('Добро пожаловать, {}'.format(username), 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверные учетные данные', 'danger')

    return render_template('login.html')

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
