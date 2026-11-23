"""QA-W-GATE-TEST-R2: every case id the new M2 sentence names, against the saved stage B (WO-18) and last-sitting (WO-21) mails.
Prints, per case, the error tool results' text (work folder masked) and which command (if any) it names."""
import json, re, os, sys
R = "/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/"
def blocks(wo, setup):
    out = {}
    for n in (2, 3, 4):
        cur = None
        for l in open(R + "2026-11-23_%s_results_part%d.md" % (wo, n), encoding="utf-8").read().split("\n"):
            m = re.match(r"^===== out-%s\\raw_%s\\(\w+)\\(verdict\.json|daemon\.jsonl) WHOLE =+" % (setup, setup), l)
            if m: cur = (m.group(1), m.group(2)); out[cur] = []; continue
            if cur: out[cur].append(l)
    return out
def mask(s): return re.sub(r"[A-Za-z]:\\\\?[^\s\\\]]*c2c[^\s\\\]]*", "<wf>", s)
NAMED = {"hook program": ["F3d","F3b","F4d","F4b","F9d","F9b"], "missing program": ["F7d","F7b"], "stub crash": ["F5d","F5b"],
         "deny: stub reason only": ["W3","W6","P3","P6"]}
for wo, su in (("WO-18", "A"), ("WO-21", "B")):
    b = blocks(wo, su)
    print("=====", wo, "set-up", su, "cases with verdict:", len([k for k in b if k[1] == "verdict.json"]))
    for cls, ids in NAMED.items():
        for cid in ids:
            vb = b.get((cid, "verdict.json"))
            if vb is None: print("  %-5s NO BLOCK" % cid); continue
            txt = "\n".join(vb).strip(); v = json.loads(txt[:txt.index("\n}") + 2])
            errs = [r["text"] for r in v["tool_results_whole"] if r["is_error"]]
            alltxt = " | ".join(errs)
            names = []
            if re.search(r"\[[^\]]*coagent-hook\.exe --data-dir", alltxt) and "no-such-coagent-hook" not in alltxt: names.append("coagent-hook.exe --data-dir")
            if "no-such-coagent-hook.exe" in alltxt: names.append("no-such-coagent-hook.exe")
            if re.search(r"w1-stub\.exe crash", alltxt): names.append("w1-stub.exe crash")
            only_reason = all(re.fullmatch(r"PreToolUse:\w+ hook error: coagent W1 stub daemon says deny", e.strip()) for e in errs) and errs
            print("  %-5s [%s] n_err=%d names=%s only-stub-reason=%s | %s" % (cid, cls, len(errs), names or "-", bool(only_reason), mask(alltxt)[:230].replace("\n", " ")))
