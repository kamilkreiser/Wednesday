#!/usr/bin/env python3
"""records_union.py <upstream.json> <local.json> <out.json>

Union two copies of a chat stream (chat_kam.json, chat_wednesday.json ...) or ack_state.json, for
panel_sync's conflict recovery. Sibling of decisions_union.py, which does the same for the cards.
WHY (2026-11-06 12:47 audit, after 12 cards were lost at 12:26): the recovery resolved every file
under dashboard/data with `checkout --ours`, which in a rebase is UPSTREAM. chat_kam.json holds
Kam's own words and ack_state.json holds which questions were answered; neither is generated data,
so a conflict there must keep both sides. Streams are one-writer, so a conflict is unlikely, not
impossible: the store was written by more than one tree on 2026-09-08.

A list is a stream: a row is identified by its whole content, and rows keep upstream's order, then
local-only rows in local order, so a row present on both sides appears once and a row repeated on
one side keeps its repeats. A dict is keyed state: the union of the keys; when both sides hold a
key with different values, the value with the later `ts` wins, else upstream's stands.
Anything else, or a type mismatch, exits non-zero and writes nothing, and the caller leaves the
file unresolved so the rebase aborts. Conservation is asserted before writing.
"""
import collections, json, os, sys, tempfile
from datetime import datetime


def row_id(row):
    return json.dumps(row, sort_keys=True, ensure_ascii=False)


def union_list(up, lo):
    left = collections.Counter(row_id(r) for r in up)
    out = list(up)
    for row in lo:
        key = row_id(row)
        if left[key] > 0:
            left[key] -= 1
        else:
            out.append(row)
    want = collections.Counter(row_id(r) for r in up) | collections.Counter(row_id(r) for r in lo)
    if collections.Counter(row_id(r) for r in out) != want:
        sys.exit("records_union: stream conservation failed, nothing written")
    return out


def stamp(value):
    if isinstance(value, dict) and isinstance(value.get("ts"), str):
        try:
            return datetime.fromisoformat(value["ts"].replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def later(up_value, lo_value):
    a, b = stamp(up_value), stamp(lo_value)
    if a is None or b is None or a.tzinfo is None or b.tzinfo is None:
        return up_value
    return lo_value if b > a else up_value


def union_dict(up, lo):
    out = dict(up)
    for key, value in lo.items():
        out[key] = later(up[key], value) if key in up else value
    if set(out) != set(up) | set(lo):
        sys.exit("records_union: key conservation failed, nothing written")
    return out


def main(upath, lpath, opath):
    up, lo = json.load(open(upath)), json.load(open(lpath))
    if isinstance(up, list) and isinstance(lo, list):
        out = union_list(up, lo)
    elif isinstance(up, dict) and isinstance(lo, dict):
        out = union_dict(up, lo)
    else:
        sys.exit(f"records_union: cannot union {type(up).__name__} with {type(lo).__name__}, nothing written")
    d = os.path.dirname(os.path.abspath(opath))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".records-union-", suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    json.load(open(tmp))
    os.replace(tmp, opath)
    print(f"records_union: {os.path.basename(opath)}: {len(up)} upstream + {len(lo)} local -> {len(out)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
