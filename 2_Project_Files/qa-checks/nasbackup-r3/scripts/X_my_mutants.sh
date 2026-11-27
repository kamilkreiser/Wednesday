#!/bin/bash
# X_my_mutants.sh — the third checker's OWN mutants on round 3's code. Same mechanics as the lane's tests/mutants.sh (a scratch
# copy per mutant, exact-once replacement, the copy's whole suite). CAUGHT = the suite exits non-zero with ANY FAIL line (looser, in
# the seat's favour); the first FAIL line is printed so a catch by an unrelated test can be seen. None repeats a lane mutant.
#   X_my_mutants.sh <base under /private/tmp> <lane copy> [parallel]
set -u
BASE="$1"; LANE="$2"; PAR="${3:-2}"; TREE="$(cd -P "$LANE/../.." && pwd)"
case "$BASE" in /private/tmp/*) ;; *) echo "refused" >&2; exit 2 ;; esac
RUN="$BASE/xmut_$(date +%Y%m%d-%H%M%S)_$$"; mkdir -p "$RUN/results" || exit 2
PY=/opt/homebrew/bin/python3; ORDER=""
copy_lane() { local c="$RUN/$1/WEDNESDAY/2_Project_Files"
  mkdir -p "$c/nas-backup/tests" "$c/nas-backup/proposed" "$c/nas-backup/jobs" "$c/fleet/cockpit" "$c/tools" "$RUN/$1/base"
  cp "$LANE/nb_core.py" "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$c/nas-backup/"
  cp "$LANE/tests/run.sh" "$LANE/tests/scan_dry_lists.py" "$c/nas-backup/tests/"; cp "$LANE/proposed/doctor_nasbackup_block.sh" "$c/nas-backup/proposed/"
  cp "$LANE/jobs/nasbackup.plist.template" "$c/nas-backup/jobs/"
  cp "$TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$c/fleet/cockpit/"; cp "$TREE/2_Project_Files/tools/seat_note.sh" "$c/tools/"; }
one() { local name="$1" guar="$2"; shift 2
  local res="$RUN/results/$name.txt" copy="$RUN/$name/WEDNESDAY/2_Project_Files/nas-backup"; copy_lane "$name"
  if ! "$PY" -c 'import sys
p, pairs = sys.argv[1], sys.argv[2:]
s = open(p, encoding="utf-8").read()
for i in range(0, len(pairs), 2):
    n = s.count(pairs[i])
    if n != 1:
        sys.stderr.write("target found %d times (need 1): %r\n" % (n, pairs[i][:70])); sys.exit(1)
    s = s.replace(pairs[i], pairs[i + 1])
open(p, "w", encoding="utf-8").write(s)' "$copy/nb_core.py" "$@" 2> "$RUN/$name/apply.err"; then
    printf '  NOT-APPLIED %-44s %s\n' "$name" "$(head -1 "$RUN/$name/apply.err")" > "$res"; return; fi
  "$PY" -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())' "$copy/nb_core.py" 2> "$RUN/$name/syntax.err" || { printf '  NOT-APPLIED %-44s the mutated file does not parse\n' "$name" > "$res"; return; }
  bash "$copy/tests/run.sh" "$RUN/$name/base" > "$RUN/$name/out.txt" 2>&1; local rc=$?
  local nfail; nfail="$(/usr/bin/grep -c -F '  FAIL  ' "$RUN/$name/out.txt")"
  if [ "$rc" -ne 0 ] && [ "$nfail" -gt 0 ]; then printf '  CAUGHT      %-44s [%s] %3s FAIL, first: %s\n' "$name" "$guar" "$nfail" "$(/usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | head -1 | cut -c9-120)" > "$res"
  else printf '  SURVIVED    %-44s [%s] exit %s, %s FAIL, %s PASS (load: %s)\n' "$name" "$guar" "$rc" "$nfail" "$(/usr/bin/grep -c -F '  PASS  ' "$RUN/$name/out.txt")" "$(uptime | sed 's/.*averages: //')" > "$res"; fi; }
N=0; mutant() { ORDER="$ORDER $1"; one "$@" & N=$((N+1)); if [ $((N % PAR)) -eq 0 ]; then wait; fi; }
echo "third checker's mutants, under $RUN, $PAR at a time; $(date); $(uptime)"
mutant X01-deletion-checked-once-not-twice "deletion proof" '    for attempt in (1, 2):
        try:
            rs = os.stat(root)' '    for attempt in (2,):
        try:
            rs = os.stat(root)'
mutant X02-conf-ceiling-on-deletions-off "deletion limit" '            assert 0 <= c["max_deleted_files"] <= 100 and 0 <= c["max_deleted_fraction"] <= 0.01' '            assert True'
mutant X03-deleted-files-not-named-in-last-lines "deleted are named" '        for d in deleted_all[:600]:' '        for d in []:'
mutant X04-cap-ignored-in-the-full-read-back "read-back and the cap" '                            if time.time() >= deadline:
                                for r2 in rest[i:]:' '                            if False:
                                for r2 in rest[i:]:'
mutant X08-mount-not-rechecked-per-chunk "mount per chunk" '                        if not nas_is_smb_mounted(ctx):
                            raise Refused("REFUSED — %s is no longer mounted as a network share; stopped in set %s before "' '                        if False:
                            raise Refused("REFUSED — %s is no longer mounted as a network share; stopped in set %s before "'
mutant X09-mount-not-checked-before-GOOD "mount before GOOD" '        if mode == "run" and not nas_is_smb_mounted(ctx):
            problems.append("%s is no longer mounted as a network share at the end of the run" % c["nas_root"])' '        if False:
            problems.append("%s is no longer mounted as a network share at the end of the run" % c["nas_root"])'
mutant X12-roots-not-searched-one-level-down "forbidden roots" '        for d in level1:
            if os.path.realpath(d) != self.tree and not os.path.basename(d).startswith("."):' '        for d in []:
            if os.path.realpath(d) != self.tree and not os.path.basename(d).startswith("."):'
mutant X13-roots-beside-the-tree-not-searched "forbidden roots" '        if os.path.realpath(parent) != vol and os.path.isdir(parent):
            consider(parent, both)' '        if False:
            consider(parent, both)'
mutant X15-good-although-NAS-manifest-failed "GOOD truthful" '            problems.append("could not write the manifest or the completion marker on the NAS: %s" % e)
            good = False' '            pass'
mutant X18-index-drop-not-committed "sample never ages out" '        self.db.executemany("DELETE FROM files WHERE setname=? AND rel=?", [(setname, r) for r in rels])
        self.db.commit()' '        self.db.executemany("DELETE FROM files WHERE setname=? AND rel=?", [(setname, r) for r in rels])'
mutant X21-no-damage-notice-for-the-index "damage reaches a seat" '            ctx.note_damage("index", dst, e)' '            pass'
mutant X26-accounting-only-over-the-copy-list "the one subtraction" '                planned = set(src["files"])
                why = {}' '                planned = set(plan["copy"])
                why = {}'
mutant X28-two-sets-may-share-a-destination "destination overlap" '            if key in seen:
                raise Refused("two sets share the destination %s/%s" % (s["client"], s["dest"]))' '            if False:
                raise Refused("two sets share the destination %s/%s" % (s["client"], s["dest"]))'
mutant X33-watch-does-not-restart-clock-at-lift "hold and the clock" '    if not os.path.exists(ctx.hold_file) and ctx.hold_lifted(st):' '    if False and ctx.hold_lifted(st):'
mutant X34-nightly-does-not-restart-clock-at-lift "hold and the clock" '    st["last_fire"] = {"time": ctx.now, "time_local": now_local_str(ctx.now), "decision": action, "reason": reason}
    ctx.hold_lifted(st)' '    st["last_fire"] = {"time": ctx.now, "time_local": now_local_str(ctx.now), "decision": action, "reason": reason}'
mutant X37-cap-ignored-while-comparing-in-the-plan "cap between files" '            if deadline is not None and time.time() >= deadline:
                # The cap is honoured HERE' '            if False:
                # The cap is honoured HERE'
mutant X40-deleted-count-not-in-the-manifest "deleted are named" '                mset.update({"deleted_during_run": sorted(deleted)[:5000], "deleted_count": len(deleted),' '                mset.update({"deleted_during_run": [], "deleted_count": 0,'
mutant X41-type-change-moved-without-a-versions-copy "nothing destroyed" '                        os.makedirs(os.path.dirname(vpath), exist_ok=True)
                        os.rename(os.path.join(dest_dir, drel), vpath)' '                        os.makedirs(os.path.dirname(vpath), exist_ok=True)
                        os.rename(os.path.join(dest_dir, drel), os.path.join(croot, "_tmp_incoming", "x%d" % len(plan["type_changes"])))'
wait
echo; C=0; SV=0; NA=0
for n in $ORDER; do cat "$RUN/results/$n.txt"; if /usr/bin/grep -q -F '  CAUGHT ' "$RUN/results/$n.txt"; then C=$((C+1)); elif /usr/bin/grep -q -F 'NOT-APPLIED' "$RUN/results/$n.txt"; then NA=$((NA+1)); else SV=$((SV+1)); fi; done
echo; echo "$C caught, $SV survived, $NA not applied (of $((C+SV+NA))); outputs under $RUN; $(date); $(uptime)"
