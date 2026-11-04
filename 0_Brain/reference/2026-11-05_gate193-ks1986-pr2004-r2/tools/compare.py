# Gate 192: compare two PG harness runs (A = reference, B = subject). usage: python3 -I compare.py A.jsonl B.jsonl [--fields]
# Prints, per (cell, path), a one-line summary of each side and the direction class for v1 paths:
#   SAME            identical certification id (or both none) and identical body
#   SAME-CERT       same certification id, body differs elsewhere
#   LESS            A presents a certification, B presents none
#   NEW             B presents a certification, A presents none          (more permissive)
#   DIFFERENT       both present one, different certification ids
# --fields prints a field-by-field diff of the body (flattened keys) for every row whose body differs.
import json, sys

def load(p):
    out = {}
    for line in open(p):
        r = json.loads(line)
        out[(r["cell"], r["path"])] = r
    return out

def flat(o, pre=""):
    if isinstance(o, dict):
        d = {}
        for k, v in o.items():
            d.update(flat(v, f"{pre}.{k}" if pre else k))
        return d
    if isinstance(o, list):
        d = {}
        for i, v in enumerate(o):
            d.update(flat(v, f"{pre}[{i}]"))
        return d if o else {pre: []}
    return {pre: o}

def cert(r):
    b = r["body"]
    if r["path"] == "v2":
        return tuple((m.get("certification") or {}).get("certificationId") for m in b.get("matches", []))
    c = b.get("certification")
    return c.get("certificationId") if isinstance(c, dict) else None

def summ(r):
    b = r["body"]
    if r["path"] == "v2":
        return f"http={r['http']} count={b.get('count')} docs={[m.get('documentId') for m in b.get('matches', [])]} certs={cert(r)} leaks={r['leaks']}"
    c = b.get("certification") if isinstance(b.get("certification"), dict) else {}
    return (f"http={r['http']} doc={b.get('documentId')} status={b.get('status')} verified={b.get('verified')} "
            f"isCert={(b.get('checks') or {}).get('isCertified')} cert={cert(r)} certOrg={c.get('certifierOrganizationId', '-') if c else '-'} "
            f"certBy={c.get('certifiedBy', '-') if c else '-'} title={b.get('title', '(absent)')} issuer={b.get('issuer', '(absent)')} "
            f"src={b.get('source', '-')} leaks={r['leaks']} q={r['q']['plat']}/{r['q']['tenant']}/{r['q']['local']} reads={r['q']['tenantsRead']} "
            f"chain={r['chainCalls']} warn1986={r['warnKS1986']} err={r['errors']}")

A, B = load(sys.argv[1]), load(sys.argv[2])
fields = "--fields" in sys.argv
counts = {}
for key in A:
    if key not in B:
        print("MISSING in B", key); continue
    a, b = A[key], B[key]
    ca, cb = cert(a), cert(b)
    same_body = a["body"] == b["body"] and a["http"] == b["http"]
    if key[1] == "v2":
        cls = "V2-EQUAL" if same_body else "V2-DIFF"
    elif ca == cb:
        cls = "SAME" if same_body else "SAME-CERT"
    elif ca and not cb:
        cls = "LESS"
    elif cb and not ca:
        cls = "NEW"
    else:
        cls = "DIFFERENT"
    counts[cls] = counts.get(cls, 0) + 1
    print(f"{cls:10s} {key[0]} {key[1]}")
    print(f"    A: {summ(a)}")
    print(f"    B: {summ(b)}")
    if fields and not same_body:
        fa, fb = flat(a["body"]), flat(b["body"])
        for k in sorted(set(fa) | set(fb)):
            if fa.get(k, "<absent>") != fb.get(k, "<absent>"):
                print(f"      ~ {k}: {json.dumps(fa.get(k, '<absent>'))} -> {json.dumps(fb.get(k, '<absent>'))}")
        if a["headers"] != b["headers"]:
            print(f"      ~ headers: {a['headers']} -> {b['headers']}")
print("COUNTS", json.dumps(counts, sort_keys=True), "rows", len(A))
