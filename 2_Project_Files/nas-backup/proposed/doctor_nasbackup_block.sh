# doctor_nasbackup_block.sh — the nightly NAS backup's block for doctor.sh (WED-170, round 2). SOURCED by doctor.sh:
#     . "$PROJECT_DIR/2_Project_Files/nas-backup/proposed/doctor_nasbackup_block.sh"
# It needs doctor's own ok / warn / fail helpers and PROJECT_DIR, nothing else. It is a FILE, not pasted lines,
# so tests/run.sh exercises exactly what doctor will run (T8, T16, T24).
#
# THIS IS THE CHANNEL BY WHICH THE THREE-DAY CARD REACHES A SEAT (QA finding 6). While a card is due and no seat
# has recorded it as raised, this prints a HARD-failure line (doctor's "fail") that names the one command to run.
# The launcher carries doctor's hard-failure lines into the boot prompt on a rotation and stops a human launch
# to show them; it cuts each line at 400 characters, so the line is kept short and the command comes first.
# Once a seat has added the card and run --mark-raised it drops to a warning.
#
# THE SEAT comes from the TREE (tools/seat_note.sh), never from a default (QA minor: doctor's own default made a
# TUESDAY tree look at HOLD_wednesday). HELD is reported at most ONCE A DAY per seat.
NB_DIR="$PROJECT_DIR/2_Project_Files/nas-backup"
_nb_seat=""
if [ -f "$PROJECT_DIR/2_Project_Files/tools/seat_note.sh" ]; then
  . "$PROJECT_DIR/2_Project_Files/tools/seat_note.sh"
  if seat_note_dir "$PROJECT_DIR" doctor-nasbackup 2>&1; then _nb_seat="$SEAT_NOTE_SEAT"; fi
fi
_nb_lane="$NB_DIR"; [ -n "${NB_TEST_ROOT:-}" ] && _nb_lane="$NB_TEST_ROOT/lane"
_nb_now=(); [ -n "${NB_TEST_ROOT:-}" ] && [ -n "${NB_DOCTOR_NOW:-}" ] && _nb_now=( --now "$NB_DOCTOR_NOW" )
if [ -z "$_nb_seat" ]; then
  warn "nas-backup: seat of this tree unknown" "tools/seat_note.sh could not name the seat of $PROJECT_DIR; the NAS backup check was NOT run"
elif [ ! -x "$NB_DIR/nas_backup_watch.sh" ]; then
  warn "nas-backup/nas_backup_watch.sh missing" "restore it from git (chmod +x): without it a backup that stopped is invisible"
elif [ -e "$_nb_lane/HOLD_$_nb_seat" ]; then
  _nb_mark="$_nb_lane/state/doctor_held_$_nb_seat.last"
  if [ "$(cat "$_nb_mark" 2>&1)" = "$(date +%F)" ]; then
    ok "nightly NAS backup: held for seat $_nb_seat (already reported today)"
  else
    warn "nightly NAS backup HELD (seat $_nb_seat)" "by design: nas-backup/HOLD_$_nb_seat. Lifting it is the coordinator's word on Kam's instruction (reported once a day)"
    mkdir -p "$_nb_lane/state" && date +%F > "$_nb_mark"
  fi
else
  _nb_out="$(bash "$NB_DIR/nas_backup_watch.sh" --check ${_nb_now[@]+"${_nb_now[@]}"} 2>&1)"; _nb_rc=$?
  _nb_line="$(printf '%s\n' "$_nb_out" | head -1 | cut -c1-200)"
  case "$_nb_rc" in
    0) ok "nightly NAS backup: $_nb_line" ;;
    3) fail "NO GOOD NAS BACKUP FOR 3 DAYS" "RUN: bash 2_Project_Files/nas-backup/nas_backup_watch.sh --card   then add the ONE card it prints for Kam and run --mark-raised <its id>. Do NOT run a backup outside the window without his ruling. [$_nb_line]" ;;
    4) warn "no good NAS backup for 3 days" "the card for Kam is recorded as raised; nothing more until he rules or a backup completes. [$_nb_line]" ;;
    *) warn "nas_backup_watch.sh exited $_nb_rc" "$_nb_line" ;;
  esac
fi
