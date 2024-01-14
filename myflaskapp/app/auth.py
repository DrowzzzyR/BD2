from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
# from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# from app.config import DB_CONFIG, SECRET_KEY
from models import *

bp = Blueprint("auth", __name__, url_prefix="/auth")

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

# Регистрация пользователя
# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         role = request.form['role']
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Используем pbkdf2_sha256 для хэширования

#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
#                        (username, hashed_password, role))
#         mysql.connection.commit()
#         cursor.close()

#         flash('Регистрация прошла успешно', 'success')
#         return redirect(url_for('login'))

#     return render_template('register.html')

# Авторизация пользователя
# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#         user = cursor.fetchone()
#         cursor.close()

#         if user and check_password_hash(user[2], password):  
#             session['user_id'] = user[0]
#             flash('Добро пожаловать, {}'.format(username), 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Неверные учетные данные', 'danger')

#     return render_template('login.html')

# Выход из системы
# @bp.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('login'))
