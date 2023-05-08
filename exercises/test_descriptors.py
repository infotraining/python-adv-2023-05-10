
import pytest

class Person:
    def __init__(self, name: str, age: int, height: int) -> None:
        self.name = name
        self.age = age
        self.height = height


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
        
