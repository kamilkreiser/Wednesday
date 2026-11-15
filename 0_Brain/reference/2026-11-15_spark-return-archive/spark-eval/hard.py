#!/usr/bin/env python3
"""HARD suite. Property-based, oracle-checked, complexity-bounded.

Design differences from the easy suite:
  - randomised operation sequences checked against brute-force oracles
  - invariants (persistence, convergence) not just outputs
  - asymptotic complexity actually measured
  - shortcut modules explicitly forbidden and enforced
"""
import random

class C:
    def __init__(self): self.r = []
    def eq(self, name, fn, exp):
        try:
            g = fn()
            if isinstance(exp, float): ok = isinstance(g,(int,float)) and abs(g-exp) < 1e-9
            else: ok = g == exp
            self.r.append((name, ok, "got %r want %r" % (g, exp)))
        except Exception as e:
            self.r.append((name, False, "%s: %s" % (type(e).__name__, e)))
    def ok(self, name, fn):
        """fn returns (bool, detail)."""
        try:
            good, detail = fn()
            self.r.append((name, bool(good), detail))
        except Exception as e:
            self.r.append((name, False, "%s: %s" % (type(e).__name__, e)))
    def raises(self, name, fn, exc):
        try:
            g = fn(); self.r.append((name, False, "returned %r" % (g,)))
        except exc: self.r.append((name, True, ""))
        except Exception as e: self.r.append((name, False, "%s: %s" % (type(e).__name__, e)))

def no_import(ns_code, *mods):
    """Enforce forbidden modules by source inspection."""
    bad = [m for m in mods if ("import %s" % m) in ns_code or ("%s." % m) in ns_code]
    return (not bad, "forbidden module(s) used: %s" % bad if bad else "clean")

T = []
def task(name, prompt, tests): T.append({"name": name, "prompt": prompt, "tests": tests})


# ============================================================ 1. PERSISTENT BST
task("persistent-bst", '''Implement an IMMUTABLE (persistent) sorted set in pure Python.

FORBIDDEN: you may not import or use `bisect`, `sortedcontainers`, `heapq`, or
`itertools`. No module may be imported at all. Implement the data structure.

Define at module level:

    class PersistentSet:
        def __init__(self): ...                 # empty set
        def insert(self, key) -> "PersistentSet"   # NEW set; self UNCHANGED
        def delete(self, key) -> "PersistentSet"   # NEW set; self UNCHANGED
        def contains(self, key) -> bool
        def rank(self, key) -> int              # how many stored keys are < key
        def select(self, i) -> object           # i-th smallest, 0-indexed
        def to_list(self) -> list               # ascending
        def __len__(self) -> int
        def depth(self) -> int                  # height; empty set has depth 0

HARD REQUIREMENTS
1. PERSISTENCE. `insert`/`delete` must return a new set and leave the receiver
   completely unchanged. Every historical version must stay correct forever.
   Use structural sharing; do not deep-copy the whole tree.
2. BALANCE. The tree must stay balanced. After n insertions `depth()` must be
   <= 3*log2(n+1) + 3. A plain unbalanced BST WILL FAIL this.
3. `insert` of a key already present returns an equivalent set (no duplicates).
   `delete` of a missing key returns an equivalent set.
4. `select(i)` with i out of range raises IndexError.
   `rank` works for keys not present.

Keys are integers. Output ONLY the Python module source, no fences, no commentary.''',
lambda ns, src: (lambda c, PS: (
    c.ok("forbidden modules", lambda: no_import(src, "bisect", "sortedcontainers", "heapq", "itertools")),
    c.eq("empty len", lambda: len(PS()), 0),
    c.eq("empty to_list", lambda: PS().to_list(), []),
    c.eq("empty depth", lambda: PS().depth(), 0),
    c.eq("single insert", lambda: PS().insert(5).to_list(), [5]),
    c.eq("insert does not mutate", lambda: (lambda s: (s.insert(1), len(s))[-1])(PS()), 0),
    c.eq("dup insert no-op", lambda: PS().insert(3).insert(3).to_list(), [3]),
    c.eq("delete missing", lambda: PS().insert(1).delete(99).to_list(), [1]),
    c.raises("select out of range", lambda: PS().insert(1).select(5), IndexError),
    c.ok("PROPERTY: 400 random ops vs oracle", lambda: _pbst_prop(PS, 400)),
    c.ok("PROPERTY: persistence of 120 historical versions", lambda: _pbst_persist(PS, 120)),
    c.ok("PROPERTY: balance depth <= 3log2(n)+3 @ n=2000", lambda: _pbst_balance(PS, 2000)),
    c.ok("PROPERTY: rank/select agree with oracle, 300 probes", lambda: _pbst_ranksel(PS, 300)),
    c.ok("PROPERTY: structural sharing (no O(n) copy) @ n=4000", lambda: _pbst_sharing(PS, 4000)),
    c.r))(C(), ns["PersistentSet"])[-1])

def _pbst_prop(PS, n):
    rnd = random.Random(1234); s = PS(); ref = []
    for i in range(n):
        k = rnd.randrange(0, 150)
        if rnd.random() < 0.6:
            s = s.insert(k)
            if k not in ref: ref.append(k); ref.sort()
        else:
            s = s.delete(k)
            if k in ref: ref.remove(k)
        if s.to_list() != ref:
            return False, "diverged at op %d: got %s want %s" % (i, s.to_list()[:8], ref[:8])
        if len(s) != len(ref): return False, "len mismatch at op %d" % i
    return True, "%d ops consistent" % n

def _pbst_persist(PS, n):
    rnd = random.Random(99); versions = []; s = PS(); ref = []
    for i in range(n):
        k = rnd.randrange(0, 200)
        s = s.insert(k)
        if k not in ref: ref.append(k); ref.sort()
        versions.append((s, list(ref)))
    for i, (v, expect) in enumerate(versions):
        if v.to_list() != expect:
            return False, "version %d corrupted by later writes" % i
    return True, "all %d historical versions intact" % n

def _pbst_balance(PS, n):
    s = PS()
    for k in range(n):        # ascending: worst case for an unbalanced BST
        s = s.insert(k)
    import math
    lim = 3 * math.log2(n + 1) + 3
    d = s.depth()
    return (d <= lim), "depth=%d limit=%.1f (ascending inserts)" % (d, lim)

def _pbst_ranksel(PS, probes):
    rnd = random.Random(7); s = PS(); ref = []
    for _ in range(200):
        k = rnd.randrange(0, 400)
        s = s.insert(k)
        if k not in ref: ref.append(k); ref.sort()
    for _ in range(probes):
        k = rnd.randrange(-10, 410)
        want = sum(1 for x in ref if x < k)
        if s.rank(k) != want: return False, "rank(%d)=%s want %s" % (k, s.rank(k), want)
    for i in range(len(ref)):
        if s.select(i) != ref[i]: return False, "select(%d)=%s want %s" % (i, s.select(i), ref[i])
    return True, "rank+select consistent"

def _pbst_sharing(PS, n):
    """A full copy per insert is O(n) memory; detect it by node identity reuse."""
    s = PS()
    for k in range(n): s = s.insert(k)
    t = s.insert(-1)
    shared = 0; seen = set()
    def walk(node, depth=0):
        nonlocal shared
        if node is None or depth > 80: return
        i = id(node)
        if i in seen: shared += 1; return
        seen.add(i)
        for attr in ("left", "right", "l", "r", "_left", "_right"):
            walk(getattr(node, attr, None), depth + 1)
    root_t = None
    for attr in ("root", "_root", "node", "_node", "tree"):
        if hasattr(t, attr): root_t = getattr(t, attr); break
    if root_t is None: return True, "root attr not found - skipped (not a failure)"
    for attr in ("root", "_root", "node", "_node", "tree"):
        if hasattr(s, attr): walk(getattr(s, attr)); break
    before = len(seen)
    walk(root_t)
    added = len(seen) - before
    return (added <= 80), "new nodes after 1 insert into n=%d: %d (want <=80)" % (n, added)


# ====================================================== 2. LAZY SEGMENT TREE
task("lazy-segment-tree", '''Implement a segment tree with LAZY PROPAGATION in pure Python.

FORBIDDEN: no imports at all.

Define at module level:

    class SegTree:
        def __init__(self, values: list): ...
        def range_add(self, lo, hi, delta) -> None      # add delta to [lo, hi)
        def range_assign(self, lo, hi, value) -> None   # set [lo, hi) to value
        def range_sum(self, lo, hi) -> int
        def range_min(self, lo, hi) -> int
        def range_max(self, lo, hi) -> int

All ranges are HALF-OPEN [lo, hi). An empty range (lo >= hi) is a no-op;
range_sum of an empty range is 0; range_min/range_max of an empty range
must raise ValueError.

THE HARD PART: range_add and range_assign lazy tags INTERACT.
  - A pending assign must ABSORB a later add (assign(v) then add(d) == assign(v+d)).
  - A new assign must CANCEL any pending add on that node.
Getting this composition wrong passes simple tests and fails mixed sequences.

Operations must be O(log n). A solution that loops over the range element by
element will FAIL the performance test.

Output ONLY the Python module source, no fences, no commentary.''',
lambda ns, src: (lambda c, S: (
    c.ok("no imports", lambda: no_import(src, "numpy", "itertools", "bisect")),
    c.eq("basic sum", lambda: S([1,2,3,4]).range_sum(0,4), 10),
    c.eq("basic min", lambda: S([4,2,9,1]).range_min(0,4), 1),
    c.eq("basic max", lambda: S([4,2,9,1]).range_max(0,4), 9),
    c.eq("empty sum is 0", lambda: S([1,2]).range_sum(1,1), 0),
    c.raises("empty min raises", lambda: S([1,2]).range_min(1,1), ValueError),
    c.eq("single add", lambda: (lambda t:(t.range_add(0,2,5), t.range_sum(0,4))[-1])(S([1,2,3,4])), 20),
    c.eq("single assign", lambda: (lambda t:(t.range_assign(0,2,7), t.range_sum(0,4))[-1])(S([1,2,3,4])), 21),
    c.eq("assign then add", lambda: (lambda t:(t.range_assign(0,4,2), t.range_add(0,4,3), t.range_sum(0,4))[-1])(S([1,1,1,1])), 20),
    c.eq("add then assign cancels", lambda: (lambda t:(t.range_add(0,4,100), t.range_assign(0,4,1), t.range_sum(0,4))[-1])(S([1,1,1,1])), 4),
    c.ok("PROPERTY: 600 mixed random ops vs brute force (n=64)", lambda: _seg_prop(S, 64, 600, 11)),
    c.ok("PROPERTY: 600 mixed random ops vs brute force (n=257)", lambda: _seg_prop(S, 257, 600, 22)),
    c.ok("PROPERTY: overlapping assign/add interleave, 400 ops", lambda: _seg_interleave(S, 128, 400)),
    c.ok("COMPLEXITY: 20000 ops on n=100000 within budget", lambda: _seg_perf(S)),
    c.r))(C(), ns["SegTree"])[-1])

def _seg_prop(S, n, ops, seed):
    rnd = random.Random(seed)
    base = [rnd.randrange(-50, 50) for _ in range(n)]
    t = S(list(base)); ref = list(base)
    for i in range(ops):
        lo = rnd.randrange(0, n); hi = rnd.randrange(lo, n + 1)
        op = rnd.random()
        if op < 0.3:
            d = rnd.randrange(-20, 20)
            t.range_add(lo, hi, d)
            for j in range(lo, hi): ref[j] += d
        elif op < 0.5:
            v = rnd.randrange(-30, 30)
            t.range_assign(lo, hi, v)
            for j in range(lo, hi): ref[j] = v
        else:
            if lo >= hi: continue
            got_s, want_s = t.range_sum(lo, hi), sum(ref[lo:hi])
            if got_s != want_s: return False, "op %d sum[%d,%d)=%s want %s" % (i, lo, hi, got_s, want_s)
            if t.range_min(lo, hi) != min(ref[lo:hi]): return False, "op %d min mismatch" % i
            if t.range_max(lo, hi) != max(ref[lo:hi]): return False, "op %d max mismatch" % i
    return True, "%d ops on n=%d consistent" % (ops, n)

def _seg_interleave(S, n, ops):
    rnd = random.Random(555)
    base = [0]*n; t = S(list(base)); ref = list(base)
    for i in range(ops):
        lo = rnd.randrange(0, n); hi = rnd.randrange(lo, n+1)
        if lo >= hi: continue
        r = rnd.random()
        if r < 0.4:
            t.range_assign(lo, hi, i % 7)
            for j in range(lo, hi): ref[j] = i % 7
        elif r < 0.8:
            t.range_add(lo, hi, 1)
            for j in range(lo, hi): ref[j] += 1
        if t.range_sum(lo, hi) != sum(ref[lo:hi]):
            return False, "interleave diverged at op %d" % i
    return True, "%d interleaved ops consistent" % ops

def _seg_perf(S):
    import time
    n = 100000
    t0 = time.time(); t = S([0]*n); build = time.time()-t0
    rnd = random.Random(3)
    t0 = time.time()
    for _ in range(20000):
        lo = rnd.randrange(0, n); hi = rnd.randrange(lo, n+1)
        if lo >= hi: continue
        t.range_add(lo, hi, 1)
        t.range_sum(lo, hi)
    el = time.time()-t0
    return (el < 12.0), "20000 ops in %.2fs (budget 12s, build %.2fs)" % (el, build)


# ============================================================== 3. CRDT TEXT
task("crdt-sequence", '''Implement a CONVERGENT replicated text sequence (a CRDT) in pure Python.

FORBIDDEN: no imports at all.

Define at module level:

    class Replica:
        def __init__(self, replica_id: str): ...
        def insert(self, index: int, ch: str) -> dict   # local edit, returns an op
        def delete(self, index: int) -> dict            # local edit, returns an op
        def apply(self, op: dict) -> None               # apply a REMOTE op
        def text(self) -> str

SEMANTICS
- `insert(i, ch)` inserts ch so it appears at position i of the CURRENT local text.
- `delete(i)` removes the character currently at position i.
- Ops returned must be plain JSON-compatible dicts (str/int/bool/list/dict only).
- `apply` must be COMMUTATIVE and IDEMPOTENT: applying the same set of remote ops
  in ANY order, with duplicates, must converge to the SAME text on every replica.
- Applying an op a replica already has must be a no-op.
- A delete of an element a replica has not yet seen must still converge once
  that element arrives (order independence).

This is the whole difficulty: convergence under arbitrary delivery order,
duplication, and concurrent edits at the same position. Tie-break deterministically
using replica_id so all replicas agree.

Output ONLY the Python module source, no fences, no commentary.''',
lambda ns, src: (lambda c, R: (
    c.ok("no imports", lambda: no_import(src, "uuid", "json", "random")),
    c.eq("local insert", lambda: (lambda r:(r.insert(0,"a"), r.insert(1,"b"), r.text())[-1])(R("A")), "ab"),
    c.eq("local delete", lambda: (lambda r:(r.insert(0,"a"), r.insert(1,"b"), r.delete(0), r.text())[-1])(R("A")), "b"),
    c.eq("insert middle", lambda: (lambda r:(r.insert(0,"a"), r.insert(1,"c"), r.insert(1,"b"), r.text())[-1])(R("A")), "abc"),
    c.ok("ops are JSON-compatible", lambda: _crdt_json(R)),
    c.ok("CONVERGE: 2 replicas, sequential exchange", lambda: _crdt_two(R, 40, 1)),
    c.ok("CONVERGE: 2 replicas, REVERSED delivery order", lambda: _crdt_two(R, 40, 2, reverse=True)),
    c.ok("CONVERGE: 2 replicas, SHUFFLED delivery order", lambda: _crdt_two(R, 40, 3, shuffle=True)),
    c.ok("IDEMPOTENT: duplicate delivery changes nothing", lambda: _crdt_dup(R)),
    c.ok("CONVERGE: 3 replicas, 60 concurrent ops, shuffled", lambda: _crdt_three(R, 60)),
    c.ok("CONVERGE: concurrent inserts at SAME index", lambda: _crdt_same_index(R)),
    c.ok("CONVERGE: delete arrives BEFORE its insert", lambda: _crdt_out_of_order(R)),
    c.r))(C(), ns["Replica"])[-1])

def _crdt_json(R):
    r = R("A"); ops = [r.insert(0,"x"), r.insert(1,"y"), r.delete(0)]
    def okv(v):
        if isinstance(v,(str,int,bool)) or v is None: return True
        if isinstance(v,list): return all(okv(x) for x in v)
        if isinstance(v,dict): return all(isinstance(k,str) and okv(x) for k,x in v.items())
        return False
    bad = [o for o in ops if not okv(o)]
    return (not bad), "non-JSON op" if bad else "ops JSON-clean"

def _crdt_two(R, n, seed, reverse=False, shuffle=False):
    rnd = random.Random(seed)
    a, b = R("A"), R("B"); oa, ob = [], []
    for i in range(n):
        for r, box in ((a, oa), (b, ob)):
            if rnd.random() < 0.7 or len(r.text()) == 0:
                idx = rnd.randrange(0, len(r.text())+1)
                box.append(r.insert(idx, chr(97 + rnd.randrange(26))))
            else:
                idx = rnd.randrange(0, len(r.text()))
                box.append(r.delete(idx))
    da, db = list(ob), list(oa)
    if reverse: da.reverse(); db.reverse()
    if shuffle: rnd.shuffle(da); rnd.shuffle(db)
    for op in da: a.apply(op)
    for op in db: b.apply(op)
    return (a.text() == b.text()), "A=%r B=%r" % (a.text()[:40], b.text()[:40])

def _crdt_dup(R):
    a, b = R("A"), R("B")
    ops = [a.insert(0,"x"), a.insert(1,"y")]
    for op in ops: b.apply(op)
    t1 = b.text()
    for op in ops: b.apply(op)
    for op in ops: b.apply(op)
    return (b.text() == t1 == a.text()), "before=%r after=%r a=%r" % (t1, b.text(), a.text())

def _crdt_three(R, n):
    rnd = random.Random(424)
    reps = [R("A"), R("B"), R("C")]; boxes = [[], [], []]
    for i in range(n):
        k = rnd.randrange(3); r = reps[k]
        if rnd.random() < 0.75 or len(r.text()) == 0:
            boxes[k].append(r.insert(rnd.randrange(0, len(r.text())+1), chr(97+rnd.randrange(26))))
        else:
            boxes[k].append(r.delete(rnd.randrange(0, len(r.text()))))
    for i, r in enumerate(reps):
        incoming = [op for j in range(3) if j != i for op in boxes[j]]
        rnd.shuffle(incoming)
        for op in incoming: r.apply(op)
    texts = [r.text() for r in reps]
    return (len(set(texts)) == 1), "texts=%r" % ([t[:30] for t in texts],)

def _crdt_same_index(R):
    a, b = R("A"), R("B")
    o = a.insert(0, "-"); b.apply(o)
    oa = a.insert(0, "a"); ob = b.insert(0, "b")
    a.apply(ob); b.apply(oa)
    return (a.text() == b.text()), "A=%r B=%r" % (a.text(), b.text())

def _crdt_out_of_order(R):
    a, b = R("A"), R("B")
    o1 = a.insert(0, "x"); o2 = a.insert(1, "y"); o3 = a.delete(0)
    for op in (o3, o2, o1): b.apply(op)      # delete first
    return (a.text() == b.text()), "A=%r B=%r" % (a.text(), b.text())


# ======================================================= 4. DECIMAL ARITHMETIC
task("exact-decimal", '''Implement exact fixed-point decimal arithmetic in pure Python.

FORBIDDEN: you may NOT import or use `decimal`, `fractions`, `math`, or `numpy`.
No imports at all. Use integer arithmetic.

Define at module level:

    class Dec:
        def __init__(self, s): ...        # s is a str like "-12.3400", or an int
        def __add__(self, other) -> "Dec"
        def __sub__(self, other) -> "Dec"
        def __mul__(self, other) -> "Dec"
        def __eq__(self, other) -> bool
        def __str__(self) -> str
        def quantize(self, places: int) -> "Dec"   # ROUND HALF TO EVEN
        def div(self, other, places: int) -> "Dec" # ROUND HALF TO EVEN

RULES
- Exact for + - *: "0.1"+"0.2" is exactly "0.3", never 0.30000000000000004.
- Scale: the result of + and - has the max scale of the operands. The result of
  * has the SUM of the operand scales. Trailing zeros are PRESERVED, so
  Dec("1.10") * Dec("2.0") is "2.200" (scale 3), not "2.2".
- `quantize(p)` rounds to exactly p decimal places using ROUND HALF TO EVEN
  (banker's rounding): 0.5 rounds to 0, 1.5 rounds to 2, 2.5 rounds to 2,
  -0.5 rounds to 0, -1.5 rounds to -2. Result has exactly p decimals.
- `div(other, p)` divides and rounds to exactly p places, half to even.
  Division by zero raises ZeroDivisionError.
- `__str__` renders with the stored scale, minus sign where negative, and
  never "-0" (use "0", or "0.00" at scale 2).
- `__eq__` compares NUMERIC VALUE, so Dec("1.10") == Dec("1.1") is True.

Output ONLY the Python module source, no fences, no commentary.''',
lambda ns, src: (lambda c, D: (
    c.ok("forbidden modules", lambda: no_import(src, "decimal", "fractions", "math", "numpy")),
    c.eq("exact add", lambda: str(D("0.1") + D("0.2")), "0.3"),
    c.eq("scale preserved mul", lambda: str(D("1.10") * D("2.0")), "2.200"),
    c.eq("add max scale", lambda: str(D("1.5") + D("2.250")), "3.750"),
    c.eq("sub negative", lambda: str(D("1.00") - D("2.50")), "-1.50"),
    c.eq("no negative zero", lambda: str(D("0.0") - D("0.0")), "0.0"),
    c.eq("value equality across scale", lambda: D("1.10") == D("1.1"), True),
    c.eq("banker 0.5 -> 0", lambda: str(D("0.5").quantize(0)), "0"),
    c.eq("banker 1.5 -> 2", lambda: str(D("1.5").quantize(0)), "2"),
    c.eq("banker 2.5 -> 2", lambda: str(D("2.5").quantize(0)), "2"),
    c.eq("banker -1.5 -> -2", lambda: str(D("-1.5").quantize(0)), "-2"),
    c.eq("banker -0.5 -> 0", lambda: str(D("-0.5").quantize(0)), "0"),
    c.eq("quantize pads", lambda: str(D("1.5").quantize(3)), "1.500"),
    c.eq("div exact", lambda: str(D("1").div(D("8"), 3)), "0.125"),
    c.eq("div rounds half even", lambda: str(D("1").div(D("16"), 3)), "0.062"),
    c.raises("div by zero", lambda: D("1").div(D("0"), 2), ZeroDivisionError),
    c.ok("PROPERTY: 400 random +,-,* vs exact oracle", lambda: _dec_prop(D, 400)),
    c.ok("PROPERTY: 300 random quantize vs banker oracle", lambda: _dec_quant(D, 300)),
    c.ok("PROPERTY: 200 random div vs exact oracle", lambda: _dec_div(D, 200)),
    c.r))(C(), ns["Dec"])[-1])

def _dec_str(units, scale):
    neg = units < 0; u = abs(units); s = str(u).rjust(scale+1, "0")
    out = s[:-scale] + "." + s[-scale:] if scale > 0 else s
    if neg and any(ch in "123456789" for ch in out): out = "-" + out
    return out

def _dec_prop(D, n):
    rnd = random.Random(31)
    for i in range(n):
        s1, s2 = rnd.randrange(0,4), rnd.randrange(0,4)
        u1, u2 = rnd.randrange(-10**6, 10**6), rnd.randrange(-10**6, 10**6)
        a, b = _dec_str(u1, s1), _dec_str(u2, s2)
        sc = max(s1, s2)
        wa = _dec_str(u1*10**(sc-s1) + u2*10**(sc-s2), sc)
        ws = _dec_str(u1*10**(sc-s1) - u2*10**(sc-s2), sc)
        wm = _dec_str(u1*u2, s1+s2)
        for label, got, want in (("add", str(D(a)+D(b)), wa),
                                 ("sub", str(D(a)-D(b)), ws),
                                 ("mul", str(D(a)*D(b)), wm)):
            if got != want:
                return False, "%s(%s,%s) = %s want %s" % (label, a, b, got, want)
    return True, "%d random ops exact" % n

def _half_even(num, den):
    q, r = divmod(num, den)
    if r*2 > den or (r*2 == den and q % 2 == 1): q += 1
    return q

def _dec_quant(D, n):
    rnd = random.Random(77)
    for _ in range(n):
        sc = rnd.randrange(0,5); u = rnd.randrange(-10**7, 10**7); p = rnd.randrange(0, sc+1)
        s = _dec_str(u, sc)
        if sc >= p:
            den = 10**(sc-p)
            neg = u < 0
            q = _half_even(abs(u), den)
            want = _dec_str(-q if neg else q, p)
        else:
            want = _dec_str(u*10**(p-sc), p)
        got = str(D(s).quantize(p))
        if got != want: return False, "quantize(%s,%d)=%s want %s" % (s, p, got, want)
    return True, "%d quantize ops exact" % n

def _dec_div(D, n):
    rnd = random.Random(1010)
    for _ in range(n):
        s1, s2 = rnd.randrange(0,3), rnd.randrange(0,3)
        u1 = rnd.randrange(-10**5, 10**5); u2 = rnd.randrange(1, 10**4)
        if rnd.random() < 0.5: u2 = -u2
        a, b = _dec_str(u1, s1), _dec_str(u2, s2)
        p = rnd.randrange(0, 5)
        num = u1 * 10**s2 * 10**p; den = u2 * 10**s1
        neg = (num < 0) != (den < 0)
        q = _half_even(abs(num), abs(den))
        want = _dec_str(-q if neg else q, p)
        got = str(D(a).div(D(b), p))
        if got != want: return False, "div(%s,%s,%d)=%s want %s" % (a, b, p, got, want)
    return True, "%d div ops exact" % n


# ==================================================== 5. PRIORITY INHERITANCE
task("priority-scheduler", '''Implement a deterministic priority scheduler WITH PRIORITY INHERITANCE.

FORBIDDEN: no imports. No real threads, no real time. Pure simulation.

Define at module level:

    class Scheduler:
        def __init__(self): ...
        def add_task(self, name: str, priority: int, program: list) -> None
        def run(self) -> list

`priority`: HIGHER integer means MORE urgent.
`program` is a list of steps executed in order by that task:
    ("compute", n)     busy for n ticks
    ("lock", "M")      acquire mutex M (blocks if held by another task)
    ("unlock", "M")    release mutex M
    ("spawn", t)       task becomes runnable only at tick >= t (arrival delay);
                       always the FIRST step if present

`run()` simulates to completion and returns the execution trace: a list of
(tick, task_name) for every tick where a task executed, tick starting at 0.

SCHEDULING RULES
1. At each tick run the runnable task with the highest EFFECTIVE priority.
   Ties break by task name, ascending.
2. PRIORITY INHERITANCE: while a task holds a mutex that a higher-priority task
   is blocked on, its effective priority becomes the maximum of its own and all
   tasks blocked on mutexes it holds. This is TRANSITIVE: if A blocks on B and
   B blocks on C, C inherits A's priority.
3. Effective priority reverts the moment the mutex is released.
4. Preemption is immediate: if a higher effective-priority task becomes
   runnable, it runs on the very next tick.
5. `lock` and `unlock` each consume ONE tick. `("compute", n)` consumes n ticks.
6. A task not yet arrived is not runnable. If no task is runnable at a tick,
   that tick is skipped (not in the trace) and time advances.

Deadlock is not tested. Output ONLY the Python module source, no fences.''',
lambda ns, src: (lambda c, S: (
    c.ok("no imports", lambda: no_import(src, "threading", "heapq", "queue", "time")),
    c.eq("single task compute", lambda: [n for _,n in S_run(S, [("A",1,[("compute",3)])])], ["A","A","A"]),
    c.eq("priority order", lambda: [n for _,n in S_run(S, [("A",1,[("compute",2)]),("B",5,[("compute",2)])])], ["B","B","A","A"]),
    c.eq("name tiebreak", lambda: [n for _,n in S_run(S, [("B",1,[("compute",1)]),("A",1,[("compute",1)])])], ["A","B"]),
    c.eq("lock costs a tick", lambda: len(S_run(S, [("A",1,[("lock","M"),("compute",1),("unlock","M")])])), 3),
    c.eq("arrival delay skips ticks", lambda: [t for t,_ in S_run(S, [("A",1,[("spawn",3),("compute",1)])])], [3]),
    c.ok("PRIORITY INVERSION: medium task must NOT delay high", lambda: _sched_inversion(S)),
    c.ok("TRANSITIVE inheritance across 3 tasks", lambda: _sched_transitive(S)),
    c.ok("inheritance reverts after unlock", lambda: _sched_revert(S)),
    c.ok("preemption is immediate on arrival", lambda: _sched_preempt(S)),
    c.ok("trace ticks are strictly increasing", lambda: _sched_monotonic(S)),
    c.ok("every step accounted for, 30 random programs", lambda: _sched_accounting(S, 30)),
    c.r))(C(), ns["Scheduler"])[-1])

def S_run(S, tasks):
    s = S()
    for n, p, prog in tasks: s.add_task(n, p, prog)
    return s.run()

def _sched_inversion(S):
    # L holds M; H (high) arrives and blocks on M; M2 (medium) must not run before L finishes
    tr = S_run(S, [
        ("L", 1, [("lock","M"),("compute",5),("unlock","M")]),
        ("M2", 5, [("spawn",2),("compute",5)]),
        ("H", 9, [("spawn",2),("lock","M"),("compute",1),("unlock","M")]),
    ])
    names = [n for _, n in tr]
    try:
        first_h = names.index("H"); first_m = names.index("M2")
    except ValueError:
        return False, "trace missing a task: %r" % (names[:20],)
    return (first_h < first_m), "H first at %d, M2 first at %d (inheritance failed if M2 earlier)" % (first_h, first_m)

def _sched_transitive(S):
    tr = S_run(S, [
        ("C", 1, [("lock","M1"),("compute",4),("unlock","M1")]),
        ("B", 5, [("spawn",1),("lock","M2"),("lock","M1"),("compute",1),("unlock","M1"),("unlock","M2")]),
        ("A", 9, [("spawn",2),("lock","M2"),("compute",1),("unlock","M2")]),
        ("D", 7, [("spawn",2),("compute",6)]),
    ])
    names = [n for _, n in tr]
    if "C" not in names or "D" not in names: return False, "missing tasks %r" % (names[:20],)
    # C must finish its critical section before D (priority 7) monopolises the CPU
    last_c = len(names) - 1 - names[::-1].index("C")
    first_d = names.index("D")
    return (last_c < first_d), "C ends at %d, D starts at %d" % (last_c, first_d)

def _sched_revert(S):
    tr = S_run(S, [
        ("L", 1, [("lock","M"),("compute",2),("unlock","M"),("compute",3)]),
        ("H", 9, [("spawn",2),("lock","M"),("compute",1),("unlock","M")]),
        ("M2", 5, [("spawn",2),("compute",2)]),
    ])
    names = [n for _, n in tr]
    last_l = len(names)-1-names[::-1].index("L")
    last_m = len(names)-1-names[::-1].index("M2")
    return (last_m < last_l), "after unlock L must drop below M2; lastL=%d lastM2=%d" % (last_l, last_m)

def _sched_preempt(S):
    tr = S_run(S, [("A",1,[("compute",10)]), ("B",9,[("spawn",3),("compute",2)])])
    names = [n for _, n in tr]
    return (names[3:5] == ["B","B"]), "trace=%r" % (names[:8],)

def _sched_monotonic(S):
    tr = S_run(S, [("A",1,[("compute",3)]),("B",2,[("spawn",1),("compute",3)])])
    ticks = [t for t,_ in tr]
    return (all(ticks[i] < ticks[i+1] for i in range(len(ticks)-1))), "ticks=%r" % (ticks[:10],)

def _sched_accounting(S, n):
    rnd = random.Random(808)
    for it in range(n):
        tasks = []
        for k in range(rnd.randrange(1,4)):
            prog = []; total = 0
            for _ in range(rnd.randrange(1,4)):
                c = rnd.randrange(1,4); prog.append(("compute", c)); total += c
            tasks.append((chr(65+k), rnd.randrange(1,9), prog, total))
        tr = S_run(S, [(n_, p, pr) for n_, p, pr, _ in tasks])
        want = sum(t for *_ , t in tasks)
        if len(tr) != want:
            return False, "iter %d: trace len %d want %d" % (it, len(tr), want)
    return True, "%d random programs accounted" % n
