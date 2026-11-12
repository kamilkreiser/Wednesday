#!/usr/bin/env python3
"""make_stub.py RAW --kind K [--bump KEY] [--drop-failure] [--invent-failure] [--anomaly TEXT] [--verdict V] [--fence] [--garbage]
Writes to stdout a STUB Spark reply: the parser's own truth rendered in the Spark JSON shape, with an optional planted fault.
Used only by arms.sh to simulate the Spark without the network (DIGEST_SPARK_STUB)."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import digest

ap = argparse.ArgumentParser()
ap.add_argument("raw")
ap.add_argument("--kind", required=True)
ap.add_argument("--bump")
ap.add_argument("--drop-failure", action="store_true")
ap.add_argument("--invent-failure", action="store_true")
ap.add_argument("--anomaly", action="append", default=[])
ap.add_argument("--verdict")
ap.add_argument("--fence", action="store_true")
ap.add_argument("--garbage", action="store_true")
ap.add_argument("--paraphrase-error", action="store_true")
a = ap.parse_args()
if a.garbage:
    print("I am sorry, the tests look mostly fine to me.")
    sys.exit(0)
t = digest.parse(a.kind, open(a.raw, errors="replace").read())
fl = [{"name": f["name"], "error": f["error"][:160], "frame": f["frame"][:160]} for f in t["failures"]]
if a.drop_failure and fl:
    fl = fl[1:]
if a.invent_failure:
    fl.append({"name": "an invented test that never ran in this suite", "error": "", "frame": ""})
if a.paraphrase_error and fl:
    fl[0]["error"] = "the assertion was wrong about something entirely different"
c = dict(t["counts"])
if a.bump:
    c[a.bump] = c[a.bump] + 1
o = {"verdict": a.verdict or t["verdict"], **({"summary_lines": t["summaries"]} if "summaries" in t else {}), "counts": c, "failures": fl, "anomalies": a.anomaly}
s = json.dumps(o, indent=1)
print("```json\n" + s + "\n```" if a.fence else s)
