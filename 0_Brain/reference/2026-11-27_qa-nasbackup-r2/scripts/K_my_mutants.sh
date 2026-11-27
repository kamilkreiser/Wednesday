#!/bin/bash
# K_my_mutants.sh — the fresh checker's OWN mutants on round 2's nb_core.py, weighted to the HARD guarantees.
# Same mechanics as the seat's tests/mutants.sh (scratch copy of the lane per mutant, one exact-once replacement,
# run the copy's suite) but the pass rule is looser IN THE SEAT'S FAVOUR: a mutant counts as CAUGHT when the suite
# exits non-zero with ANY FAIL line. None of these repeats a mutation in tests/mutants.sh.
#   K_my_mutants.sh <base under /private/tmp> <lane copy> [parallel]
set -u
BASE="$1"; LANE="$2"; PAR="${3:-5}"
TREE="$(cd -P "$LANE/../.." && pwd)"
case "$BASE" in /private/tmp/*) ;; *) echo "refused: base not under /private/tmp" >&2; exit 2 ;; esac
RUN="$BASE/kmut_$(date +%Y%m%d-%H%M%S)_$$"; mkdir -p "$RUN/results" || exit 2
PY=/opt/homebrew/bin/python3; ORDER=""
copy_lane() { local c="$RUN/$1/WEDNESDAY/2_Project_Files"
  mkdir -p "$c/nas-backup/tests" "$c/nas-backup/proposed" "$c/nas-backup/jobs" "$c/fleet/cockpit" "$c/tools" "$RUN/$1/base"
  cp "$LANE/nb_core.py" "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$c/nas-backup/"
  cp "$LANE/tests/run.sh" "$c/nas-backup/tests/"; cp "$LANE/proposed/doctor_nasbackup_block.sh" "$c/nas-backup/proposed/"
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
    printf '  NOT-APPLIED %-38s %s\n' "$name" "$(head -1 "$RUN/$name/apply.err")" > "$res"; return; fi
  "$PY" -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())' "$copy/nb_core.py" 2> "$RUN/$name/syntax.err" || { printf '  NOT-APPLIED %-38s the mutated file does not parse\n' "$name" > "$res"; return; }
  bash "$copy/tests/run.sh" "$RUN/$name/base" > "$RUN/$name/out.txt" 2>&1; local rc=$?
  local nfail; nfail="$(/usr/bin/grep -c -F '  FAIL  ' "$RUN/$name/out.txt")"
  if [ "$rc" -ne 0 ] && [ "$nfail" -gt 0 ]; then printf '  CAUGHT      %-38s [%s] %3s FAIL line(s), first: %s\n' "$name" "$guar" "$nfail" "$(/usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | head -1 | cut -c9-100)" > "$res"
  else printf '  SURVIVED    %-38s [%s] exit %s, %s FAIL lines, %s PASS lines\n' "$name" "$guar" "$rc" "$nfail" "$(/usr/bin/grep -c -F '  PASS  ' "$RUN/$name/out.txt")" > "$res"; fi; }
N=0; mutant() { ORDER="$ORDER $1"; one "$@" & N=$((N+1)); if [ $((N % PAR)) -eq 0 ]; then wait; fi; }
echo "=== my mutants — under $RUN, $PAR at a time ==="
copy_lane control; bash "$RUN/control/WEDNESDAY/2_Project_Files/nas-backup/tests/run.sh" "$RUN/control/base" > "$RUN/control/out.txt" 2>&1; CRC=$?
echo "  CONTROL   the unmutated copy: exit $CRC — $(tail -1 "$RUN/control/out.txt" | cut -c1-28)"; [ "$CRC" -eq 0 ] || exit 1

mutant K01-unproven-files-enter-the-index "GOOD truthful" '                    index.put_many(s["dest"], good_rows, time.time())      # ONLY what was proven' '                    index.put_many(s["dest"], [(r, src["files"][r]) for r in todo if r in src["files"]], time.time())'
mutant K02-unaccounted-files-ignored "GOOD truthful" '                unaccounted = [rel for rel in src["files"] if rel not in proven and rel not in undelivered]' '                unaccounted = []'
mutant K03-broken-scope-still-copied "conf fails closed" '            elif scope_broken:' '            elif False:'
mutant K04-new-run-beside-orphan-engine "one writer" '        if ls.get("engines"):
            raise Refused("REFUSED — the run that held the lock' '        if False:
            raise Refused("REFUSED — the run that held the lock'
mutant K05-exclude_path-wildcards-accepted "conf fails closed" '            if any(ch in p for ch in "*?[]\\") or not p or ".." in p.split("/"):' '            if False:'
mutant K06-engine-accepts-any-tree-name "root isolation" '        if os.path.basename(self.tree).lower() != seat:' '        if False:'
mutant K07-tuesday-added-to-SEATS "root isolation" 'SEATS = {
    "wednesday": {' 'SEATS = {
    "tuesday": {"cap": "Tuesday", "clients": ["General"], "forbid": [], "other_client_tokens": [], "other_seat_tokens": []},
    "wednesday": {'
mutant K08-damaged-state-watch-says-ok "flag" '        out("nas-backup watch[%s]: %s" % (ctx.seat, ctx.state_note))
        return RC_OVERDUE' '        out("nas-backup watch[%s]: %s" % (ctx.seat, ctx.state_note))
        return RC_OK'
mutant K09-raised-mark-silences-every-gap "flag once per gap" '    raised = bool(flag.get("raised")) and flag.get("gap_key") == gap_key' '    raised = bool(flag.get("raised"))'
mutant K10-nightly-job-accepts-any-shrink "conf fails closed" '        rc = cmd_backup(ctx, "run", scheduled=True)' '        rc = cmd_backup(ctx, "run", scheduled=True, accept_shrink="nightly-auto")'
mutant K11-sample-of-unsent-files-empty "GOOD truthful" '                sample = random.sample(pool, min(c["hash_sample"], len(pool)))' '                sample = []'
mutant K12-test-mode-nas-fence-off "fence" '            if not c["nas_root"] or not under(c["nas_root"], self.troot) or not under(c["source_volume"], self.troot):' '            if False:'
mutant K13-oos-and-shrink-id-not-checked "approval" '                if val is not None and len(val.strip()) < 6:' '                if False:'
mutant K14-missing-destination-folder-ignored "GOOD truthful" '                        if not os.path.isdir(os.path.join(dest_dir, rel)) and os.path.isdir(os.path.join(s["src"], rel)):' '                        if False:'
mutant K15-case-colliding-names-copied "no content lost" '    if clash:
        clashset = set(clash)' '    if False:
        clashset = set(clash)'
mutant K16-dry-run-opens-index-writable "dry writes nothing" '    index = Index(ctx.index_file, readonly=(mode != "run"))' '    index = Index(ctx.index_file, readonly=False)'
mutant K17-watchdog-never-armed "time cap" '        signal.alarm(int(cap) + 900)' '        signal.alarm(0)'
mutant K18-engine-seen-only-by-group-id "one writer" '        elif "rsync" in parts[2].split(" ")[0] and any(n in parts[2] for n in needles):' '        elif False:'
mutant K19-unreadable-destination-counts-as-proven "GOOD truthful" '        hd = sha256_of(dst_path)
    except OSError:
        return ("differs", s1)' '        hd = sha256_of(dst_path)
    except OSError:
        return ("proven", s1)'
mutant K20-failed-run-recorded-as-good "GOOD truthful" '            status = {RC_CAP: "killed-cap", RC_STALLED: "stalled"}.get(result["rc"], "failed")' '            status = {RC_CAP: "killed-cap", RC_STALLED: "stalled"}.get(result["rc"], "good")'
mutant K21-sharp-fall-accepted-when-hold-absent "conf fails closed" '    elif n_src == 0 and last_count:' '    elif False:'
mutant K22-exit-code-12-tolerated "GOOD truthful" '                    elif rc not in (0, 23, 24):' '                    elif False:'
mutant K23-source-not-required-to-be-a-folder "refusal" '        if not os.path.isdir(s["src"]):
            raise Refused("REFUSED — source %s is absent' '        if False:
            raise Refused("REFUSED — source %s is absent'
mutant K24-held-watch-raises-nothing-removed "hold" '    if os.path.exists(ctx.hold_file) and action in ("check", "card"):' '    if False:'
mutant K25-nightly-records-no-fire "flag" '    st["last_fire"] = {"time": ctx.now, "time_local": now_local_str(ctx.now), "decision": action, "reason": reason}' '    pass'
wait
echo; C=0; SV=0; NA=0
for n in $ORDER; do cat "$RUN/results/$n.txt"; if /usr/bin/grep -q -F '  CAUGHT ' "$RUN/results/$n.txt"; then C=$((C+1)); elif /usr/bin/grep -q -F 'NOT-APPLIED' "$RUN/results/$n.txt"; then NA=$((NA+1)); else SV=$((SV+1)); fi; done
echo; echo "=== $C caught, $SV survived, $NA not applied (of $((C+SV+NA))) ==="
