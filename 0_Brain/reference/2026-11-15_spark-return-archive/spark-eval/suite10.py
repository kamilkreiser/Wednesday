#!/usr/bin/env python3
"""10 complex coding tasks -> Spark model.
Pipeline per task: generate (thinking off) -> execute -> hidden suite ->
repair with failure feedback -> re-test. Emits a comparison table."""
import json, time, urllib.request, traceback, sys

BASE = "http://127.0.0.1:8888/v1"
MODEL = "deepseek-v4-flash-0731"


def ask(prompt, max_tokens=4096, thinking=False):
    p = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
         "max_tokens": max_tokens, "temperature": 0.0,
         "chat_template_kwargs": {"thinking": thinking}}
    r = urllib.request.Request(BASE + "/chat/completions",
                               data=json.dumps(p).encode(),
                               headers={"Content-Type": "application/json"})
    t0 = time.time()
    b = json.loads(urllib.request.urlopen(r, timeout=3600).read().decode())
    dt = time.time() - t0
    c = b["choices"][0]
    m = c["message"]
    text = m.get("content") or m.get("reasoning_content") or m.get("reasoning") or ""
    return text, c["finish_reason"], b["usage"], dt


def strip_fences(code):
    if "```" in code:
        parts = code.split("```")
        cand = max((p for i, p in enumerate(parts) if i % 2 == 1), key=len, default=code)
        code = cand
        if code.lstrip().lower().startswith("python"):
            code = code.lstrip()[6:]
    return code


class C:
    """Tiny assertion collector."""
    def __init__(self):
        self.r = []

    def eq(self, name, fn, exp):
        try:
            g = fn()
            if isinstance(exp, float) or (isinstance(exp, int) and not isinstance(exp, bool)):
                ok = isinstance(g, (int, float)) and abs(g - exp) < 1e-9
            else:
                ok = g == exp
            self.r.append((name, ok, "got %r want %r" % (g, exp)))
        except Exception as e:
            self.r.append((name, False, "%s: %s" % (type(e).__name__, e)))

    def raises(self, name, fn, exc):
        try:
            g = fn()
            self.r.append((name, False, "returned %r want %s" % (g, exc.__name__)))
        except exc:
            self.r.append((name, True, ""))
        except Exception as e:
            self.r.append((name, False, "%s: %s want %s" % (type(e).__name__, e, exc.__name__)))


# ============================================================ TASK DEFINITIONS

T = []

def task(name, prompt, tests):
    T.append({"name": name, "prompt": prompt, "tests": tests})


# ------------------------------------------------------------------ 1. regex
task("regex-engine", '''Implement a small regular-expression matcher in pure Python (stdlib only).

Define at module level:

    def matches(pattern: str, text: str) -> bool

It returns True only if the pattern matches the ENTIRE text (full match).

Supported syntax:
  - literal characters
  - .   matches any single character
  - *   zero or more of the PRECEDING single element (a literal, . or a class)
  - +   one or more of the preceding element
  - ?   zero or one of the preceding element
  - [abc]   character class
  - [a-z]   character range inside a class
  - [^abc]  negated class

Quantifiers apply only to the single preceding element. No groups, no
alternation, no anchors (matching is already full-string).

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, f: (
    c.eq("literal", lambda: f("abc", "abc"), True),
    c.eq("literal no-match", lambda: f("abc", "abd"), False),
    c.eq("full match not prefix", lambda: f("abc", "abcd"), False),
    c.eq("dot", lambda: f("a.c", "abc"), True),
    c.eq("star many", lambda: f("a*", "aaa"), True),
    c.eq("star zero", lambda: f("a*", ""), True),
    c.eq("star middle zero", lambda: f("ab*c", "ac"), True),
    c.eq("star middle many", lambda: f("ab*c", "abbbc"), True),
    c.eq("plus needs one", lambda: f("ab+c", "ac"), False),
    c.eq("plus one", lambda: f("ab+c", "abc"), True),
    c.eq("question zero", lambda: f("ab?c", "ac"), True),
    c.eq("question one", lambda: f("ab?c", "abc"), True),
    c.eq("class plus", lambda: f("[abc]+", "cab"), True),
    c.eq("class range", lambda: f("[a-z]+", "abc"), True),
    c.eq("class range reject", lambda: f("[a-z]+", "aBc"), False),
    c.eq("negated class", lambda: f("[^a]+", "bcd"), True),
    c.eq("negated class reject", lambda: f("[^a]+", "bad"), False),
    c.eq("dot star", lambda: f("a.*z", "abcz"), True),
    c.eq("dot star empty mid", lambda: f("a.*z", "az"), True),
    c.r))(C(), ns["matches"])[-1])


# ------------------------------------------------------------- 2. topo sched
task("topo-scheduler", '''Implement a dependency scheduler in pure Python (stdlib only).

Define at module level:

    class CycleError(Exception): pass

    def schedule(deps: dict) -> list

`deps` maps a task name to a list of task names it depends on. Every name that
appears in any dependency list is also guaranteed to be a key of `deps`.

Return a list of BATCHES. Each batch is a list of task names, sorted
alphabetically. Batch 0 contains every task with no dependencies. Batch N
contains every task whose dependencies all appear in batches 0..N-1 and which
is not already in an earlier batch. Produce the minimum number of batches.

If the graph contains a cycle, raise CycleError.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, f, E: (
    c.eq("single", lambda: f({"a": []}), [["a"]]),
    c.eq("linear", lambda: f({"a": [], "b": ["a"]}), [["a"], ["b"]]),
    c.eq("two roots", lambda: f({"a": [], "b": [], "c": ["a", "b"]}), [["a", "b"], ["c"]]),
    c.eq("batch sorted", lambda: f({"b": [], "a": []}), [["a", "b"]]),
    c.eq("diamond", lambda: f({"a": [], "b": ["a"], "c": ["a"], "d": ["b", "c"]}),
         [["a"], ["b", "c"], ["d"]]),
    c.eq("three levels", lambda: f({"a": [], "b": ["a"], "c": ["b"]}), [["a"], ["b"], ["c"]]),
    c.eq("empty", lambda: f({}), []),
    c.eq("minimum batches", lambda: f({"a": [], "b": [], "c": [], "d": ["a"]}),
         [["a", "b", "c"], ["d"]]),
    c.raises("self cycle", lambda: f({"a": ["a"]}), E),
    c.raises("two cycle", lambda: f({"a": ["b"], "b": ["a"]}), E),
    c.raises("three cycle", lambda: f({"a": ["c"], "b": ["a"], "c": ["b"]}), E),
    c.raises("cycle with tail", lambda: f({"a": [], "b": ["c"], "c": ["b"]}), E),
    c.r))(C(), ns["schedule"], ns["CycleError"])[-1])


# ------------------------------------------------------------ 3. interval set
task("interval-set", '''Implement a merged interval set in pure Python (stdlib only).

Define at module level:

    class IntervalSet:
        def add(self, lo: float, hi: float) -> None
        def remove(self, lo: float, hi: float) -> None
        def contains(self, x: float) -> bool
        def total_length(self) -> float
        def intervals(self) -> list

Intervals are HALF-OPEN: [lo, hi) contains lo but not hi.
The set always stores a minimal, sorted, non-overlapping, non-adjacent list.
Adjacent intervals MUST merge: add(0,1) then add(1,2) gives [(0,2)].
`intervals()` returns a list of (lo, hi) tuples sorted by lo.
add/remove with lo >= hi is a no-op.
remove may split an interval into two.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, S: (
    c.eq("single add", lambda: (lambda s: (s.add(0, 5), s.intervals())[-1])(S()), [(0, 5)]),
    c.eq("overlap merge", lambda: (lambda s: (s.add(0, 5), s.add(3, 8), s.intervals())[-1])(S()), [(0, 8)]),
    c.eq("adjacent merge", lambda: (lambda s: (s.add(0, 1), s.add(1, 2), s.intervals())[-1])(S()), [(0, 2)]),
    c.eq("disjoint kept", lambda: (lambda s: (s.add(0, 1), s.add(5, 6), s.intervals())[-1])(S()), [(0, 1), (5, 6)]),
    c.eq("out of order sorted", lambda: (lambda s: (s.add(5, 6), s.add(0, 1), s.intervals())[-1])(S()), [(0, 1), (5, 6)]),
    c.eq("contained add noop", lambda: (lambda s: (s.add(0, 10), s.add(2, 3), s.intervals())[-1])(S()), [(0, 10)]),
    c.eq("bridge merge", lambda: (lambda s: (s.add(0, 2), s.add(4, 6), s.add(1, 5), s.intervals())[-1])(S()), [(0, 6)]),
    c.eq("contains lo", lambda: (lambda s: (s.add(0, 5), s.contains(0))[-1])(S()), True),
    c.eq("contains hi excluded", lambda: (lambda s: (s.add(0, 5), s.contains(5))[-1])(S()), False),
    c.eq("contains mid", lambda: (lambda s: (s.add(0, 5), s.contains(2.5))[-1])(S()), True),
    c.eq("contains outside", lambda: (lambda s: (s.add(0, 5), s.contains(9))[-1])(S()), False),
    c.eq("total length", lambda: (lambda s: (s.add(0, 5), s.add(10, 12), s.total_length())[-1])(S()), 7),
    c.eq("total after merge", lambda: (lambda s: (s.add(0, 5), s.add(3, 8), s.total_length())[-1])(S()), 8),
    c.eq("remove splits", lambda: (lambda s: (s.add(0, 10), s.remove(3, 5), s.intervals())[-1])(S()), [(0, 3), (5, 10)]),
    c.eq("remove head", lambda: (lambda s: (s.add(0, 10), s.remove(0, 3), s.intervals())[-1])(S()), [(3, 10)]),
    c.eq("remove all", lambda: (lambda s: (s.add(0, 10), s.remove(0, 10), s.intervals())[-1])(S()), []),
    c.eq("remove beyond", lambda: (lambda s: (s.add(0, 10), s.remove(20, 30), s.intervals())[-1])(S()), [(0, 10)]),
    c.eq("empty noop", lambda: (lambda s: (s.add(5, 5), s.intervals())[-1])(S()), []),
    c.r))(C(), ns["IntervalSet"])[-1])


# ---------------------------------------------------------------- 4. ttl lru
task("ttl-lru-cache", '''Implement a cache with both LRU eviction and TTL expiry, pure Python (stdlib only).

Define at module level:

    class TTLCache:
        def __init__(self, capacity: int, ttl: float, clock): ...
        def get(self, key): ...
        def put(self, key, value) -> None: ...
        def __len__(self) -> int: ...

`clock` is a zero-argument callable returning the current time as a float.
Call it rather than using the real clock.

- `put` inserts or updates a key and marks it most-recently-used.
- `get` returns the value, or None if the key is absent or expired.
  A successful `get` marks the key most-recently-used.
- An entry expires when `clock() - inserted_at >= ttl`. `put` resets the
  timestamp. `get` does NOT reset the timestamp.
- When inserting a NEW key would exceed capacity, evict the least-recently-used
  entry first. Expired entries must never be returned and must not count
  toward `__len__`.
- `__len__` returns the number of live (non-expired) entries.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, K: (
    c.eq("put get", lambda: (lambda t, k: (k.put("a", 1), k.get("a"))[-1])(*_clk(K, 3, 10)), 1),
    c.eq("missing is None", lambda: (lambda t, k: k.get("zz"))(*_clk(K, 3, 10)), None),
    c.eq("update value", lambda: (lambda t, k: (k.put("a", 1), k.put("a", 2), k.get("a"))[-1])(*_clk(K, 3, 10)), 2),
    c.eq("expiry", lambda: (lambda t, k: (k.put("a", 1), t.advance(10), k.get("a"))[-1])(*_clk(K, 3, 10)), None),
    c.eq("not yet expired", lambda: (lambda t, k: (k.put("a", 1), t.advance(9), k.get("a"))[-1])(*_clk(K, 3, 10)), 1),
    c.eq("put resets ttl", lambda: (lambda t, k: (k.put("a", 1), t.advance(9), k.put("a", 5), t.advance(9), k.get("a"))[-1])(*_clk(K, 3, 10)), 5),
    c.eq("get does not reset ttl", lambda: (lambda t, k: (k.put("a", 1), t.advance(9), k.get("a"), t.advance(2), k.get("a"))[-1])(*_clk(K, 3, 10)), None),
    c.eq("lru evicts oldest", lambda: (lambda t, k: (k.put("a", 1), k.put("b", 2), k.put("c", 3), k.put("d", 4), k.get("a"))[-1])(*_clk(K, 3, 100)), None),
    c.eq("lru keeps recent", lambda: (lambda t, k: (k.put("a", 1), k.put("b", 2), k.put("c", 3), k.put("d", 4), k.get("d"))[-1])(*_clk(K, 3, 100)), 4),
    c.eq("get refreshes lru", lambda: (lambda t, k: (k.put("a", 1), k.put("b", 2), k.put("c", 3), k.get("a"), k.put("d", 4), k.get("a"))[-1])(*_clk(K, 3, 100)), 1),
    c.eq("get refreshes lru evicts b", lambda: (lambda t, k: (k.put("a", 1), k.put("b", 2), k.put("c", 3), k.get("a"), k.put("d", 4), k.get("b"))[-1])(*_clk(K, 3, 100)), None),
    c.eq("len counts live", lambda: (lambda t, k: (k.put("a", 1), k.put("b", 2), len(k))[-1])(*_clk(K, 3, 100)), 2),
    c.eq("len excludes expired", lambda: (lambda t, k: (k.put("a", 1), t.advance(50), len(k))[-1])(*_clk(K, 3, 10)), 0),
    c.r))(C(), ns["TTLCache"])[-1])


# -------------------------------------------------------------- 5. json path
task("jsonpath", '''Implement a small JSONPath query engine in pure Python (stdlib only).

Define at module level:

    def query(data, path: str) -> list

`data` is nested dicts/lists. `path` always starts with "$".
Supported steps:
  .key        descend into a dict key
  [n]         index into a list (n is a non-negative integer)
  [*]         every element of a list
  .*          every value of a dict

Return a LIST of all matching values, in document order. A step that does not
match anything contributes nothing (no error). "$" alone returns [data].

Examples:
  query({"a":{"b":1}}, "$.a.b")            -> [1]
  query({"a":[10,20]}, "$.a[1]")           -> [20]
  query({"a":[{"b":1},{"b":2}]}, "$.a[*].b") -> [1,2]

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, q: (
    c.eq("root", lambda: q({"a": 1}, "$"), [{"a": 1}]),
    c.eq("one key", lambda: q({"a": 1}, "$.a"), [1]),
    c.eq("nested key", lambda: q({"a": {"b": 2}}, "$.a.b"), [2]),
    c.eq("index", lambda: q({"a": [10, 20]}, "$.a[1]"), [20]),
    c.eq("index zero", lambda: q({"a": [10, 20]}, "$.a[0]"), [10]),
    c.eq("wildcard list", lambda: q({"a": [1, 2, 3]}, "$.a[*]"), [1, 2, 3]),
    c.eq("wildcard then key", lambda: q({"a": [{"b": 1}, {"b": 2}]}, "$.a[*].b"), [1, 2]),
    c.eq("dict wildcard", lambda: q({"a": {"x": 1, "y": 2}}, "$.a.*"), [1, 2]),
    c.eq("missing key empty", lambda: q({"a": 1}, "$.zz"), []),
    c.eq("index out of range", lambda: q({"a": [1]}, "$.a[5]"), []),
    c.eq("deep chain", lambda: q({"a": {"b": {"c": [7, 8]}}}, "$.a.b.c[1]"), [8]),
    c.eq("wildcard missing key skips", lambda: q({"a": [{"b": 1}, {"z": 9}]}, "$.a[*].b"), [1]),
    c.eq("root list wildcard", lambda: q([1, 2], "$[*]"), [1, 2]),
    c.eq("key on list empty", lambda: q({"a": [1, 2]}, "$.a.b"), []),
    c.r))(C(), ns["query"])[-1])


# ------------------------------------------------------------ 6. shunting yd
task("expr-evaluator", '''Implement an arithmetic expression evaluator in pure Python (stdlib only).

Define at module level:

    class ParseError(Exception): pass

    def evaluate(expr: str) -> float

Support:
  - numeric literals (integer or decimal)
  - binary + - * / with standard precedence, left-associative
  - binary ^ for exponentiation, RIGHT-associative, higher precedence than * /
  - unary minus, which binds tighter than binary operators but looser than ^
    so -2^2 is -4
  - parentheses
  - two-argument functions max(a,b) and min(a,b), case-insensitive, nestable
  - arbitrary whitespace

Raise ParseError on malformed input. Raise ParseError on division by zero.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, e, E: (
    c.eq("int", lambda: e("42"), 42),
    c.eq("decimal", lambda: e("3.5"), 3.5),
    c.eq("add", lambda: e("1+2"), 3),
    c.eq("precedence", lambda: e("2+3*4"), 14),
    c.eq("parens", lambda: e("(2+3)*4"), 20),
    c.eq("left assoc minus", lambda: e("10-3-2"), 5),
    c.eq("left assoc div", lambda: e("100/5/2"), 10),
    c.eq("unary minus", lambda: e("-5+3"), -2),
    c.eq("double negative", lambda: e("3 - -2"), 5),
    c.eq("pow", lambda: e("2^3"), 8),
    c.eq("pow right assoc", lambda: e("2^3^2"), 512),
    c.eq("unary vs pow", lambda: e("-2^2"), -4),
    c.eq("pow precedence", lambda: e("2*3^2"), 18),
    c.eq("max fn", lambda: e("max(3,7)"), 7),
    c.eq("min fn", lambda: e("min(3,7)"), 3),
    c.eq("fn case insensitive", lambda: e("MAX(1,2)"), 2),
    c.eq("nested fn", lambda: e("max(1,min(5,3))"), 3),
    c.eq("fn in expr", lambda: e("max(2,3)*2"), 6),
    c.eq("whitespace", lambda: e("  1  +  2  "), 3),
    c.raises("malformed", lambda: e("2+*3"), E),
    c.raises("unbalanced", lambda: e("(1+2"), E),
    c.raises("div zero", lambda: e("1/0"), E),
    c.r))(C(), ns["evaluate"], ns["ParseError"])[-1])


# ----------------------------------------------------------------- 7. trie
task("fuzzy-trie", '''Implement a trie with fuzzy search in pure Python (stdlib only).

Define at module level:

    class Trie:
        def insert(self, word: str) -> None
        def search(self, word: str) -> bool
        def starts_with(self, prefix: str) -> list
        def fuzzy(self, word: str, max_dist: int = 1) -> list

- `search` is exact membership.
- `starts_with` returns every inserted word having that prefix, sorted
  alphabetically. A word is a prefix of itself.
- `fuzzy` returns every inserted word whose Levenshtein edit distance from
  `word` is <= max_dist, sorted alphabetically. Levenshtein counts single
  character insertions, deletions and substitutions.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, T: (
    c.eq("insert search", lambda: (lambda t: (t.insert("cat"), t.search("cat"))[-1])(T()), True),
    c.eq("search absent", lambda: (lambda t: (t.insert("cat"), t.search("dog"))[-1])(T()), False),
    c.eq("prefix not word", lambda: (lambda t: (t.insert("cat"), t.search("ca"))[-1])(T()), False),
    c.eq("starts_with", lambda: (lambda t: ([t.insert(w) for w in ("cat", "car", "dog")], t.starts_with("ca"))[-1])(T()), ["car", "cat"]),
    c.eq("starts_with self", lambda: (lambda t: (t.insert("cat"), t.starts_with("cat"))[-1])(T()), ["cat"]),
    c.eq("starts_with none", lambda: (lambda t: (t.insert("cat"), t.starts_with("zz"))[-1])(T()), []),
    c.eq("starts_with empty prefix", lambda: (lambda t: ([t.insert(w) for w in ("b", "a")], t.starts_with(""))[-1])(T()), ["a", "b"]),
    c.eq("fuzzy exact", lambda: (lambda t: (t.insert("cat"), t.fuzzy("cat", 1))[-1])(T()), ["cat"]),
    c.eq("fuzzy substitution", lambda: (lambda t: (t.insert("cat"), t.fuzzy("bat", 1))[-1])(T()), ["cat"]),
    c.eq("fuzzy deletion", lambda: (lambda t: (t.insert("cat"), t.fuzzy("ct", 1))[-1])(T()), ["cat"]),
    c.eq("fuzzy insertion", lambda: (lambda t: (t.insert("cat"), t.fuzzy("cart", 1))[-1])(T()), ["cat"]),
    c.eq("fuzzy too far", lambda: (lambda t: (t.insert("cat"), t.fuzzy("dogs", 1))[-1])(T()), []),
    c.eq("fuzzy dist2", lambda: (lambda t: (t.insert("cat"), t.fuzzy("bam", 2))[-1])(T()), ["cat"]),
    c.eq("fuzzy multiple sorted", lambda: (lambda t: ([t.insert(w) for w in ("cat", "bat", "rat")], t.fuzzy("cat", 1))[-1])(T()), ["bat", "cat", "rat"]),
    c.eq("fuzzy zero dist", lambda: (lambda t: ([t.insert(w) for w in ("cat", "bat")], t.fuzzy("cat", 0))[-1])(T()), ["cat"]),
    c.r))(C(), ns["Trie"])[-1])


# ---------------------------------------------------------------- 8. semver
task("semver-resolver", '''Implement a semantic-version constraint resolver in pure Python (stdlib only).

Define at module level:

    def resolve(constraint: str, versions: list) -> str

`versions` is a list of version strings like "1.2.3" (always MAJOR.MINOR.PATCH,
all non-negative integers). Return the HIGHEST version satisfying the
constraint, or None if none does.

Constraint forms:
  "1.2.3"    exactly that version
  "*"        any version
  ">=1.2.0"  also >, <=, <
  "^1.2.3"   >=1.2.3 and <2.0.0   (same MAJOR; if MAJOR is 0, ^0.2.3 means
             >=0.2.3 and <0.3.0, i.e. same MINOR)
  "~1.2.3"   >=1.2.3 and <1.3.0   (same MAJOR and MINOR)

Version comparison is numeric per component, not lexicographic: 1.10.0 > 1.9.0.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, r: (
    c.eq("exact", lambda: r("1.2.3", ["1.2.3", "1.2.4"]), "1.2.3"),
    c.eq("exact missing", lambda: r("9.9.9", ["1.2.3"]), None),
    c.eq("star highest", lambda: r("*", ["1.0.0", "2.0.0", "1.5.0"]), "2.0.0"),
    c.eq("numeric not lexi", lambda: r("*", ["1.9.0", "1.10.0"]), "1.10.0"),
    c.eq("gte", lambda: r(">=1.2.0", ["1.1.0", "1.2.0", "1.3.0"]), "1.3.0"),
    c.eq("gt", lambda: r(">1.2.0", ["1.2.0", "1.2.1"]), "1.2.1"),
    c.eq("lte", lambda: r("<=1.2.0", ["1.1.0", "1.2.0", "1.3.0"]), "1.2.0"),
    c.eq("lt", lambda: r("<1.2.0", ["1.1.0", "1.2.0"]), "1.1.0"),
    c.eq("caret major", lambda: r("^1.2.3", ["1.2.3", "1.9.9", "2.0.0"]), "1.9.9"),
    c.eq("caret excludes next major", lambda: r("^1.2.3", ["2.0.0"]), None),
    c.eq("caret floor", lambda: r("^1.2.3", ["1.2.2"]), None),
    c.eq("caret zero major", lambda: r("^0.2.3", ["0.2.9", "0.3.0"]), "0.2.9"),
    c.eq("tilde", lambda: r("~1.2.3", ["1.2.3", "1.2.9", "1.3.0"]), "1.2.9"),
    c.eq("tilde excludes minor bump", lambda: r("~1.2.3", ["1.3.0"]), None),
    c.eq("none match", lambda: r(">=5.0.0", ["1.0.0"]), None),
    c.eq("empty list", lambda: r("*", []), None),
    c.r))(C(), ns["resolve"])[-1])


# ------------------------------------------------------------------ 9. diff
task("line-diff", '''Implement a line diff in pure Python (stdlib only).

Define at module level:

    def diff(a: list, b: list) -> list

`a` and `b` are lists of strings (lines). Return a list of (op, line) tuples
where op is one of "equal", "delete", "insert".

The result must, read in order, transform `a` into `b`:
  - "equal"  line present in both
  - "delete" line present in `a` only
  - "insert" line present in `b` only

Use a longest-common-subsequence diff so the number of equal lines is MAXIMAL.
When a line is both deleted and inserted at the same position, emit the
"delete" tuple BEFORE the "insert" tuple.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, d: (
    c.eq("identical", lambda: d(["a", "b"], ["a", "b"]), [("equal", "a"), ("equal", "b")]),
    c.eq("empty both", lambda: d([], []), []),
    c.eq("all insert", lambda: d([], ["a"]), [("insert", "a")]),
    c.eq("all delete", lambda: d(["a"], []), [("delete", "a")]),
    c.eq("append", lambda: d(["a"], ["a", "b"]), [("equal", "a"), ("insert", "b")]),
    c.eq("prepend", lambda: d(["b"], ["a", "b"]), [("insert", "a"), ("equal", "b")]),
    c.eq("remove middle", lambda: d(["a", "b", "c"], ["a", "c"]),
         [("equal", "a"), ("delete", "b"), ("equal", "c")]),
    c.eq("replace delete first", lambda: d(["a", "x", "c"], ["a", "y", "c"]),
         [("equal", "a"), ("delete", "x"), ("insert", "y"), ("equal", "c")]),
    c.eq("maximal lcs", lambda: d(["a", "b", "c", "d"], ["a", "c", "d"]),
         [("equal", "a"), ("delete", "b"), ("equal", "c"), ("equal", "d")]),
    c.eq("disjoint", lambda: d(["x"], ["y"]), [("delete", "x"), ("insert", "y")]),
    c.eq("roundtrip a", lambda: [l for o, l in d(["a", "b", "c"], ["a", "c"]) if o in ("equal", "delete")], ["a", "b", "c"]),
    c.eq("roundtrip b", lambda: [l for o, l in d(["a", "b", "c"], ["a", "c"]) if o in ("equal", "insert")], ["a", "c"]),
    c.eq("roundtrip b complex", lambda: [l for o, l in d(["a", "x", "c"], ["a", "y", "c"]) if o in ("equal", "insert")], ["a", "y", "c"]),
    c.r))(C(), ns["diff"])[-1])


# --------------------------------------------------------- 10. state machine
task("state-machine", '''Implement a finite state machine in pure Python (stdlib only).

Define at module level:

    class InvalidTransition(Exception): pass

    class Machine:
        def __init__(self, transitions: dict, initial: str): ...
        @property
        def state(self) -> str: ...
        def apply(self, event: str) -> str: ...
        def history(self) -> list: ...
        def can(self, event: str) -> bool: ...
        def replay(self, events: list) -> str: ...
        def reset(self) -> None: ...

`transitions` maps a state name to a dict of {event_name: next_state}.

- `apply(event)` moves to the next state and returns it. If the event is not
  valid from the current state, raise InvalidTransition and leave the state
  and history UNCHANGED.
- `history()` returns the list of events successfully applied, in order.
- `can(event)` returns True if the event is valid from the current state.
- `replay(events)` applies each event in order from the CURRENT state and
  returns the final state. If any event is invalid, raise InvalidTransition
  and leave the machine exactly as it was BEFORE replay started (atomic).
- `reset()` returns to the initial state and clears history.

Output ONLY the Python module source. No fences, no commentary.''',
lambda ns: (lambda c, M, E, TR: (
    c.eq("initial state", lambda: M(TR, "idle").state, "idle"),
    c.eq("apply returns", lambda: M(TR, "idle").apply("start"), "running"),
    c.eq("state after apply", lambda: (lambda m: (m.apply("start"), m.state)[-1])(M(TR, "idle")), "running"),
    c.eq("two steps", lambda: (lambda m: (m.apply("start"), m.apply("finish"), m.state)[-1])(M(TR, "idle")), "done"),
    c.eq("history", lambda: (lambda m: (m.apply("start"), m.apply("finish"), m.history())[-1])(M(TR, "idle")), ["start", "finish"]),
    c.eq("history empty", lambda: M(TR, "idle").history(), []),
    c.eq("can true", lambda: M(TR, "idle").can("start"), True),
    c.eq("can false", lambda: M(TR, "idle").can("finish"), False),
    c.raises("invalid raises", lambda: M(TR, "idle").apply("finish"), E),
    c.eq("state unchanged after invalid", lambda: (lambda m: (_swallow(lambda: m.apply("finish")), m.state)[-1])(M(TR, "idle")), "idle"),
    c.eq("history unchanged after invalid", lambda: (lambda m: (_swallow(lambda: m.apply("finish")), m.history())[-1])(M(TR, "idle")), []),
    c.eq("replay ok", lambda: M(TR, "idle").replay(["start", "finish"]), "done"),
    c.raises("replay invalid raises", lambda: M(TR, "idle").replay(["start", "bogus"]), E),
    c.eq("replay atomic state", lambda: (lambda m: (_swallow(lambda: m.replay(["start", "bogus"])), m.state)[-1])(M(TR, "idle")), "idle"),
    c.eq("replay atomic history", lambda: (lambda m: (_swallow(lambda: m.replay(["start", "bogus"])), m.history())[-1])(M(TR, "idle")), []),
    c.eq("reset state", lambda: (lambda m: (m.apply("start"), m.reset(), m.state)[-1])(M(TR, "idle")), "idle"),
    c.eq("reset history", lambda: (lambda m: (m.apply("start"), m.reset(), m.history())[-1])(M(TR, "idle")), []),
    c.r))(C(), ns["Machine"], ns["InvalidTransition"],
          {"idle": {"start": "running"}, "running": {"finish": "done", "cancel": "idle"}, "done": {}})[-1])


# --------------------------------------------------------------------- utils
class _Clock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t
    def advance(self, d): self.t += d

def _clk(K, cap, ttl):
    c = _Clock()
    return c, K(cap, ttl, c)

def _swallow(fn):
    try: fn()
    except Exception: pass
    return None


# ================================================================== pipeline

def score(ns, tests):
    res = tests(ns)
    return sum(1 for _, ok, _ in res if ok), len(res), res


def attempt(prompt, tests, budget, label):
    try:
        text, finish, usage, dt = ask(prompt, budget, False)
    except Exception as e:
        return None, "request failed: %r" % (e,), 0, 0, None
    if finish == "length":
        return None, "TRUNCATED at %d tokens" % usage["completion_tokens"], 0, dt, None
    code = strip_fences(text)
    ns = {}
    try:
        exec(compile(code, "<gen>", "exec"), ns)
    except Exception as e:
        return None, "import error: %s: %s" % (type(e).__name__, e), 0, dt, code
    try:
        p, n, res = score(ns, tests)
    except Exception as e:
        return None, "suite crashed: %s: %s" % (type(e).__name__, e), 0, dt, code
    return (p, n, res), None, usage["completion_tokens"], dt, code


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    out = []
    for i, t in enumerate(T, 1):
        if only and only != t["name"]:
            continue
        print("\n" + "=" * 72, flush=True)
        print("TASK %d/%d: %s" % (i, len(T), t["name"]), flush=True)
        print("=" * 72, flush=True)

        r1, err1, tok1, dt1, code1 = attempt(t["prompt"], t["tests"], 4096, "r1")
        if r1 is None:
            print("  ROUND 1 FAILED: %s (%.1fs)" % (err1, dt1), flush=True)
            out.append({"task": t["name"], "r1": None, "r2": None,
                        "n": None, "err1": err1, "t1": dt1, "t2": None})
            continue
        p1, n, res1 = r1
        print("  round 1: %d/%d  (%d tok, %.1fs)" % (p1, n, tok1, dt1), flush=True)
        for name, ok, d in res1:
            if not ok:
                print("     FAIL %-38s %s" % (name, d), flush=True)

        if p1 == n:
            out.append({"task": t["name"], "r1": p1, "r2": p1, "n": n,
                        "err1": None, "t1": dt1, "t2": 0.0})
            print("  perfect on round 1, no repair needed", flush=True)
            continue

        fails = "\n".join("  - %s: %s" % (name, d) for name, ok, d in res1 if not ok)
        fb = ("""Your implementation of the following task failed %d of %d hidden tests.

ORIGINAL TASK
-------------
%s

YOUR IMPLEMENTATION
-------------------
%s

FAILING TESTS (test name: actual vs expected)
---------------------------------------------
%s

Rewrite the COMPLETE module fixing these failures while keeping everything that
already passes. Output ONLY the Python module source, no fences, no commentary.
""" % (n - p1, n, t["prompt"], code1, fails))

        r2, err2, tok2, dt2, code2 = attempt(fb, t["tests"], 6144, "r2")
        if r2 is None:
            print("  ROUND 2 FAILED: %s (%.1fs)" % (err2, dt2), flush=True)
            out.append({"task": t["name"], "r1": p1, "r2": None, "n": n,
                        "err1": None, "t1": dt1, "t2": dt2})
            continue
        p2, _, res2 = r2
        print("  round 2: %d/%d  (%d tok, %.1fs)   delta %+d" % (p2, n, tok2, dt2, p2 - p1), flush=True)
        for name, ok, d in res2:
            if not ok:
                print("     STILL FAIL %-33s %s" % (name, d), flush=True)
        out.append({"task": t["name"], "r1": p1, "r2": p2, "n": n,
                    "err1": None, "t1": dt1, "t2": dt2})

    print("\n\n" + "=" * 72)
    print("COMPARISON")
    print("=" * 72)
    print("%-20s %>8s %>8s %>8s %>9s" .replace(">", "") % ("task", "round1", "round2", "tests", "time(s)"))
    print("-" * 72)
    tot1 = tot2 = totn = 0
    for r in out:
        if r["r1"] is None:
            print("%-20s %8s %8s %8s %9.1f   %s" % (r["task"], "ERR", "-", "-", r["t1"] or 0, r["err1"]))
            continue
        n = r["n"]; totn += n; tot1 += r["r1"]
        tot2 += (r["r2"] if r["r2"] is not None else r["r1"])
        print("%-20s %8s %8s %8d %9.1f" % (
            r["task"], "%d" % r["r1"],
            ("%d" % r["r2"]) if r["r2"] is not None else "ERR",
            n, (r["t1"] or 0) + (r["t2"] or 0)))
    print("-" * 72)
    if totn:
        print("%-20s %8d %8d %8d" % ("TOTAL", tot1, tot2, totn))
        print("%-20s %7.1f%% %7.1f%%" % ("pass rate", 100.0 * tot1 / totn, 100.0 * tot2 / totn))
    json.dump(out, open("/home/datasec-rd/spark-eval/suite10_results.json", "w"), indent=2)
    print("\nraw -> /home/datasec-rd/spark-eval/suite10_results.json")


if __name__ == "__main__":
    main()
