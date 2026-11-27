#!/usr/bin/env python3
"""qlib.py - shared helpers for the third checker's attacks on brain-db round 4b.
Runs the SCRATCH COPY of the tool only (never the lane's own copy, never the lane's cluster)."""
import os, subprocess, re, sys

S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/063b86e1-bf25-4ab6-9e57-b16c1f229efa/scratchpad/r4b"
TOOL = os.environ.get("QTOOL") or S + "/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh"   # QTOOL: another scratch copy (the name-test comparison)
PGBIN = "/opt/homebrew/opt/postgresql@15/bin"
L = "0_Brain/learnings/"


def clean_env(extra=None):
    e = dict((k, v) for k, v in os.environ.items() if not k.startswith("BRAINDB_") and k != "WED_AGENT" and not k.startswith("PG"))
    e.update(extra or {})
    return e


def tool(args, root, pgd, sock, scope=None, extra=None, toolpath=TOOL, timeout=600):
    e = dict(BRAINDB_ROOT=root, BRAINDB_PGDATA=pgd, BRAINDB_SOCKDIR=sock)
    if scope:
        e["BRAINDB_SCOPE"] = scope
    if os.environ.get("QPY"):
        e["BRAINDB_PYTHON"] = os.environ["QPY"]          # run the tool under another Python (3.9.6)
    e.update(extra or {})
    r = subprocess.run(["/bin/bash", toolpath] + list(args), env=clean_env(e), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


def dump(sock, port="5432"):
    r = subprocess.run([PGBIN + "/pg_dump", "--data-only", "--schema=brain", "-h", sock, "-p", port, "-d", "braindb"],
                       env=clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        return None, r.stderr.decode("utf-8", errors="replace")
    return r.stdout.decode("utf-8", errors="replace"), ""


def psql(sock, sql, db="braindb", port="5432"):
    r = subprocess.run([PGBIN + "/psql", "-X", "-At", "-h", sock, "-p", port, "-d", db, "-c", sql], env=clean_env(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.returncode, r.stdout.decode("utf-8", errors="replace").strip(), r.stderr.decode("utf-8", errors="replace").strip()


def left_out_from_report(out):
    """rebuild report -> {file name: clause}"""
    cl, res = None, {}
    for line in out.split("\n"):
        m = re.match(r"\s+clause \((\w)\) ", line)
        if m:
            cl = m.group(1)
            continue
        m = re.match(r"\s{11}(.+?)  \[(.*)\]$", line)
        if m and cl:
            res[m.group(1)] = (cl, m.group(2))
            continue
        if not line.startswith("     "):
            cl = None
    return res


def w(root, rel, data):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(data, bytes):
        with open(p, "wb") as f:
            f.write(data)
    else:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(data)
    return p


def row(key, seats="all", status="live", trig="drive", rule=None, fam="learning-loop"):
    return "\t".join([key, status, seats, fam, trig, "-", rule or "When testing: do the thing."])


FM = "---\ndate: 2027-01-01\ntype: correction\nstatus: live\ntier: W\n---\n"


def base_tree(root):
    """the non-lesson files of a minimal WEDNESDAY tree, plus one control lesson (token qzcontrol)"""
    w(root, "CLAUDE.md", "# Rules\n\n0. **First.** qzrulesfile lives here.\n")
    w(root, "0_Brain/CLAUDE.md", "# Brain\n\n## Folders\n\nqzbrainfile\n")
    w(root, "0_Brain/skills/ritual.md", "# ritual\n\nqzskill\n")
    w(root, L + "_ledger.md", "# Ledger\n\n| Date | What |\n|---|---|\n| 2027-01-01 | **qzledger thing** [[2027-01-01_q-control]] Rule: do it. | x |\n")
    w(root, L + "2027-01-01_q-control.md", FM + "\n# Control\n\nThe word is qzcontrol here.\n")
    return [row("2027-01-01_q-control.md", rule="When testing: qzcontrolrule do it.")]
