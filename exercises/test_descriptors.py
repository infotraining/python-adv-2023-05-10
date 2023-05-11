from typing import Callable
import pytest

# class ValidatorAge:
#     def __get__(self, instance, owner_class=None):
#         value = instance._age
#         return value

#     def __set__(self, instance, value):
#         if value < 0:
#             raise AttributeError
#         instance._age = value


# class ValidatorHeight:
#     def __get__(self, instance, owner_class=None):
#         value = instance._height
#         return value

#     def __set__(self, instance, value):
#         if value < 0:
#             raise AttributeError
#         instance._height = value


class Validator:

    def __init__(self, validator: Callable):
        self.validator = validator

    def __set_name__(self, owner, name):
        self.priv_name = "_" + name

    def __set__(self, instance, value):
        if self.validator(value):
            setattr(instance, self.priv_name, value)
        else:
            raise AttributeError(f"{value!r} must be positive")

    def __get__(self, instance, owner):
        return getattr(instance, self.priv_name)


class Person:
    age = Validator(lambda x: x > 0)
    height = Validator(lambda x: x > 0)

    def __init__(self, name: str, age: int, height: int) -> None:
        self.name = name
        self.age = age
        self.height = height

    def getting_older(self):
        self.age += 1


def test_init_negative_age_raises_error():
    with pytest.raises(AttributeError):
        p = Person("John", -3, 170)


def test_init_negative_height_raises_error():
    with pytest.raises(AttributeError):
        p = Person("John", 44, -20)


def test_init_positive_values():
    p = Person("John", 44, 180)    
    assert p.age == 44
    assert p.height == 180


def test_age_setting_negative_value_raises_error():
    p = Person("John", 44, 180)    
    with pytest.raises(AttributeError):
        p.age = -78    


def test_height_setting_negative_value_raises_error():
    p = Person("John", 44, 180)    
    with pytest.raises(AttributeError):
        p.height = -78    


def test_age_setting_positive_value():
    p = Person("John", 44, 180)    
    p.age = 78    
    assert p.age == 78


def test_height_setting_positive_value():
    p = Person("John", 44, 180)    
    p.height = 178    
    assert p.height == 178
        
