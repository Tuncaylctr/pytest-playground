from hands_on.src import Product, OrderError, process_order
from datetime import datetime
import pytest

def test_process_order():
    product = Product(
        name = 'Banana',
        price = 1,
        stock = 100_000,
    )
    order_meta = process_order(
        product = product,
        quantity = 10_000,
        is_premium_user = False,
        order_time = datetime.now()
    )
    assert order_meta['product'] == 'Banana'
    assert order_meta['total'] == 10_000 * 1

def test_premium_user():
    product = Product(
        name = 'Banana',
        price = 1,
        stock = 100_000,
    )
    order_meta = process_order(
        product = product,
        quantity = 10_000,
        is_premium_user = True,
        order_time = datetime.now()
    )
    assert order_meta['product'] == 'Banana'
    assert order_meta['total'] == 9_000 * 1

def test_too_large_order():
    product = Product(
        name = 'Banana',
        price = 1,
        stock = 100,
    )
    with pytest.raises(OrderError):
         process_order(
            product = product,
            quantity = 10_000,
            is_premium_user = False,
            order_time = datetime.now()
    )
def test_expedited():
    product = Product(
        name='Banana',
        price=1,
        stock=100_000,
    )
    order_meta = process_order(
        product=product,
        quantity=10_000,
        is_premium_user=True,
        order_time=datetime(2026, 8, 28, 0, 39, 15)
    )
    assert order_meta['expedited']

def test_estimated_delivery():
    product =  Product(
        name = 'Banana',
        price = 1,
        stock = 100_000,
    )
    order_meta = process_order(
        product=product,
        quantity=10_000,
        is_premium_user=True,
        order_time = datetime(2026, 7, 28, 0, 39, 15)
    )
    assert order_meta['estimated_delivery'] == "2026-07-29"




