# QA-POLICY-NOTES D-B comparator (independent check). Run: python3 -B -I cmp_db.py BASE.txt NEW.txt [--off item]...
# Walks the two outputs of zz_qpn_db.rs in lockstep. Every non-column line must be identical (the action, decide).
# Every differing COLUMN line is attributed by MY predicates, computed here from the printed hook JSON, the printed
# scan words and the state names the harness built (never from the code under test), with NO order between items:
#   item 2   : a scan word that, after one trailing .exe/.cmd/.bat/.ps1 and any '@' suffix after the first character
#              (either order), is in my copy of BYPASS_REFUSED_WORDS or is 'claude-code'
#              -> the new answer is the owner refusal with the AgentProgramWord text
#   item 3(a): tool_name == "Bash" and tool_input's "command" missing, not a string, or ""  -> new answer == decide's
#   item 3(b): "dangerouslyDisableSandbox" present in tool_input and not JSON false -> owner refusal, SandboxBypass text
#   item 4   : the hook cwd is not absolute (does not start with '/')      -> owner refusal, UnresolvedTarget text
# A line is attributed only if the column's view is LIVE for the hook's session and one holding item's answer is the
# new line. Also: LOOSER (new is an Allow where old was not), the item-1-gone check, and the FR(3) check.
import json, sys, collections

WORDS = {"coagent", "coagentd", "coagent-hook", "coagent-mcp", "claude"}  # my copy, patterns.rs:504-513 at f193620
PFX = "coagent: not allowed even in ALLOW mode: "
TXT = {
    "2": "names CoAgent's own programs or an agent program",
    "3b": "asks to run outside the sandbox",
    "4": "a path the gate could not resolve",
}
OWNER_ALLOW = "allowed: the owner chose ALLOW for this session"


def cut_at(w):
    i = w.find("@", 1)
    return w if i < 0 else w[:i]


def cut_ext(w):
    for e in (".exe", ".cmd", ".bat", ".ps1"):
        if w.endswith(e):
            return w[: -len(e)]
    return w


def spelled(w):
    return any(c in WORDS or c == "claude-code" for c in (cut_ext(cut_at(w)), cut_at(cut_ext(w))))


def text_of(line):  # the TEXT "..." part of a column/decide line
    i = line.rfind(' TEXT "')
    if i < 0:
        return None
    return json.loads(line[i + 6:]) if line.endswith('"') else None


def kind(line):  # a short answer class for the difference table
    t = text_of(line) or ""
    if line.startswith("Allow"):
        return "owner allow" if t == OWNER_ALLOW else "allow " + line.split("{")[1].split()[1]
    if line.startswith("Ask"):
        return "ask " + line.split("tier: ", 1)[1].split(",")[0]
    if t.startswith(PFX):
        return "refused: " + t[len(PFX):]
    return "deny " + line.split("reason: ", 1)[1].split(" ")[0].rstrip("{")


def main():
    a, b = sys.argv[1], sys.argv[2]
    off = set()
    for i, x in enumerate(sys.argv):
        if x == "--off":
            off.add(sys.argv[i + 1])
    fa, fb = open(a, "rb"), open(b, "rb")
    states = {}
    hook = None
    words = []
    st = None
    dec = None
    c = collections.Counter()
    reach = collections.Counter()   # lines each item explains (no ordering; a line may count for two)
    only = collections.Counter()    # lines exactly one item explains
    bycol = collections.Counter()
    examples = collections.defaultdict(list)
    trans = collections.Counter()
    n = 0
    while True:
        la, lb = fa.readline(), fb.readline()
        if not la and not lb:
            break
        n += 1
        la = la.decode("utf-8", "surrogateescape").rstrip("\n")
        lb = lb.decode("utf-8", "surrogateescape").rstrip("\n")
        if la.startswith("S") and la[1:2].isdigit():
            if la != lb:
                c["noncol_diff"] += 1
            k, rest = la.split(" ", 1)
            f = dict(x.split("=", 1) for x in rest.split() if "=" in x)
            states[k[1:]] = (int(f["exn"]) > 0 or f["gx"] == "list", rest)
            continue
        if la.startswith("A") and " HOOK " in la:
            if la != lb:
                c["noncol_diff"] += 1
            hook = json.loads(la.split(" HOOK ", 1)[1])
            continue
        if la.startswith("W "):
            if la != lb:
                c["noncol_diff"] += 1
            words = json.loads(la[2:])
            continue
        if la.startswith(" s"):
            if la != lb:
                c["noncol_diff"] += 1
            st = la.split()[0][1:]
            dec = la.split(" D ", 1)[1]
            continue
        if not la.startswith("  "):
            if la != lb and not la.startswith("cases"):
                c["noncol_diff"] += 1
            continue
        col, va = la[2:].split(" ", 1)
        colb, vb = lb[2:].split(" ", 1)
        if col != colb:
            c["noncol_diff"] += 1
            continue
        c["col_lines"] += 1
        old = dec if va == "=" else va
        new = dec if vb == "=" else vb
        ti = hook.get("tool_input")
        ti = ti if isinstance(ti, dict) else {}
        sess = hook.get("session_id")
        live = (col in ("still", "allowed") and sess == "sess-q") or (col == "elsewhere" and sess == "sess-other")
        excl = states[st][0]
        p = {
            "2": any(spelled(w) for w in words),
            "3a": hook.get("tool_name") == "Bash" and (
                "command" not in ti or not isinstance(ti["command"], str) or ti["command"] == ""),
            "3b": "dangerouslyDisableSandbox" in ti and not (ti["dangerouslyDisableSandbox"] is False),
            "4": not str(hook.get("cwd", "")).startswith("/"),
        }
        for k in off:
            p[k] = False
        any_pred = any(p.values())
        old_owner_allow = old.startswith("Allow") and text_of(old) == OWNER_ALLOW
        # item 1 gone: Bash, something excluded, main answers the owner allow, no item 2-4 predicate
        if hook.get("tool_name") == "Bash" and excl and old_owner_allow and not any_pred:
            c["item1_check_same" if va == vb else "item1_check_DIFFERENT"] += 1
            if va != vb and len(examples["item1"]) < 3:
                examples["item1"].append((n, hook, old[:160], new[:200]))
        # MISSED: a live view, an item 2 / 3 (b) / 4 predicate (or 3 (a) under Allowed), and the head still answers
        # the OWNER allow (an allow from steps [1]-[7b], before the mode, is main's and not counted)
        new_owner_allow = new.startswith("Allow") and text_of(new) == OWNER_ALLOW
        if live and new_owner_allow:
            for k in ("2", "3b", "4", "3a"):
                if p[k]:
                    c["MISSED_" + k] += 1
                    if len(examples["missed"]) < 5:
                        examples["missed"].append((n, col, k, hook, words[:12]))
        if live:
            for k in ("2", "3b", "4"):
                if p[k]:
                    c["live_pred_" + k] += 1
        if va == vb:
            continue
        c["differ"] += 1
        bycol[col] += 1
        if new.startswith("Allow") and not old.startswith("Allow"):
            c["LOOSER"] += 1
            examples["looser"].append((n, hook, old[:200], new[:200]))
        nt = text_of(new)
        expl = []
        if live:
            for k in ("2", "3b", "4"):
                if p[k] and new.startswith("Deny") and "RefusedInAllow" in new and nt == PFX + TXT[k]:
                    expl.append(k)
            if p["3a"] and vb == "=":
                expl.append("3a")
        if not expl:
            c["UNATTRIBUTED"] += 1
            if len(examples["unattr"]) < 5:
                examples["unattr"].append((n, col, hook, words[:12], states[st][1], old[:220], new[:220]))
            continue
        c["attributed"] += 1
        trans["+".join(expl), col, kind(old), kind(new)] += 1
        for k in expl:
            reach[k] += 1
        if len(expl) == 1:
            only[expl[0]] += 1
        # FR(3): an empty Bash command in a state with something excluded: is every such differing line 3(a)'s answer?
        if p["3a"] and excl:
            others = p["2"] or p["3b"] or p["4"]
            c["fr3_lines_with_other_pred" if others else "fr3_lines"] += 1
            if not others:
                c["fr3_is_decide" if vb == "=" else "fr3_NOT_decide"] += 1
    print(f"lines {n}; column lines {c['col_lines']}; non-column differences {c['noncol_diff']}")
    print(f"differing column lines {c['differ']} by column {dict(bycol)}")
    print(f"attributed {c['attributed']}; UNATTRIBUTED {c['UNATTRIBUTED']}; LOOSER {c['LOOSER']}  (off: {sorted(off)})")
    print(f"reach per item (no order; a line may count twice): {dict(sorted(reach.items()))}")
    print(f"explained by exactly one item: {dict(sorted(only.items()))}")
    print(f"item 1 gone check (Bash, something excluded, main = owner allow, no item 2-4 predicate): "
          f"same {c['item1_check_same']}, DIFFERENT {c['item1_check_DIFFERENT']}")
    print(f"FR(3) empty Bash with exclusions, differing, no other predicate: {c['fr3_lines']}; equal to decide "
          f"{c['fr3_is_decide']}; not {c['fr3_NOT_decide']} (with another predicate too: {c['fr3_lines_with_other_pred']})")
    print("MISSED (predicate holds, view live, head = owner allow): "
          + str({k: c["MISSED_" + k] for k in ("2", "3a", "3b", "4")})
          + "; live column lines with the predicate: " + str({k: c["live_pred_" + k] for k in ("2", "3b", "4")}))
    for (it, col, o, nw), v in sorted(trans.items()):
        print(f"TRANS item {it} | {col} | {o} -> {nw} | {v}")
    for k, v in examples.items():
        for e in v[:5]:
            print("EXAMPLE", k, json.dumps(e, ensure_ascii=True)[:1200])


main()
