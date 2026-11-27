#!/bin/bash
# tests/mutants.sh — proof that tests/run.sh CAN FAIL, round 2 (2026-08-07_a-check-that-cannot-fail; QA finding 10:
# "a guard without a test that can fail is not a guard").
# For each named guard it makes a scratch COPY of this lane, breaks that one guard in the copy's nb_core.py, runs
# the copy's tests/run.sh, and requires (a) a non-zero exit and (b) a FAIL line carrying the id of the test that
# owns the guard. A mutant the suite does not catch is SURVIVED and fails this script; a mutation that no longer
# applies (the code moved) is BROKEN and fails it too. The real lane is never edited. Under /private/tmp only. No rm.
# Three groups: M = the seat's round 1 guards (re-pointed at the round 2 code); Q = the independent checker's 18
# (14 of which survived round 1); N = new mutants on round 2's new code.
#   tests/mutants.sh [base dir under /private/tmp] [how many at once, default 5]
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="$(cd -P "$HERE/.." && pwd)"
TREE="$(cd -P "$LANE/../.." && pwd)"
BASE="${1:-/private/tmp/nas-backup-tests}"
PAR="${2:-5}"
case "$BASE" in /private/tmp/*) ;; *) echo "mutants: REFUSED — the base must be under /private/tmp" >&2; exit 2 ;; esac
RUN="$BASE/mutants_$(date +%Y%m%d-%H%M%S)_$$"
mkdir -p "$RUN/results" || exit 2
PY=/opt/homebrew/bin/python3; [ -x "$PY" ] || PY=/usr/bin/python3
ORDER=""

copy_lane() { # name
  local c="$RUN/$1/WEDNESDAY/2_Project_Files"
  mkdir -p "$c/nas-backup/tests" "$c/nas-backup/proposed" "$c/nas-backup/jobs" "$c/fleet/cockpit" "$c/tools" "$RUN/$1/base"
  cp "$LANE/nb_core.py" "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$c/nas-backup/"
  cp "$LANE/tests/run.sh" "$c/nas-backup/tests/"; cp "$LANE/proposed/doctor_nasbackup_block.sh" "$c/nas-backup/proposed/"
  cp "$LANE/jobs/nasbackup.plist.template" "$c/nas-backup/jobs/"
  cp "$TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$c/fleet/cockpit/"; cp "$TREE/2_Project_Files/tools/seat_note.sh" "$c/tools/"
}
one() { # name  expected-test-id  old new [old new ...]   -> writes ONE result line
  local name="$1" want="$2"; shift 2
  local res="$RUN/results/$name.txt" copy="$RUN/$name/WEDNESDAY/2_Project_Files/nas-backup"
  copy_lane "$name"
  if ! "$PY" -c 'import sys
p, pairs = sys.argv[1], sys.argv[2:]
s = open(p, encoding="utf-8").read()
for i in range(0, len(pairs), 2):
    n = s.count(pairs[i])
    if n != 1:
        sys.stderr.write("mutation target found %d times (need exactly 1): %r\n" % (n, pairs[i])); sys.exit(1)
    s = s.replace(pairs[i], pairs[i + 1])
open(p, "w", encoding="utf-8").write(s)' "$copy/nb_core.py" "$@" 2> "$RUN/$name/apply.err"; then
    printf '  BROKEN    %-34s the mutation could not be applied: %s\n' "$name" "$(head -1 "$RUN/$name/apply.err")" > "$res"; return
  fi
  bash "$copy/tests/run.sh" "$RUN/$name/base" > "$RUN/$name/out.txt" 2>&1; local rc=$?
  local nfail; nfail="$(/usr/bin/grep -c -F '  FAIL  ' "$RUN/$name/out.txt")"
  if [ "$rc" -ne 0 ] && /usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | /usr/bin/grep -q -F "$want"; then
    printf '  CAUGHT    %-34s %3s FAIL line(s), including: %s\n' "$name" "$nfail" "$(/usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | /usr/bin/grep -F "$want" | head -1 | cut -c9-118)" > "$res"
  else
    printf '  SURVIVED  %-34s exit %s, %s FAIL line(s), none for [%s] (output: %s)\n' "$name" "$rc" "$nfail" "$want" "$RUN/$name/out.txt" > "$res"
  fi
}
N=0
mutant() { ORDER="$ORDER $1"; one "$@" & N=$((N+1)); if [ $((N % PAR)) -eq 0 ]; then wait; fi; }

echo "=== mutants (round 2) — scratch copies under $RUN, $PAR at a time ==="
copy_lane control
bash "$RUN/control/WEDNESDAY/2_Project_Files/nas-backup/tests/run.sh" "$RUN/control/base" > "$RUN/control/out.txt" 2>&1; CRC=$?
echo "  CONTROL   the unmutated copy: exit $CRC — $(tail -1 "$RUN/control/out.txt" | cut -c1-28)"
[ "$CRC" -eq 0 ] || { echo "mutants: the CONTROL failed; nothing below would mean anything" >&2; exit 1; }

# ── M: the seat's round 1 guards ──
mutant M01-keeps-no-previous-version "T3 the PREVIOUS a.txt" '"--files-from=" + list_path, "--backup",
                            "--backup-dir=" + bdir, ' '"--files-from=" + list_path, '
mutant M02-credentials-folder-allowed "T4 no secret" 'if "4_credentials" in n or "3_access_keys" in n:' 'if False:'
mutant M03-git-allowed "T4 no secret" '("git", "any", [".git"]),' '("git", "any", []),'
mutant M04-other-seat-folders-allowed "T4 no secret" 'self.tokens += [("other-seat", t) for t in ctx.info["other_seat_tokens"]]' 'pass'
mutant M05-mount-check-off "T5a NAS not in the mount table" 'return any(needle in ln for ln in mount_lines(ctx))' 'return True'
mutant M06-case-check-off "T5c " '    if name in names:
        return "exact"' '    if True:
        return "exact"'
mutant M07-free-space-floor-off "T5d free space under the floor" 'if free < c["min_free_gib"]:' 'if False:'
mutant M08-lock-ignored "T5e live lock" '    except FileExistsError:
        ls = lock_status(ctx) or {}' '    except FileExistsError:
        return
        ls = lock_status(ctx) or {}'
mutant M09-foreign-source-allowed "T5f'"' a source outside' 'if not under(s["src"], c["source_volume"]) or os.stat(s["src"]).st_dev != tree_dev:' 'if False:'
mutant M10-allow-list-off "T5g destination in another client" '            if s["client"] not in self.info["clients"]:' '            if False:' '        if client not in self.info["clients"]:' '        if False:'
mutant M11-window-check-off "T5i a real run at 14:00" 'if not inw and not out_of_sequence:' 'if False:'
mutant M12-hold-ignored "T5j HOLD file present" 'if mode == "run" and os.path.exists(ctx.hold_file):' 'if False:'
mutant M13-deletion-flag-allowed "T5k every deletion-capable" 'if a == bad or a.startswith(bad + "=") or a.startswith("--delete") or a.startswith("--del"):' 'if False:'
mutant M14-file-ceiling-off "T5m a set above max_files" 'if n_src > c["max_files"]:' 'if False:'
mutant M15-deleting-line-ignored "T6 exit 9" 'if low.startswith("*deleting") or low.startswith("deleting "):' 'if False:'
mutant M16-catches-nothing-up "T7 a second fire the same night" 'if lg and wall(lg["time"]) >= o:' 'if False:'
mutant M17-runs-outside-window "T7 day 3, 14:00" '    if not inw:
        if c["late_fire"] == "run":' '    if False:
        if c["late_fire"] == "run":'
mutant M18-flag-never "T8 at the next boot doctor" 'overdue = hours >= FLAG_AFTER_HOURS' 'overdue = False'
mutant M19-raised-mark-ignored "T8 once raised" 'raised = bool(flag.get("raised")) and flag.get("gap_key") == gap_key' 'raised = False'
mutant M20-index-trusted-blindly "T3 same-size change" 'if ix is not None and tuple(ix) == tuple(sv):' 'if ix is not None:'
# ── Q: the independent checker's 18 (D_my_mutants.sh), re-pointed at the round 2 code ──
mutant Q01-other-client-names-off "T14 a name containing the other client" 'self.tokens = [("other-client", t) for t in ctx.info["other_client_tokens"]]' 'self.tokens = []'
mutant Q02-arrival-check-vacuous "T12 H1 same-size change" '    return ("proven", s1) if hs == hd else ("differs", s1)' '    return ("proven", s1)'
mutant Q03-exclude_path-ignored "T15 exclude_path, exclude_name" '        if rel in self.paths:' '        if False:'
mutant Q04-exclude_name-ignored "T15 exclude_path, exclude_name" '        for p in self.conf_names:
            if fnmatch.fnmatchcase(n, p):' '        for p in []:
            if fnmatch.fnmatchcase(n, p):'
mutant Q05-symlink-source-allowed "T14 a source that is itself a symlink" '        if os.path.islink(s["src"]):' '        if False:' '        if s["real"] != os.path.normpath(s["src"]):' '        if False:'
mutant Q06-test-root-fence-off "T14 test mode outside /private/tmp" '    if not rt.startswith("/private/tmp/") or not os.path.isdir(rt):' '    if not os.path.isdir(rt):'
mutant Q07-dest-dotdot-allowed "T14 a destination name with .." '            if not s["dest"] or s["dest"].startswith("/") or any(p in ("", ".", "..") for p in s["dest"].split("/")):' '            if False:'
mutant Q08-rsync-version-check-off "T15 an engine that is not rsync 3" '    if "openrsync" in r.stdout or "version 2." in first or "version 3." not in first:' '    if False:'
mutant Q09-hash-sample-ignored "T12 a destination copy that changed behind our back" '                    if verdict == "differs":
                        bad_hash.append(rel)' '                    if False:
                        bad_hash.append(rel)'
mutant Q10-env-variants-allowed "T13 NOT ONE of the 35" '    if n.startswith(".env") or ".env." in n or n.endswith(".env"):' '    if n == ".env":'
mutant Q11-type-change-not-handled "T17 folder -> file" '                    os.rename(os.path.join(dest_dir, drel), vpath)' '                    pass'
mutant Q12-source-errors-silent "T15 a source folder that cannot be read" '    if src["errors"]:' '    if False:'
mutant Q13-dry-creates-on-nas "T1 nothing created on the fake NAS" '            if mode == "run":
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)' '            if True:
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)'
mutant Q14-window-never-closes "T5i a real run at 14:00" '    return (o, c, o <= w < c)' '    return (o, c, o <= w)'
mutant Q15-complete-marker-always "T6 no COMPLETE marker" '                if good:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp)' '                if True:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp)'
mutant Q16-forbid-source-off "T5g'"' a Datasec source path' '                        if f in comp.casefold():' '                        if False:'
mutant Q17-other-seats-state-accepted "T14 a state file that says it is another seat" '        if st.get("seat") != self.seat:' '        if False:'
mutant Q18-attempt-history-cut "T8 the BLUF counts all three" 'st.get("recent_attempts", []))[:RECENT_ATTEMPTS]' 'st.get("recent_attempts", []))[:1]'
# ── N: new mutants on round 2's new code ──
mutant N01-end-marker-not-required "T15 a conf that lost its END marker" '        if not content or not re.match(r"^END lines=\d+$", content[-1][1]):' '        if not content:'
mutant N02-line-count-not-checked "T15 a conf that lost its exclude lines" '        if declared != len(content) - 1:' '        if False:'
mutant N03-missing-exclude_path-accepted "T15 an exclude_path that names nothing" '            if os.path.isdir(src) and not os.path.lexists(os.path.join(src, p)):' '            if False:'
mutant N04-exclude-everything-accepted "T15 exclude_name=*" '            if match_everything(p):' '            if False:'
mutant N05-empty-scope-is-good "T15 a set that became EMPTY" '    if n_src == 0 and not src["dirs"]:' '    if False:' '    elif n_src == 0 and last_count:' '    elif False:' '    elif last_count and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:' '    elif last_count and n_src and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:'
mutant N06-sharp-fall-is-good "T15 a set that lost more than half" '    elif last_count and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:' '    elif False:'
mutant N07-hard-links-travel "T13 NOT ONE of the 35" '                        if rules is not None and s.st_nlink > 1:' '                        if False:'
mutant N08-key-extensions-travel "T13 NOT ONE of the 35" '        if n.endswith(e) or (e + ".") in n or (e + " ") in n:' '        if False:'
mutant N09-deploy-keys-travel "T13 NOT ONE of the 35" '            or n.startswith("github_deploy") or "deploy_key" in n or "deploy-key" in n
            or n.endswith("_deploy_rw") or n.endswith("_deploy_ro")):' '            ):'
mutant N10-first-attempt-rolls "T9 day 10, never armed" '        if not st.get("first_attempt_at"):
            st["first_attempt_at"] = self.now          # stored ONCE, never rolled (finding 5)' '        if True:
            st["first_attempt_at"] = self.now' '    if not st.get("first_attempt_at"):
        st["first_attempt_at"] = ctx.now
    ctx.write_state(st)
    rc = RC_OK' '    st["first_attempt_at"] = ctx.now
    ctx.write_state(st)
    rc = RC_OK'
mutant N11-damaged-state-crashes "T16 the watch on a truncated state file" '        except (ValueError, OSError) as e:
            q = os.path.join(self.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))' '        except KeyError as e:
            q = os.path.join(self.state_dir, "_quarantine_%s" % time.strftime("%Y-%m-%d"))'
mutant N12-nightly-prints-the-card "T8 ... but the nightly job" '    cmd_watch(ctx, "check")
    return rc' '    cmd_watch(ctx, "card")
    return rc'
mutant N13-engine-group-not-recorded "T18 the lock records the engine" '        write_owner(ctx, "run", engine_pgid=p.pid)' '        pass'
mutant N14-clear-lock-beside-engine "T18 the tool was killed outright" '    if ls.get("engines"):
        raise Refused("REFUSED — the holder (pid %s) is gone but %d copy-engine' '    if False:
        raise Refused("REFUSED — the holder (pid %s) is gone but %d copy-engine'
mutant N15-new-lock-called-stale "T18 ... it is '"'another run holds the lock'"'" '    info["fresh"] = (not readable) and age < 15' '    info["fresh"] = False'
mutant N16-reused-pid-is-holder "T18 a live process that merely has" '    return proc_started(pid) == owner.get("pid_started")' '    return True'
mutant N17-window-in-elapsed-seconds "T19 spring-forward night, 05:40" '    c = o + datetime.timedelta(hours=window_hours)' '    c = datetime.datetime.fromtimestamp(time.mktime(o.timetuple()) + window_hours * 3600.0)'
mutant N18-dot-underscore-folders-dropped "T13 a real FOLDER named" '("system", "files", ["._*"]),' '("system", "any", ["._*"]),'
mutant N19-nightly-ignores-the-hold "T20 ... and the refusal is in the nightly log" '        if os.path.exists(ctx.hold_file):
            record("nightly[%s]: HELD' '        if False:
            record("nightly[%s]: HELD'
mutant N20-resend-overwrites-kept-copy "T12 ... night 1" 'bdir = os.path.join(croot, "versions", stamp + tag, *s["dest"].split("/"))' 'bdir = os.path.join(croot, "versions", stamp, *s["dest"].split("/"))'
mutant N21-client-tokens-not-reported "T14 ... and REPORTED per token" '                token_counts[label] += sum(1 for rel in src["files"] if rx.search(rel.lower()))' '                token_counts[label] += 0'
mutant N22-watch-never-starts-the-clock "T9 72 h, the job NEVER fired" '        st["first_attempt_at"] = ctx.now
        ctx.write_state(st)
        out("nas-backup watch[%s]: nothing on record' '        out("nas-backup watch[%s]: nothing on record'
mutant N23-real-path-not-checked "T14 ... the REAL path is named" '            for cand in (s["src"], s["real"]):' '            for cand in (s["src"],):'
mutant N24-unstable-source-called-proven "T12 a file appended to DURING the copy" '    if s1 != s2:
        return ("unstable", None)' '    if False:
        return ("unstable", None)' '                        elif verdict == "unstable" or (st3 is not None and st3 != tuple(src["files"][rel])):' '                        elif False:'
mutant N25-undelivered-not-recorded "T12 H1 the state the watch reads" '"undelivered_count": len(undelivered_all),' '"undelivered_count": 0,'
wait

echo
C=0; SV=0
for n in $ORDER; do cat "$RUN/results/$n.txt"; if /usr/bin/grep -q -F '  CAUGHT ' "$RUN/results/$n.txt"; then C=$((C+1)); else SV=$((SV+1)); fi; done
echo
echo "=== $C mutants caught, $SV survived or broken (of $((C+SV))) — outputs kept under $RUN ==="
[ "$SV" -eq 0 ]
