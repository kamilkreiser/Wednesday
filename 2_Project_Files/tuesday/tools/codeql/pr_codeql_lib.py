#!/usr/bin/env python3
"""Helpers for pr_codeql_check.sh (stdlib only).

  diffranges <unified-diff-file> <out.json>
      Added-line ranges of head vs base: {"path": [[start, end], ...]} (new-side line numbers).
  verdict <head.sarif> <base.sarif> <ranges.json> <out.json> [--allow-empty]
      Applies the PR post-filter on the head SARIF, compares head vs base, prints the verdict table.
      rc 0 pass, 1 would block, 2 tool error.

Severity rule ("high or above"): a result is HIGH+ when its rule has a security-severity >= 7.0
(GitHub's "high" band); a rule with NO security-severity is HIGH+ when its problem.severity is "error".
This mirrors the hosted ruleset: security_alerts_threshold high_or_higher, alerts_threshold errors.
"""
import json, re, sys
from collections import Counter

HIGH = 7.0


def die(msg):
    print("TOOL ERROR: " + msg, file=sys.stderr)
    sys.exit(2)


def diffranges(diff_file, out):
    ranges = {}
    cur = None
    with open(diff_file, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("+++ "):
                p = line[4:].split("\t")[0]
                if p == "/dev/null":
                    cur = None
                else:
                    if p.startswith('"') and p.endswith('"'):
                        p = p[1:-1]
                    cur = p[2:] if p.startswith("b/") else p
                continue
            m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if m and cur:
                s = int(m.group(1))
                n = int(m.group(2)) if m.group(2) is not None else 1
                if n > 0:
                    ranges.setdefault(cur, []).append([s, s + n - 1])
    with open(out, "w") as f:
        json.dump(ranges, f, indent=1, sort_keys=True)
    print("diff pack: %d files with added lines, %d ranges" % (len(ranges), sum(len(v) for v in ranges.values())))


def load(path):
    try:
        with open(path) as f:
            s = json.load(f)
    except Exception as e:
        die("cannot read SARIF %s: %s" % (path, e))
    res = []
    for run in s.get("runs", []):
        rules = {}
        tool = run.get("tool", {})
        for r in tool.get("driver", {}).get("rules", []) or []:
            rules[r["id"]] = r
        for ext in tool.get("extensions", []) or []:
            for r in ext.get("rules", []) or []:
                rules.setdefault(r["id"], r)
        for r in run.get("results", []):
            ru = rules.get(r.get("ruleId"), {})
            pr = ru.get("properties", {}) or {}
            ss = pr.get("security-severity")
            try:
                ss = float(ss) if ss is not None else None
            except ValueError:
                ss = None
            psev = pr.get("problem.severity") or (ru.get("defaultConfiguration") or {}).get("level")
            high = (ss >= HIGH) if ss is not None else (psev == "error")
            loc = r["locations"][0]["physicalLocation"]
            res.append({
                "rule": r.get("ruleId"),
                "file": loc["artifactLocation"]["uri"],
                "line": loc["region"]["startLine"],
                "col": loc["region"].get("startColumn"),
                "fp": (r.get("partialFingerprints") or {}).get("primaryLocationLineHash"),
                "sev": ss if ss is not None else psev,
                "high": high,
                "locs": [(l["physicalLocation"]["artifactLocation"]["uri"], l["physicalLocation"]["region"]["startLine"])
                         for l in (r["locations"] + (r.get("relatedLocations") or []))
                         if "region" in l.get("physicalLocation", {})],
            })
    return res


def verdict(head_p, base_p, ranges_p, out, allow_empty):
    head, base = load(head_p), load(base_p)
    ranges = json.load(open(ranges_p))
    if (len(head) == 0) != (len(base) == 0) and not allow_empty:
        die("one side has 0 results and the other has %d (head %d, base %d): looks like a broken analysis; "
            "rerun, or pass --allow-empty if this is genuinely expected" % (max(len(head), len(base)), len(head), len(base)))

    def added(f, l):
        return any(a <= l <= b for a, b in ranges.get(f, []))

    for r in head:
        r["kept"] = any(added(f, l) for f, l in r["locs"])
    kept = [r for r in head if r["kept"]]
    key = lambda r: (r["rule"], r["file"], r["fp"])
    hk, bk = Counter(key(r) for r in head), Counter(key(r) for r in base)
    new_c, gone_c = hk - bk, bk - hk
    sev_of = {}
    for r in head + base:
        sev_of[key(r)] = r["high"]
    newrows = sorted(new_c.elements(), key=str)
    gonerows = sorted(gone_c.elements(), key=str)
    new_high = [k for k in newrows if sev_of.get(k)]
    kept_high = [r for r in kept if r["high"]]
    sev = lambda r: ("HIGH+ " if r["high"] else "below ") + str(r["sev"])

    print("")
    print("VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)")
    print("  results   head %d   base %d" % (len(head), len(base)))
    print("  KEPT      total %d   high+ %d   (post-filter: primary or any related location START line is an added line)" % (len(kept), len(kept_high)))
    print("  NEW       total %d   high+ %d   (rule,file,primaryLocationLineHash multiset, head minus base)" % (len(newrows), len(new_high)))
    print("  GONE      total %d" % len(gonerows))
    for r in sorted(kept, key=lambda r: (r["file"], r["line"], r["rule"])):
        print("  KEPT  %-30s %s:%s:%s  fp=%s  [%s]" % (r["rule"], r["file"], r["line"], r["col"], r["fp"], sev(r)))
    for k in newrows:
        print("  NEW   %-30s %s  fp=%s  [%s]" % (k[0], k[1], k[2], "HIGH+" if sev_of.get(k) else "below"))
    for k in gonerows:
        print("  GONE  %-30s %s  fp=%s" % (k[0], k[1], k[2]))
    bad = len(kept_high) > 0 or len(new_high) > 0
    print("  RESULT    %s" % ("rc 1 WOULD BLOCK (KEPT high+ %d, NEW high+ %d)" % (len(kept_high), len(new_high)) if bad
                              else "rc 0 PASS (KEPT high+ 0, NEW high+ 0)"))
    with open(out, "w") as f:
        json.dump({"kept": kept, "new": [list(k) for k in newrows], "gone": [list(k) for k in gonerows],
                   "kept_high": len(kept_high), "new_high": len(new_high)}, f, indent=1, default=str)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "diffranges":
        diffranges(a[1], a[2])
    elif len(a) >= 5 and a[0] == "verdict":
        verdict(a[1], a[2], a[3], a[4], "--allow-empty" in a[5:])
    else:
        die("usage: pr_codeql_lib.py diffranges <diff> <out.json> | verdict <head.sarif> <base.sarif> <ranges.json> <out.json> [--allow-empty]")
