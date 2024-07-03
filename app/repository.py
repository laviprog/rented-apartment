from app.models import Apartment, Rent
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


def delete_apartment(apartment_id):
    db.session.delete(apartment_id)
    db.session.commit()


def delete_rent(rent_id):
    db.session.delete(rent_id)
    db.session.commit()


def rollback_db():
    db.session.rollback()
