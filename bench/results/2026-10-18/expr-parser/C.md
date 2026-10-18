# evaluate(expr)

A recursive-descent parser, with no `eval` or `exec`. The grammar runs from lowest to highest precedence:

```
expr    := term (('+' | '-') term)*
term    := factor (('*' | '/') factor)*
factor  := ('+' | '-') factor | power
power   := atom ('**' factor)?
atom    := NUMBER | '(' expr ')'
```

The `power` rule makes `**` bind tighter than unary minus, so `-2 ** 2` is `-4`. It is right-associative, so `2 ** 3 ** 2` is `512`. Its right operand is a `factor`, so `2 ** -1` works the way it does in Python.

```python
import re

_NUMBER_RE = re.compile(r"[0-9]+(?:\.[0-9]*)?|\.[0-9]+")


def _tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
        elif c in "0123456789.":
            m = _NUMBER_RE.match(expr, i)
            if not m:
                raise ValueError(f"malformed number at position {i}")
            tokens.append(("num", m.group()))
            i = m.end()
        elif c == "*":
            if expr.startswith("**", i):
                tokens.append(("op", "**"))
                i += 2
            else:
                tokens.append(("op", "*"))
                i += 1
        elif c in "+-/":
            tokens.append(("op", c))
            i += 1
        elif c in "()":
            tokens.append(("lp" if c == "(" else "rp", c))
            i += 1
        else:
            raise ValueError(f"invalid character {c!r} at position {i}")
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self):
        tok = self._peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        self.pos += 1
        return tok

    def _at_op(self, *ops):
        tok = self._peek()
        return tok is not None and tok[0] == "op" and tok[1] in ops

    def parse(self):
        if not self.tokens:
            raise ValueError("empty expression")
        value = self._expr()
        if self._peek() is not None:
            raise ValueError(f"unexpected token {self._peek()[1]!r}")
        return value

    def _expr(self):
        value = self._term()
        while self._at_op("+", "-"):
            op = self._advance()[1]
            rhs = self._term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _term(self):
        value = self._factor()
        while self._at_op("*", "/"):
            op = self._advance()[1]
            rhs = self._factor()
            value = value * rhs if op == "*" else value / rhs
        return value

    def _factor(self):
        if self._at_op("+", "-"):
            op = self._advance()[1]
            operand = self._factor()
            return -operand if op == "-" else operand
        return self._power()

    def _power(self):
        base = self._atom()
        if self._at_op("**"):
            self._advance()
            return base ** self._factor()
        return base

    def _atom(self):
        kind, text = self._advance()
        if kind == "num":
            return float(text) if "." in text else int(text)
        if kind == "lp":
            value = self._expr()
            tok = self._peek()
            if tok is None or tok[0] != "rp":
                raise ValueError("missing closing parenthesis")
            self._advance()
            return value
        raise ValueError(f"unexpected token {text!r}")


def evaluate(expr):
    try:
        return _Parser(_tokenize(expr)).parse()
    except RecursionError:
        raise ValueError("expression nested too deeply") from None
```

## Expected results

| Input | Result |
|---|---|
| `"1 + 2 * 3"` | `7` |
| `"-2 ** 2"` | `-4` |
| `"2 ** 3 ** 2"` | `512` |
| `"2 ** -1"` | `0.5` |
| `" ( 1.5 + 2.5 ) * -2 "` | `-8.0` |
| `"7 / 2"` | `3.5` |
| `"1 / 0"` | `ZeroDivisionError` |
| `"1 / (2 - 2)"` | `ZeroDivisionError` |
| `"2 +"` | `ValueError` |
| `"(1"` | `ValueError` |
| `"1 2"` | `ValueError` |

## Notes

- I traced these cases by hand but did not execute the code.
- Integer-only input returns `int`. Any decimal literal makes the result a `float`.
- Division uses Python's `/`, so `ZeroDivisionError` comes from Python itself, including `0 ** -1`.
- Unary plus is accepted. Leading-dot decimals such as `.5` are accepted. Exponent notation such as `1e3` is rejected.
- Not guarded: huge integer powers such as `9 ** 9 ** 9` can run for a very long time, and float overflow such as `10.0 ** 400` raises `OverflowError` rather than `ValueError`.
