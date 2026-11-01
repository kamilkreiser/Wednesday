#!/bin/bash
# Gate 73 Q7: docs-fragments.mjs check, clean and with planted defects (untracked files, removed after each run).
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888
R=$G/repo; X="$R/Blockchain/Dev/scripts/docs-fragments.mjs"; FR="$R/Projects Documents/fragments"
[ "$(git -C $R rev-parse --show-toplevel)" = "$R" ] || exit 98
chk() { node "$X" check > "$G/logs/$1.log" 2>&1; echo "rc=$?" >> "$G/logs/$1.log"; echo "$1: $(tail -2 "$G/logs/$1.log" | tr '\n' ' ')"; }
chk fragments_check_clean
# P1: cheat fragment with prose outside any table
P1="$FR/cheat/KS-1868-gate73-planted-prose.html"
printf '<h2>gate73 planted</h2>\nloose prose outside a table\n' > "$P1"; chk fragments_check_planted_cheat_prose; rm -f "$P1"
# P2: flow fragment with a literal section number instead of the <!--n--> token
P2="$FR/flow/KS-1868-gate73-planted-literal.html"
printf '<h2>999. gate73 planted</h2>\n<table class="pmatrix"><tr><td>x</td></tr></table>\n' > "$P2"; chk fragments_check_planted_flow_literal; rm -f "$P2"
# P3: the PR's own flow fragment with an unbalanced tag (copy edited in place, restored by sha256)
F="$FR/flow/KS-1868-shared-audit-logger-unreadable-thrown-value.html"
S0=$(shasum -a 256 "$F" | cut -d' ' -f1); cp "$F" "$G/logs/.flow_frag.bak"
printf '<table class="pmatrix"><tr><td>unclosed\n' >> "$F"; chk fragments_check_planted_pr_flow_unbalanced
cp "$G/logs/.flow_frag.bak" "$F"; rm -f "$G/logs/.flow_frag.bak"
[ "$(shasum -a 256 "$F" | cut -d' ' -f1)" = "$S0" ] && echo "PR flow fragment restored sha256 OK" || echo "RESTORE FAILED"
chk fragments_check_clean2
git -C $R status --short; echo "status above (empty = clean)"
