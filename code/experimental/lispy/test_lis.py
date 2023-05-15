from collections import ChainMap
import pytest
from typing import Any, TypeAlias, NoReturn
import operator as op
import math

from .lis import parse, evaluate, Environment, Procedure, standard_env

def test_parse_number():
    assert parse('1.5') == 1.5


def test_parse_string():
    assert parse('hello!') == 'hello!'


def test_parse_unexpected_bracket():
    with pytest.raises(SyntaxError):
        parse(')')


def test_parse_missing_bracket():
    with pytest.raises(IndexError):
        parse('(')


def test_parse_simple_expression():
    assert parse('(gcd 18 45)') == ['gcd', 18, 45]


def test_parse_function():
    program = """
(define double
    (lambda (n)
        (* n 2)
    )
)
"""
    assert parse(program) == ['define', 'double',
                              ['lambda', ['n'], ['*', 'n', 2]]]


def test_parse_lambda():
    program = "(lambda (a b)(* (/ a b) 100))"
    assert parse(program) == ['lambda', ['a', 'b'],
                              ['*', ['/', 'a', 'b'], 100]]


@pytest.fixture
def env() -> Environment:
    inner_env = {'a': 2}
    outer_env = {'a': 0, 'b': 1}
    return Environment(inner_env, outer_env)


def test_environment_lookup_for_value(env):
    assert env['a'] == 2


def test_environment_setting_value(env):
    env['a'] = 111
    assert env['a'] == 111


def test_environment_changing_value(env):
    env.change('b', 333)
    assert env['b'] == 333


def lispstr(exp: object) -> str:
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


def test_evaluate_numbers():
    assert evaluate(parse("1.5"), Environment({})) == 1.5
    assert evaluate(parse("42"), Environment({})) == 42


def test_evaluate_symbols():
    env = Environment({'a': 42})
    assert evaluate(parse("a"), env) == 42


def test_evaluate_std_library_function():
    assert evaluate(parse("+"), standard_env()) == op.add
    assert evaluate(parse("sin"), standard_env()) == math.sin


def test_evaluate_quote():
    assert evaluate(parse('(quote no-such-name)'),
                    standard_env()) == 'no-such-name'
    assert evaluate(parse('(quote (99 bottles of wine))'),
                    standard_env()) == [99, 'bottles', 'of', 'wine']
    assert evaluate(parse('(quote (/ 10 0))'), standard_env()) == ['/', 10, 0]


def test_evaluate_if():
    assert evaluate(parse("(if (= 3 3) 1 0))"), standard_env()) == 1
    assert evaluate(parse("(if (< 3 2) 1 0))"), standard_env()) == 0


def test_evaluate_aggregate_expression():
    assert evaluate(parse("(* (/ 10 2)(- 4 2))"), standard_env()) == 10


class TestLambdaExpression:
    def test_evaluation_of_lambda_returns_procedure(self):
        expr = "(lambda (a b)(* (/ a b) 100))"
        f = evaluate(parse(expr), standard_env())

        assert isinstance(f, Procedure)

    def test_evaluated_lambda_can_be_called(self):
        expr = "(lambda (a b)(* (/ a b) 100))"
        f = evaluate(parse(expr), standard_env())
        assert f(15, 20) == 75


class TestDefineKeyword:
    def test_define_creates_variable(self):
        program = "(define answer (* 7 6))"
        global_env = standard_env()
        evaluate(parse(program), global_env)

        assert "answer" in global_env
        assert global_env["answer"] == 42

    def test_define_creates_named_function(self):
        program = "(define (average a b) (/ (+ a b) 2))"
        global_env = standard_env()

        evaluate(parse(program), global_env)

        function = global_env["average"]
        assert isinstance(function, Procedure)

    def test_define_creates_named_function_that_can_be_called(self):
        program = "(define (% a b) (* (/ a b) 100))"
        global_env = standard_env()
        evaluate(parse(program), global_env)

        assert global_env['%'](170, 200) == 85


class TestSetKeyword:
    def test_set_changes_value_of_previously_defined_varaible(self):
        global_env = standard_env()
        evaluate(parse("(define n 10)"), global_env)
        assert global_env['n'] == 10

        statement = "(set! n (+ n 1))"
        evaluate(parse(statement), global_env)
        assert global_env['n'] == 11
