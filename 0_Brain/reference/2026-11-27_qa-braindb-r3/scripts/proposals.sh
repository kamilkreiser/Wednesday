#!/bin/bash
# proposals.sh - apply each proposed block to SCRATCH COPIES of the real targets, and run the two blocks in a stub
# harness under the real files' shell options, against scratch trees and a scratch socket directory.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3
REAL=/Volumes/DevMASTER/WEDNESDAY; PFC="$S/lanecopy/WEDNESDAY/2_Project_Files"; PROP="$PFC/brain-db/proposed/PROPOSALS.md"
W="$S/prop-$(date +%H%M%S)"; mkdir -p "$W" || exit 2
export BRAINDB_SOCKDIR=/tmp/qa3p     # never the seat's real socket directory
sh() { awk -v n="${1:-220}" '{print substr($0,1,n)}' | sed "s|$W/||g"; }
nprocs() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $1"; }
hr() { echo; echo "######## $1"; }
# the two blocks, cut from the proposal by their fences
awk '/^## 3\. /{s=1} s && /^```bash/{f=1; next} f && /^```/{exit} f' "$PROP" > "$W/doctor.block"
awk '/^## 4\. /{s=1} s && /^```bash/{f=1; next} f && /^```/{exit} f' "$PROP" > "$W/launcher.block"
echo "doctor block: $(wc -l < "$W/doctor.block" | tr -d ' ') lines ; launcher block: $(wc -l < "$W/launcher.block" | tr -d ' ') lines"

hr "D1 apply to scratch copies of the real files: does the anchor exist, does the result parse (bash 3.2 -n)?"
cp "$REAL/2_Project_Files/doctor.sh" "$W/doctor.sh"; cp "$REAL/Launch_Wednesday.command" "$W/Launch_Wednesday.command"; cp "$REAL/PORTABILITY.md" "$W/PORTABILITY.md"; cp "/Volumes/DevMASTER/!SYNC FILES/devnas.prf" "$W/devnas.prf"
python3 - "$W" <<'PY'
import sys, re
W = sys.argv[1]
d = open(W + "/doctor.sh").read(); blk = open(W + "/doctor.block").read()
anchor = 'else warn "postgresql@15 keg missing"'
i = d.find(anchor); print("doctor.sh: anchor (the postgresql@15 keg check) found %d time(s), at line %d" % (d.count(anchor), d[:i].count("\n") + 1))
j = d.find("\n", i) + 1; open(W + "/doctor.patched.sh", "w").write(d[:j] + "\n" + blk + d[j:])
l = open(W + "/Launch_Wednesday.command").read(); blk = open(W + "/launcher.block").read()
m = re.search(r'RULES_CARD="\$PROJECT_DIR.*?\n  rm -f /tmp/wednesday_rules_card\.\$\$\nfi\n', l, re.S)
print("launcher: rules-card block found: %s, ends at line %d ; line 29 is %r" % (bool(m), l[:m.end()].count("\n") if m else -1, l.split("\n")[28]))
open(W + "/Launch.patched.command", "w").write(l[:m.end()] + "\n" + blk + l[m.end():])
p = open(W + "/PORTABILITY.md").read()
print("PORTABILITY.md: '- **Machine-local:** `/opt/homebrew/opt/postgresql@15`' x%d ; '- **No service:** no `brew services` job' x%d ; last item heading: %s"
      % (p.count("- **Machine-local:** `/opt/homebrew/opt/postgresql@15`"), p.count("- **No service:** no `brew services` job"), re.findall(r"(?m)^## (\d+)\. ", p)[-1]))
f = open(W + "/devnas.prf").read().split("\n")
first = next(i for i, x in enumerate(f, 1) if x.startswith("ignore"))
print("devnas.prf: first ignore line is line %d: %r ; root lines: %s" % (first, f[first - 1], [x for x in f if x.startswith(("root", "path"))][:6]))
PY
/bin/bash -n "$W/doctor.patched.sh"; echo "bash -n doctor.patched.sh rc=$? ($(/bin/bash --version | head -1 | sh 60))"
/bin/bash -n "$W/Launch.patched.command"; echo "bash -n Launch.patched.command rc=$?"
echo "doctor.sh shell options: $(/usr/bin/grep -n -m1 -E '^set -' "$W/doctor.sh") ; launcher: $(/usr/bin/grep -n -m1 -E '^set -' "$W/Launch_Wednesday.command")"
echo "names the sync-ignore lines would also hide ANYWHERE under the synced roots (they are 'Name' patterns, not paths): existing matches outside this lane, depth <= 6:"
( find /Volumes/DevMASTER -maxdepth 6 \( -name .git -o -name node_modules \) -prune -o \( -name 'pgdata-*' -o -name '_probe_*' \) -print 2>/dev/null | /usr/bin/grep -v -F '/WEDNESDAY/2_Project_Files/brain-db/' | head -8 ) ; echo "(end of list; control: the same find sees this lane's own: $(find /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db -maxdepth 1 -name 'pgdata-*' | wc -l | tr -d ' ') entries)"

hr "D2 the blocks in a stub harness, on scratch trees (doctor under set -uo pipefail, launcher under set -u)"
mk() { # mk <tree dir> <content tree to copy or ''> <scope: wednesday|tuesday|none>
  mkdir -p "$1/2_Project_Files/fleet/cockpit" "$1/2_Project_Files/tools" "$1/2_Project_Files/brain-db/scope"
  [ -n "$2" ] && cp -R "$2/." "$1/"
  cp "$PFC/brain-db/braindb.sh" "$PFC/brain-db/braindb_index.py" "$PFC/brain-db/braindb_lock.py" "$1/2_Project_Files/brain-db/"; chmod +x "$1/2_Project_Files/brain-db/braindb.sh"
  cp "$PFC/fleet/cockpit/seat_resolve.sh" "$1/2_Project_Files/fleet/cockpit/"; cp "$PFC/tools/seat_note.sh" "$1/2_Project_Files/tools/"
  case "$3" in wednesday) cp "$PFC/brain-db/scope/wednesday.scope" "$1/2_Project_Files/brain-db/scope/" ;; tuesday) cp "$PFC/brain-db/proposed/scope/tuesday.scope" "$1/2_Project_Files/brain-db/scope/" ;; esac
}
python3 "$PFC/brain-db/tests/make_fixtures.py" "$W/fx" > /dev/null 2>&1
mk "$W/a/WEDNESDAY" "$S/realcopy/WEDNESDAY" wednesday
mk "$W/b/TUESDAY" "$W/fx" none
mk "$W/c/TUESDAY" "$W/fx" tuesday
mk "$W/d/FRIDAY" "$W/fx" none
mk "$W/e/WEDNESDAY-old" "$W/fx" wednesday
cat > "$W/doctor.harness" <<'H'
set -uo pipefail
QUIET=""; WARNS=0; HARD_FAIL=0
ok()   { [ "$QUIET" = "--quiet" ] || printf "  ✓ %s\n" "$1"; }
warn() { printf "  ⚠ %-38s %s\n" "$1" "${2:-}"; WARNS=$((WARNS+1)); }
PROJECT_DIR="$1"
H
cat "$W/doctor.block" >> "$W/doctor.harness"; echo 'echo "   [doctor continued; WARNS=$WARNS]"' >> "$W/doctor.harness"
cat > "$W/launcher.harness" <<'H'
set -u
PROJECT_DIR="$1"
H
cat "$W/launcher.block" >> "$W/launcher.harness"; echo 'echo "   [launcher continued]"' >> "$W/launcher.harness"
D() { /bin/bash "$W/doctor.harness" "$@" 2>&1 | sh 230; }
LA() { local t0; t0=$(date +%s); /bin/bash "$W/launcher.harness" "$@" 2>&1 | sh 230; echo "   (returned in $(( $(date +%s) - t0 )) s)"; }
A="$W/a/WEDNESDAY"; AB="$A/2_Project_Files/brain-db/braindb.sh"
echo "-- a. WEDNESDAY tree (copy of the real allowed files), first boot: no cluster yet"
env -u WED_AGENT /bin/bash -c "$(declare -f D sh); W='$W'; D '$A'"
env -u WED_AGENT /bin/bash -c "$(declare -f LA sh); W='$W'; LA '$A'"
echo "   servers for this tree after the launcher block: $(nprocs "$A/2_Project_Files/brain-db/pgdata-wednesday")  (the launcher block STARTS a server and creates the cluster with no human step)"
env -u WED_AGENT /bin/bash -c "$(declare -f D sh); W='$W'; D '$A'"
echo "-- a2. a file changes; doctor (starts nothing, rebuilds nothing), then the launcher block (rebuilds)"
echo "- 09:00 a new bullet" >> "$A/0_Brain/daily/2026-11-27.md"
env -u WED_AGENT /bin/bash -c "$(declare -f D sh); W='$W'; D '$A'"
env -u WED_AGENT /bin/bash -c "$(declare -f LA sh); W='$W'; LA '$A'"
echo "-- a3. WED_AGENT=wednesday exported (as a launcher does) and WED_AGENT=tuesday (Launch_Tuesday.command run from the wrong tree)"
WED_AGENT=wednesday /bin/bash -c "$(declare -f D sh); W='$W'; D '$A'"
WED_AGENT=tuesday /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$A'; LA '$A'"
echo "-- a4. server stopped: doctor must start nothing"
env -u WED_AGENT /bin/bash "$AB" stop 2>&1 | tail -1 | sh 60
env -u WED_AGENT /bin/bash -c "$(declare -f D sh); W='$W'; D '$A'"; echo "   servers after doctor: $(nprocs "$A/2_Project_Files/brain-db/pgdata-wednesday")"
echo "-- a5. a lesson with a broken tier line and a hard-linked skill appear; what does the launcher block SHOW of the fail-closed exclusions?"
printf -- '---\ntier: W\ntier: P-Datasec/X\n---\n# t\n\nx\n' > "$A/0_Brain/learnings/2026-11-27_broken-tier.md"
env -u WED_AGENT /bin/bash -c "$(declare -f LA sh); W='$W'; LA '$A'"
env -u WED_AGENT /bin/bash -c "$(declare -f D sh); W='$W'; D '$A'"
echo "   (the names of excluded lessons appear in neither line: they are only in the body of a rebuild report nobody is shown)"
env -u WED_AGENT /bin/bash "$AB" stop 2>&1 | tail -1 | sh 60
echo "-- b. TUESDAY tree with NO scope file, WED_AGENT=tuesday (as Launch_Tuesday.command exports)"
WED_AGENT=tuesday /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$W/b/TUESDAY'; LA '$W/b/TUESDAY'"
echo "   cluster directory created? $([ -e "$W/b/TUESDAY/2_Project_Files/brain-db/pgdata-tuesday" ] && echo YES || echo no) ; lock file created? $([ -e "$W/b/TUESDAY/2_Project_Files/brain-db/pgdata-tuesday.lock" ] && echo YES || echo no)"
echo "-- c. TUESDAY tree that adopted the proposed scope"
WED_AGENT=tuesday /bin/bash -c "$(declare -f D LA sh); W='$W'; LA '$W/c/TUESDAY'; D '$W/c/TUESDAY'"
WED_AGENT=tuesday /bin/bash "$W/c/TUESDAY/2_Project_Files/brain-db/braindb.sh" stop 2>&1 | tail -1 | sh 60
echo "-- d. FRIDAY tree, no scope, WED_AGENT unset"
env -u WED_AGENT /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$W/d/FRIDAY'; LA '$W/d/FRIDAY'"
echo "-- e. a tree folder that is not a seat name (a backup copy named WEDNESDAY-old)"
env -u WED_AGENT /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$W/e/WEDNESDAY-old'; LA '$W/e/WEDNESDAY-old'"
echo "-- f. python3 absent from PATH; braindb.sh not executable"
env -u WED_AGENT PATH=/usr/bin/nothing:/bin /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$A'; LA '$A'" 2>&1 | sh 200
chmod -x "$AB"; env -u WED_AGENT /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$A'; LA '$A'"; chmod +x "$AB"
echo "-- g. another cluster answering on this seat's socket directory when doctor runs (tree e's twin: a second WEDNESDAY tree)"
mk "$W/g/WEDNESDAY" "$W/fx" wednesday
env -u WED_AGENT /bin/bash "$W/g/WEDNESDAY/2_Project_Files/brain-db/braindb.sh" up > "$W/g-up.out" 2>&1; echo "   second WEDNESDAY tree up rc=$?"
env -u WED_AGENT /bin/bash -c "$(declare -f D LA sh); W='$W'; D '$A'; LA '$A'"
env -u WED_AGENT /bin/bash "$W/g/WEDNESDAY/2_Project_Files/brain-db/braindb.sh" stop 2>&1 | tail -1 | sh 60

hr "END"; echo "processes with a data directory under $W: $(nprocs "$W")"; date '+%Y-%m-%d %H:%M:%S %Z'
