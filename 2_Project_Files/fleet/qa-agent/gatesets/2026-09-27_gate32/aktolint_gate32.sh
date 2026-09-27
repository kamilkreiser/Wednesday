#!/bin/bash
# aktolint_gate32.sh <scratchpad> — the drafter's MEASUREMENT of #1308's akto lint (systemTest/akto `npm run lint` = tsc -p tsconfig.json --noEmit &&
# eslint . && stylelint), at THREE trees, each exported by `git archive` from the scratch clone (a READ of the object store) into a fresh workdir under
# <scratchpad>/g32_aktolint_<HHMMSS>/, with node_modules a SYMLINK to the checkout's systemTest/akto/node_modules (read-only use: require()):
#   HEAD   — #1308's head: the claim is rc 0;
#   BASE   — the merge-base: rc 0 expected (the package lints clean without the PR);
#   GOLDEN — #1308's head with the new test file REPLACED by the golden's test section (the model's own output, before the ruled 16-line departure):
#            the CONTROL — it must be rc != 0 with jsdoc/prettier errors naming THAT file (the instrument can fail, and fails for the reason disclosed).
# The golden test bytes are read ONCE; their sha256 is printed and re-asserted on the file written (verified bytes == used bytes).
# Writes: aktolint_1.out + aktolint_gate32.json beside this script (via the caller's redirect / python), the workdirs in the scratchpad. Nothing in the checkout.
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: aktolint_gate32.sh <scratchpad>"; exit 9;; esac
CL="$SP/g32_sp/clone.git"; [ -d "$CL" ] || { echo "no scratch clone $CL (run predict_gate32.py first)"; exit 9; }
NM='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/systemTest/akto/node_modules'
HEAD_SHA="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1308"]["head"])' "$GS/pins_gate32.json")"
MB="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1308"]["develop_merge_base"])' "$GS/pins_gate32.json")"
GOLD='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1108/KS-1108.recounted-at-94c9c7aa.diff'
TF='tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts'
W="$SP/g32_aktolint_$(date -u +%H%M%S)"; mkdir -p "$W"
echo "aktolint_gate32 $(date -u +%FT%TZ) | node $(node --version) | npm $(npm --version) | head $HEAD_SHA | merge-base $MB | node_modules -> $NM | workdir $W"
arm() { # $1 name $2 commit
  local d="$W/$1"; mkdir -p "$d"
  git --git-dir "$CL" archive "$2" systemTest/akto | tar -x -C "$d" || { echo "ARM $1: archive failed"; return 1; }
  ln -s "$NM" "$d/systemTest/akto/node_modules"
}
arm HEAD "$HEAD_SHA"; arm BASE "$MB"; arm GOLDEN "$HEAD_SHA"
python3 - "$GOLD" "$W/GOLDEN/systemTest/akto/$TF" "$W/HEAD/systemTest/akto/$TF" <<'PY'
import hashlib, re, sys
g = open(sys.argv[1], 'rb').read(); gs = hashlib.sha256(g).hexdigest()
t = g.decode('utf-8'); i = t.index('+++ b/systemTest/akto/tests/unit/config/ks1108'); sec = t[i:].split('\n')[2:]
body = '\n'.join(l[1:] for l in sec if l and l[0] == '+') + '\n'
open(sys.argv[2], 'w', encoding='utf-8').write(body)
used = hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest()
print('GOLDEN test bytes: the golden diff read once (%d B, sha256 %s); re-read at the point of use %s -> %s; test body written %d lines, sha256 %s; HEAD test sha256 %s' % (
    len(g), gs[:16], used[:16], 'SAME' if used == gs else 'DIFFERENT', body.count('\n'), hashlib.sha256(body.encode()).hexdigest()[:16], hashlib.sha256(open(sys.argv[3], 'rb').read()).hexdigest()[:16]))
PY
for a in HEAD BASE GOLDEN; do
  ( cd "$W/$a/systemTest/akto" && /usr/bin/env npm run lint > "$W/$a.lint.out" 2> "$W/$a.lint.err"; echo $? > "$W/$a.lint.rc" )
  echo "== $a: npm run lint rc $(cat "$W/$a.lint.rc") | stdout $(wc -l < "$W/$a.lint.out" | tr -d ' ') lines, stderr $(wc -l < "$W/$a.lint.err" | tr -d ' ') lines | error lines naming the ks1108 cell: $(/usr/bin/grep -c -E '^\s+[0-9]+:[0-9]+\s+error' "$W/$a.lint.out") | problems line: $(/usr/bin/grep -E '✖ [0-9]+ problem' "$W/$a.lint.out" || echo none)"
  /usr/bin/grep -E '^\s+[0-9]+:[0-9]+\s+(error|warning)' "$W/$a.lint.out" | sed 's/  */ /g' | head -8 | sed 's/^/    /'
  tail -3 "$W/$a.lint.err" | sed 's/^/    stderr: /'
done
python3 - "$W" "$GS/aktolint_gate32.json" <<'PY'
import json, re, sys
W = sys.argv[1]; r = {}
for a in ('HEAD', 'BASE', 'GOLDEN'):
    o = open('%s/%s.lint.out' % (W, a)).read(); rc = int(open('%s/%s.lint.rc' % (W, a)).read().strip())
    errs = re.findall(r'^\s+\d+:\d+\s+error\s+.*?\s{2,}(\S+)\s*$', o, re.M)
    r[a] = {'rc': rc, 'errors': len(re.findall(r'^\s+\d+:\d+\s+error', o, re.M)), 'rules': sorted(set(errs)), 'names_cell': 'ks1108-secrets-parse-failure' in o}
ok = r['HEAD']['rc'] == 0 and r['BASE']['rc'] == 0 and r['GOLDEN']['rc'] != 0 and r['GOLDEN']['names_cell'] and all(x.startswith(('jsdoc/', 'prettier/')) for x in r['GOLDEN']['rules'])
r['summary'] = 'npm run lint rc %d at #1308 HEAD (%d errors), rc %d at the merge-base; CONTROL: the golden (model) test file in place of the head\'s reds rc %d with %d error(s), rules %s, naming the ks1108 cell: %s -> the instrument can fail, and fails ONLY on the jsdoc/prettier rules the ruled departure fixes: %s' % (
    r['HEAD']['rc'], r['HEAD']['errors'], r['BASE']['rc'], r['GOLDEN']['rc'], r['GOLDEN']['errors'], r['GOLDEN']['rules'], r['GOLDEN']['names_cell'], ok)
r['ok'] = ok; r['workdir'] = W
json.dump(r, open(sys.argv[2], 'w'), indent=1)
print('SUMMARY ' + r['summary'])
sys.exit(0 if ok else 1)
PY
