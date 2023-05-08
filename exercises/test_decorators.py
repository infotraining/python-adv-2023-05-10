from functools import wraps
from typing import Callable, TypeVar

@nullable
def square(x: float) -> float:
    return x * x

def test_nullable():
    assert square(None) is None
    assert square(2.0) == 4.0


#########################################################


@bad_char_remove("$", ",")
def currency_to_float(text: str) -> float:
    return float(text)

def test_bad_char_remove():
    assert currency_to_float("13") == 13
    assert currency_to_float("$3.14") == 3.14
    assert currency_to_float("$1,701.99") == 1701.99