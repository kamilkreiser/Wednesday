import subprocess, os, sys
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/chk"
A = open(S + "/atk/LAST").read().strip()
base = open("/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/scope/wednesday.scope", encoding="utf-8").read()
B = ["/bin/bash", "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh"]
tree = A + "/tree"
# extra plants for the scope attacks
def w(rel, text):
    p = os.path.join(tree, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(text)
w("4_Credentials/cred.md", "# c\n\nzscope_cred\n"); w("3_Access_Keys/k.md", "# k\n\nzscope_key\n")
w("0_Brain/dashboard/d.md", "# d\n\nzscope_dash\n"); w("0_Brain/reference/r/r.md", "# r\n\nzscope_ref\n")
w("0_Brain/tasks/NEXT-PICKUP-TUESDAY.md", "# p\n\nzscope_pickup\n"); w("0_Brain/tasks/WEEK-friday.md", "# p\n\nzscope_week\n")
w("../outside/out.md", "# o\n\nzscope_outside\n")
if not os.path.lexists(tree + "/0_Brain/esc"): os.symlink("../../outside", tree + "/0_Brain/esc")
if not os.path.lexists(tree + "/0_Brain/skills/nested"): os.makedirs(tree + "/0_Brain/skills/nested"); w("0_Brain/skills/nested/n.md", "# n\n\nzscope_nested\n")
SENS = ["zscope_cred","zscope_key","zscope_dash","zscope_ref","zscope_pickup","zscope_week","zscope_outside","zscope_nested","xcanary22","xcanary23","xcanary37","xcanary38","xcanary77","xcanary15","xcanary47"]
V = [
 ("control: base scope unchanged", base),
 ("trailing spaces on every line", "\n".join(l + "   " for l in base.split("\n"))),
 ("CRLF line endings", base.replace("\n", "\r\n")),
 ("leading BOM", "﻿" + base),
 ("tabs instead of spaces", base.replace("allow skill        ", "allow\tskill\t")),
 ("very long comment line (2 MB)", base + "# " + "x" * 2000000 + "\n"),
 ("very long allow line (300 KB pattern)", base + "allow skill 0_Brain/skills/" + "a" * 300000 + "*.md\n"),
 ("allow skill 0_Brain/skills/../../4_Credentials/*.md", None),
 ("allow skill 0_Brain/skills/..∕..∕4_Credentials/*.md", None),
 ("allow skill ./4_Credentials/*.md", None),
 ("allow skill 0_Brain/../4_Credentials/*.md", None),
 ("allow skill 4_CREDENTIALS/*.md", None),
 ("allow skill 4_Credentials /*.md", None),
 ("allow skill 4_Credentials​/*.md", None),
 ("allow skill 4_Credentials./*.md", None),
 ("allow skill 0_Brain/Dashboard/*.md", None),
 ("allow skill 0_Brain/dashboard//*.md", None),
 ("allow skill 0_Brain/esc/*.md", None),
 ("allow skill 0_Brain/skills/**/*.md", None),
 ("allow skill 0_Brain/skills/nested/../*.md", None),
 ("allow skill ~/*.md", None),
 ("allow skill $HOME/*.md", None),
 ("allow skill 0_Brain/tasks/*.md", None),
 ("allow skill 0_Brain/tasks/NEXT-PICKUP-TUESDAY.md", None),
 ("allow lesson 0_Brain/learnings/*.md", None),
 ("allow skill 0_Brain/learnings/_ledger_*.md", None),
 ("allow ledger 0_Brain/learnings/_ledger_*.md", None),
 ("allow daily 0_Brain/daily_tuesday/20*.md", None),
 ("allow skill 0_Brain/daily_tuesday/*.md", None),
 ("allow skill 2_Project_Files/tuesday/*.md", None),
 ("allow rules 4_Credentials.md", None),
 ("allow rules CLAUDE.md/../4_Credentials/cred.md", None),
 ("allow rules_index 4_Credentials/x.tsv", None),
 ("allow skill 0_Brain/skills/*.md\x00/../../4_Credentials/*.md", None),
 ("seat tuesday", None),
 ("own_clients datasec", None),
 ("deny_clients", None),
 ("deny_path", None),
 ("deny_seat_word tues*", None),
 ("include /etc/passwd", None),
]
def run(args, scope):
    env = dict(os.environ, BRAINDB_ROOT=tree, BRAINDB_PGDATA=A+"/pg", BRAINDB_SOCKDIR="/tmp/qa3c", BRAINDB_SCOPE=scope, WED_AGENT="wednesday")
    r = subprocess.run(B + args, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode("utf-8", "replace")
def dump():
    r = subprocess.run(["/opt/homebrew/opt/postgresql@15/bin/pg_dump","--data-only","--schema=brain","-h","/tmp/qa3c","-d","braindb"], stdout=subprocess.PIPE)
    return r.stdout.decode("utf-8", "replace")
for i, (name, text) in enumerate(V):
    if text is None: text = base + name + "\n"
    p = "%s/scope_%02d.scope" % (A, i)
    try:
        open(p, "w", encoding="utf-8", newline="").write(text)
    except Exception as e:
        print("%02d %-60s could not write the scope file: %s" % (i, name[:60], e)); continue
    rc, out = run(["rebuild"], p)
    d = dump()
    got = [t for t in SENS if t in d]
    tb = "TRACEBACK " if "Traceback" in out else ""
    first = next((l for l in out.split("\n") if l.startswith("braindb:")), "")
    tail = [l for l in out.strip().split("\n") if l][-1] if out.strip() else ""
    print("%02d rc=%d %s%-58s IN-INDEX=%s" % (i, rc, tb, name[:58].replace("\x00","<NUL>"), got or "-"))
    if rc != 0: print("       " + (first or tail)[:230])
    if tb: print("       " + tail[:230])
rc, out = run(["rebuild"], "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/scope/wednesday.scope")
print("restore base scope: rc=%d ; sensitive tokens now: %s ; control xneighbour01 present: %s" % (rc, [t for t in SENS if t in dump()] or "-", "xneighbour01" in dump()))
