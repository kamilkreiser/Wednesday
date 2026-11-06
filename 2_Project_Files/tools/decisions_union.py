#!/usr/bin/env python3
"""decisions_union.py <upstream.json> <local.json> <out.json>

Union two copies of decisions.json by card id, for panel_sync's conflict recovery.
WHY (2026-11-06 12:26): the recovery resolved this file with `checkout --ours`, which in a
rebase is UPSTREAM, so 12 of Kam's cards and rulings written since the last pull vanished.
Cards are records, not generated data: neither side may be dropped.

Rule per id present on both sides: a ruled card beats an open one; between two ruled cards the
later ruled_ts wins; otherwise upstream's copy stands. Cards keep upstream's order, then local-only
cards in local order. Exits non-zero and writes nothing unless the output holds exactly the union
of the two id sets, each id once.
"""
import json, os, sys, tempfile


def pick(up, lo):
    if lo.get("status") == "ruled" and up.get("status") != "ruled":
        return lo
    if up.get("status") == "ruled" and lo.get("status") == "ruled":
        return lo if (lo.get("ruled_ts") or "") > (up.get("ruled_ts") or "") else up
    return up


def main(upath, lpath, opath):
    up, lo = json.load(open(upath)), json.load(open(lpath))
    L = {c["id"]: c for c in lo}
    U = {c["id"]: c for c in up}
    out = [pick(c, L[c["id"]]) if c["id"] in L else c for c in up]
    out += [c for c in lo if c["id"] not in U]
    ids = [c["id"] for c in out]
    if len(ids) != len(set(ids)) or set(ids) != set(U) | set(L):
        sys.exit("decisions_union: conservation failed, nothing written")
    d = os.path.dirname(os.path.abspath(opath))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".decisions-union-", suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    json.load(open(tmp))
    os.replace(tmp, opath)
    print(f"decisions_union: {len(U)} upstream + {len(L)} local -> {len(out)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
