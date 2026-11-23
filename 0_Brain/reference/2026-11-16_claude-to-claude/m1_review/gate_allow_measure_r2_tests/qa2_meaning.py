#!/usr/bin/env python3
"""QA-ALLOW-MEASURE-R2 item 5b: independent meaning check of the re-redaction (not the builder's meaning_check.py).
For every round-1 raw file: compare d76a83b with the head. For a changed file, align lines; every changed line must
differ only in segments where the OLD text is an API message id (msg_...) or a workspace-path form (shell-escaped
or URL-encoded, which round 1 left) and the NEW text is the matching placeholder. Paths are passed in env QA_WS and
never printed. Also: line counts equal; verdict markers (decisions, modes, dialog texts, markers) identical.
usage: qa2_meaning.py <clone> <old> <new>"""
import difflib, os, re, subprocess, sys
clone, old, new = sys.argv[1:4]; P = "spikes/U-B1-hook-allow-silent/"
WS = [p for p in os.environ.get("QA_WS", "").split("|") if p]
def g(rev, f): return subprocess.run(["git", "-C", clone, "show", "%s:%s" % (rev, f)], capture_output=True).stdout.decode("utf-8", "replace")
files = subprocess.run(["git", "-C", clone, "ls-tree", "-r", "--name-only", old, "--", P + "raw"], capture_output=True, text=True).stdout.split()
newfiles = set(subprocess.run(["git", "-C", clone, "ls-tree", "-r", "--name-only", new, "--", P + "raw"], capture_output=True, text=True).stdout.split())
MSG = re.compile(r"^msg_[A-Za-z0-9]{8,}$"); PH = {"<MSG>", "<RUN>", "<WORKTREE>", "<COAGENT>", "<CLAUDE_CONFIG_DIR>"}
def is_path_form(s):
    u = s.replace("\\ ", " ").replace("\\!", "!").replace("%20", " ").replace("%21", "!")
    return any(u.startswith(w) or w.startswith(u) for w in WS) and u != s     # an ESCAPED/ENCODED form of a workspace root
VERDICT = re.compile(r"permissionDecision|permission_mode|permissionMode|Do you want|STEP |MK3|M7_|TTYLINE|_GOT=|OPEN=|tool_dispatch|Skipping|hook_event_name|is_error|permission_denials|Exit code|mode on|bypassing|denied")
unchanged = 0; changed = []; bad = []; missing = []
for f in files:
    if f not in newfiles: missing.append(f); continue
    a, b = g(old, f), g(new, f)
    if a == b: unchanged += 1; continue
    la, lb = a.splitlines(), b.splitlines(); nlines = 0; segs = {"msg": 0, "path": 0}; why = []
    if len(la) != len(lb): why.append("line count %d -> %d" % (len(la), len(lb)))
    for x, y in zip(la, lb):
        if x == y: continue
        nlines += 1
        # tokens: placeholders and runs of non-space; then diff the token streams
        tok = lambda s: re.findall(r"<[A-Z_]+>|msg_[A-Za-z0-9]+|[^\s\"'`=,:]+(?:\\ [^\s\"'`=,:]+)*|.", s)
        sm = difflib.SequenceMatcher(None, tok(x), tok(y), autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal": continue
            o = "".join(tok(x)[i1:i2]); n = "".join(tok(y)[j1:j2])
            if MSG.match(o) and n == "<MSG>": segs["msg"] += 1
            elif any(p in n for p in PH) and is_path_form(o.split("<")[0] if "<" in o else o): segs["path"] += 1
            elif any(p in n for p in PH) and any(is_path_form(o[:k]) for k in range(len(o), 0, -1)): segs["path"] += 1
            else: why.append("unexplained segment (len old %d -> new %r)" % (len(o), n[:40]))
        vx = VERDICT.findall(x); vy = VERDICT.findall(y)
        if vx != vy: why.append("verdict markers differ on a changed line")
    changed.append((f[len(P):], nlines, segs)); (bad.append((f[len(P):], why[:3])) if why else None)
print("round-1 raw files: %d; unchanged %d; changed %d; missing at head %d" % (len(files), unchanged, len(changed), len(missing)))
for f, n, s in changed: print("  CHANGED %-45s lines %3d  msg->%d  path-form->%d" % (f, n, s["msg"], s["path"]))
print("files with any change NOT explained by the two new rules:", len(bad))
for f, w in bad: print("  ", f, w)
