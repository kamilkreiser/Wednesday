#!/bin/bash
# LINEAGE (Seat X 7th, 2026-11-06): copy of Seat V 24th's overlap_gate.sh (sha256 6573b2bf...) by tools/rekey_push_x7.py; the body holds no seat token outside earlier LINEAGE lines. Logic unchanged.
# LINEAGE (Seat V 24th, 2026-11-06): re-keyed from Seat V 23rd's overlap_gate.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v24.py); gate logic unchanged; two path-value deviations declared in evidence/declared_changes_push.md.
# LINEAGE (Seat V 23rd, 2026-11-05): re-keyed from Seat V 22nd's overlap_gate.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v23.py). Logic unchanged.
# LINEAGE (Seat V 22nd, 2026-11-05): re-keyed from Seat V 21st's overlap_gate.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v22.py). Logic unchanged.
# LINEAGE (Seat V 21st, 2026-11-05): copy of Seat V 20th's overlap_gate.sh; the body holds no seat token outside earlier LINEAGE lines. Logic unchanged.
# LINEAGE (Seat V 20th, 2026-11-05): derived from Seat W 28th's overlap_gate.sh by tools/rekey_push_v20.py (counted named replacements on non-LINEAGE lines; no logic line changed).
# LINEAGE (Seat W 28th, 2026-11-05): copy of Seat F 31st's overlap_gate.sh; the only change is this line (the body holds no seat token outside earlier LINEAGE lines; read whole at boot).
# LINEAGE (Seat F 31st, 2026-11-05): re-keyed copy of Seat F 29th's overlap_gate.sh by named replacements (counts: {}); logic unchanged.
# LINEAGE (Seat F 29th, 2026-11-04): re-keyed from Seat R 81st's overlap_gate.sh by NAMED edits (each replacement count-checked, listed in evidence/rekey_push.out); logic unchanged.
# LINEAGE (Seat R 81st, 2026-11-04): re-keyed from Seat R 80th's overlap_gate.sh by NAMED edits read one by one (tools/rekey_named_r81.py, diff in evidence/rekey/overlap_gate.diff): NOTHING in the body (the file holds no seat token outside old LINEAGE lines); only this lineage line is added. Logic unchanged.
# LINEAGE (Seat R 80th, 2026-11-03): re-keyed from Seat R 79th's overlap_gate.sh by NAMED edits read one by one (tools/rekey_named_r80.py, diff in evidence/rekey/overlap_gate.diff): no edit: the file holds no seat token outside old LINEAGE lines (the driver finds it next to itself); only this lineage line is added. Logic unchanged.
# LINEAGE (Seat R 79th, 2026-11-03): copy of Seat R 78th's overlap_gate.sh with the r78 tokens on matching lines changed to r79 by rekey_r79.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 78th, 2026-11-03): copy of Seat R 77th's overlap_gate.sh with the r77 tokens on matching lines changed to r78 by rekey_r78.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 77th, 2026-11-03): copy of Seat R 76th's overlap_gate.sh with the r76 tokens on matching lines changed to r77 by rekey_r77.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 76th, 2026-11-03): copy of Seat R 75th's overlap_gate.sh (itself re-keyed from Seat W 17th's) with the r75 tokens on matching lines changed to r76 by rekey_r76.py (a named-file pass, the diff read line by line, no logic line changed). Older LINEAGE lines below were written by earlier seats and carry the new seat token only because of this pass.
# LINEAGE (Seat R 76th, 2026-11-03): re-keyed copy of Seat W 17th's overlap_gate.sh by READING it: only the seat token, the env-var prefix W17_ -> R76_, tool names, paths and the planted-control path changed; every gate is unchanged. Remaining mentions of W 17th are historical comments, listed in evidence/rekey_batch3.out.
# Wednesday's condition on the KS-1458 baseline grant (ANSWER 13:04:46Z): re-run the open-PR intersection
# immediately before the push; if ANY open PR touches one of the paths, STOP.
# usage: overlap_gate.sh PATHSFILE      PATHSFILE = one repo-relative path per line (no defaults; nothing inherited)
# exit 0 = no open PR touches any listed path (prints the PR count and the cap check)
# exit 1 = at least one open PR touches a listed path (prints PR number, path)
# exit 2 = the gate cannot say (gh failed, empty list, unreadable token, a PR at gh's 100-file cap)
# Optional env OVL_IGNORE_PRS="1796": my own PR numbers, excluded by name and printed in the verdict.
# Optional env OVL_IGNORE_HEADS="<branch> <branch>" (W 13th): my own PRs by head branch, for a driver started before the PR has a number. Same semantics, printed too.
# W 13th port (2026-10-31 04:5xZ) of an earlier seat's fix (W 17th: the seat token in this historical line was rewritten by successive re-keys; the originator is not recoverable from this file), as Wednesday's ALL SEATS mail 04:54:58Z directs: a PR that `gh pr list` caps at 100 files is
# no longer an automatic "cannot say": its FULL list is read from REST pulls/N/files (100 per page, up to 30 pages) and judged like any other; gh's 100
# names must all be in the REST list (consistency control); a PR still unfinished at 30 pages is "cannot say". One W 13th change against R's: a REST
# read that RAISES (network, HTTP error) makes that PR unresolved, so the gate says "cannot say" (rc 2) with the reason, never a traceback (rc 1 = OVERLAP).
# The project's own GH_TOKEN (kksecura) is read from 4_Credentials/.env and handed to ONE gh process; it is never printed.
[ $# -eq 1 ] && [ -f "$1" ] || { echo "usage: overlap_gate.sh PATHSFILE" >&2; exit 2; }
ENVF=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env
TOK=$(grep -E '^GH_TOKEN=' "$ENVF" | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")
[ -n "$TOK" ] || { echo "no GH_TOKEN in the project env"; exit 2; }
OUT=$(mktemp "${TMPDIR:-/tmp}/ovl.XXXXXX") || exit 2
GH_TOKEN="$TOK" gh pr list --repo Secuura/Distributed_Secuura --state open --limit 200 --json number,headRefName,files > "$OUT" 2> "$OUT.err"
grc=$?
if [ "$grc" -ne 0 ]; then echo "gh pr list failed rc=$grc: $(head -c 200 "$OUT.err")"; rm -f "$OUT" "$OUT.err"; exit 2; fi
GH_TOKEN="$TOK" python3 -I - "$OUT" "$1" <<'EOF'
import json, os, sys
prs = json.load(open(sys.argv[1]))
# OVL_IGNORE_PRS = space-separated PR numbers that are MY OWN (named, printed, never silent); default none
ignore = set(os.environ.get('OVL_IGNORE_PRS', '').split())
heads = set(os.environ.get('OVL_IGNORE_HEADS', '').split())
mine = lambda p: str(p['number']) in ignore or p.get('headRefName') in heads
# Exact names only (set membership: never a prefix or a pattern). Printed on every run; an empty list prints nothing, so the output is byte-identical to the unknobbed gate.
named = (' | ignore-heads (exact, mine): %s' % sorted(heads)) if heads else ''
ignored = [p['number'] for p in prs if mine(p)]
prs = [p for p in prs if not mine(p)]
paths = [l.rstrip("\n") for l in open(sys.argv[2]) if l.strip()]
if not prs or not paths:
    print("cannot say: %d open PRs listed, %d paths" % (len(prs), len(paths)) + named); sys.exit(2)
capped = [p["number"] for p in prs if len(p.get("files") or []) >= 100]
import urllib.request
def full_files(n):
    names, pg = [], 1
    while pg <= 30:
        rq = urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d/files?per_page=100&page=%d" % (n, pg),
                                    headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
        chunk = json.load(urllib.request.urlopen(rq, timeout=60))
        names += [f["filename"] for f in chunk]
        if len(chunk) < 100: return names, True
        pg += 1
    return names, False
expanded, unresolved, why = {}, [], []
for p in prs:
    if p["number"] in capped:
        try:
            names, complete = full_files(p["number"])
        except Exception as e:
            unresolved.append(p["number"]); why.append("PR %d REST read raised %s" % (p["number"], type(e).__name__)); continue
        gh100 = [f["path"] for f in p["files"]]
        if not complete or set(gh100) - set(names):
            unresolved.append(p["number"]); why.append("PR %d %s" % (p["number"], "unfinished at 30 pages" if not complete else "gh's names not all in the REST list")); continue
        expanded[p["number"]] = names
        p["files"] = [{"path": x} for x in names]
capped = unresolved
hits = [(p["number"], f["path"], p["headRefName"][:50]) for p in prs for f in (p.get("files") or []) if f["path"] in paths]
if hits:
    print("OVERLAP: %d open PR file(s) touch the paths: %s" % (len(hits), hits) + named); sys.exit(1)
if capped:
    print("cannot say: PR(s) %s list 100 files (gh's cap) and their full lists could not be read (%s)" % (capped, "; ".join(why)) + named); sys.exit(2)
print("no overlap: %d open PRs, none touches any of %d paths; PRs read past gh's 100-file cap via REST (number: files): %s; unresolved capped PRs: none; ignored (mine, named): %s" % (len(prs), len(paths), {k: len(v) for k, v in expanded.items()}, ignored) + named)
EOF
rc=$?
rm -f "$OUT" "$OUT.err"
exit $rc
