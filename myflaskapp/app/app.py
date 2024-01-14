from flask import Flask, render_template
# импортирует класс `Flask` из модуля `flask`
from sqlalchemy import MetaData
# импортируется класс MetaData из библиотеки SQLAlchemy - это объект, который содержит информацию о базе данных SQL
from flask_sqlalchemy import SQLAlchemy
# импортируется класс SQLAlchemy из Flask SQLAlchemy  - это расширение Flask, которое предоставляет доступ к объекту базы данных SQLAlchemy в приложении Flask
from flask_migrate import Migrate
# Библиотека Flask-Migrate позволяет мигрировать базы данных в приложении Flask, используя SQLAlchemy
from flask_login import login_required
from flask import request, flash, redirect, url_for

from prometheus_client import Summary, generate_latest
# from prometheus_client import Counter, start_http_server
from prometheus_flask_exporter import PrometheusMetrics

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# создание метрики для отслеживания затраченного времени и выполненных запросов.

app = Flask(__name__)
# создает экземпляр приложения Flask, с именем текущего модуля (__name__ - это встроенная переменная, которая содержит имя текущего модуля)

application = app
# копирует объект приложения Flask в новую переменную `application`. Обычно используется, когда запускается сервер приложений, который ожидает переменную `application` в качестве имени приложения

metrics = PrometheusMetrics(app, group_by='endpoint')

app.config.from_pyfile('config.py')
# подклюячаем 'config.py', он содержит переменные с параметрами конфигурации, которые могут быть использованы в приложении (настройки базы данных, настройки безопасности, параметры сессии)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# Создание словаря "convention", содержащего соглашение об именовании для различных ограничений таблицы

metadata = MetaData(naming_convention=convention)
# Создание объекта "metadata" класса MetaData, принимающего словарь "convention" в качестве параметра
db = SQLAlchemy(app, metadata=metadata)
#  Создание объекта SQLAlchemy для взаимодействия с базой данных, принимающего объект "app" (Flask-приложение) и объект "metadata" в качестве параметров
migrate = Migrate(app, db)
# Создание объекта "migrate" класса Migrate для выполнения миграций в базе данных, принимающего объект "app" и объект SQLAlchemy "db" в качестве параметров
from models import *
# Чтобы flask_migrate увидел нашу модель, ее надо импортировать

from auth import bp as auth_bp, init_login_manager
app.register_blueprint(auth_bp)

init_login_manager(app)

@app.route('/')
@REQUEST_TIME.time()
def index():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    return generate_latest()


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/products')
def products():
    products_data = Product.query.all()
    supplies_data = Supply.query.all()
    # Передача данных в шаблон и отображение страницы
    return render_template('products.html', products=products_data, supplies=supplies_data)

@app.route('/add_product', methods=['POST'])
@login_required
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

from datetime import datetime

@app.route('/add_supply', methods=['POST'])
@login_required
def add_supply():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        supply_date = request.form['supply_date']
        supply_description = request.form.get('supply_description')

        try:
            supply_item = Supply(product_id=product_id, quantity=quantity, price=supply_date, description=supply_description)
            db.session.add(supply_item)
            db.session.commit()
            flash('Supply added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding supply: {}'.format(str(e)), 'danger')
    return redirect(url_for('dashboard'))

# if __name__ == '__main__':
#     app.run(debug=True, threaded=True)