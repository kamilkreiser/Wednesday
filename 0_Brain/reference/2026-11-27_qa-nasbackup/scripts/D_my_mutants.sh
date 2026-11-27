#!/bin/bash
# D — the checker's OWN mutants (none repeats one of the seat's 20). For each: copy the scratch copy of the lane,
# break ONE guard in the copy's nb_core.py, run the copy's tests/run.sh. CAUGHT = suite exit non-zero AND >=1 FAIL
# line. SURVIVED = the suite stayed green with the guard removed (the guard is untested).
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-nasbackup
SRC="$S/copy/WEDNESDAY/2_Project_Files"
RUN="$S/my_mutants_$$"; mkdir -p "$RUN"
PY=/opt/homebrew/bin/python3
CAUGHT=0; SURV=0; BROKEN=0
mutant() { # name  old new [old new ...]
  local name="$1"; shift
  local copy="$RUN/$name/WEDNESDAY/2_Project_Files/nas-backup"
  mkdir -p "$copy/tests" "$RUN/$name/WEDNESDAY/2_Project_Files/fleet/cockpit" "$RUN/$name/base"
  cp "$SRC/nas-backup/nb_core.py" "$SRC/nas-backup/nb_common.sh" "$SRC/nas-backup/nas_backup.sh" "$SRC/nas-backup/nas_backup_nightly.sh" "$SRC/nas-backup/nas_backup_watch.sh" "$copy/"
  cp "$SRC/nas-backup/tests/run.sh" "$copy/tests/"; cp "$SRC/fleet/cockpit/seat_resolve.sh" "$RUN/$name/WEDNESDAY/2_Project_Files/fleet/cockpit/"
  if [ "$name" != "CONTROL-unmutated" ]; then
    if ! "$PY" -c 'import sys
p, pairs = sys.argv[1], sys.argv[2:]
s = open(p, encoding="utf-8").read()
for i in range(0, len(pairs), 2):
    n = s.count(pairs[i])
    if n != 1:
        sys.stderr.write("target found %d times: %r\n" % (n, pairs[i])); sys.exit(1)
    s = s.replace(pairs[i], pairs[i + 1])
open(p, "w", encoding="utf-8").write(s)' "$copy/nb_core.py" "$@"; then BROKEN=$((BROKEN+1)); printf 'BROKEN    %s (mutation not applied)\n' "$name"; return; fi
  fi
  bash "$copy/tests/run.sh" "$RUN/$name/base" > "$RUN/$name/out.txt" 2>&1; local rc=$?
  local nf; nf="$(/usr/bin/grep -c -F '  FAIL  ' "$RUN/$name/out.txt")"; local np; np="$(/usr/bin/grep -c -F '  PASS  ' "$RUN/$name/out.txt")"
  if [ "$rc" -ne 0 ] && [ "$nf" -gt 0 ]; then CAUGHT=$((CAUGHT+1)); printf 'CAUGHT    %-34s exit %s, %s PASS, %s FAIL; first: %s\n' "$name" "$rc" "$np" "$nf" "$(/usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | head -1 | cut -c9-120)"
  else SURV=$((SURV+1)); printf 'SURVIVED  %-34s exit %s, %s PASS, %s FAIL\n' "$name" "$rc" "$np" "$nf"; fi
}
echo "mutants under $RUN"
mutant CONTROL-unmutated
[ "$SURV" -eq 1 ] || { echo "CONTROL did not pass: stop"; exit 1; }; SURV=0; echo "(the CONTROL line above reads SURVIVED because the unmutated suite is green: that is the control passing)"
mutant Q01-other-client-names-off '"other_client_names": ["*[Dd]atasec*", "*DATASEC*"],' '"other_client_names": [],'
mutant Q02-arrival-check-vacuous '                    if dsz == sv[0]:
                        observed_ok.add(rel)' '                    if True:
                        observed_ok.add(rel)'
mutant Q03-exclude_path-ignored '        if rel in self.paths:' '        if False:'
mutant Q04-exclude_name-ignored '        for p in ctx.conf["exclude_name"]:
            self.pats.append(("conf", p))' '        for p in []:
            self.pats.append(("conf", p))' '            if d == set_dest:
                self.pats.append(("conf", p))' '            if False:
                self.pats.append(("conf", p))'
mutant Q05-symlink-source-allowed '        if os.path.islink(s["src"]):' '        if False:'
mutant Q06-test-root-fence-off '    if not rt.startswith("/private/tmp/") or not os.path.isdir(rt):' '    if not os.path.isdir(rt):'
mutant Q07-dest-dotdot-allowed '            if not s["dest"] or s["dest"].startswith("/") or any(p in ("", ".", "..") for p in s["dest"].split("/")):' '            if False:'
mutant Q08-rsync-version-check-off '    if "openrsync" in r.stdout or "version 2." in first:' '    if False:'
mutant Q09-hash-sample-ignored '                            bad_hash.append(rel)' '                            pass'
mutant Q10-env-variants-allowed '".env", ".env.*", "*.env", "*.pem", "*.key", "*.p12", "*.pfx",' '".env", "*.pem",'
mutant Q11-type-conflict-silent '    if plan["type_conflicts"]:' '    if False:'
mutant Q12-source-errors-silent '    if src["errors"]:' '    if False:'
mutant Q13-dry-creates-on-nas '            if mode == "run":
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)' '            if True:
                ensure_dest_chain(os.path.join(c["nas_root"], s["client"]), [ctx.info["cap"], BACKUP_FOLDER], create=True)'
mutant Q14-window-never-closes '    return (o, c, o <= now < c)' '    return (o, c, o <= now)'
mutant Q15-complete-marker-always '                if good:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp)' '                if True:
                    with open(os.path.join(croot, "runs", "RUN_%s_COMPLETE.txt" % stamp)'
mutant Q16-forbid-source-off '                if f in comps:' '                if False:'
mutant Q17-seat-forbid-in-unlisted-off '        if st.get("seat") != self.seat:' '        if False:'
mutant Q18-state-attempt-cap '                                       "reason": reason}] + st.get("recent_attempts", []))[:12]' '                                       "reason": reason}] + st.get("recent_attempts", []))[:1]'
echo
echo "MY MUTANTS: $CAUGHT caught, $SURV survived, $BROKEN not applied (of $((CAUGHT+SURV+BROKEN)))"
