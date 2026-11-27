#!/usr/bin/env python3
"""search_truth.py <work dir> <tool> <sock> <tree copy>: questions of my own (written before any was run) on a scratch
index built from a COPY of the real allowed brain files. For each: the first three results, and an INDEPENDENT test
of the neutral last line: (a) are the words it names really the question's rarest (by my own count of rows holding
each stem); (b) does the first result's row really hold every 'holds' word and none of the 'lacks' words."""
import os, sys, subprocess, re
W, TOOL, SOCK, ROOT = sys.argv[1:5]
PGBIN = "/opt/homebrew/opt/postgresql@15/bin"; PG = os.path.join(W, "pg"); os.makedirs(W, exist_ok=True)
def tool(*args):
    env = dict(os.environ, BRAINDB_ROOT=ROOT, BRAINDB_PGDATA=PG, BRAINDB_SOCKDIR=SOCK); env.pop("WED_AGENT", None)
    r = subprocess.run(["/bin/bash", TOOL] + list(args), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode("utf-8", "replace")
def psql(sql, *vars_):
    cmd = [PGBIN + "/psql", "-X", "-At", "-F", "\t", "-h", SOCK, "-d", "braindb"]
    for i, v in enumerate(vars_): cmd += ["-v", "v%d=%s" % (i, v)]
    r = subprocess.run(cmd, input=sql.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.stdout.decode("utf-8", "replace").strip()
rc, o = tool("rebuild"); print("rebuild rc=%d : %s" % (rc, [l for l in o.split("\n") if "total" in l][:1]))
Q = [  # (question, what I expect first, written before running)
 ("one question at a time", "rules: CLAUDE.md rule 0b"),
 ("ledger archive rows older than three days", "rules: CLAUDE.md session end 3c"),
 ("regenerate both boot digests by tier", "rules: session end 3b"),
 ("never edit files inside other coding projects", "rules: rule 0a (manage, don't do)"),
 ("what must be true before I close a pane", "lesson: a pane close is a session kill"),
 ("where do screenshots go, nothing else lives in the root", "rules: folder map / root row"),
 ("mental model is not the source of truth validate first", "rules: 0_Brain/CLAUDE.md mental model section, or its lesson"),
 ("secrets env never committed", "rules: rule 5 (secrets)"),
 ("retro candidate filed or discarded same action", "rules: session end 2a"),
 ("speak greeting status Moira voice", "rules: rule 3 (verbal channel)"),
 ("how do I name a git branch", "nothing right exists (the seat's own known wrong-neighbour case)"),
 ("Kam", "no single right answer: a one-word question"),
 ("doctor check new machine-local tool dependency", "rules: session end 3a"),
 ("Linear is the task source of truth", "rules: rule 0c"),
 ("drive pane wake", "three common words: does a rules row holding all three go first wrongly?"),
 ("the of and", "stop words only"),
 ("xqzzyunknownword pane", "one word not in the index at all"),
]
bad_truth = 0
for q, expect in Q:
    rc, out = tool("search", q)
    lines = out.rstrip("\n").split("\n")
    print("\n=== Q: %s\n    expected first: %s   (rc %d)" % (q, expect, rc))
    res = [l for l in lines if re.match(r"^\s*\d+\. ", l)]
    heads = [l for l in lines if l.strip().startswith("heading:")]
    for i, l in enumerate(res[:3]):
        print("    " + l.strip()[:150] + ("   | " + heads[i].strip()[:110] if i < len(heads) else ""))
    last = lines[-1]; print("    LAST LINE: " + last[:260])
    m = re.search(r"holds all (\d+) of the question's rarest words \[(.*?)\]", last)
    m2 = re.search(r"of the question's (\d+) rarest words it holds (\d+) \[(.*?)\] and lacks (\d+) \[(.*?)\]", last)
    if not res or not (m or m2):
        print("    (no first-result statement to test)"); continue
    held = (m.group(2) if m else m2.group(3)).split(); lack = [] if m else m2.group(5).split()
    # (a) my own rarity count: rows whose tsv holds the stem; the question's stems from to_tsvector
    stems = [s for s in psql("select unnest(tsvector_to_array(to_tsvector('english', :'v0')))", q).split("\n") if s]
    cnt = {}
    for s in stems:
        cnt[s] = int(psql("select count(*) from brain.chunks where tsv @@ quote_literal(:'v0')::tsquery", s) or 0)
    mine = sorted(stems, key=lambda s: (cnt[s], s))[:4]
    ok_a = set(mine) == set(held + lack) or sorted(cnt[s] for s in mine) == sorted(cnt[s] for s in held + lack if s in cnt)
    # (b) the first result's row: found by path and line as printed
    first = res[0]; pm = re.search(r"\]\s+(\S.*?)(?::(\d+))?$", first.strip())
    path, line = pm.group(1), pm.group(2)
    okb = True; detail = []
    for wd, want in [(h, "t") for h in held] + [(l_, "f") for l_ in lack]:
        got = psql("select bool_or(tsv @@ quote_literal(:'v0')::tsquery) from brain.chunks where path = :'v1' and line = :'v2'::int", wd, path, line or "0")
        detail.append("%s=%s" % (wd, got))
        if got != want: okb = False
    if not (ok_a and okb): bad_truth += 1
    print("    TRUTH: (a) named words are the %d rarest by my count %s: %s ; (b) row %s:%s holds/lacks as stated: %s  [%s]"
          % (len(held + lack), dict((s, cnt[s]) for s in mine), "yes" if ok_a else "NO", path[-60:], line, "yes" if okb else "NO", " ".join(detail)))
print("\nquestions with a first-result statement that is NOT true by my independent test: %d" % bad_truth)
print("positive control for test (b): a word the first row of Q1 surely lacks ->", psql("select bool_or(tsv @@ 'xqzzyunknownword'::tsquery) from brain.chunks where id = (select min(id) from brain.chunks)"))
rc, o = tool("stop"); print(o.strip().split("\n")[-1][:70])
