from src.math import add_two_numbers, diff_two_numbers, mult_two_numbers
import pytest

def test_add_two_numbers():
    assert add_two_numbers(5,2)  == 7

def test_diff_two_numbers():
    assert diff_two_numbers(6,3) == 3

@pytest.mark.xfail(reason = 'Buggy function - to be fixed in ticket 124')
def test_mult_two_numbers():
    assert mult_two_numbers(2,7) == 14

@pytest.mark.skip(reason = 'Buggy function - to be fixed in ticket 123')
def test_failure():
    assert [1,2,3] == [1,3,2]


