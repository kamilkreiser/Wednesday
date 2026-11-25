#!/usr/bin/env python3
"""QA-MEASURE-2-R2 task 2: my own comparison of spikes/U-B2-host-facts at OLD against NEW, both read from the git object
store (never from a worktree), independent of the seat's compare_r2.py (its code was read, none of it is imported).
usage: python3 -I -B qm2r_rawcmp.py <clone> <old> <new> <word1> <word2> [--control keyalter|swallow|short|none]
  word1 / word2: the coordinator folder's name and the credentials component, passed at run time (never stored here).
For every CHANGED raw file (raw/** and rehearsal.txt) every differing line must be EITHER the old line with placeholders put
in place of substrings that the placeholder's class matches IN FULL - no more (the old substring is exactly one class
match) and no less (the character after it cannot extend the match; for <CLAUDE-TMP> a "/private" just before it must be
inside it) - OR a line deleted from raw/S1/debug.excerpt.log that holds both words (the dropped lines). Everything else
is UNATTRIBUTED. Classes are written here from the placeholders' meaning, not copied from redact.py:
  <TMUX-SOCKET>  (/private)?/tmp/tmux-<digits>/<name chars>      <CLAUDE-TMP>  (/private)?/tmp/claude-<digits>
  <COORD-NAME>   word1 as a whole path component (any case)       <CRED-DIR>    word2 likewise
--control mutates ONE line of the NEW tree in memory before comparing (keyalter: KEY->KEX in raw/E3-r1/keys.log;
swallow: the word after a <TMUX-SOCKET> deleted, as if the placeholder ate it; short: the old socket name's last
character left after the placeholder). Prints counts, file names and placeholder names only, never a masked value."""
import collections, difflib, re, subprocess, sys
sys.dont_write_bytecode = True
args = [a for a in sys.argv[1:] if not a.startswith("--")]
ctl = sys.argv[sys.argv.index("--control") + 1] if "--control" in sys.argv else "none"
if ctl != "none": args = [a for a in args if a != ctl]
clone, old, new, w1, w2 = args[:5]
PFX = "spikes/U-B2-host-facts/"
def git(*a): return subprocess.run(["git", "-C", clone, *a], capture_output=True, check=True).stdout
def tree(rev):
    out = {}
    for l in git("ls-tree", "-r", rev, "--", PFX).decode().splitlines():
        meta, p = l.split("\t", 1); out[p[len(PFX):]] = meta.split()[2]
    return out
CLS = {"<TMUX-SOCKET>": (r"(?:/private)?/tmp/tmux-\d+/[A-Za-z0-9_.-]+", r"[A-Za-z0-9_.-]"),
       "<CLAUDE-TMP>": (r"(?:/private)?/tmp/claude-\d+", r"\d"),
       "<COORD-NAME>": (re.escape(w1), r"[A-Za-z0-9_]"),
       "<CRED-DIR>": (re.escape(w2), r"[A-Za-z0-9_]")}
PH = re.compile("|".join(re.escape(k) for k in CLS))
def masks_only(o, n, tally):
    phs = PH.findall(n)
    if not phs: return False
    parts = PH.split(n)
    rx = "".join(re.escape(parts[i]) + ("(%s)" % CLS[phs[i]][0] if i < len(phs) else "") for i in range(len(parts)))
    m = re.fullmatch(rx, o, re.S | (re.I if any(p in ("<COORD-NAME>", "<CRED-DIR>") for p in phs) else 0))
    if not m: return False
    for i, ph in enumerate(phs):
        s, e = m.span(i + 1); nxt = o[e:e + 1]; prv = o[max(0, s - 8):s]
        if nxt and re.fullmatch(CLS[ph][1], nxt): return False                      # swallowed less: the match could go on
        if ph in ("<TMUX-SOCKET>", "<CLAUDE-TMP>") and prv.endswith("/private") and not m.group(i + 1).startswith("/private"): return False
        if ph in ("<COORD-NAME>", "<CRED-DIR>"):
            b = o[s - 1:s] if s else ""
            if b not in ("/", "\\", "~", "-"): return False                       # must be a path component
    for ph in phs: tally[ph] += 1
    return True
T_old, T_new = tree(old), tree(new)
counts = collections.Counter(); tally = collections.Counter(); per = {}; un = 0; masked = 0; dropped = 0
for p in sorted(set(T_old) | set(T_new)):
    if p not in T_new: counts["removed"] += 1; print("REMOVED", p); continue
    if p not in T_old: counts["new"] += 1; print("NEW    ", p); continue
    ob = git("cat-file", "blob", T_old[p]); nb = git("cat-file", "blob", T_new[p])
    if ctl == "keyalter" and p == "raw/E3-r1/keys.log": nb = nb.replace(b"KEY", b"KEX", 1)
    if ctl in ("swallow", "short") and p == "raw/E3-r1/keys.log":
        t = nb.decode()
        i = t.index("<TMUX-SOCKET>") + len("<TMUX-SOCKET>")
        if ctl == "swallow":
            m = re.match(r"(\S*\s+\S+)", t[i:]); t = t[:i] + t[i + len(m.group(1)):]   # the closing quote and the next word
        else:
            orig = re.search(r"/tmp/tmux-\d+/([A-Za-z0-9_.-]+)", ob.decode()).group(1); t = t[:i] + orig[-1] + t[i:]
        nb = t.encode()
    if ob == nb: counts["identical"] += 1; continue
    counts["changed"] += 1
    if not (p.startswith("raw/") or p == "rehearsal.txt"): print("CHANGED (not raw) %s" % p); continue
    ol = ob.decode("utf-8", "surrogateescape").split("\n"); nl = nb.decode("utf-8", "surrogateescape").split("\n")
    fm = fd = fu = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes():
        if op == "equal": continue
        if op == "delete" and p == "raw/S1/debug.excerpt.log":
            for l in ol[i1:i2]:
                if re.search(r"(?i)[/\\]" + re.escape(w1) + r"[/\\]", l) and re.search(r"(?i)[/\\]" + re.escape(w2) + r"[/\\]", l): fd += 1
                else: fu += 1; print("  UNATTRIBUTED delete in %s old line %d" % (p, i1 + 1))
            continue
        if op == "replace" and i2 - i1 == j2 - j1:
            for k, (o, n) in enumerate(zip(ol[i1:i2], nl[j1:j2])):
                if masks_only(o, n, tally): fm += 1
                else: fu += 1; print("  UNATTRIBUTED in %s line %d (placeholders in the new line: %s)" % (p, j1 + k + 1, PH.findall(n)))
            continue
        fu += max(i2 - i1, j2 - j1); print("  UNATTRIBUTED %s in %s old %d-%d new %d-%d" % (op, p, i1 + 1, i2, j1 + 1, j2))
    per[p] = (fm, fd, fu); masked += fm; dropped += fd; un += fu
for p, (fm, fd, fu) in per.items(): print("CHANGED raw %-40s masked %3d dropped %d unattributed %d" % (p, fm, fd, fu))
print("control: %s" % ctl)
print("SUMMARY files %s ; changed raw files %d ; masked lines %d ; dropped lines %d ; placeholders put in %s ; UNATTRIBUTED %d"
      % (dict(counts), len(per), masked, dropped, dict(tally), un))
