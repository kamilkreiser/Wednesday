import subprocess, os, sys
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/chk"
A = open(S + "/atk/LAST").read().strip()
cwd = A + "/cwd"
env = dict(os.environ, BRAINDB_ROOT=A+"/tree", BRAINDB_PGDATA=A+"/pg", BRAINDB_SOCKDIR="/tmp/qa3c", WED_AGENT="wednesday")
B = ["/bin/bash", "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh"]
def psql(sql):
    r = subprocess.run(["/opt/homebrew/opt/postgresql@15/bin/psql","-X","-At","-h","/tmp/qa3c","-d","braindb","-c",sql], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.stdout.decode().strip()
def state():
    return psql("select (select count(*) from brain.files)||'/'||(select count(*) from brain.chunks)||'/'||(select count(*) from brain.rules)||'/'||(select count(*) from pg_tables where schemaname='brain')||'/'||(select count(*) from pg_database)||'/'||(select count(*) from pg_roles where rolcanlogin)")
before = state(); print("state before (files/chunks/rules/tables/databases/login-roles):", before)
P = cwd
payloads = [
 ["search", "'; drop schema brain cascade; --"],
 ["search", "x'); DROP TABLE brain.files; --"],
 ["search", "$(touch %s/PWNED_q1) `touch %s/PWNED_q2`" % (P, P)],
 ["search", "\\! touch %s/PWNED_q3" % P],
 ["search", "zebraword\n\\! touch %s/PWNED_q4\n" % P],
 ["search", "\\copy brain.files to program 'touch %s/PWNED_q5'" % P],
 ["search", ":'kind' :lim :q \\\\ \\' \\\" %s %%s"],
 ["search", "zebraword", "--kind", "lesson' or '1'='1"],
 ["search", "zebraword", "--kind", "lesson; drop schema brain cascade"],
 ["search", "zebraword", "--limit", "5; drop schema brain cascade"],
 ["search", "zebraword", "--limit", "5) ; drop schema brain cascade; --"],
 ["search", "zebraword", "--limit", "-1"],
 ["search", "\\set lim 1 \\\\ drop schema brain cascade;"],
 ["search", "a' | 'b' & !'c' <-> 'd':*  (e) \\"],
 ["search", "\x1f\x1e\x00x"] if False else ["search", "\x1f\x1e x zebraword"],
 ["at", "pane'; drop schema brain cascade; --"],
 ["at", "pane\n"],
 ["at", "pane\n\\! touch %s/PWNED_at1" % P],
 ["at", "$(touch PWNED_trig)"],
 ["at", "`touch PWNED_bt`"],
 ["at", "\\! touch PWNED_meta"],
 ["at", "pane", "--top", "1; drop schema brain cascade"],
 ["search", "zatkneigh72rule"],
 ["search", "zatkneigh95"],
 ["search", "zatkctl1"],
 ["search", "PWNED_head1 touch"],
]
for p in payloads:
    r = subprocess.run(B + p, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode("utf-8", "replace")
    last = [l for l in out.strip().split("\n") if l.strip()]
    print("rc=%d args=%r" % (r.returncode, p))
    for l in last[:1] + last[-2:]:
        print("      | " + l[:200])
after = state(); print("state after:", after, "UNCHANGED" if after == before else "CHANGED")
r = subprocess.run(B + ["check"], cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT); print("check rc=%d: %s" % (r.returncode, r.stdout.decode().strip().split("\n")[0][:200]))
hits = []
for d, _, fs in os.walk(A):
    if "/pg" in d: continue
    hits += [os.path.join(d, f) for f in fs if f.upper().startswith("PWNED")]
print("PWNED files created:", hits, "| control: files in cwd:", os.listdir(cwd), "| expect.json exists:", os.path.exists(A + "/expect.json"))
