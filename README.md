# shlipple
SHitty LIsp in Python Provides Lots of Entertainment.

Shoutout to my peeps McCarthy, Abelson, Sussman, Graham! I mostly relied on the latter's paper on McCarthy ("The Roots of Lisp").

Start a REPL with `python shlipple.py` and code away. The REPL only supports single-line expressions currently, tho (very shitty). Pass file names as command line arguments to import their functions (functions need to be delimited with `;;`). For example, run `python shlipple.py playground.shlipple` to import the `(fizzbuzz max)` function.

Of course, we feature an amazing shlipple-interpreter in shlipple, to be found in the `eval` function within the shlipple.shlipple library (see below).

Needs Python >= 3.10 because I added a match-case statement in there.

## Currently implemented

In Python:

- atoms (strings, `#t`, `#f`, positive integers)
- lists `(...)`
- `quote`, `'`
- `atom`
- `eq`
- `car`
- `cdr`
- `cons`
- `cond`
- `defun`
- `dec`
- `inc`
- `env` (alist of  all currently active variable and function bindings)
- `lambda`
- `label`
- `number`

In Shlipple:

- `null`
- `and`
- `or`
- `not`
- `append`
- `+`
- `-`
- `*`
- `<`
- `>`
- `reverse`
- `map`
- `zip`
- `assoc`


In optional library math.shlipple:

- `square`
- `cube`
- `factorial` - there's no tail-call recursion yet, so...

All very shittily, of course.

## Eval (lisp interpreter in shlipple)
`Eval` implements all the basic commands except `defun` and `env` (and I think there are some issues with the `'` shorthand (for  `quote` ) for atoms, which I am too lazy to figure our right now).
Optionally use `(env)` to pass all shlipple-core bindings (and others you have added) to `(eval)`. Eval takes an s-expr and an alist of bindings.

```
python shlipple.py shlipple.shlipple

(eval '(map '(lambda (x) (+ x 1)) '(1 2 3 4 5)) (env))
;=> ( 2 3 4 5 6 )

```

## Examples

### Map

```
(map 'inc '(1 2 3 4 5))
; => (2 3 4 5 6)

(map '(lambda (x) (* x 2)) '(1 2 3 4 5))
; => (2 4 6 8 10)
 
```


### Fizzbuzz

```
(defun fizzbuzz (max)
  (reverse ((label iter
                   (lambda (n mod3 mod5 acc)
                     (cond ((eq n (inc max)) acc)
                           ((and (eq mod3 3) (eq mod5 5)) (iter
                                                           (inc n)
                                                           1
                                                           1
                                                           (cons 'FIZZBUZZ acc)))
                           ((eq mod3 3) (iter
                                         (inc n)
                                         1
                                         (inc mod5)
                                         (cons 'FIZZ acc)))
                           ((eq mod5 5) (iter
                                         (inc n)
                                         (inc mod3)
                                         1
                                         (cons 'BUZZ acc)))
                           (#t (iter (inc n)
                                     (inc mod3)
                                     (inc mod5)
                                     (cons n acc))))))
            0 0 0 '())))       
            
(fizzbuzz 100)
;=> (0 1 2 FIZZ 4 BUZZ FIZZ 7 8 FIZZ BUZZ 11 FIZZ 13 14 FIZZBUZZ 16 17 FIZZ 19 BUZZ FIZZ 22 23 FIZZ BUZZ 26 FIZZ 28 29 FIZZBUZZ 31 32 FIZZ 34 BUZZ FIZZ 37 38 FIZZ BUZZ 41 FIZZ 43 44 FIZZBUZZ 46 47 FIZZ 49 BUZZ FIZZ 52 53 FIZZ BUZZ 56 FIZZ 58 59 FIZZBUZZ 61 62 FIZZ 64 BUZZ FIZZ 67 68 FIZZ BUZZ 71 FIZZ 73 74 FIZZBUZZ 76 77 FIZZ 79 BUZZ FIZZ 82 83 FIZZ BUZZ 86 FIZZ 88 89 FIZZBUZZ 91 92 FIZZ 94 BUZZ FIZZ 97 98 FIZZ BUZZ
```
