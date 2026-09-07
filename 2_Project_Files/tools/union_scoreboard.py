#!/usr/bin/env python3
"""Union-merge scoreboard.md — an append-at-top table two Wednesday seats both write.

Rows are whole lines beginning '| '. Keep every row from both sides: take the
upstream file as the base (it carries the other seat's newest rows in their own
order) and insert any row unique to our side directly after the '|---' separator,
so newest-at-top is preserved for both.

Nothing is ever dropped, and the conservation check refuses rather than guesses.

Usage: union_scoreboard.py <ours> <theirs> <out>
  ours   = stage :2 (upstream / the other seat)
  theirs = stage :3 (this seat's commit)
"""
import sys

ours_p, theirs_p, out_p = sys.argv[1], sys.argv[2], sys.argv[3]

ours = open(ours_p).readlines()
theirs = open(theirs_p).readlines()

def rows(lines):
    return [l for l in lines if l.startswith("| ") and not l.startswith("|---")]

ours_rows, theirs_rows = rows(ours), rows(theirs)
ours_set = set(ours_rows)
mine_only = [l for l in theirs_rows if l not in ours_set]
theirs_set = set(theirs_rows)
upstream_only = [l for l in ours_rows if l not in theirs_set]

sep = next(i for i, l in enumerate(ours) if l.startswith("|---"))
merged = ours[: sep + 1] + mine_only + ours[sep + 1 :]

print(f"  upstream rows {len(ours_rows)} · this seat's rows {len(theirs_rows)}")
print(f"  unique to upstream {len(upstream_only)} · unique to this seat {len(mine_only)}")

out_rows = rows(merged)
print(f"  UNION = {len(out_rows)} rows")

# Conservation: every row from either side must survive.
missing = [l for l in set(ours_rows) | set(theirs_rows) if l not in set(out_rows)]
assert not missing, f"{len(missing)} row(s) would be lost — REFUSING"
assert len(out_rows) >= max(len(ours_rows), len(theirs_rows)), "union smaller than an input — REFUSING"

open(out_p, "w").writelines(merged)
print(f"  wrote {out_p}")
