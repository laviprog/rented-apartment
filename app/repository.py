from app.models import Apartment, Rent, Expense
from . import db


def find_apartment_by_id(apartment_id):
    return db.session.query(Apartment).filter_by(id=apartment_id).first()


def all_rents():
    return db.session.query(Rent).all()


def all_rents_by_apartment(apartment_id):
    return db.session.query(Apartment).filter_by(id=apartment_id).first().rents


def add_rent(rent: Rent):
    db.session.add(rent)
    db.session.commit()
    return rent


def add_apartment(apartment: Apartment):
    db.session.add(apartment)
    db.session.commit()
    return apartment


def delete_apartment_db(apartment):
    print(apartment.id)
    db.session.delete(apartment)
    db.session.commit()


def delete_rent_db(rent_id):
    db.session.query(Rent).filter_by(id=rent_id).delete()
    db.session.commit()


def rollback_db():
    db.session.rollback()


def add_expense(expense: Expense):
    db.session.add(expense)
    db.session.commit()
    return expense


def delete_expense_db(expense_id):
    db.session.query(Expense).filter_by(id=expense_id).delete()
    db.session.commit()
