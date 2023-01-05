#!/usr/bin/env python3

import re

globalenv = {"a": 10}

def parse_layer(s):
    exprs = []
    inner_expr = ""
    paren_counter = 0
    words = s[1:-1].strip().split()
    quoted = False
    for word in words:
        if word == "(":
            paren_counter += 1
            inner_expr += " " + word
        elif word == ")":
            paren_counter -= 1
            inner_expr += word + " "
            if paren_counter == 0:
                if quoted:
                    inner_expr += ")"
                    quoted = False
                exprs.append(inner_expr.strip())
                inner_expr = ""
        elif paren_counter == 0:
            if word == "'":
                quoted = True
                inner_expr = "( quote "
            else:
                exprs.append(word)
        else:
            inner_expr += " " + word + " "
    return exprs

def reader_replace(sexp):
    if isinstance(sexp, str) and sexp[0] == "'":
        return "( quote " + sexp[1:] + " )"
    return sexp

### basic type checks

def is_atom(sexp):
    return bool(isinstance(sexp, int) or (re.fullmatch(r'[<>\*\+\-#\w\d]+', sexp)))

def is_list(sexp):
    if not (isinstance(sexp, str)):
        return False
    return bool(re.fullmatch(r'\(.*\)', sexp))

def is_empty_list(sexp):
    if not (isinstance(sexp, str)):
        return False
    return bool(re.fullmatch(r'\( *\)', sexp))

### lisp functions

def _atom(sexp):
    if is_atom(sexp) or is_empty_list(sexp):
        return "#t"
    else:
        return "#f"

def _eq(sexp1, sexp2):
    if is_atom(sexp1) and is_atom(sexp2) and str(sexp1) == str(sexp2):
        return "#t"
    elif is_empty_list(sexp1) and is_empty_list(sexp2):
        return "#t"
    else:
        return "#f"

def _car(sexp):
    return parse_layer(sexp)[0]

def _cdr(sexp):
    return "(" + " ".join(parse_layer(sexp)[1:]) + ")"

def _cons(sexp1, sexp2):
    return "(" + str(sexp1) + " " + " ".join(parse_layer(sexp2)) + ")"

def _cond(sexps, binds):
    for clause in sexps:
        clause = parse_layer(clause)
        if eval(clause[0], binds) == "#t":
            return eval(clause[1], binds)
    return "#undefined: no condition was satisfied"

def _lambda(params, exp, args, binds):
    new_binds = {}
    for p, a in zip(parse_layer(params), args):
        new_binds.update({p: eval(a, binds)})
    binds = binds.copy()
    binds.update(new_binds)
    return eval(exp, binds)

def _label(name, lambda_expr, args, binds):
    params = lambda_expr[1]
    exp = lambda_expr[2]
    binds = binds.copy()
    binds.update({name: "( " + " ".join(lambda_expr) + " )"})
    return _lambda(params, exp, args, binds)

def _defun(name, params, expr, binds):
    binds.update({name: "( lambda " + params + " " + expr + " )" })
    return "#<lambda>"

def _dec(val):
    if not isinstance(val, int):
        return "#err not a number"
    return val - 1

def _inc(val):
    if not isinstance(val, int):
        return "#err not a number"
    return val + 1

def _env(binds):
    return "# active bindings: " + str(binds)

def eval(sexp, binds):
    sexp = reader_replace(sexp)
    if is_atom(sexp):
        if sexp.isdigit():
            return int(sexp)
        elif sexp == "#t" or sexp == "#f":
            return sexp
        else:
            try:
                return binds[sexp]
            except KeyError:
                return "#err: var not bound"
    elif is_empty_list(sexp):
        return sexp
    elif is_list(sexp):
        sexp = parse_layer(sexp)
        if is_atom(sexp[0]):
            match sexp[0]:
                case "quote":
                    return sexp[1]
                case "atom":
                    return _atom(eval(sexp[1], binds))
                case "eq":
                    return _eq(eval(sexp[1], binds), eval(sexp[2], binds))
                case "car":
                    return _car(eval(sexp[1], binds))
                case "cdr":
                    return _cdr(eval(sexp[1], binds))
                case "cons":
                    return _cons(eval(sexp[1], binds), eval(sexp[2], binds))
                case "cond":
                    return _cond(sexp[1:], binds)
                case "defun":
                    return _defun(sexp[1], sexp[2], sexp[3], binds)
                case "dec":
                    return _dec(eval(sexp[1], binds))
                case "inc":
                    return _inc(eval(sexp[1], binds))
                case "env":
                    return _env(binds)
                case _:
                    try:
                        exec = "( " + binds[sexp[0]]
                        exec += " " + " ".join(sexp[1:]) + " )"
                        return eval(exec, binds)
                    except KeyError:
                        return "#err: invalid function call"
        elif is_list(sexp[0]):
            first_list = parse_layer(sexp[0])
            match first_list[0]:
                case "lambda":
                    params = first_list[1]
                    exp = first_list[2]
                    args = sexp[1:]
                    return _lambda(params, exp, args, binds)
                case "label":
                    name = first_list[1]
                    lambda_expr = parse_layer(first_list[2])
                    args = sexp[1:]
                    return _label(name, lambda_expr, args, binds)
    else:
        return "#err: not a valid s-expression"

def prepare(s):
    s = re.sub(r'\(', " ( ", s)
    s = re.sub(r'\)', " ) ", s)
    if s[0] == ";":
        return "'()"
    return ' '.join(s.split())

with open('core.shlipple', 'r') as core_file:
    core_library = core_file.read().split(";;")

for core_func in core_library:
    if not core_func:
        continue
    eval(prepare(core_func), globalenv)

while True:
    sexpr = prepare(input("> "))
    output = eval(sexpr, globalenv)
    print(output)
