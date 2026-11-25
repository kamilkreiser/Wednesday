# QA-AUDIT-HOST-NOTES item 4: compare the per-case lines (QAHN CASE) of the old head, the new head and
# the ablation tree (the new head minus the one N-d line, seal cases only), case by case.
# Usage: python3 -B -I compare.py base.log head.log abl.log out_prefix
# Attribution (my method, not the builder's rule): a base-vs-head difference is item 5 (N-d) ONLY if the
# ablation tree (head without the N-d `ensure_anchor`) answers that case EXACTLY as the base does: the
# one removed line then explains the whole difference. Anything else is UNATTRIBUTED.
import sys, re, json, collections

FIELDS = ["short", "member", "fresh", "dirty", "retry", "final", "before", "extra", "problems", "detail"]

def norm(s):
    # random record content, digests, keys and temporary names vary per run: mask long hex runs
    return re.sub(r"[0-9a-f]{16,}", "<hex>", s)

def load(path):
    d, dup, seals = {}, 0, {}
    for line in open(path, errors="replace"):
        i = line.find("QAHN CASE ")
        if i >= 0:
            body = line[i + len("QAHN CASE "):].rstrip("\n")
            head, rest = body.split(" | ", 1)
            run, case, kind, sched = head.split(" ", 3)
            parts = rest.split(" | ")
            rec = {"run": run, "case": case, "kind": kind, "sched": sched, "short": parts[0]}
            for p in parts[1:]:
                k, _, v = p.partition(" ")
                if k == "dirty":
                    rec["dirty"] = v
                else:
                    rec[k] = v
            rec["detail"] = norm(rec.get("detail", ""))
            key = (run, case, sched)
            if key in d:
                dup += 1
            d[key] = rec
            continue
        i = line.find("QAHN SEALLIMITS ")
        if i >= 0:
            body = line[i + len("QAHN SEALLIMITS "):].rstrip("\n")
            head, v = body.split(" | ", 1)
            run, case, sched = head.split(" ", 2)
            seals[(run, case, sched)] = v
    return d, dup, seals

def same(a, b, fields=FIELDS):
    return all(a.get(f) == b.get(f) for f in fields)

def main():
    base, dupb, _ = load(sys.argv[1])
    head, duph, seals = load(sys.argv[2])
    abl, dupa, _ = load(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != "-" else ({}, 0, {})
    out = sys.argv[4] if len(sys.argv) > 4 else None
    print(f"cases: base {len(base)} (dup keys {dupb}), head {len(head)} (dup {duph}), ablation {len(abl)} (dup {dupa})")
    for name, d in (("base", base), ("head", head), ("ablation", abl)):
        per = collections.Counter((r["run"], r["kind"]) for r in d.values())
        probs = sum(int(r.get("problems", "0")) for r in d.values())
        print(f"  {name}: problems {probs}; per run {dict(collections.Counter(r['run'] for r in d.values()))}")
    only_b = set(base) - set(head); only_h = set(head) - set(base)
    print(f"keys only in base {len(only_b)}, only in head {len(only_h)}")
    diffs = [k for k in base if k in head and not same(base[k], head[k])]
    fdiff = [k for k in base if k in head and same(base[k], head[k]) and base[k].get("failed") != head[k].get("failed")]
    print(f"DIFFERENCES (any compared field): {len(diffs)}; same answer but other failed-operation names: {len(fdiff)}")
    by_kind = collections.Counter(base[k]["kind"] for k in diffs)
    print(f"  by kind: {dict(by_kind)}")
    # ablation over seal cases
    seal_keys = [k for k in base if base[k]["kind"] == "Seal"]
    if abl:
        missing = [k for k in seal_keys if k not in abl]
        ab_diff = [k for k in seal_keys if k in abl and not same(base[k], abl[k])]
        print(f"ablation: seal cases {len(seal_keys)}, missing in ablation {len(missing)}, ablation != base in {len(ab_diff)}")
        for k in ab_diff[:10]:
            print("  ABL!=BASE", k, {f: (base[k].get(f), abl[k].get(f)) for f in FIELDS if base[k].get(f) != abl[k].get(f)})
    attributed, unattributed = [], []
    for k in diffs:
        if base[k]["kind"] == "Seal" and k in abl and same(abl[k], base[k]) and not same(abl[k], head[k]):
            attributed.append(k)
        else:
            unattributed.append(k)
    print(f"ATTRIBUTED to item 5 (N-d) by ablation: {len(attributed)}; UNATTRIBUTED: {len(unattributed)}")
    for k in unattributed[:20]:
        print("  UNATTRIBUTED", k, {f: (base[k].get(f), head[k].get(f)) for f in FIELDS if base[k].get(f) != head[k].get(f)})
    # the classes of the differences
    cls = collections.Counter()
    rows = []
    for k in diffs:
        b, h = base[k], head[k]
        cls[(b["short"], h["short"])] += 1
        rows.append({"key": list(k), "base": b, "head": h})
    print("answer changes (base -> head: count):")
    for (x, y), n in cls.most_common():
        print(f"  {x} -> {y}: {n}")
    detail_only = sum(1 for k in diffs if base[k]["short"] == head[k]["short"])
    print(f"differences with the same short answer (detail/fresh/retry/final only): {detail_only}")
    # problems at the head in the differing cases
    print(f"harness problems in the differing cases at head: {sum(int(head[k].get('problems','0')) for k in diffs)}")
    # SealReport.limits at the head
    vals = collections.Counter(seals.values())
    print(f"head SealReport.limits values over {len(seals)} cases with an Ok seal: {dict(vals)}")
    if out:
        json.dump(rows, open(out + "_diffs.json", "w"), indent=0)
        json.dump([list(k) for k in unattributed], open(out + "_unattributed.json", "w"))
    sys.exit(1 if unattributed or only_b or only_h else 0)

if __name__ == "__main__":
    main()
