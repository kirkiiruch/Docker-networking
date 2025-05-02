from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from sqlalchemy.sql import func
from passlib.hash import pbkdf2_sha256
from decouple import config

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/expense_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Модель для транзакций
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    type = db.Column(db.String(10), nullable=False, default='expense')

    def __repr__(self):
        return f'<Transaction {self.amount} {self.currency} in {self.category}>'

# Создание таблиц
with app.app_context():
    try:
        db.create_all()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

# Декоратор для проверки авторизации
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Получение курса валют через API
def get_exchange_rate(from_currency, to_currency):
    api_key = config('EXCHANGE_RATE_API_KEY')
    url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
    response = requests.get(url)
    if response.status_code == 200:
        rates = response.json()['rates']
        return rates.get(to_currency, 1.0)
    return 1.0

# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('register.html')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'danger')
            return render_template('register.html')
        new_user = User(username=username, password=pbkdf2_sha256.hash(password))
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

# Главная страница
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    try:
        user_id = session['user_id']
        base_currency = request.args.get('currency', 'USD')
        period = request.args.get('period', 'month')
        current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        # Фильтрация по периоду
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        if period == 'month':
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            transactions = [t for t in transactions if start_date <= t.date <= datetime.now()]
        elif period == 'year':
            start_date = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            transactions = [t for t in transactions if start_date <= t.date <= datetime.now()]

        # Конвертация сумм в выбранную валюту
        converted_expenses = []
        converted_incomes = []
        for t in transactions:
            rate = get_exchange_rate(t.currency, base_currency)
            converted_amount = t.amount * rate
            original_amount = t.amount
            if t.type == 'expense':
                converted_expenses.append((t.id, converted_amount, original_amount, t.category, t.date, t.currency))
            else:
                converted_incomes.append((t.id, converted_amount, original_amount, t.category, t.date, t.currency))

        # Подсчет общих затрат и доходов
        total_expenses = sum(t[1] for t in converted_expenses) if converted_expenses else 0
        total_incomes = sum(t[1] for t in converted_incomes) if converted_incomes else 0

        return render_template('index.html', 
                              expenses=converted_expenses,
                              incomes=converted_incomes,
                              total_expenses=total_expenses,
                              total_incomes=total_incomes,
                              username=session['username'],
                              base_currency=base_currency,
                              period=period,
                              currencies=['USD', 'EUR', 'RUB'],
                              current_datetime=current_datetime)
    except Exception as e:
        return f"Error fetching transactions: {e}", 500

# Добавление транзакции
@app.route('/add', methods=['POST'])
@login_required
def add_transaction():
    try:
        user_id = session['user_id']
        amount = float(request.form['amount'])
        category = request.form['category']
        currency = request.form['currency']
        date_str = request.form.get('date', datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        # Парсим дату в формате datetime-local (с 'T')
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        transaction_type = request.form['type']

        new_transaction = Transaction(
            user_id=user_id,
            amount=amount,
            category=category,
            date=date,
            currency=currency,
            type=transaction_type
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error adding transaction: {e}", 500

# Удаление транзакции
@app.route('/delete/<int:id>')
@login_required
def delete_transaction(id):
    try:
        user_id = session['user_id']
        transaction = Transaction.query.filter_by(id=id, user_id=user_id).first_or_404()
        db.session.delete(transaction)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting transaction: {e}", 500

# Выход
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)