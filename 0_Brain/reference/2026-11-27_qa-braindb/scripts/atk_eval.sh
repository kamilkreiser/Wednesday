#!/bin/bash
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
A="$(cat "$S/atk/LAST")"; tag="${1:-base}"
/opt/homebrew/opt/postgresql@15/bin/pg_dump --data-only --schema=brain -h /tmp/qa-bdb-501 -d braindb > "$A/dump-$tag.sql" || echo "pg_dump failed"
echo "dump lines: $(wc -l < "$A/dump-$tag.sql" | tr -d ' ')   (control) 'xneighbour01' count: $(/usr/bin/grep -i -F -c xneighbour01 "$A/dump-$tag.sql")   builder canaries 'xcanary' count: $(/usr/bin/grep -i -F -c xcanary "$A/dump-$tag.sql")"
python3 - "$A" "$tag" <<'PY'
import json, sys
A, tag = sys.argv[1], sys.argv[2]
d = open(A + "/dump-%s.sql" % tag, encoding="utf-8", errors="replace").read()
bad = 0
for tok, want, what in json.load(open(A + "/expect.json")):
    n = d.count(tok)
    got = "present" if n else "absent"
    v = "ok  " if got == want else "LEAK" if want == "absent" else "MISS"
    if got != want: bad += 1
    print("%s %-13s want %-7s got %-7s (%d)  %s" % (v, tok, want, got, n, what))
print("unexpected: %d" % bad)
PY
echo "---- PWNED files anywhere under the run dir (want none); control: expect.json is found by the same find"
find "$A" -maxdepth 2 \( -iname 'PWNED*' -o -name expect.json \) -not -path '*/pg/*' | sed "s|$A/||"
find "$A/tree" -iname 'PWNED*' | head
