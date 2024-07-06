from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from .models import Expense
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


@service.route('/apartment/<int:apartment_id>', methods=['POST', 'GET'])
@login_required
def apartment(apartment_id):
    if any(el.id == apartment_id for el in current_user.apartments):
        now_apartment = find_apartment_by_id(apartment_id)
        if request.method == 'POST':
            delete_apartment_db(now_apartment)
            return redirect(url_for('service.profile'))
        return render_template('apartment.html', apartment=now_apartment, rents=now_apartment.rents,
                               expenses=now_apartment.expenses)


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


@service.route('/apartment/<int:apartment_id>/rent/<int:rent_id>', methods=['POST'])
@login_required
def delete_rent(apartment_id, rent_id):
    delete_rent_db(rent_id)
    return redirect(url_for('service.apartment', apartment_id=apartment_id))


@service.route('/apartment/<int:apartment_id>/expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(apartment_id, expense_id):
    delete_expense_db(expense_id)
    return redirect(url_for('service.apartment', apartment_id=apartment_id))


@service.route('apartment/<int:apartment_id>/expense', methods=['POST'])
@login_required
def create_expense(apartment_id):
    new_expense = Expense(
        apartment_id=apartment_id,
        name=request.form.get('name'),
        description=request.form.get('description'),
        value=request.form.get('value'),
        date=request.form.get('date'),
        expense_type=request.form.get('expense_type')
    )
    try:
        add_expense(new_expense)
        flash('Расход успешно добавлена.')
    except Exception as e:
        rollback_db()
        flash(f'Ошибка при создании расхода: {e}')
    return redirect(url_for('service.apartment', apartment_id=apartment_id))
