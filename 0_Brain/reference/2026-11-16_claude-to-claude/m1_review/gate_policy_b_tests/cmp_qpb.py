# QA-POLICY-B comparer (the check's OWN; its attribution is NOT a port of scan B).
# usage: python3 -B -I cmp_qpb.py <base.jsonl> <head.jsonl> [label]
# Rules (from the docs and the brief, not from shell/mod.rs):
#  - command rows (Bash, PowerShell, Monitor without ws.url): every scan column and every answer byte-equal.
#  - every row: the command scans equal; scan A's pieces equal; the base's InText list a prefix of the head's.
#  - each differing cell: rank Allow < Ask < Deny; an ask: tier not lower and reasons a superset; anything else LOOSER.
#  - a head "denied as excluded" cell is attributed when the BASE engine, given the oracle's words (whitespace and JSON
#    escapes only, quotes dropped) that end within 1 200 characters of the field, denies as excluded ("twin");
#    E-2 for a web fetch, E-1 when the twin without escape blanking also denies, otherwise E-3; band <=1000 / 1000-1200.
#  - a head "too large" cell is attributed when the check's OWN arithmetic over the head's scan B pieces
#    (sum of 16 + path components + non-slash characters // 8; count) is over 1 024 pieces or 8 000 units.
#  - docs-tier completeness (one-sided, added after plant P-4 was missed): where the base engine given the docs'
#    second-tier words denies as excluded, the head's decide is not an allow or an ask (rows under the guard).
#  - completeness (one-sided): a planted name that is a whitespace/escape-delimited word of a window must be a piece
#    (A or B) on every row under the guard.
import json, sys
from collections import Counter, defaultdict

B, Hh = sys.argv[1], sys.argv[2]
LABEL = sys.argv[3] if len(sys.argv) > 3 else ""
TOO_LARGE_TEXT = "a text holding more name-like words than the gate can check"
COLS = ["decide", "would", "live", "live_shell", "expired", "other", "nobody", "own_none", "StillAsk", "Allowed", "Allowed_other", "Allowed_nobody"]
RANK = {"A": 0, "Q": 1, "D": 2}

def tierv(t):
    return int(t.lstrip("T")) if t and t[0] == "T" else -1

def my_work(stats):
    return sum(16 + c + ch // 8 for c, ch in stats), len(stats)

def direction(b, h):
    db, dh = b["d"], h["d"]
    kb, kh = db["k"], dh["k"]
    if kb == "W":
        if db == dh and b["h"] == h["h"]: return "same"
        if tierv(dh["tier"]) >= tierv(db["tier"]) and set(dh["rs"]) >= set(db["rs"]): return "stricter-w"
        return "looser"
    if RANK[kh] > RANK[kb]: return "stricter"
    if RANK[kh] < RANK[kb]: return "looser"
    if kb == "Q":
        if tierv(dh["tier"]) < tierv(db["tier"]) or not set(dh["rs"]) >= set(db["rs"]): return "looser"
        if dh != db: return "stricter-ask"
        return "card"
    if kb == "D":
        return "deny-other" if db["r"] != dh["r"] else "deny-text"
    return "allow-other"

fb, fh = open(B), open(Hh)
mb, mh = json.loads(fb.readline()), json.loads(fh.readline())
assert not mb["head"] and mh["head"], (mb, mh)
assert mb["rows"] == mh["rows"] and mb["states"] == mh["states"] and mb["seed"] == mh["seed"], (mb, mh)
states = mb["states"]
cnt = Counter(); dist = Counter(); attr = Counter(); per_state = Counter()
fails = defaultdict(list); deny_other = []; cmdfield_diff = []; monurl_diff = []
reach_rows = set(); over_rows = 0; under_rows = 0
for lb, lh in zip(fb, fh):
    rb, rh = json.loads(lb), json.loads(lh)
    rid = rb["id"]
    assert rid == rh["id"], (rid, rh["id"])
    cnt["rows"] += 1
    tool = rb["tool"]
    has_cmd = bool(rb["cmds"])
    monitor_url = tool == "Monitor" and any(w["k"] == "url" for w in rb["wins"])
    cls = "command" if tool in ("Bash", "PowerShell") or (tool == "Monitor" and not monitor_url) else (
        "monitor_url" if monitor_url else ("cmdfield" if has_cmd else "free"))
    cnt["class:" + cls] += 1
    # every row: identical command scans, facts, scan A; prefix
    if rb["cmds"] != rh["cmds"]: fails["command-scan differs"].append(rid)
    if rb["facts"] != rh["facts"]: fails["facts differ"].append(rid)
    if rb["canon"] != rh["canon"]: fails["canonical input differs"].append(rid)
    if rb["a_h"] != rh["a_h"]: fails["scan A pieces differ"].append(rid)
    if rb["it_h"] != rb["a_h"]: fails["base InText is not scan A (harness)"].append(rid)
    if not rh["it_h"].startswith(rb["it_h"]): fails["PREFIX: base pieces not the head's first"].append(rid)
    bad = rh.get("b_ad")
    if bad is None: fails["no adapter figures at head"].append(rid)
    elif not bad["eq_action"]: fails["adapter B pieces != action's B pieces"].append(rid)
    work, n = my_work(rh["b_stats"])
    my_over = n > 1024 or work > 8000
    if bad is not None and bad["work"] != work and not bad["over"]:
        fails["work arithmetic differs from the head's"].append((rid, work, bad["work"]))
    if bad is not None and my_over != bad["over"]:
        fails["over differs from the check's arithmetic"].append((rid, n, work, bad["over"]))
    head_text_oversize = rh["oversize"] == TOO_LARGE_TEXT
    if my_over: over_rows += 1
    else: under_rows += 1
    if my_over and rb["oversize"] is None and not head_text_oversize:
        fails["EXPECTED-L: over by arithmetic, not denied as too large"].append(rid)
    if head_text_oversize and not my_over:
        fails["too large though under the guard by arithmetic"].append((rid, n, work))
    # completeness: a planted name as a whitespace/escape-delimited word must be a piece, under the guard
    if not my_over and rh["oversize"] is None:
        for nm in rh.get("names", []):
            if nm["word_ends"] and not nm["in_pieces"]:
                fails["COMPLETENESS: name a word of the window, not a piece"].append((rid, nm["name"], nm["word_ends"][:3]))
    for sb, sh in zip(rb["states"], rh["states"]):
        sn = sb["st"]
        twin = sb.get("twin")
        # docs-tier completeness (added after plant P-4 was missed): under the guard, where the BASE engine given the
        # docs' second-tier words (punctuation split, after `@`, quoted parts) denies as excluded, the head's `decide`
        # must not be an allow or an ask.
        if twin and len(twin) > 3 and twin[3] == "X" and not my_over and rh["oversize"] is None:
            hd = sh["cols"][0]
            if hd["d"]["k"] in ("A", "Q", "W"):
                fails["DOCS-COMPLETENESS: docs-tier name not denied at the head"].append((rid, sn, hd["c"]))
        for ci, (cb, ch) in enumerate(zip(sb["cols"], sh["cols"])):
            cnt["cells"] += 1
            if cb == ch:
                continue
            d = direction(cb, ch)
            if d == "same":
                continue
            cnt["differing cells"] += 1
            reach_rows.add(rid)
            dist[(cb["c"], ch["c"], d)] += 1
            per_state[(sn, COLS[ci], cb["c"], ch["c"])] += 1
            if cls == "command":
                fails["COMMAND ROW answer differs"].append((rid, sn, COLS[ci], cb["c"], ch["c"]))
                continue
            if cls == "cmdfield":
                cmdfield_diff.append((rid, sn, COLS[ci], cb["c"], ch["c"], d))
            if cls == "monitor_url":
                monurl_diff.append((rid, sn, COLS[ci], cb["c"], ch["c"], d))
            if d in ("looser", "card", "allow-other", "stricter-w", "stricter-ask", "deny-text"):
                fails["LOOSER or unexplained: " + d].append((rid, sn, COLS[ci], cb["c"], ch["c"]))
                continue
            hc = ch["c"]
            if d == "deny-other":
                deny_other.append((rid, sn, COLS[ci], cb["d"]["r"][:60], ch["d"]["r"][:60]))
            # attribution
            if hc == "L":
                if my_over and head_text_oversize:
                    attr["guard (too large; the check's arithmetic over)"] += 1
                else:
                    fails["UNATTRIBUTED too large"].append((rid, sn, COLS[ci], n, work))
            elif hc == "X":
                if twin and twin[1] == "X":
                    band = "<=1000" if twin[0] == "X" else "1000-1200"
                    if tool == "WebFetch":
                        item = "E-2 (web fetch)"
                    else:
                        item = "E-1" if twin[2] == "X" else "E-3"
                    attr[f"{item} {band}"] += 1
                elif twin and len(twin) > 3 and twin[3] == "X":
                    attr[("E-2 (web fetch)" if tool == "WebFetch" else "E-1/E-3") + " tier 2 (the docs' punctuation split or after @)"] += 1
                else:
                    fails["UNATTRIBUTED denied as excluded"].append((rid, sn, COLS[ci], cb["c"], twin))
            else:
                fails["UNATTRIBUTED other deny"].append((rid, sn, COLS[ci], cb["c"], hc))

print(f"== QPB compare {LABEL}: seed {mb['seed']} rows {cnt['rows']} states {len(states)} cells {cnt['cells']}")
print("classes:", {k: v for k, v in cnt.items() if k.startswith("class:")})
print(f"differing cells {cnt['differing cells']} in {len(reach_rows)} rows; rows over the guard by the check's arithmetic {over_rows}, under {under_rows}")
print("distribution (base, head, direction):")
for k, v in sorted(dist.items(), key=lambda x: -x[1]): print(f"   {k}: {v}")
print("attribution:")
for k, v in sorted(attr.items()): print(f"   {k}: {v}")
print(f"deny -> other deny (same rank) cells: {len(deny_other)}")
c = Counter((x[3], x[4]) for x in deny_other)
for k, v in c.most_common(10): print(f"   {k}: {v}")
print(f"command-field calls (untaught, mcp__, Agent, ...) differing cells: {len(cmdfield_diff)} in {len(set(x[0] for x in cmdfield_diff))} rows")
for k, v in Counter((x[3], x[4], x[5]) for x in cmdfield_diff).most_common(): print(f"   {k}: {v}")
print(f"Monitor with ws.url differing cells: {len(monurl_diff)} in {len(set(x[0] for x in monurl_diff))} rows")
for k, v in Counter((x[3], x[4], x[5]) for x in monurl_diff).most_common(): print(f"   {k}: {v}")
print("per state x column (top 40):")
for k, v in per_state.most_common(40): print(f"   {k}: {v}")
nf = 0
for k, v in fails.items():
    nf += len(v)
    print(f"FAIL {k}: {len(v)}; first: {v[:4]}")
looser = sum(len(v) for k, v in fails.items() if k.startswith("LOOSER"))
unattr = sum(len(v) for k, v in fails.items() if k.startswith("UNATTRIBUTED"))
cmdd = len(fails.get("COMMAND ROW answer differs", [])) + len(fails.get("command-scan differs", []))
print(f"SUMMARY {LABEL}: looser {looser}, unattributed {unattr}, command differences {cmdd}, prefix failures {len(fails.get('PREFIX: base pieces not the head' + chr(39) + 's first', []))}, "
      f"expected-L failures {len(fails.get('EXPECTED-L: over by arithmetic, not denied as too large', []))}, completeness misses {len(fails.get('COMPLETENESS: name a word of the window, not a piece', []))}, docs-tier misses {len(fails.get('DOCS-COMPLETENESS: docs-tier name not denied at the head', []))}, "
      f"other failures {nf - looser - unattr - cmdd}, reach {cnt['differing cells']}")
print("RESULT", "PASS" if nf == 0 and cnt["differing cells"] > 0 else "FAIL")
sys.exit(0 if nf == 0 and cnt["differing cells"] > 0 else 1)
