from collections import ChainMap
import pytest
from typing import Any, TypeAlias, NoReturn
import operator as op
import math

Symbol: TypeAlias = str
Atom: TypeAlias = float | int | Symbol
Expression: TypeAlias = Atom | list


def tokenize(s: str) -> list[str]:
    "Convert a string into a list of tokens."
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens: list[str]) -> Expression:
    "Read an expression from a sequence of tokens"
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        exp = []
        while tokens[0] != ')':
            exp.append(read_from_tokens(tokens))
        tokens.pop(0)  # discard ')'
        return exp
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return parse_atom(token)


def parse_atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


class Environment(ChainMap[Symbol, Any]):
    "A ChainMap that allows changing an item in-place."

    def change(self, key: Symbol, value: Any) -> None:
        "Find where key is defined and change the value there."
        for map in self.maps:
            if key in map:
                map[key] = value
                return
        raise KeyError(key)


def standard_env() -> Environment:
    env = Environment()
    env.update(vars(math))
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '=': op.eq,
        '!=': op.ne,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le
    })

    return env


def parse(program: str) -> Expression:
    return read_from_tokens(tokenize(program))


KEYWORDS = ['quote', 'if', 'lambda', 'define', 'set!']


class Procedure:
    "A user-defined Scheme procedure."

    def __init__(self, params: list[Symbol], body: list[Expression], env: Environment):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args: Expression) -> Any:
        local_env = dict(zip(self.params, args))
        env = Environment(local_env, self.env)
        result = None
        for exp in self.body:
            result = evaluate(exp, env)
        return result


def lispstr(exp: object) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


def evaluate(exp: Expression, env: Environment) -> Any:
    match exp:
        case int(x) | float(x):
            return x
        case Symbol(var):
            return env[var]
        case ['quote', x]:
            return x
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        case ['lambda', [*params], *body] if body:
            return Procedure(params, body, env)
        case ['define', Symbol(name), value_exp]:
            env[name] = evaluate(value_exp, env)
        case ['define', [Symbol(name), *params], *body] if body:
            env[name] = Procedure(params, body, env)
        case ['set!', Symbol(name), value_exp]:
            env.change(name, evaluate(value_exp, env))
        case [func_exp, *args] if func_exp not in KEYWORDS:
            proc = evaluate(func_exp, env)
            values = [evaluate(arg, env) for arg in args]
            return proc(*values)
        case _:
            raise SyntaxError(lispstr(exp))


def repl(prompt: str = 'lis.py> ') -> NoReturn:
    "A prompt-read-eval-print loop."
    global_env = Environment({}, standard_env())
    program = ""
    while True:
        line = input(prompt)
        if line.endswith("\\"):
            program += line.rstrip('\\')
            program += ' '
        else:
            program += line
            try:
                ast = parse(program)
                val = evaluate(ast, global_env)
                if val is not None:
                    print(lispstr(val))
            except Exception as excpt:
                print(excpt)
            finally:
                program = ""

            


if __name__ == "__main__":
    repl()