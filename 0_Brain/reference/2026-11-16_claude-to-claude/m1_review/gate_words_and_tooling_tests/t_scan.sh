#!/bin/bash
# scan_bytes.py base vs head: planted controls. Own planted files only.
W=/private/tmp/claude-501/qwt/scan_t; mkdir -p $W/sub $W/real
S=/private/tmp/claude-501/qwt/sbh2/spikes/U-B1-hook-allow-silent         # head spike folder
mkdir -p $W/base; cp $S/* $W/base/ 2>/dev/null; cp /private/tmp/claude-501/qwt/scan_bytes_base.py $W/base/scan_bytes.py   # base scan next to head redact.py
SECRET='planted.person@corp.example sk-ant-ABCDEFGH98765432 req_011ZZZZZZZZZ 9f1c2d3e-aaaa-4bbb-8ccc-0123456789ab'
printf '%s\n' "$SECRET" > $W/plain.txt
printf '%s\n' "$SECRET" > $W/sub/redact.py          # same BASENAME as the spike's own, but not it
printf 'x = "x@example.org"  # synthetic quoted\n' > $W/sub/scan_bytes.py   # basename match, only a synthetic literal
printf 'a x@example.org b\n' > $W/unquoted.txt       # synthetic literal bare, not an own file
printf 'junk "x@example.org"planted2@corp.example\n' > $W/sub/adj.py
printf 'no secret here\n' > $W/clean.txt
for v in base head; do
  D=$([ $v = base ] && echo $W/base || echo $S)
  echo "===== $v"
  for f in plain.txt sub/redact.py sub/scan_bytes.py unquoted.txt sub/adj.py clean.txt; do
    printf '%-18s ' $f; python3 -B -I $D/scan_bytes.py --control $W/$f 2>&1 | head -1 | cut -c1-200; done
done
