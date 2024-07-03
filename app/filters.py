from typing import List

from app.models import Rent
from repository import *


def filters_all_rents(date_start, date_end):
    return [rent for rent in all_rents() if date_start <= rent.date_start <= date_end]


def filters_rents_by_apartment(date_start, date_end, apartment_id):
    return [rent for rent in find_apartment_by_id(apartment_id).rents if
            date_start <= rent.date_start <= date_end]


def revenue(rents: List[Rent]):
    res = 0
    for rent in rents:
        res += rent.price * (rent.date_end - rent.date_start)
    return res


def costs(rents: List[Rent]):
    res = 0
    for rent in rents:
        res += rent.tax + rent.expenses
    return res


def profit(rents: List[Rent]):
    return revenue(rents) - costs(rents)
