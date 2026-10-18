Here's an `evaluate` function built from a small tokenizer and a recursive-descent parser. Operator precedence and associativity match Python.

```python
import re

_NUMBER = re.compile(r"[0-9]+(?:\.[0-9]*)?|\.[0-9]+")


def _tokenize(s):
    """Split the input into numbers (int/float) and operator strings."""
    tokens = []
    pos, n = 0, len(s)
    while pos < n:
        ch = s[pos]
        if ch.isspace():
            pos += 1
            continue
        m = _NUMBER.match(s, pos)
        if m:
            text = m.group()
            tokens.append(float(text) if "." in text else int(text))
            pos = m.end()
            continue
        if s.startswith("**", pos):
            tokens.append("**")
            pos += 2
            continue
        if ch in "+-*/()":
            tokens.append(ch)
            pos += 1
            continue
        raise ValueError(f"unexpected character {ch!r} at position {pos}")
    return tokens


class _Parser:
    """
    Grammar (same precedence as Python):

        expr   := term (('+' | '-') term)*
        term   := unary (('*' | '/') unary)*
        unary  := '-' unary | power
        power  := atom ['**' unary]          # right-assoc; exponent may be negative
        atom   := NUMBER | '(' expr ')'
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def _peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def _take(self):
        if self.i >= len(self.tokens):
            raise ValueError("unexpected end of expression")
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    @staticmethod
    def _is_op(tok, ops):
        return isinstance(tok, str) and tok in ops

    def parse(self):
        if not self.tokens:
            raise ValueError("empty expression")
        value = self._expr()
        if self.i != len(self.tokens):
            raise ValueError(f"unexpected token {self._peek()!r}")
        return value

    def _expr(self):
        value = self._term()
        while self._is_op(self._peek(), ("+", "-")):
            op = self._take()
            rhs = self._term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _term(self):
        value = self._unary()
        while self._is_op(self._peek(), ("*", "/")):
            op = self._take()
            rhs = self._unary()
            # Python raises ZeroDivisionError for x / 0 on its own
            value = value * rhs if op == "*" else value / rhs
        return value

    def _unary(self):
        if self._is_op(self._peek(), ("-",)):
            self._take()
            return -self._unary()
        return self._power()

    def _power(self):
        base = self._atom()
        if self._is_op(self._peek(), ("**",)):
            self._take()
            exponent = self._unary()  # recursion gives right-associativity
            result = base ** exponent  # 0 ** -1 raises ZeroDivisionError
            if isinstance(result, complex):
                raise ValueError("result is not a real number")
            return result
        return base

    def _atom(self):
        tok = self._take()
        if not isinstance(tok, str):
            return tok
        if tok == "(":
            value = self._expr()
            if self._peek() != ")":
                raise ValueError("expected ')'")
            self._take()
            return value
        raise ValueError(f"unexpected token {tok!r}")


def evaluate(expr):
    """Evaluate an arithmetic expression string without eval/exec.

    Supports + - * / **, unary minus, parentheses, integers and decimals.
    Raises ValueError on malformed input and ZeroDivisionError on division by zero.
    """
    if not isinstance(expr, str):
        raise TypeError("expr must be a string")
    try:
        return _Parser(_tokenize(expr)).parse()
    except RecursionError:
        raise ValueError("expression is nested too deeply") from None
```

Some quick checks:

```python
assert evaluate("1 + 2 * 3") == 7
assert evaluate("(1 + 2) * 3") == 9
assert evaluate("2 ** 3 ** 2") == 512        # right-associative
assert evaluate("-2 ** 2") == -4             # ** binds tighter than unary minus
assert evaluate("2 ** -1") == 0.5            # unary minus allowed in the exponent
assert evaluate("--3") == 3
assert evaluate(" 1.5 * .5 + 3. ") == 3.75
assert evaluate("7 / 2") == 3.5
assert evaluate("10 - 4 - 3") == 3           # left-associative

for bad in ["2 +", "(1", "1 2", "", "()", "1 + * 2", "1.2.3", "2 * * 3", "abc", ")"]:
    try:
        evaluate(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"expected ValueError for {bad!r}")

for zero in ["1 / 0", "1 / (2 - 2)", "0 ** -1"]:
    try:
        evaluate(zero)
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError(f"expected ZeroDivisionError for {zero!r}")
```

How some edge cases behave:

- **Numeric types work like Python's.** `"2 + 3"` gives `int` 5, any decimal gives a `float`, and `/` always gives a `float`.
- **`**` needs its two stars together.** `"2 * * 3"` is rejected, just as it is in Python. Spaces are allowed anywhere else, but they still separate tokens, so `"1 2"` is an error rather than 12.
- **Accepted number forms:** `.5` and `5.` both work, as in Python. Text like `1.2.3` splits into two numbers and is rejected.
- **Results that aren't real numbers are rejected.** `(-8) ** 0.5` would give a complex number in Python, so it raises `ValueError` instead.
- **Unary plus isn't supported** because it wasn't in the spec. To add it, change `("-",)` in `_unary` to `("-", "+")` and return the operand unchanged for `+`.
- **Untrusted input:** something like `9 ** 9 ** 9` will run for a very long time and use a lot of memory. If people other than you can send expressions, cap the size of the exponent in `_power`. A float overflow such as `10.0 ** 400` raises `OverflowError`.
