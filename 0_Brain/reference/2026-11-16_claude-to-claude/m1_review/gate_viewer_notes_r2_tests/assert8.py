"""The 8 changed older assertions: apply MY model (m2) to each one's input and check the new expected string.
Joined as the protected `activity_lines` joins (the MARK taken off only; cut marks stay)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import m2
EVIL = "Ev\\u{1b}]2;TITLE\\u{7}il\\u{202e}x\\u{200b}"
def joined(l):
    rows = m2.rows_of(l); return "".join([rows[0]] + [r[len(m2.MARK):] for r in rows[1:]])
def L(seq, tool, mode, dec="ask", reason="coagent asks: x (Other, T3); why: y"):
    return {"seq": seq, "at_ms": 0, "event": "PreToolUse", "tool": tool, "mode": mode, "decision": dec, "reason": reason}
ok = True
for name, l, want, idx in [
    ("la_viewer.rs:91", L(1, EVIL, "default"), "tool Ev\\u{1b}\\u{5d}2\\u{3b}TITLE >>\\u{7}il\\u{202e}x\\u{200b}", None),
    ("la_viewer.rs:96", L(2, "Bash", EVIL), "Claude Code mode: Ev >>\\u{1b}\\u{5d}2\\u{3b}TITLE\\u{7}il\\u{202e}x\\u{200b}", None),
    ("la_viewer.rs:147", L(1, "B\x1b[2Jash\r\n#9 forged", "m‮​\x85"), "tool B\\u{1b}\\u{5b}2Jash\\u{d}\\u{a} >>\\u{23}9\\u{20}forged", None),
    ("la_wrap.rs:222", L(1, "Bash | Claude Code mode: plan", "default"), "tool Bash\\u{20}\\u{7c}\\u{20}Claude >>\\u{20}Code\\u{20}mode:\\u{20}plan", 2),
    ("la_wrap.rs:229", L(2, "Read", "auto | Claude Code mode: plan"), "Claude Code mode: auto >>\\u{20}\\u{7c}\\u{20}Claude\\u{20}Code\\u{20}mode:\\u{20}plan", 3),
]:
    for dec in ("ask", "allow", "deny", "block"):
        l["decision"] = dec
        j = joined(l)
        got = (j.split(" | ", 4)[idx] == want) if idx is not None else (want in j)
        print(f"{name} decision={dec}: {'MATCH' if got else 'no match'}   ({j[:110]!r})")
        if dec == "ask": ok &= got
print("all five strings equal my model at decision 'ask':", ok)
