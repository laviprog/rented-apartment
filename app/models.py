from datetime import datetime
from enum import Enum

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
    rents = db.relationship('Rent', backref='apartment', lazy=True, cascade="all, delete-orphan")
    expenses = db.relationship('Expense', backref='apartment', lazy=True, cascade="all, delete-orphan")

    def __str__(self):
        return f'Apartment: {self.name}, {self.description}, {self.price}'

    def get_revenue_all_time(self):
        pass

    def get_profit_all_time(self):
        pass

    def get_revenue(self, start: datetime, end: datetime):
        pass

    def get_profit(self, start: datetime, end: datetime):
        pass

    def get_roi(self):
        pass

    # заселяемость квартиры
    def get_occupancy_rate(self):
        pass

    # TODO
    # показывать процентную доходность в год, расходы, прибыль за вычетом расходов
    # показывает статистику за месяц с первой ренты,
    # которая начинается в этом месяце до самой последней ренты
    # добавить Амортизационные отчисления (на ремонт, замену техники)


class Rent(db.Model):
    __tablename__ = 'rents'

    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)

    def get_date(self):
        return f'{self.date_start.strftime('%d.%m.%Y')} – {self.date_end.strftime('%d.%m.%Y')}'

    def get_revenue(self):
        return (self.date_end - self.date_start).days * self.price

    def __str__(self):
        return f'Rent: {self.date_start}, {self.date_end}, {self.price}'


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    value = db.Column(db.Float, nullable=False)

    # values:  HOUSEHOLD, TAX, COMMUNAL, REPAIR, OTHER
    expense_type = db.Column(db.String(20), nullable=False)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)

    def get_date(self):
        return str(self.date.strftime('%d.%m.%Y'))

    def __str__(self):
        return f'Expense: {self.name}, {self.date}, {self.value}, {self.description}'
