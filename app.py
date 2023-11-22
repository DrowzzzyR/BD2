from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.config['MYSQL_HOST'] = DB_CONFIG['host']
app.config['MYSQL_USER'] = DB_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DB_CONFIG['password']
app.config['MYSQL_DB'] = DB_CONFIG['database']
app.config['SECRET_KEY'] = SECRET_KEY
mysql = MySQL(app)

# Функция для проверки авторизации пользователя
def login_required(role='operator'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'user_id' in session:
                user_id = session['user_id']
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
                user_role = cursor.fetchone()[0]
                cursor.close()
                if user_role == role or user_role == 'admin':
                    return fn(*args, **kwargs)
                flash('Недостаточно прав для доступа', 'danger')
                return redirect(url_for('login'))
            flash('Необходима авторизация', 'danger')
            return redirect(url_for('login'))
        return decorated_view
    return wrapper

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

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):  
            session['user_id'] = user[0]
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

# Маршрут для корневой страницы
@app.route('/')
def index():
    return render_template('index.html')

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
        product_name = request.form['product_name']
        description = request.form['description']
        price = request.form['price']

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
                           (product_name, description, price))
            mysql.connection.commit()
            flash('Product added successfully', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error adding product: {}'.format(str(e)), 'danger')
        finally:
            cursor.close()

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
    # Подключение к базе данных
    cursor = mysql.connection.cursor()

    # Выполнение запроса к базе данных для объединения данных из таблиц products и supplies
    cursor.execute("""
        SELECT p.id, p.name, p.description, p.price, s.id, s.product_id, s.quantity, s.supply_date
        FROM products p
        LEFT JOIN supplies s ON p.id = s.product_id
    """)

    # Получение результатов запроса
    products_data = cursor.fetchall()

    # Закрытие соединения с базой данных
    cursor.close()

    print(products_data)

    # Передача данных в шаблон и отображение страницы
    return render_template('products.html', products=products_data)


if __name__ == '__main__':
    app.run(debug=True)
