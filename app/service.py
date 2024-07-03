from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Apartment, Rent

service = Blueprint('service', __name__)


@service.route('/')
@login_required
def profile():
    return render_template('profile.html', user=current_user, apartments=current_user.apartments)


@service.route('/apartment', methods=['POST'])
@login_required
def create_apartment():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    new_apartment = Apartment(name=name, description=description, price=price, user_id=current_user.id)
    print(new_apartment)
    try:
        db.session.add(new_apartment)
        db.session.commit()
        flash('Квартира успешно добавлена.')
        print('Квартира успешно добавлена.')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при создании квартиры: {e}')
        print(f'Квартира не была добавлена: {e}')
    return redirect(url_for('service.profile'))


@service.route('/apartment/<int:apartment_id>', methods=['DELETE', 'GET'])
@login_required
def apartment(apartment_id):
    now_apartment = db.session.query(Apartment).filter_by(id=apartment_id).first()
    if request.method == 'DELETE':
        db.session.delete(now_apartment)
        db.session.commit()
        return redirect(url_for('service.profile'))
    return render_template('apartment.html', apartment=now_apartment, rents=now_apartment.rents)


@service.route('/apartment/<int:apartment_id>/rent', methods=['POST'])
@login_required
def create_rent(apartment_id):
    new_rent = Rent(
        apartment_id=apartment_id,
        user_id=current_user.id,
        date_start=request.form.get('date_start'),
        date_end=request.form.get('date_end'),
        price=request.form.get('price'),
        expenses=request.form.get('expenses'),
        tax=request.form.get('tax')
    )
    print(new_rent)
    try:
        db.session.add(new_rent)
        db.session.commit()
        flash('Рента успешно добавлена.')
        print('Рента успешно добавлена.')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при создании ренты: {e}')
        print(f'Рента не была добавлена: {e}')
    return redirect(url_for('service.apartment', apartment_id=apartment_id))


@service.route('/apartment/<int:apartment_id>/rent/<int:rent_id>', methods=['DELETE'])
@login_required
def delete_rent(apartment_id, rent_id):
    db.session.query(Rent).filter_by(id=rent_id).delete()
    db.session.commit()
    return redirect(url_for('service.profile.apartment.apartment_id'))


