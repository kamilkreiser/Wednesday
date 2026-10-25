#!/usr/bin/env python3
"""gate_facts.py — deterministic helpers for spark_gate.sh (no LLM). Python 3 stdlib only.

  junit <junit.xml> <out.json> [--require-file REL ...]
      Parse a pytest junit file into {tests, passed, failed, errors, skipped, failing:[{name,kind,text}], files_seen:[...]}.
      Exit 4 (and write nothing misleading) if the file is missing/unparseable, if tests == 0, or if a --require-file
      has no test in the report (a test that cannot be found must refuse, never report 0).
  assemble <out facts.json> key=path.json ...   merge named JSON fragments under their keys.
"""
import json, sys, xml.etree.ElementTree as ET


def junit(path, out, required):
    try:
        root = ET.parse(path).getroot()
    except Exception as e:
        sys.stderr.write(f"gate_facts: junit unreadable ({path}): {e!r}\n"); return 4
    res = {"tests": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0, "failing": [], "files_seen": []}
    seen = set()
    for tc in root.iter("testcase"):
        res["tests"] += 1
        cls = tc.get("classname", ""); name = tc.get("name", "")
        full = f"{cls}::{name}"
        seen.add(cls.replace(".", "/"))
        kids = {c.tag: c for c in tc}
        if "failure" in kids or "error" in kids:
            k = "failure" if "failure" in kids else "error"
            el = kids[k]
            res["failed" if k == "failure" else "errors"] += 1
            text = (el.get("message") or "") + "\n" + (el.text or "")
            res["failing"].append({"name": full, "kind": k, "text": text.strip()[:1500]})
        elif "skipped" in kids:
            res["skipped"] += 1
        else:
            res["passed"] += 1
    res["files_seen"] = sorted(seen)
    # collection errors appear as testcase-less <error> under testsuite
    for ts in root.iter("testsuite"):
        for e in ts.findall("error"):
            res["errors"] += 1
            res["failing"].append({"name": "(collection)", "kind": "error", "text": ((e.get("message") or "") + (e.text or ""))[:1500]})
    if res["tests"] == 0 and res["errors"] == 0:
        sys.stderr.write("gate_facts: REFUSE — 0 tests in the report; a test that cannot be found is not a pass\n"); return 4
    for rq in required:
        stem = rq[:-3] if rq.endswith(".py") else rq
        if not any(s == stem or s.startswith(stem + "/") for s in seen):
            if res["errors"] == 0:
                sys.stderr.write(f"gate_facts: REFUSE — required test file {rq} has no test in the report\n"); return 4
    json.dump(res, open(out, "w"), indent=1)
    return 0


def assemble(out, pairs):
    d = {}
    for p in pairs:
        k, f = p.split("=", 1)
        d[k] = json.load(open(f))
    json.dump(d, open(out, "w"), indent=1)
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "junit":
        req = [a[i + 1] for i, x in enumerate(a) if x == "--require-file"]
        sys.exit(junit(a[1], a[2], req))
    if a and a[0] == "assemble":
        sys.exit(assemble(a[1], a[2:]))
    sys.stderr.write(__doc__); sys.exit(2)
