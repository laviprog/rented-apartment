from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from .repository import *

service = Blueprint('service', __name__)


# TODO add loggers
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
    try:
        add_apartment(new_apartment)
        flash('Квартира успешно добавлена.')
    except Exception as e:
        rollback_db()
        flash(f'Ошибка при создании квартиры: {e}')
    return redirect(url_for('service.profile'))


@service.route('/apartment/<int:apartment_id>', methods=['DELETE', 'GET'])
@login_required
def apartment(apartment_id):
    now_apartment = find_apartment_by_id(apartment_id)
    if request.method == 'DELETE':
        delete_apartment(now_apartment)
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
    try:
        add_rent(new_rent)
        flash('Рента успешно добавлена.')
    except Exception as e:
        rollback_db()
        flash(f'Ошибка при создании ренты: {e}')
    return redirect(url_for('service.apartment', apartment_id=apartment_id))


@service.route('/apartment/<int:apartment_id>/rent/<int:rent_id>', methods=['DELETE'])
@login_required
def rent(apartment_id, rent_id):
    delete_rent(rent_id)
    return redirect(url_for('service.profile.apartment.apartment_id'))
