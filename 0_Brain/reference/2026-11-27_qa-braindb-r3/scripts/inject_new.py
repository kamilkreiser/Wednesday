#!/usr/bin/env python3
"""inject_new.py <work dir> <tool> <sock>: NEW injection payloads through file names, headings, bodies, rules-index
fields and through search / at arguments. Checks: no PWNED file anywhere under the work dir or cwd; database object
counts identical before and after; the rows carrying payloads are stored verbatim and found (positive control)."""
import os, sys, subprocess
W, TOOL, SOCK = sys.argv[1:4]
PGBIN = "/opt/homebrew/opt/postgresql@15/bin"
PG = os.path.join(W, "pg"); ROOT = os.path.join(W, "tree"); CWD = os.path.join(W, "cwd")
os.makedirs(CWD, exist_ok=True)
L = os.path.join(ROOT, "0_Brain/learnings"); os.makedirs(L, exist_ok=True)
os.makedirs(os.path.join(ROOT, "0_Brain/daily"), exist_ok=True)
P = CWD
def w(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(s if isinstance(s, bytes) else s.encode("utf-8"))
names = [
 "2026-04-01_'; DROP SCHEMA brain CASCADE; --.md",
 "2026-04-02_\\.\ninjected line after a newline in the NAME.md",
 "2026-04-03_$$; select pg_sleep(1); $$.md",
 "2026-04-04_\\copy brain.files to program 'touch %s_PWNED_n4'.md" % "x",
 "2026-04-05_\\! touch PWNED_n5.md",
 "2026-04-06_-leading-dash --all --kind.md",
 "2026-04-07_\ttab\\N\\t.md",
 "2026-04-08_:'q' :\"kind\" :lim.md",
 "2026-04-09_`touch PWNED_n9`$(touch PWNED_n9b).md",
 "2026-04-10_\x1b[2J\x1b[31mANSI.md",
]
rows = ["# h\n"]
for i, n in enumerate(names):
    w(os.path.join(L, n), "---\ntier: W\n---\n# heading \\. $$ '; drop schema brain cascade; -- %d\n\nzinjname%02d body\n\\.\n\\N\nCOPY brain.files FROM PROGRAM 'touch %s/PWNED_body%d';\n\\! touch %s/PWNED_bang%d\n" % (i, i, P, i, P, i))
    rows.append("\t".join([n.replace("\n", " "), "live", "all", "fam\\", "pane", "-", "rule \\. \\N $$ '); drop schema brain cascade; -- zinjrule%02d" % i]) + "\n")
w(os.path.join(L, "2026-04-20_lone-terminator.md"), "---\ntier: W\n---\n# t\n\nzloneterm before\n\\.\nzloneafter after the terminator line\n")
rows.append("2026-04-20_lone-terminator.md\tlive\tall\tf\tpane,\\.\t-\t\\.\n")
w(os.path.join(L, "_rules_index.tsv"), "".join(rows))
w(os.path.join(L, "_ledger.md"), "| date | x |\n|---|---|\n| 2026-04-01 | **\\.** zinjledger '; drop schema brain cascade; -- \\N \\\\ $$ |\n| 2026-04-02 | \\. |\n")
w(os.path.join(ROOT, "0_Brain/daily/2026-04-01.md"), "# d\n\n## S \\.\n- 06:19 zinjdaily \\. \\N ' \" $$ \\copy x to program 'touch %s/PWNED_daily'\n\\.\n" % P)
w(os.path.join(ROOT, "CLAUDE.md"), "# R \\.\n\n1. **\\.** zinjrulesfile '; drop schema brain cascade; --\n\\.\n2. \\N\n")

def tool(*args):
    env = dict(os.environ, BRAINDB_ROOT=ROOT, BRAINDB_PGDATA=PG, BRAINDB_SOCKDIR=SOCK); env.pop("WED_AGENT", None)
    r = subprocess.run(["/bin/bash", TOOL] + list(args), cwd=CWD, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode("utf-8", "replace")
def psql(sql):
    r = subprocess.run([PGBIN + "/psql", "-X", "-At", "-h", SOCK, "-d", "braindb", "-c", sql], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.stdout.decode().strip()
def state():
    return psql("select (select count(*) from brain.files)||'/'||(select count(*) from brain.chunks)||'/'||(select count(*) from brain.rules)||'/'||(select count(*) from pg_tables where schemaname='brain')||'/'||(select count(*) from pg_database)||'/'||(select count(*) from pg_roles where rolcanlogin)||'/'||(select count(*) from pg_proc where pronamespace = 'public'::regnamespace)")
rc, o = tool("rebuild")
print("rebuild rc=%d ; last: %s" % (rc, o.strip().split("\n")[-1]))
open(os.path.join(W, "rebuild.out"), "w").write(o)
print("files indexed: %s ; lessons with payload names stored verbatim: %s of %d" % (psql("select count(*) from brain.files"),
      psql("select count(*) from brain.lessons where file like '2026-04-%'"), len(names) + 1))
print("the text AFTER a lone '\\.' line is in the index (zloneafter): %s ; ledger payload row: %s ; daily payload row: %s ; rules-file payload row: %s ; rule lines carrying payloads: %s"
      % (psql("select count(*) from brain.chunks where body like '%zloneafter%'"), psql("select count(*) from brain.chunks where body like '%zinjledger%'"),
         psql("select count(*) from brain.chunks where body like '%zinjdaily%'"), psql("select count(*) from brain.chunks where body like '%zinjrulesfile%'"),
         psql("select count(*) from brain.rules where rule like '%zinjrule%'")))
before = state(); print("state before (files/chunks/rules/tables/databases/login-roles/public functions):", before)
payloads = [
 ["search", "$$; drop schema brain cascade; $$"],
 ["search", "\\\\copy brain.files to program 'touch %s/PWNED_s1'" % P],
 ["search", "x\n\\! touch %s/PWNED_s2\n" % P],
 ["search", "x' || (select pg_sleep(0)) || '"],
 ["search", "\\g |touch %s/PWNED_s3" % P],
 ["search", "\\o %s/PWNED_s4" % P],
 ["search", "\\set q `touch %s/PWNED_s5`" % P],
 ["search", ":'kind'); drop schema brain cascade; --"],
 ["search", "\\gexec"],
 ["search", "x", "--kind", "lesson'; drop schema brain cascade; --"],
 ["search", "x", "--limit", "1; drop schema brain cascade"],
 ["search", "x", "--limit", "0"],
 ["search", "x", "--limit", "201"],
 ["search", "--", "--all", "-x", "--kind"],
 ["search", "-x"],
 ["search", "--kind", "lesson", "--all", "x"],
 ["search", "'"],
 ["search", "\\"],
 ["search", "\\."],
 ["search", "a" * 5000 + " " + " ".join("w%d" % i for i in range(3000))],
 ["search", "zinjname03 \x00"] if False else ["search", "zinjname03 \u0000".replace("\u0000", "")],
 ["search", "\ufeff\u200bzinjname04"],
 ["at", "pane; drop schema brain cascade"],
 ["at", "-pane"],
 ["at", "--top"],
 ["at", "pane", "--top", "1; drop schema brain cascade"],
 ["at", "pane", "--top", "-5"],
 ["at", "\\."],
 ["at", "pane\\"],
 ["at", "$$"],
]
envp = [("BRAINDB_TOPK", "4; drop schema brain cascade"), ("BRAINDB_TOPK", "0"), ("BRAINDB_PORT", "5432; drop"), ]
for p in payloads:
    rc, out = tool(*p)
    lines = [l for l in out.strip().split("\n") if l.strip()]
    print("rc=%d args=%r" % (rc, [a[:70] for a in p]))
    for l in lines[-1:]:
        print("      | " + l[:170])
    if "Traceback" in out: print("      | TRACEBACK")
for k, v in envp:
    os.environ[k] = v; rc, out = tool("search", "zinjname03"); del os.environ[k]
    print("rc=%d env %s=%r : %s" % (rc, k, v, (out.strip().split("\n") or [""])[-1][:150]))
after = state(); print("state after:", after, "UNCHANGED" if after == before else "CHANGED")
rc, out = tool("search", "zinjname03"); print("positive control, search zinjname03: rc=%d ; %s" % (rc, [l for l in out.split("\n") if "2026-04-" in l][:1]))
rc, out = tool("check"); print("check rc=%d: %s" % (rc, out.strip().split("\n")[0][:120]))
hits = []
for d, _, fs in os.walk(W):
    if d.startswith(PG): continue
    hits += [os.path.join(d, f) for f in fs if "PWNED" in f.upper() and not d.startswith(L)]
print("PWNED files created outside the planted lesson names:", hits, "| control: this walk does see files (rebuild.out present: %s)" % os.path.exists(os.path.join(W, "rebuild.out")))
print("files in cwd:", os.listdir(CWD))
rc, out = tool("stop"); print(out.strip().split("\n")[-1][:80])
