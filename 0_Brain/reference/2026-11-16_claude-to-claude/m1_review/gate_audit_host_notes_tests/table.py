# QA-AUDIT-HOST-NOTES item 7: the docs' P-4 answer table (docs/AUDIT-HOST.md §3 at 52ad858, 13 rows)
# applied MECHANICALLY to every answer of the head's fault schedules (the QAHN CASE lines).
# Each answer is mapped to the row that names it; the row's retry column gives a decision; that
# decision is compared with what the harness's caller did (its final open then checked "exactly once").
# Answers no row names are listed. Usage: python3 -B -I table.py head.log
import sys, re, collections
sys.path.insert(0, "/private/tmp/claude-501/qahn/bin")

ROWS = {
    1: "record/own checkpoint LANDED -> Ok(Recorded)/Ok(Checkpoint): nothing",
    2: "other change landed -> Err(Reopened{landed:true}): nothing",
    3: "did NOT land -> Err(Reopened{landed:false}): the same change, once",
    4: "UNKNOWN -> Err(LandedUnknown): open again, read, decide",
    5: "release landed -> Ok(Released): nothing",
    6: "release not landed / in part -> Err(Audit(..)): the release again",
    7: "seal commit error -> Err(SealCommitFailed{segment_now}): a seal only if segment_now did not move",
    8: "limits changed -> Err(LimitsChanged{answer}): as the row of answer",
    9: "release any other Err (Dir, ArchiveMismatch, Audit(ExportTooLarge)): the release again",
    10: "ordinary failure, store not poisoned -> Err(Audit(..)): the same change, once",
    11: "seal Ok, N-3 re-open failed (host closed): nothing; open again",
    12: "seal Ok, limits changed in the N-3 re-open (limits: Some): nothing",
    13: "seal_begin Err(AnchorNotSaved) / anchors/limits Dir error (N-d): the seal, once the write succeeds",
}

def tup(s):
    return tuple(x for x in s.strip("()").split(","))

def row_of(kind, short, detail, member, seallimits):
    """(row, decision) where decision is 'none', 'retry', 'read', 'retry-if-not-moved'; row None = no row."""
    if short.startswith("Err(LimitsChanged"):
        return 8, None  # unwrap: not reached in these schedules (defaults in force); listed if seen
    if short.startswith("Ok("):
        if kind == "Seal":
            if seallimits and "Some(" in seallimits:
                return 12, "none"
            if member == "false":
                return 11, "none"
            return "Ok", "none"
        if short.startswith("Ok(Recorded") or short.startswith("Ok(Checkpoint"):
            return 1, "none"
        if short.startswith("Ok(Released"):
            return 5, "none"
        return "Ok", "none"
    if short.startswith("Err(Reopened{landed:true"):
        return 2, "none"
    if short.startswith("Err(Reopened{landed:false"):
        return 3, "retry"
    if short.startswith("Err(LandedUnknown"):
        return 4, "read"
    if kind in ("Release", "ReleaseTomb"):
        if short == "Err(Audit(ExportTooLarge))":
            return 9, "retry"
        if short.startswith("Err(Audit("):
            return 6, "retry"
        if short.startswith("Err(Dir(") or short.startswith("Err(ArchiveMismatch"):
            return 9, "retry"
        return None, None
    if kind == "Seal":
        if short.startswith("Err(SealCommitFailed"):
            return 7, "retry-if-not-moved"
        if short == "Err(AnchorNotSaved)":
            return 13, "retry"
        if short.startswith("Err(Dir(") and '"anchors/limits"' in detail:
            return 13, "retry"
        if short.startswith("Err(Audit("):
            return 10, "retry"
        return None, None
    if short.startswith("Err(Audit("):
        return 10, "retry"
    return None, None

def main():
    from compare import load  # noqa
    d, _, seals = load(sys.argv[1])
    by_row = collections.Counter()
    unnamed = collections.Counter()
    unnamed_ex = {}
    mismatch = []
    for k, r in d.items():
        row, dec = row_of(r["kind"], r["short"], r["detail"], r["member"], seals.get(k))
        if row is None:
            m = re.search(r'name: "([^"]*)"', r["detail"]); what = re.search(r'what: "([^"]*)"', r["detail"])
            tag = (r["kind"], r["short"], (what.group(1) if what else ""), re.sub(r"\d+", "#", m.group(1)) if m else "")
            unnamed[tag] += 1
            unnamed_ex.setdefault(tag, (k, r))
            continue
        by_row[row] += 1
        b, f = tup(r["before"]), tup(r["final"])
        harness_retried = r["retry"] != "-"
        if dec == "none":
            want = False
        elif dec == "retry":
            want = True
        elif dec == "retry-if-not-moved":
            seg_now = int(re.search(r"segment_now:(\d+)", r["short"]).group(1))
            want = seg_now == int(b[2])
        elif dec == "read":
            # open again and read: the change is there iff the fresh open shows it; retry iff not
            want = None
        else:
            want = None
        if want is not None and want != harness_retried:
            mismatch.append((k, row, dec, r["short"], r["retry"]))
    total = sum(by_row.values()) + sum(unnamed.values())
    print(f"cases {total}; answers per row: " + ", ".join(f"{k}: {v}" for k, v in sorted(by_row.items(), key=lambda x: str(x[0]))))
    print(f"row decision differs from the harness caller's (whose final open found each change exactly once): {len(mismatch)}")
    for m in mismatch[:15]:
        print("  MISMATCH", m)
    print(f"answers NO row names: {sum(unnamed.values())}")
    for tag, n in unnamed.most_common():
        k, r = unnamed_ex[tag]
        print(f"  {n:5d} {tag}  e.g. {k}: retry {r['retry']}, before {r['before']}, final {r['final']}, problems {r['problems']}")
        print(f"        detail {r['detail'][:260]}")

main()
