#!/bin/bash
# drafter_probe1285.sh <scratchpad> — PREDICTIONS for gate27 (never evidence): #1285's base-image-watch.sh --self-test run from `git archive`
# extracts of the merge-base 00de57baeb40 and the head c7779a33 (whole tree: the self-test reads deployment/ and the Dockerfiles), under
# /bin/bash 3.2 with a `docker` SHIM first on PATH that exits 97 and logs every call (the self-test must call it ZERO times). Two red arms in
# COPIES: T = the merge-base + the test hunk ALONE (hunk 2 of 3, applied by `patch`); C = the head with the producer's future arm replaced by
# the old clamp `max(age, 0)`. Counts are of INDENTED result lines (`^\s+PASS` / `^\s+FAIL`) — the anchored `^PASS` count is printed as the
# seat's control (it reads 0). Writes only under <scratchpad>/g27_probe1285/.
set -u
SP="$1"; CL="$SP/g27_sp/clone.git"; W="$SP/g27_probe1285_$(date -u +%H%M%S)"; F=Blockchain/Dev/scripts/base-image-watch.sh
MB=00de57baeb405d0081fe8b6f192bd40d35acef61; H=c7779a33031813cac9dab62abd0cb8fd9d73f2f9
mkdir -p "$W/shim" "$W/base" "$W/head" "$W/armT" "$W/armC"
printf '#!/bin/sh\necho "GATE27 SHIM: docker was called: $*" >&2\nexit 97\n' > "$W/shim/docker"; chmod +x "$W/shim/docker"
git --git-dir "$CL" archive "$MB" | tar -x -C "$W/base"; git --git-dir "$CL" archive "$H" | tar -x -C "$W/head"
echo "work $W | blobs: base $(git --git-dir "$CL" hash-object "$W/base/$F") head $(git --git-dir "$CL" hash-object "$W/head/$F") (== ls-tree: $(git --git-dir "$CL" rev-parse "$H:$F"))"
git --git-dir "$CL" diff "$MB" "$H" -- "$F" > "$W/full.diff"
python3 - "$W/full.diff" "$W/testhunk.diff" <<'PY'
import sys, re
t = open(sys.argv[1]).read(); parts = re.split(r'(?m)^(?=@@ )', t)
print('hunks %d: %s' % (len(parts) - 1, [h.splitlines()[0][:22] for h in parts[1:]]))
open(sys.argv[2], 'w').write(parts[0] + parts[2])
PY
cp -R "$W/base/." "$W/armT/"; patch -s -p1 -d "$W/armT" < "$W/testhunk.diff"; echo "armT: the test hunk applied to the merge-base rc $?"
cp -R "$W/head/." "$W/armC/"
python3 - "$W/armC/$F" <<'PY'
import sys
p = sys.argv[1]; t = open(p).read(); o = '    if age < 0:\n        print("future")\n    else:\n        print(f"{age:.2f}")\n'
assert t.count(o) == 1, 'the tamper anchor is absent: %d' % t.count(o)
open(p, 'w').write(t.replace(o, '    print(f"{max(age, 0):.2f}")\n')); print('armC: the producer clamp restored (anchor found once)')
PY
for v in base head armT armC; do
  PATH="$W/shim:/usr/bin:/bin:/opt/homebrew/bin" /bin/bash "$W/$v/$F" --self-test > "$W/$v.out" 2> "$W/$v.err"; rc=$?
  echo "$v: rc $rc | PASS $(/usr/bin/grep -c -E '^[[:space:]]+PASS' "$W/$v.out") FAIL $(/usr/bin/grep -c -E '^[[:space:]]+FAIL' "$W/$v.out") | anchored ^PASS $(/usr/bin/grep -c '^PASS' "$W/$v.out") | docker shim calls $(/usr/bin/grep -i -c 'gate27 shim' "$W/$v.err") | last: $(tail -n 1 "$W/$v.out")"
  /usr/bin/grep -E '^[[:space:]]+FAIL' "$W/$v.out" | sed 's/^/      /'
done
echo "shim control: the shim's own marker is findable by the same grep: $(/usr/bin/grep -i -c 'gate27 shim' "$W/shim/docker")"
