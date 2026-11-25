# QA-POLICY-AT comparer (the check's OWN; never the engine's code). usage:
#   python3 -B -I cmp_qpa.py <base.jsonl (run with QPA_TWIN=1)> <head.jsonl> <report.txt> [<diffcells.jsonl>]
# Per row (the two files are line-aligned: the same generated rows in the same order):
#  - generation: id, tool, cwd, input identical;
#  - scans: same texts; `words` and `exact` byte-equal; the base `pieces` a PREFIX of the head's; the extra pieces
#    EXACTLY this file's own prediction (the text after each `@` of each exact word, then of each base piece, not
#    empty, not starting with `-`, not already present, until 161 pieces); the base harness's twin list equal to it;
#  - every cell (state x 12 columns) equal, or a difference that is (a) on a row whose text holds `@` with a non-empty
#    prediction, (b) STRICTER by rank (Allow < Ask < Deny; asks: tier not lower and reasons a superset; would-have-been
#    the same), and (c) whose head answer EQUALS THE MODEL: the base engine deciding the base action with this
#    harness's own predicted pieces added where the rule puts them (and oversize by its own count). The model is
#    checked against the head on EVERY cell of every row with a prediction, not only on differing cells.
#    Anything else: LOOSER or UNATTRIBUTED. Deny -> other deny is counted apart; would-have-been on a row the head
#    newly marks oversize is counted apart (an audit input, every decision column is the step [4] deny).
# Exit 1 on any looser, unattributed, scan or generation failure.
import sys, json
from collections import Counter, defaultdict

COLS = ["decide", "would", "m:live", "m:live_shell", "m:expired", "m:other", "m:nobody",
        "o:none", "o:StillAsk", "o:Allowed", "o:Allowed_other", "o:Allowed_nobody"]
CAP = 161
MAX_MENTIONS = 160
MAX_COMP = 2048
ROOT_COMPONENTS = {"<root>": 6, "<o2>": 5}  # /private/tmp/claude-501/qpa/fix/root, /private/tmp/claude-501/qpa/outside2
DK = "rows whose @ appears only after $'..' decoding"
RANK = {"A": 0, "Q": 1, "D": 2}
TIER = {"T0": 0, "T1": 1, "T2": 2, "T3": 3}

def predict(exact, pieces):
    have = set(pieces); n = len(pieces); out = []
    for w in list(exact) + list(pieces):
        i = w.find('@')
        while i >= 0:
            if n >= CAP:
                return out
            s = w[i + 1:]
            if s and not s.startswith('-') and s not in have:
                have.add(s); out.append(s); n += 1
            i = w.find('@', i + 1)
    return out

def comps(p):
    n = 0
    for c in p.replace('\\', '/').split('/'):
        if c:
            n += ROOT_COMPONENTS.get(c, 1)
    return max(n, 1)

def over(pieces):
    return len(pieces) > MAX_MENTIONS or sum(comps(p) for p in pieces) > MAX_COMP

def code(c):
    k = c["k"]
    if k == "A":
        return "allow:" + ("owner" if "OwnerChoseAllow" in c["w"] else "both-agree" if "Bypass" in c["w"] else c["w"][:30])
    if k == "Q":
        return "ask " + c["tier"]
    if k == "W":
        return "would " + c["tier"]
    r = c["r"]
    for key, name in [("TooLargeToCheck", "too large"), ("Excluded", "denied excluded"), ("HardDeny", "hard deny")]:
        if r.startswith(key):
            return name
    if r.startswith("RefusedInAllow") or r.startswith("BypassRefused"):
        who = "owner" if r.startswith("RefusedInAllow") else "both-agree"
        txt = r[r.find('"') + 1:r.rfind('"')]
        return f"refused({who}): {txt[:48]}"
    return "deny " + r[:40]

def main():
    bpath, hpath, rpath = sys.argv[1:4]
    dpath = sys.argv[4] if len(sys.argv) > 4 else None
    dfile = open(dpath, "w") if dpath else None
    stats = Counter(); dist = Counter(); d2d = Counter(); d2d_rows = defaultdict(list)
    fails = defaultdict(list); reach_rows = set(); bound_cross = Counter(); at_rows = 0; rows = 0
    state_col = Counter()
    for lb, lh in zip(open(bpath), open(hpath)):
        b = json.loads(lb); h = json.loads(lh); rows += 1
        rid = b["id"]
        if (b["id"], b["tool"], b["cwd"], b["input"]) != (h["id"], h["tool"], h["cwd"], h["input"]):
            fails["generation"].append(rid); continue
        if b["facts"] != h["facts"]:
            fails["facts"].append(rid)
        # scans
        extras_all = []
        scan_ok = True
        if [s["src"] for s in b["scans"]] != [s["src"] for s in h["scans"]]:
            fails["scan-sources"].append(rid); scan_ok = False
        crossed = False
        for sb, sh in zip(b["scans"], h["scans"]):
            if sb["words"] != sh["words"]:
                fails["words"].append(rid); scan_ok = False
            if sb["exact"] != sh["exact"]:
                fails["exact"].append(rid); scan_ok = False
            bp, hp = sb["pieces"], sh["pieces"]
            if hp[:len(bp)] != bp:
                fails["prefix"].append(rid); scan_ok = False; continue
            pred = predict(sb["exact"], bp)
            if hp[len(bp):] != pred:
                fails["extras!=prediction"].append(rid); scan_ok = False
            for e in pred:
                if e not in extras_all:
                    extras_all.append(e)
            if sb["src"].startswith("cmd") and not over(bp) and over(hp):
                crossed = True
            if sb["src"].startswith("cmd") and over(bp) != (sb["raw_pieces_n"] > MAX_MENTIONS or sum(comps(p) for p in bp) > MAX_COMP):
                fails["component-count-self-check"].append(rid)
        model = b.get("model")
        if (model["extras"] if model else []) != extras_all:
            fails["twin-list!=prediction"].append(rid)
        if model and model["oversize"] != h["oversize"]:
            fails["model-oversize!=head"].append(rid)
        if model:
            for st in b["cols"]:
                for ci in range(12):
                    stats["model cells"] += 1
                    if model["cols"][st][ci] != h["cols"][st][ci]:
                        stats["MODEL != HEAD"] += 1
                        if len(fails["model!=head"]) < 40:
                            fails["model!=head"].append((rid, st, COLS[ci], h["cols"][st][ci], model["cols"][st][ci]))
        decoded_only = b["at"] and '@' not in b["input"]
        if decoded_only:
            stats[DK] += 1
        has_at = b["at"]
        if b["at"]:
            at_rows += 1
        if b["oversize"] != h["oversize"] and not b.get("model"):
            fails["oversize-unpredicted"].append(rid)
        row_changed = False
        for st in b["cols"]:
            for ci, (cb, ch) in enumerate(zip(b["cols"][st], h["cols"][st])):
                stats["cells"] += 1
                if cb == ch:
                    continue
                row_changed = True
                stats["differing cells"] += 1
                col = COLS[ci]
                key = (code(cb), code(ch), st, col)
                verdict, why = judge(cb, ch, ci, st, b, has_at, extras_all, crossed, scan_ok, h)
                if decoded_only:
                    stats["differing cells on decoded-@ rows"] += 1
                stats[verdict] += 1
                dist[(code(cb), code(ch), verdict)] += 1
                state_col[(st, col, code(cb), code(ch), verdict)] += 1
                if cb["k"] == "D" and ch["k"] == "D":
                    d2d[(code(cb), code(ch), verdict)] += 1
                    if len(d2d_rows[(code(cb), code(ch))]) < 8:
                        d2d_rows[(code(cb), code(ch))].append((rid, st, col, b["input"][:120]))
                if code(cb) != code(ch):
                    reach_rows.add(rid)
                if ch["k"] == "D" and ch["r"].startswith("TooLarge") and cb["k"] != "D" or (cb["k"] == "D" and ch["k"] == "D" and ch["r"].startswith("TooLarge") and not cb["r"].startswith("TooLarge")):
                    bound_cross[(code(cb), st, col)] += 1
                if verdict in ("LOOSER", "UNATTRIBUTED"):
                    fails[verdict].append((rid, st, col, code(cb), code(ch), why, b["input"][:160]))
                if dfile:
                    dfile.write(json.dumps({"id": rid, "st": st, "col": col, "b": code(cb), "h": code(ch), "v": verdict, "why": why, "input": b["input"][:300]}) + "\n")
        if row_changed and not has_at:
            stats["rows without @ that differ"] += 1
    out = []
    p = out.append
    p(f"rows {rows}; rows whose text holds @ (harness flag) {at_rows}; cells {stats['cells']}")
    p(f"differing cells {stats['differing cells']}: STRICTER {stats['STRICTER']}, DENY->OTHER DENY (attributed) {stats['DENY2DENY']}, WOULD-ON-OVERSIZE (apart) {stats['W-OVERSIZE']}, LOOSER {stats['LOOSER']}, UNATTRIBUTED {stats['UNATTRIBUTED']}")
    p(f"rows without @ that differ {stats['rows without @ that differ']}")
    p(f"model: cells checked {stats['model cells']}, MODEL != HEAD {stats['MODEL != HEAD']}")
    p(f"rows whose @ appears only after $'..' decoding: {stats[DK]}; differing cells on them {stats['differing cells on decoded-@ rows']}")
    p(f"would-have-been on rows newly oversize (apart): {stats['W-OVERSIZE']}")
    p(f"reach (rows whose answer code changed in some cell): {len(reach_rows)}")
    p(f"bound-crossing cells (to too large): {sum(bound_cross.values())}")
    for k in ["generation", "facts", "scan-sources", "words", "exact", "prefix", "extras!=prediction", "twin-list!=prediction",
              "oversize-unpredicted", "component-count-self-check", "model-oversize!=head", "model!=head"]:
        p(f"FAIL {k}: {len(fails[k])} {fails[k][:5]}")
    p("--- distribution (base answer -> head answer, verdict): cells, all states and columns")
    for (a, b2, v), n in sorted(dist.items(), key=lambda x: -x[1]):
        p(f"{n:9d}  {a}  ->  {b2}  [{v}]")
    p("--- deny -> other deny (counted apart)")
    for (a, b2, v), n in sorted(d2d.items(), key=lambda x: -x[1]):
        p(f"{n:9d}  {a}  ->  {b2}  [{v}]   e.g. {d2d_rows[(a, b2)][:3]}")
    p("--- bound crossings (base answer, state, column)")
    for k, n in sorted(bound_cross.items()):
        p(f"{n:6d}  {k}")
    p("--- per state and column")
    for k, n in sorted(state_col.items()):
        p(f"{n:7d}  {k}")
    for k in ["LOOSER", "UNATTRIBUTED"]:
        p(f"--- {k} (first 40)")
        for x in fails[k][:40]:
            p("  " + repr(x))
    bad = stats["LOOSER"] + stats["UNATTRIBUTED"] + stats["rows without @ that differ"] + sum(
        len(fails[k]) for k in ["generation", "facts", "scan-sources", "words", "exact", "prefix", "extras!=prediction",
                                "twin-list!=prediction", "oversize-unpredicted", "model-oversize!=head"]) + stats["MODEL != HEAD"]
    p("RESULT: " + ("PASS" if bad == 0 else f"FAIL ({bad})"))
    open(rpath, "w").write("\n".join(out) + "\n")
    print("\n".join(out[:16]))
    print(out[-1])
    sys.exit(0 if bad == 0 else 1)

def looser(cb, ch, b, h):
    """Direction first, whatever the attribution: the reason a cell is looser, or None."""
    if cb["k"] == "W":
        if TIER[ch["tier"]] < TIER[cb["tier"]] or not set(ch["rs"]) >= set(cb["rs"]):
            if b["oversize"] is None and h["oversize"] is not None:
                return None  # counted apart (W-OVERSIZE)
            return "would-have-been lower or reasons lost"
        return None
    rb, rh = RANK[cb["k"]], RANK[ch["k"]]
    if rh < rb:
        return "lower rank"
    if rb == rh == 0:
        return "allow reason changed"
    if rb == rh == 1:
        if TIER[ch["tier"]] < TIER[cb["tier"]]:
            return "ask tier lower"
        if not set(ch["rs"]) >= set(cb["rs"]):
            return "ask reason line dropped"
        if ch.get("tg") is not None and cb.get("tg") is not None and not all(t in ch["tg"] for t in cb["tg"]):
            return "a target line dropped from the card"
    return None

def judge(cb, ch, ci, st, b, has_at, extras, crossed, scan_ok, h):
    lw = looser(cb, ch, b, h)
    if lw:
        return "LOOSER", lw
    if not has_at:
        return "UNATTRIBUTED", "no @ in the row (text or scan)"
    if not scan_ok:
        return "UNATTRIBUTED", "scan property failed"
    if not extras:
        return "UNATTRIBUTED", "no predicted extra piece"
    m = b.get("model")
    if not m or m["cols"][st][ci] != ch:
        return "UNATTRIBUTED", "head answer is not the model's"
    if cb["k"] == "W":
        if TIER[ch["tier"]] < TIER[cb["tier"]] or not set(ch["rs"]) >= set(cb["rs"]):
            if b["oversize"] is None and h["oversize"] is not None:
                return "W-OVERSIZE", "would-have-been reasons dropped with the mentions of a newly oversize command"
            return "LOOSER", "would-have-been lower or reasons lost"
        return "STRICTER", "would-have-been: the model's"
    rb, rh = RANK[cb["k"]], RANK[ch["k"]]
    if rh < rb:
        return "LOOSER", "lower rank"
    if rb == rh == 0:
        return "LOOSER", "allow reason changed"
    if rb == rh == 1:
        if TIER[ch["tier"]] < TIER[cb["tier"]]:
            return "LOOSER", "ask tier lower"
        if not set(ch["rs"]) >= set(cb["rs"]):
            return "LOOSER", "ask reason line dropped"
        if ch.get("tg") is not None and cb.get("tg") is not None and not all(t in ch["tg"] for t in cb["tg"]):
            return "LOOSER", "a target line dropped from the card"
        return "STRICTER", "ask: the model's (tier kept, reasons/targets added)"
    if rh == 2 and rb < 2:
        return "STRICTER", "deny: the model's"
    return "DENY2DENY", "deny -> other deny: the model's"

main()
