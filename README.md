# shlipple
SHitty LIsp in Python Provides Lots of Entertainment.

Shoutout to my peeps McCarthy, Abelson, Sussman, Graham! I mostly relied on the latter's paper on McCarthy ("The Roots of Lisp").

Start a REPL with `python shlipple.py` and code away.

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
- `env` (shows currently active variable and function bindings)
- `lambda`
- `label`

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
- reverse

All very shittily, of course.

## Fizzbuzz

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
```
