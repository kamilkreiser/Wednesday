
class CircularReference(Exception):
    pass

class FormulaError(Exception):
    pass

class Sheet:
    def __init__(self):
        self.cells = {}          # ref -> content (raw)
        self.cache = {}           # ref -> computed float
        self.dependencies = {}   # ref -> set of refs it depends on
        self.dependents = {}      # ref -> set of refs that depend on it

    def _normalize_ref(self, ref):
        ref = ref.strip().upper()
        if not ref:
            raise FormulaError("Empty cell reference")
        i = 0
        while i < len(ref) and ref[i].isalpha():
            i += 1
        if i == 0 or i == len(ref):
            raise FormulaError("Invalid cell reference")
        col_str = ref[:i]
        row_str = ref[i:]
        if not row_str.isdigit() or int(row_str) <= 0:
            raise FormulaError("Invalid cell reference")
        col = 0
        for ch in col_str:
            col = col * 26 + (ord(ch) - ord('A') + 1)
        row = int(row_str)
        return (col, row)

    def _ref_to_string(self, ref_tuple):
        col, row = ref_tuple
        col_str = ""
        while col > 0:
            col, rem = divmod(col - 1, 26)
            col_str = chr(ord('A') + rem) + col_str
        return f"{col_str}{row}"

    def set_cell(self, ref, content):
        norm_ref = self._normalize_ref(ref)
        ref_str = self._ref_to_string(norm_ref)
        self.cells[ref_str] = content
        # Invalidate cache and dependencies for this cell and all dependents
        self._invalidate(ref_str)

    def _invalidate(self, ref_str):
        # Remove from cache
        self.cache.pop(ref_str, None)
        # Remove dependencies for this cell
        self.dependencies.pop(ref_str, None)
        # Recursively invalidate dependents
        if ref_str in self.dependents:
            for dep in list(self.dependents[ref_str]):
                self._invalidate(dep)

    def get_value(self, ref):
        norm_ref = self._normalize_ref(ref)
        ref_str = self._ref_to_string(norm_ref)
        if ref_str in self.cache:
            return self.cache[ref_str]
        # Compute value
        value = self._compute(ref_str, set())
        self.cache[ref_str] = value
        return value

    def _compute(self, ref_str, visiting):
        if ref_str in visiting:
            raise CircularReference(f"Circular reference involving {ref_str}")
        visiting.add(ref_str)
        try:
            content = self.cells.get(ref_str, "")
            if isinstance(content, (int, float)):
                return float(content)
            if not isinstance(content, str):
                return 0.0
            if content == "":
                return 0.0
            if content.startswith("="):
                # Parse formula
                expr = content[1:]
                # Tokenize and parse
                tokens = self._tokenize(expr)
                parser = Parser(tokens, self, visiting)
                result = parser.parse_expression()
                return float(result)
            else:
                # Literal string -> 0
                return 0.0
        finally:
            visiting.remove(ref_str)

    def _tokenize(self, expr):
        tokens = []
        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit() or (ch == '.' and i+1 < n and expr[i+1].isdigit()):
                # Number
                start = i
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    i += 1
                num_str = expr[start:i]
                try:
                    num = float(num_str)
                except ValueError:
                    raise FormulaError("Invalid number")
                tokens.append(('NUM', num))
                continue
            if ch.isalpha():
                # Cell reference or function name
                start = i
                while i < n and (expr[i].isalpha() or expr[i].isdigit()):
                    i += 1
                word = expr[start:i]
                # Check if it's a function name followed by '('
                if i < n and expr[i] == '(':
                    upper = word.upper()
                    if upper in ('SUM', 'MIN', 'MAX', 'AVG'):
                        tokens.append(('FUNC', upper))
                        continue
                    else:
                        raise FormulaError("Unknown function")
                else:
                    # Cell reference
                    try:
                        norm = self._normalize_ref(word)
                        tokens.append(('CELL', self._ref_to_string(norm)))
                    except FormulaError:
                        raise FormulaError("Invalid cell reference")
                continue
            if ch in '+-*/()':
                tokens.append(('OP', ch))
                i += 1
                continue
            if ch == ',':
                tokens.append(('COMMA', ','))
                i += 1
                continue
            raise FormulaError(f"Unexpected character: {ch}")
        tokens.append(('EOF', None))
        return tokens

class Parser:
    def __init__(self, tokens, sheet, visiting):
        self.tokens = tokens
        self.pos = 0
        self.sheet = sheet
        self.visiting = visiting

    def peek(self):
        return self.tokens[self.pos]

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_):
        tok = self.next()
        if tok[0] != type_:
            raise FormulaError(f"Expected {type_}, got {tok[0]}")
        return tok

    def parse_expression(self):
        return self.parse_add_sub()

    def parse_add_sub(self):
        left = self.parse_mul_div()
        while True:
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] in ('+', '-'):
                self.next()
                right = self.parse_mul_div()
                if tok[1] == '+':
                    left = left + right
                else:
                    left = left - right
            else:
                break
        return left

    def parse_mul_div(self):
        left = self.parse_unary()
        while True:
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] in ('*', '/'):
                self.next()
                right = self.parse_unary()
                if tok[1] == '*':
                    left = left * right
                else:
                    if right == 0:
                        raise FormulaError("Division by zero")
                    left = left / right
            else:
                break
        return left

    def parse_unary(self):
        tok = self.peek()
        if tok[0] == 'OP' and tok[1] == '-':
            self.next()
            return -self.parse_unary()
        else:
            return self.parse_primary()

    def parse_primary(self):
        tok = self.next()
        if tok[0] == 'NUM':
            return tok[1]
        elif tok[0] == 'CELL':
            ref = tok[1]
            return self.sheet._compute(ref, self.visiting)
        elif tok[0] == 'OP' and tok[1] == '(':
            val = self.parse_expression()
            self.expect('OP')  # should be ')'
            if self.tokens[self.pos-1][1] != ')':
                raise FormulaError("Expected closing parenthesis")
            return val
        elif tok[0] == 'FUNC':
            func_name = tok[1]
            # Expect '('
            self.expect('OP')  # '('
            # Parse first cell ref
            first_tok = self.next()
            if first_tok[0] != 'CELL':
                raise FormulaError("Expected cell reference in range")
            first_ref = first_tok[1]
            # Expect ':'
            colon_tok = self.next()
            if colon_tok[0] != 'OP' or colon_tok[1] != ':':
                raise FormulaError("Expected ':' in range")
            # Parse second cell ref
            second_tok = self.next()
            if second_tok[0] != 'CELL':
                raise FormulaError("Expected cell reference in range")
            second_ref = second_tok[1]
            # Expect ')'
            self.expect('OP')  # ')'
            if self.tokens[self.pos-1][1] != ')':
                raise FormulaError("Expected closing parenthesis")
            # Compute range
            first_norm = self.sheet._normalize_ref(first_ref)
            second_norm = self.sheet._normalize_ref(second_ref)
            col1, row1 = first_norm
            col2, row2 = second_norm
            min_col = min(col1, col2)
            max_col = max(col1, col2)
            min_row = min(row1, row2)
            max_row = max(row1, row2)
            values = []
            for c in range(min_col, max_col+1):
                for r in range(min_row, max_row+1):
                    ref_str = self.sheet._ref_to_string((c, r))
                    values.append(self.sheet._compute(ref_str, self.visiting))
            if func_name == 'SUM':
                return sum(values)
            elif func_name == 'MIN':
                if not values:
                    return 0.0
                return min(values)
            elif func_name == 'MAX':
                if not values:
                    return 0.0
                return max(values)
            elif func_name == 'AVG':
                if not values:
                    return 0.0
                return sum(values) / len(values)
            else:
                raise FormulaError("Unknown function")
        else:
            raise FormulaError("Unexpected token")
