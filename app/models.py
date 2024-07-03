from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    apartments = db.relationship('Apartment', backref='owner', lazy=True)
    rents = db.relationship('Rent', backref='owner_rent', lazy=True)

    def __str__(self):
        return f'User: {self.username}, {self.email}'


class Apartment(db.Model):
    __tablename__ = 'apartments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rents = db.relationship('Rent', backref='apartment', lazy=True)
    expenses = db.relationship('Expense', backref='apartment', lazy=True)

    def __str__(self):
        return f'Apartment: {self.name}, {self.description}, {self.price}'

    # TODO может говорить сколько она генерит прибыли в месяц, год,
    # показывать процентную доходность в год, расходы, прибыль за вычетом расходов
    # показывает статистику за месяц с первой ренты,
    # которая начинается в этом месяце до самой последней ренты


class Rent(db.Model):
    __tablename__ = 'rents'

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)

    def __str__(self):
        return f'Rent: {self.date_start}, {self.date_end}, {self.price}, {self.expenses}, {self.tax}'


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    value = db.Column(db.Float, nullable=False)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)

    def __str__(self):
        return f'Expense: {self.name}, {self.date}, {self.value}, {self.description}'
