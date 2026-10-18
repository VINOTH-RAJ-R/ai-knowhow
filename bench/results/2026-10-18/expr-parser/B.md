```python
_DIGITS = "0123456789"
_SPACES = " \t\r\n\f\v"


def _tokenize(text):
    """Return a list of (kind, value, position) tuples ending with an 'END' token.

    kind is 'NUM' (value is int or float), one of '+', '-', '*', '/', '**', '(', ')',
    or 'END'. Any other character raises ValueError.
    """
    tokens = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in _SPACES:
            i += 1
        elif ch in _DIGITS:
            j = i
            while j < n and text[j] in _DIGITS:
                j += 1
            if j < n and text[j] == ".":
                j += 1
                frac_start = j
                while j < n and text[j] in _DIGITS:
                    j += 1
                if j == frac_start:
                    raise ValueError(f"expected digits after '.' at position {j}")
                tokens.append(("NUM", float(text[i:j]), i))
            else:
                tokens.append(("NUM", int(text[i:j]), i))
            i = j
        elif text.startswith("**", i):
            tokens.append(("**", None, i))
            i += 2
        elif ch in "+-*/()":
            tokens.append((ch, None, i))
            i += 1
        else:
            raise ValueError(f"unexpected character {ch!r} at position {i}")
    tokens.append(("END", None, n))
    return tokens


class _Parser:
    """Recursive-descent parser. Grammar, lowest to highest precedence:

        expr    := term (('+' | '-') term)*
        term    := unary (('*' | '/') unary)*
        unary   := '-' unary | power
        power   := primary ('**' unary)?      # right-associative
        primary := NUM | '(' expr ')'
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _kind(self):
        return self.tokens[self.pos][0]

    def _advance(self):
        tok = self.tokens[self.pos]
        if tok[0] != "END":
            self.pos += 1
        return tok

    def _fail(self):
        kind, _, where = self.tokens[self.pos]
        names = {"NUM": "number", "END": "end of input"}
        raise ValueError(f"unexpected {names.get(kind, repr(kind))} at position {where}")

    def parse(self):
        value = self._expr()
        if self._kind() != "END":
            self._fail()
        return value

    def _expr(self):
        value = self._term()
        while self._kind() in ("+", "-"):
            op = self._advance()[0]
            rhs = self._term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _term(self):
        value = self._unary()
        while self._kind() in ("*", "/"):
            op = self._advance()[0]
            rhs = self._unary()
            value = value * rhs if op == "*" else value / rhs
        return value

    def _unary(self):
        if self._kind() == "-":
            self._advance()
            return -self._unary()
        return self._power()

    def _power(self):
        base = self._primary()
        if self._kind() == "**":
            self._advance()
            result = base ** self._unary()
            if isinstance(result, complex):
                raise ValueError("result is not a real number")
            return result
        return base

    def _primary(self):
        kind = self._kind()
        if kind == "NUM":
            return self._advance()[1]
        if kind == "(":
            self._advance()
            value = self._expr()
            if self._kind() != ")":
                raise ValueError(f"expected ')' at position {self.tokens[self.pos][2]}")
            self._advance()
            return value
        self._fail()


def evaluate(expr):
    """Evaluate an arithmetic expression string without eval/exec.

    Raises ValueError for malformed input and ZeroDivisionError for division by zero.
    """
    tokens = _tokenize(expr)
    try:
        return _Parser(tokens).parse()
    except RecursionError:
        raise ValueError("expression is nested too deeply") from None


if __name__ == "__main__":
    valid = {
        "1 + 2 * 3": 7,
        "(1 + 2) * 3": 9,
        "-2 ** 2": -4,
        "2 ** -1": 0.5,
        "2 ** 3 ** 2": 512,
        "2 ** -2 ** 2": 0.0625,
        "10 - 4 - 3": 3,
        "8 / 4 / 2": 1.0,
        "-2 ** 2 * 3": -12,
        "--2": 2,
        "1.5 * 2": 3.0,
        "  3 -  -2 ": 5,
    }
    for expr, want in valid.items():
        assert evaluate(expr) == want, (expr, want)

    malformed = ["2 +", "(1", "1 2", "", "()", "1 + * 2", ")", "2 $ 3", ".5", "1.", "+1", "(-8) ** (1/3)"]
    for expr in malformed:
        try:
            evaluate(expr)
        except ValueError:
            continue
        raise AssertionError(f"no ValueError for {expr!r}")

    for expr in ["1 / 0", "1 / (2 - 2)", "0 ** -1"]:
        try:
            evaluate(expr)
        except ZeroDivisionError:
            continue
        raise AssertionError(f"no ZeroDivisionError for {expr!r}")

    print("all checks passed")
```

Design: a tokenizer feeds a recursive-descent parser that mirrors Python's grammar, so `**` binds tighter than unary minus on its left, is right-associative, and its exponent can itself be a unary (`2 ** -1`). Numbers keep Python's int/float types and operators, so results match Python's arithmetic; unary plus, `.5`, `1.`, and complex results are rejected as ValueError, while float overflow such as `10.0 ** 400` raises OverflowError, which the spec does not cover.

Tested: nothing was executed in this run, so the asserts in the `__main__` block are unrun; the expected values were checked by hand against Python's operator semantics.

Not verified: whether the code runs and every assert passes. Run `python3` on the file; it should print "all checks passed".
