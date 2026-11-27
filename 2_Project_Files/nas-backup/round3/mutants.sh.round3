#!/bin/bash
# tests/mutants.sh — proof that tests/run.sh CAN FAIL, round 3 (2026-08-07_a-check-that-cannot-fail; QA finding 10:
# "a guard without a test that can fail is not a guard").
# For each named guard it makes a scratch COPY of this lane, breaks that one guard in the copy's nb_core.py, runs
# the copy's tests/run.sh, and requires (a) a non-zero exit and (b) a FAIL line carrying the id of the test that
# owns the guard. A mutant the suite does not catch is SURVIVED and fails this script; a mutation that no longer
# applies (the code moved) is BROKEN and fails it too. The real lane is never edited. Under /private/tmp only. No rm.
# Five groups: M = the seat's round 1 guards; Q = the first checker's 18 (14 of which survived round 1); N = round
# 2's own; K = the SECOND checker's 25 (K_my_mutants.sh; 15 of which survived round 2), each re-pointed at the
# round 3 code with the same intent and named for the test that must catch it; R = new mutants on round 3's code.
# Where round 3 rewrote the line a mutant aimed at, the mutant here breaks the line that now does that job.
#   tests/mutants.sh [base dir under /private/tmp] [how many at once, default 5] [only mutants whose name starts with this, an extended regex such as 'M20|Q16']
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="$(cd -P "$HERE/.." && pwd)"
TREE="$(cd -P "$LANE/../.." && pwd)"
BASE="${1:-/private/tmp/nas-backup-tests}"
PAR="${2:-5}"
ONLY="${3:-}"
case "$BASE" in /private/tmp/*) ;; *) echo "mutants: REFUSED — the base must be under /private/tmp" >&2; exit 2 ;; esac
RUN="$BASE/mutants_$(date +%Y%m%d-%H%M%S)_$$"
mkdir -p "$RUN/results" || exit 2
PY=/opt/homebrew/bin/python3; [ -x "$PY" ] || PY=/usr/bin/python3
ORDER=""

copy_lane() { # name
  local c="$RUN/$1/WEDNESDAY/2_Project_Files"
  mkdir -p "$c/nas-backup/tests" "$c/nas-backup/proposed" "$c/nas-backup/jobs" "$c/fleet/cockpit" "$c/tools" "$RUN/$1/base"
  cp "$LANE/nb_core.py" "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$c/nas-backup/"
  cp "$LANE/tests/run.sh" "$LANE/tests/scan_dry_lists.py" "$c/nas-backup/tests/"; cp "$LANE/proposed/doctor_nasbackup_block.sh" "$c/nas-backup/proposed/"
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
mutant() { if [ -n "$ONLY" ] && ! printf '%s' "$1" | /usr/bin/grep -q -E "^($ONLY)"; then return 0; fi
  ORDER="$ORDER $1"; one "$@" & N=$((N+1)); if [ $((N % PAR)) -eq 0 ]; then wait; fi; }

echo "=== mutants (round 3) — scratch copies under $RUN, $PAR at a time ==="
copy_lane control
bash "$RUN/control/WEDNESDAY/2_Project_Files/nas-backup/tests/run.sh" "$RUN/control/base" > "$RUN/control/out.txt" 2>&1; CRC=$?
echo "  CONTROL   the unmutated copy: exit $CRC — $(tail -1 "$RUN/control/out.txt" | cut -c1-28)"
[ "$CRC" -eq 0 ] || { echo "mutants: the CONTROL failed; nothing below would mean anything" >&2; exit 1; }

# ── M: the seat's round 1 guards ──
mutant M01-keeps-no-previous-version "T3 the PREVIOUS a.txt" '"--files-from=" + list_path, "--backup",
                                    "--backup-dir=" + bdir, ' '"--files-from=" + list_path, '
mutant M02-credentials-folder-allowed "T4 no secret" 'if "4_credentials" in n or "3_access_keys" in n:' 'if False:'
mutant M03-git-allowed "T4 no secret" '("git", "any", [".git"]),' '("git", "any", []),'
mutant M04-other-seat-folders-allowed "T14 a name containing the other client" 'self.tokens += [("other-seat", t) for t in ctx.info["other_seat_tokens"]]' 'pass'
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
mutant M20-index-trusted-blindly "T3 sample off" 'if ix is not None and tuple(ix) == tuple(sv):' 'if ix is not None:'
# ── Q: the independent checker's 18 (D_my_mutants.sh), re-pointed at the round 2 code ──
mutant Q01-other-client-names-off "T14 a name containing the other client" 'self.tokens = [("other-client", t) for t in ctx.info["other_client_tokens"]]' 'self.tokens = []'
mutant Q02-arrival-check-vacuous "T12 H1 same-size change" '    return ("proven", s1, "") if hs == hd else ("differs", s1, "the destination copy holds other content")' '    return ("proven", s1, "")'
mutant Q03-exclude_path-ignored "T15 exclude_path, exclude_name" '        if rel in self.paths:' '        if False:'
mutant Q04-exclude_name-ignored "T15 exclude_path, exclude_name" '        for p in self.conf_names:
            if fnmatch.fnmatchcase(n, p):' '        for p in []:
            if fnmatch.fnmatchcase(n, p):'
mutant Q05-symlink-source-allowed "T14 a source that is itself a symlink" '        if os.path.islink(s["src"]):' '        if False:' '        if s["real"] != os.path.normpath(s["src"]):' '        if False:'
mutant Q06-test-root-fence-off "T14 test mode outside /private/tmp" '    if not rt.startswith("/private/tmp/") or not os.path.isdir(rt):' '    if not os.path.isdir(rt):'
mutant Q07-dest-dotdot-allowed "T14 a destination name with .." '            if not s["dest"] or s["dest"].startswith("/") or any(p in ("", ".", "..") for p in s["dest"].split("/")):' '            if False:'
mutant Q08-rsync-version-check-off "T15 an engine that is not rsync 3" '    if "openrsync" in r.stdout or "version 2." in first or "version 3." not in first:' '    if False:'
mutant Q09-hash-sample-ignored "T12 ... the destination holds the source's content again" '                        if verdict != "proven":
                            repair.append(rel)' '                        if False:
                            repair.append(rel)'
mutant Q10-env-variants-allowed "T13 NOT ONE of the 35" '    if n.startswith(".env") or ".env." in n or n.endswith(".env"):' '    if n == ".env":'
mutant Q11-type-change-not-handled "T17 folder -> file" '                        os.rename(os.path.join(dest_dir, drel), vpath)' '                        pass'
mutant Q12-source-errors-silent "T15 a source folder that cannot be read" '    if src["errors"]:' '    if False:'
mutant Q13-dry-creates-on-nas "T1 nothing created on the fake NAS" '            if mode == "run":
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)' '            if True:
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)'
mutant Q14-window-never-closes "T5i a real run at 14:00" '    return (o, c, o <= w < c)' '    return (o, c, o <= w)'
mutant Q15-complete-marker-always "T6 no COMPLETE marker" '                if good:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp)' '                if True:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp)'
mutant Q16-forbid-source-off "T14 a source inside a datasec-named folder four levels down" '                        if f in comp.casefold():' '                        if False:'
mutant Q17-other-seats-state-accepted "T14 a state file that says it is another seat" '        if st.get("seat") != self.seat:' '        if False:'
mutant Q18-attempt-history-cut "T8 the BLUF counts all three" 'st.get("recent_attempts", []))[:RECENT_ATTEMPTS]' 'st.get("recent_attempts", []))[:1]'
# ── N: new mutants on round 2's new code ──
mutant N01-end-marker-not-required "T15 a conf that lost its END marker" '        if not content or not re.match(r"^END lines=\d+$", content[-1][1]):' '        if not content:'
mutant N02-line-count-not-checked "T15 a conf that lost its exclude lines" '        if declared != len(content) - 1:' '        if False:'
mutant N03-missing-exclude_path-accepted "T15 an exclude_path that names nothing" '            if os.path.isdir(src) and not os.path.lexists(os.path.join(src, p)):' '            if False:'
mutant N04-exclude-everything-accepted "T15 exclude_name=*" '            if match_everything(p):' '            if False:'
mutant N05-empty-scope-is-good "T15 a set that became EMPTY" '    if n_src == 0 and s["dest"] not in c["allow_empty"]:' '    if False:' '    elif last_count and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:' '    elif last_count and n_src and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:'
mutant N06-sharp-fall-is-good "T15 a set that lost more than half" '    elif last_count and n_src < last_count * (1.0 - c["max_drop_fraction"]) and not accept_shrink:' '    elif False:'
mutant N07-hard-links-travel "T13 NOT ONE of the 35" '                        if rules is not None and s.st_nlink > 1:' '                        if False:'
mutant N08-key-extensions-travel "T13 NOT ONE of the 35" '        if n.endswith(e) or (e + ".") in n or (e + " ") in n:' '        if False:'
mutant N09-deploy-keys-travel "T13 NOT ONE of the 35" '            or n.startswith("github_deploy") or "deploy_key" in n or "deploy-key" in n
            or n.endswith("_deploy_rw") or n.endswith("_deploy_ro")):' '            ):'
mutant N10-first-attempt-rolls "T9 day 10, never armed" '            if not st.get("first_attempt_at"):
                st["first_attempt_at"] = self.now      # stored ONCE, never rolled (finding 5)' '            if True:
                st["first_attempt_at"] = self.now' '    if not st.get("first_attempt_at"):
        st["first_attempt_at"] = ctx.now
    ctx.write_state(st)
    rc = RC_OK' '    st["first_attempt_at"] = ctx.now
    ctx.write_state(st)
    rc = RC_OK'
mutant N11-damaged-state-crashes "T16 the watch on a truncated state file" '        except (ValueError, OSError) as e:
            if self.readonly:' '        except KeyError as e:
            if self.readonly:'
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
mutant N20-resend-overwrites-kept-copy "T12 ... night 1" '                            bdir = os.path.join(croot, "versions", stamp + tag, *s["dest"].split("/"))' '                            bdir = os.path.join(croot, "versions", stamp, *s["dest"].split("/"))'
mutant N21-client-tokens-not-reported "T14 ... and REPORTED per token" '                token_counts[label] += sum(1 for rel in src["files"] if rx.search(rel.lower()))' '                token_counts[label] += 0'
mutant N22-watch-never-starts-the-clock "T9 72 h, the job NEVER fired" '        st["first_attempt_at"] = ctx.now
        ctx.write_state(st)
        out("nas-backup watch[%s]: nothing on record' '        out("nas-backup watch[%s]: nothing on record'
mutant N23-real-path-not-checked "T14 ... refused by its REAL path's name" '            for cand in (s["src"], s["real"]):' '            for cand in (s["src"],):'
mutant N24-unstable-source-called-proven "T12 a file appended to DURING the copy" '    if s1 != s2:
        return ("unstable", None, "the source changed while it was being read")' '    if False:
        return ("unstable", None, "")' '                                elif verdict == "unstable" or (st3 is not None and st3 != tuple(src["files"][rel])):' '                                elif False:'
mutant N25-undelivered-not-recorded "T12 H1 the state the watch reads" '"undelivered_count": len(undelivered_all),' '"undelivered_count": 0,'
# ── K: the SECOND checker's 25 (0_Brain/reference/2026-11-27_qa-nasbackup-r2/scripts/K_my_mutants.sh), re-pointed ──
mutant K01-unproven-files-enter-the-index "T12 H1 ... and it is sent again" '                                else:
                                    why[rel] = note
                            saver.flush()' '                                else:
                                    why[rel] = note
                                    saver.add(rel, tuple(src["files"][rel]))
                            saver.flush()'
mutant K02-unaccounted-files-ignored "T12 H1 same-size change" '                not_proven = sorted(rel for rel in planned if rel not in proven and rel not in gone)' '                not_proven = []'
mutant K03-broken-scope-still-copied "T22 ... a new file in it did not travel" '            elif scope_broken:' '            elif False:'
mutant K04-new-run-beside-orphan-engine "T18 ... for the same reason" '        if ls.get("engines"):
            raise Refused("REFUSED — the run that held the lock' '        if False:
            raise Refused("REFUSED — the run that held the lock'
mutant K05-exclude_path-wildcards-accepted "T22 ... refused as not a literal path" '            if any(ch in p for ch in "*?[]\\") or not p or ".." in p.split("/"):' '            if False:'
mutant K06-engine-accepts-any-tree-name "T27 the engine called directly" '        if os.path.basename(self.tree).lower() != seat:' '        if False:'
mutant K07-another-seat-added-to-SEATS "T14 ... no confirmed scope" 'SEATS = {
    "wednesday": {' 'SEATS = {
    "tuesday": {"cap": "Tuesday", "clients": ["General"], "forbid": [], "other_client_tokens": [], "other_seat_tokens": []},
    "wednesday": {'
mutant K08-damage-notice-watch-says-ok "T16 the watch on a truncated state file" '    rc_quiet = RC_DAMAGE_NOTICE if notices else RC_OK' '    rc_quiet = RC_OK'
mutant K09-raised-mark-silences-every-gap "T8 a second gap" '    raised = bool(flag.get("raised")) and flag.get("gap_key") == gap_key' '    raised = bool(flag.get("raised"))'
mutant K10-nightly-job-accepts-any-shrink "T22 the NIGHTLY job on a set that fell" '        rc = cmd_backup(ctx, "run", scheduled=True)' '        rc = cmd_backup(ctx, "run", scheduled=True, accept_shrink="nightly-auto")'
mutant K11-sample-of-unsent-files-empty "T12 ... the destination holds the source's content again" '                    sample = random.sample(pool, min(c["hash_sample"], len(pool)))' '                    sample = []'
mutant K12-test-mode-nas-fence-off "T27 ... refused BY THE TEST-MODE FENCE" '            if not c["nas_root"] or not under(c["nas_root"], self.troot) or not under(c["source_volume"], self.troot):' '            if False:'
mutant K13-oos-and-shrink-id-not-checked "T5i an empty-ish approval" '            if val is not None and len(val.strip()) < 6:' '            if False:'
mutant K14-missing-destination-folder-ignored "T27 an engine that does not create" '                                if not os.path.isdir(os.path.join(dest_dir, rel)) and os.path.isdir(os.path.join(s["src"], rel)):' '                                if False:'
mutant K15-case-colliding-names-copied "T11 only the non-colliding" '    if clash:
        clashset = set(clash)' '    if False:
        clashset = set(clash)'
mutant K16-dry-run-opens-index-writable "T1 no index file created" '        index = Index(ctx, readonly=(mode != "run"))' '        index = Index(ctx, readonly=False)'
mutant K17-watchdog-never-armed "T26 ... and it is the WATCHDOG that says so" '        signal.alarm(int(cap) + margin)' '        signal.alarm(0)'
mutant K18-engine-seen-only-by-group-id "T27 a lock with no recorded engine group" '        elif "rsync" in parts[2].split(" ")[0] and any(n in parts[2] for n in needles):' '        elif False:'
mutant K19-unreadable-destination-counts-as-proven "T21j a destination copy that cannot be read back" '        hd = sha256_of(dst_path)
    except OSError as e:
        return ("differs", s1, "the destination copy is absent or could not be read (%s)" % (e.strerror or e))' '        hd = sha256_of(dst_path)
    except OSError as e:
        return ("proven", s1, "")'
mutant K20-failed-run-recorded-as-good "T6 state: no good backup recorded" '            status = {RC_CAP: "killed-cap", RC_STALLED: "stalled"}.get(result["rc"], "failed")' '            status = {RC_CAP: "killed-cap", RC_STALLED: "stalled"}.get(result["rc"], "good")'
mutant K21-zero-files-with-folders-is-good "T22 FIRST run of a set holding folders" '    if n_src == 0 and s["dest"] not in c["allow_empty"]:' '    if n_src == 0 and not src["dirs"] and s["dest"] not in c["allow_empty"]:'
mutant K22-exit-code-12-tolerated "T27 an engine that exits 12" '                            elif rc not in (0, 23, 24):' '                            elif False:'
mutant K23-source-not-required-to-be-a-folder "T22 ... refused as not a folder" '        if not os.path.isdir(s["src"]):
            raise Refused("REFUSED — source %s is absent' '        if False:
            raise Refused("REFUSED — source %s is absent'
mutant K24-held-watch-raises-nothing-removed "T9 HELD: exit 0" '    if os.path.exists(ctx.hold_file) and action in ("check", "card"):' '    if False:'
mutant K25-nightly-records-no-fire "T7 ... the fire and its decision are RECORDED" '    st["last_fire"] = {"time": ctx.now, "time_local": now_local_str(ctx.now), "decision": action, "reason": reason}' '    pass'
# ── R: new mutants on round 3's code ──
mutant R01-unreadable-counts-as-deleted "T21a a source file with mode 000" '                                    if source_deleted(s["src"], plan["root_id"], rel):' '                                    if True:'
mutant R02-deleted-although-still-listed "T21l a name that is still there" '        if name in names:
            return False' '        if False:
            return False'
mutant R03-unlistable-parent-means-deleted "T21h a planned file whose parent folder went away" '            names = os.listdir(parent)
        except OSError:
            return False' '            names = os.listdir(parent)
        except OSError:
            return True'
mutant R04-root-identity-not-checked "T21l a root that is no longer" '            if (rs.st_dev, rs.st_ino) != tuple(root_id) or not stat.S_ISDIR(rs.st_mode):
                return False' '            if False:
                return False'
mutant R05-deleted-limit-off "T21g six planned files" '                if len(deleted) > allowed:' '                if False:'
mutant R06-non-regular-source-hashed "T21i ... named, with the reason" '        if not stat.S_ISREG(os.lstat(src_path).st_mode):' '        if False:'
mutant R07-sample-finding-keeps-its-index-row "T23 the NEXT night" '                        index.drop(s["dest"], repair)' '                        pass'
mutant R36-no-read-back-after-a-sample-finding "T23 ... not one destination copy differs" '                    if wrong_at_dest:' '                    if False:'
mutant R37-own-run-state-in-the-plan "T27 the lane's own state folder" '        if self.own_state is not None and rel == self.own_state:' '        if False:'
mutant R38-empty-plan-judged-before-the-collisions "T11 a set whose ONLY files" '    n_src = len(src["files"])
    # AN EMPTY PLAN IS NEVER GOOD' '    n_src = n_src + len(plan["collision_skipped"])
    # AN EMPTY PLAN IS NEVER GOOD'
mutant R08-sample-finding-not-resent "T12 a destination copy that changed behind our back" '                    todo_all = sorted(set(plan["copy"]) | set(repair))' '                    todo_all = sorted(set(plan["copy"]))'
mutant R09-ancestor-of-forbidden-root-allowed "T24 a set= whose folder holds" '                if contains(r, s["real"]) or contains(s["real"], r):' '                if contains(r, s["real"]):'
mutant R10-ancestor-of-own-tree-allowed "T24 ... refused as an ANCESTOR of this seat" '            if s["real"] != self.tree and contains(s["real"], self.tree):' '            if False:'
mutant R11-nested-sets-allowed "T24 a set INSIDE another set" '                    if a["real"] == b["real"] or (a["dest"], relp) not in c["exclude_path"]:' '                    if False:'
mutant R12-seat-named-folder-travels "T24 a FOLDER named exactly" '        if is_dir and n in self.seat_names:' '        if False:'
mutant R13-no-damage-notice-for-the-state "T25 ... and LEAVES A NOTICE" '            self.note_damage("state file", dst, e)' '            pass'
mutant R14-damaged-index-crashes "T25 a DRY run with a damaged index" '        except sqlite3.Error as e:
            # A DAMAGED INDEX' '        except KeyError as e:
            # A DAMAGED INDEX'
mutant R15-dry-run-moves-damaged-state "T25 ... and leaves it where it is" '            if self.readonly:
                # A dry run writes nothing' '            if False:
                # A dry run writes nothing'
mutant R16-state-not-validated "T25 a state file that is valid JSON" '            self.validate_state(st)' '            pass'
mutant R17-future-times-accepted "T25 a last_good 400 days" '            if future and v > self.now + FUTURE_SLACK:' '            if False:'
mutant R18-lock-left-after-a-run "T2 the lock was released" '        signal.alarm(0)
        if mode == "run":
            lock_release(ctx)' '        signal.alarm(0)
        if False:
            lock_release(ctx)'
mutant R19-proof-saved-only-at-the-end "T26 SIGTERM mid-copy" '        self.rows.append((rel, st3))
        if len(self.rows) >= PROOF_BATCH:
            self.flush()' '        self.rows.append((rel, st3))' '                            saver.flush()
                            for rel in todo_dirs:' '                            for rel in todo_dirs:' '                finally:
                    saver.flush()          # an interruption keeps every proof made so far' '                finally:
                    pass'
mutant R20-no-chunks "T26 SIGTERM: the engine reached its third chunk" '        if len(cur) >= chunk_files or nbytes >= CHUNK_BYTES:' '        if False:'
mutant R21-hold-refusal-starts-the-clock "T27 ... and does not start the clock" '        if status == "held":' '        if False:'
mutant R22-lifting-the-hold-keeps-the-old-clock "T27 the hold lifted four days" '        if not (st.get("held_seen") or legacy_held(st)):
            return False' '        if True:
            return False'
mutant R23-mount-not-rechecked-per-set "T27 ... the second set was not started" '            if not nas_is_smb_mounted(ctx):
                raise Refused("REFUSED — %s is no longer mounted as a network share (it was when this run started); "' '            if False:
                raise Refused("REFUSED — %s is no longer mounted as a network share (it was when this run started); "'
mutant R24-reused-group-id-is-an-engine "T27 the same group id now held" '    if pg and (owner or {}).get("engine_started") and pid_exists(pg) and proc_started(pg) != owner.get("engine_started"):' '    if False:'
mutant R25-duplicate-key-accepted "T22 a key given twice" '                if k in scalar_seen:' '                if False:'
mutant R26-emptying-patterns-accepted "T22 exclude_name=*.* on a first run" '    return (all(fnmatch.fnmatchcase(x, pt) for x in _PROBE_PLAIN)
            or all(fnmatch.fnmatchcase(x, pt) for x in _PROBE_DOTTED))' '    return False'
mutant R27-baseline-only-in-the-state-file "T22 ... the fall is still seen" '        last_counts = dict(index.baseline())' '        last_counts = {}'
mutant R28-tfvars-travel "T28 NOT ONE of the checker" '    if ".tfvars" in n:' '    if False:'
mutant R29-private-key-names-travel "T28 NOT ONE of the checker" '    if _RX_PRIVATE_KEY.search(n):' '    if False:'
mutant R30-local-settings-travels "T28 NOT ONE of the checker" '"local.settings.json", "application_default_credentials.json", ".dockercfg", ".vault-token",' '"application_default_credentials.json", ".dockercfg", ".vault-token",'
mutant R31-auth-folder-travels "T28 nor one of 25 more" '".docker", ".auth", "gcloud", ".secret", ".secrets")' '".docker", "gcloud", ".secret", ".secrets")'
mutant R32-sighup-not-handled "T26 SIGHUP: the lock is released" '        for sg in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):' '        for sg in (signal.SIGTERM, signal.SIGINT):'
mutant R33-damage-notice-cleared-by-a-good-run "T25 ... and the watch reports the damage to whoever asks" '    notices = ctx.damage_notices()
    for d in notices:' '    notices = [] if st.get("last_good") else ctx.damage_notices()
    for d in notices:'
mutant R34-cap-ignored-while-proving "T26 a copy stopped by the cap: exit 4" '                                if time.time() >= deadline:
                                    for r2 in todo[i:]:' '                                if False:
                                    for r2 in todo[i:]:' '            if time.time() >= deadline:
                kill_child()
                return ("killed-cap", None)' '            if False:
                kill_child()
                return ("killed-cap", None)'
mutant R35-unreached-sets-not-named "T26 ... a set the run never reached" '            if s["dest"] not in done_sets:' '            if False:'
wait

echo
C=0; SV=0
for n in $ORDER; do cat "$RUN/results/$n.txt"; if /usr/bin/grep -q -F '  CAUGHT ' "$RUN/results/$n.txt"; then C=$((C+1)); else SV=$((SV+1)); fi; done
echo
echo "=== $C mutants caught, $SV survived or broken (of $((C+SV))) — outputs kept under $RUN ==="
[ "$SV" -eq 0 ]
