from typing import Tuple
from functools import wraps

def nullable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except TypeError:
            ret = None
        return ret

    return wrapper

@nullable
def square(x: float) -> float:
    return x * x


def test_nullable():
    assert square(None) is None
    assert square(2.0) == 4.0

def bad_char_remove(*remove_chars):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            new_arg = []
            for a in args:
                for ch in remove_chars:
                    a = a.replace(ch, "")
                new_arg.append(a)
            return func(*new_arg, **kwargs)
        return wrapper
    return decorator

# #########################################################
# def bad_char_remove(*chars):
#     def wrapper(func):
#         @wraps(func)
#         def inner(text: str):
#             for ch in chars:
#                 text = text.replace(ch, '')
#             return func(text)

#         return inner

#     return wrapper



# def bad_char_remove(char_1, char_2):
#     def _bad_char_remove(func):
#         @wraps(func)
#         def wrapper(input_str):
#             for char in [char_1, char_2]:
#                 input_str = input_str.replace(char, "")
#             return func(input_str)
#         return wrapper
#     return _bad_char_remove

@bad_char_remove("$", ",")
def currency_to_float(text1: str, text2: str) -> Tuple[float, float]:
    return (float(text1), float(text2))


def test_bad_char_remove():
    # assert currency_to_float("13") == (13,)
    # assert currency_to_float("$3.14") == (3.14,)
    assert currency_to_float("$1,701.99", "$1.99") == (1701.99, 1.99)
