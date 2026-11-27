# QA-POLICY-B item 10 (adapted from the QA-POLICY-WORDS check): byte scan for names. Words come ONLY from the command line (never written to a file).
# usage: python3 -B -I namescan.py <word> [<word> ...]
# Each word is searched case-insensitively as bytes in five forms: plain, URL-encoded, backslash-escaped (space and
# punctuation), slug (lower-case, runs of non-alphanumerics -> '-'), and UTF-16LE. Output masks the matched text as
# <w<index>>, so the log never holds a name.
import re, subprocess, sys, urllib.parse
C = "/private/tmp/claude-501/qpb/repo"; B = "5cab5e42df6cb3db05f3d38c7ba973beafd044b2"; H = "cd7b6fdd1a4b2de5937795b052a68d793146eb6d"
SIX = ["BACKLOG.md", "crates/coagent-policy/Cargo.toml", "crates/coagent-policy/red-controls.sh", "crates/coagent-policy/src/action.rs",
       "crates/coagent-policy/src/shell/mod.rs", "crates/coagent-policy/tests/t25_owner_allow.rs", "crates/coagent-policy/tests/t27_owner_dark.rs",
       "crates/coagent-policy/tests/t28_at_names.rs", "crates/coagent-policy/tests/t29_free_text.rs", "docs/M0-OUTCOMES.md", "docs/POLICY.md"]
words = sys.argv[1:]
def forms(w):
    f = {w, urllib.parse.quote(w), urllib.parse.quote_plus(w), re.sub(r"([ !~&()'\"$\\])", r"\\\1", w),
         re.sub(r"[^a-z0-9]+", "-", w.lower()).strip("-")}
    out = [x.encode() for x in f if x]
    out.append(w.encode("utf-16-le"))
    return out
PAT = [(i, re.compile(re.escape(x), re.I)) for i, w in enumerate(words) for x in forms(w)]
def g(*a): return subprocess.run(["git", "-C", C, *a], capture_output=True, check=True).stdout
def scan(label, data, base_lines=None):
    hits = 0
    for ln, line in enumerate(data.split(b"\n"), 1):
        found = sorted({i for i, p in PAT if p.search(line)})
        if not found: continue
        hits += 1
        spans = sorted({(m.start(), m.end(), i) for i, p in PAT for m in p.finditer(line)}, key=lambda t: (t[0], -t[1]))
        out, pos, firsts = b"", 0, {}
        for a, b, i in spans:
            if a < pos: continue
            firsts.setdefault(i, len(out) + (a - pos))
            out += line[pos:a] + f"<w{i}>".encode(); pos = b
        out += line[pos:]
        tag = "BASE-IDENTICAL" if base_lines is not None and line in base_lines else "NEW"
        ctx = out.decode("utf-8", "replace")
        for i in found:
            k = ctx.find(f"<w{i}>")
            if k < 0: k = 0   # this word's span lay inside another word's mask
            print(f"  HIT {label}:{ln} {tag} word#{i} ...{ctx[max(0, k-30):k+40]}...")
    return hits
print("words:", len(words), "patterns:", len(PAT))
total = {}
diff = g("diff", B, H)
added = b"\n".join(l[1:] for l in diff.split(b"\n") if l.startswith(b"+") and not l.startswith(b"+++"))
total["added lines"] = scan("ADDED", added)
for p in SIX:
    try: base = set(g("show", f"{B}:{p}").split(b"\n"))
    except subprocess.CalledProcessError: base = set()
    total[p] = scan(p, g("show", f"{H}:{p}"), base)
total["8 commit messages"] = scan("COMMIT-MSG", g("log", "--format=%B", B + ".." + H))
for extra in sys.stdin.read().split():   # controls: paths given on stdin
    total["control " + extra] = scan("CONTROL " + extra, open(extra, "rb").read())
for k, v in total.items(): print(f"TOTAL {v} hit lines: {k}")
