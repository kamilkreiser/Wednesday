#!/bin/bash
# A3 — item 1: can a file that STILL EXISTS be counted "deleted at source"? Every stub acts on the first engine call, between plan and proof.
. "$(dirname "$0")/lib3.sh"; date; uptime
t() { # name, stub body, [extra setup already done]
  CONF_RSYNC="$(mk_stub "$1" "$2")"; std_conf
  local rc; rc=$(run "$(at 0 1 0)" r)
  say "  $1: rc=$rc GOOD=$(good r) deleted-line: $(line r 'DELETED at the source during' 1 90) | first NOT DELIVERED: $(line r 'NOT DELIVERED:' 1 150)"; }
say "== a. parent folder REPLACED by another folder of the same name (files live on in sub.old)"
fixture a; t parent_swapped 'if [ "$N" = 1 ]; then mv "$V/sub" "$V/sub.old"; mkdir "$V/sub"; fi; "$REAL" "$@"; exit $?'
say "     the file still exists at: $(find "$T/vol" -name b.txt | sed "s|$T/||")"
say "== b. parent folder replaced by a SYMLINK to a listable folder outside the set"
fixture b; mkdir -p "$T/vol/elsewhere"; t parent_symlink 'if [ "$N" = 1 ]; then mv "$V/sub" "$STUBDIR/taken/sub"; ln -s "$STUBDIR/../vol/elsewhere" "$V/sub"; fi; "$REAL" "$@"; exit $?'
say "== c. file renamed to a name differing only in CASE and made unreadable (this scratch volume folds case)"
fixture c; t case_rename_000 'if [ "$N" = 1 ]; then mv "$V/sub/b.txt" "$V/sub/tmpname"; mv "$V/sub/tmpname" "$V/sub/B.TXT"; chmod 000 "$V/sub/B.TXT"; fi; "$REAL" "$@"; exit $?'
say "     listing of sub: $(ls "$T/vol/WEDNESDAY/sub" | tr '\n' ' ') ; path sub/b.txt still resolves: $([ -e "$T/vol/WEDNESDAY/sub/b.txt" ] && echo YES || echo no)"
chmod 644 "$T/vol/WEDNESDAY/sub/B.TXT"
say "== c2. the same rename, file left readable (control: must be PROVEN through the folded name)"
fixture c2; t case_rename 'if [ "$N" = 1 ]; then mv "$V/sub/b.txt" "$V/sub/tmpname"; mv "$V/sub/tmpname" "$V/sub/B.TXT"; fi; "$REAL" "$@"; exit $?'
say "== d. file replaced by a FIFO, by a socket-like special, by a symlink (same name stays in the listing)"
fixture d1; t to_fifo 'if [ "$N" = 1 ]; then mv "$V/sub/b.txt" "$STUBDIR/taken/"; mkfifo "$V/sub/b.txt"; fi; "$REAL" "$@"; exit $?'
fixture d2; t to_symlink 'if [ "$N" = 1 ]; then mv "$V/sub/b.txt" "$STUBDIR/taken/"; ln -s ../a.txt "$V/sub/b.txt"; fi; "$REAL" "$@"; exit $?'
say "== e. name absent at the first listing, back before the second (re-created 0.1 s later by a background writer)"
fixture e; t reappears 'if [ "$N" = 1 ]; then mv "$V/sub/b.txt" "$STUBDIR/taken/b.keep"; ( while [ ! -e "$STUBDIR/stopflap" ]; do if [ ! -e "$V/sub/b.txt" ]; then sleep 0.1; echo back > "$V/sub/b.txt"; fi; sleep 0.02; done ) & fi; "$REAL" "$@"; exit $?'
: > "$T/stub/stopflap"
say "== f. the unit function on more shapes"
fixture f; U="$T/u"; mkdir -p "$U/root/dir" "$U/root/emptied" "$U/away"; echo x > "$U/root/dir/Here.txt"; ln -s "$U/away" "$U/root/linkdir"; mkfifo "$U/root/dir/pipe"
"$PY" - "$LANE" "$U" <<'PYEOF'
import os, sys, unicodedata
sys.path.insert(0, sys.argv[1]); import nb_core
U = sys.argv[2]; r = os.stat(U + "/root"); rid = (r.st_dev, r.st_ino)
print("  case-differing name present (dir/here.txt asked, Here.txt on disk; path resolves=%s): deleted=%s" % (os.path.exists(U + "/root/dir/here.txt"), nb_core.source_deleted(U + "/root", rid, "dir/here.txt")))
nfc = unicodedata.normalize("NFC", "café.txt"); nfd = unicodedata.normalize("NFD", nfc)
open(U + "/root/dir/" + nfd, "w").write("x")
print("  NFD on disk, NFC asked (path resolves=%s): deleted=%s" % (os.path.exists(U + "/root/dir/" + nfc), nb_core.source_deleted(U + "/root", rid, "dir/" + nfc)))
print("  parent is a symlink to a listable folder without the name: deleted=%s" % nb_core.source_deleted(U + "/root", rid, "linkdir/x.txt"))
print("  name present as a FIFO: deleted=%s" % nb_core.source_deleted(U + "/root", rid, "dir/pipe"))
print("  emptied folder: deleted=%s" % nb_core.source_deleted(U + "/root", rid, "emptied/x.txt"))
for planned, mf, mfr in ((587130, 5, 0.001), (587130, 100, 0.01), (265280, 100, 0.01), (10, 100, 0.01)):
    print("  deleted_allowed(planned=%d, max_files=%d, fraction=%g) = %d" % (planned, mf, mfr, nb_core.deleted_allowed({"max_deleted_files": mf, "max_deleted_fraction": mfr}, planned)))
real = [265280, 587130, 145279, 6322] + [8099 // 11] * 11
print("  real 15 sets, defaults: total allowed deleted on a GOOD night = %d ; at the conf ceiling (100 files, 1%%) = %d" % (
    sum(nb_core.deleted_allowed({"max_deleted_files": 5, "max_deleted_fraction": 0.001}, n) for n in real),
    sum(nb_core.deleted_allowed({"max_deleted_files": 100, "max_deleted_fraction": 0.01}, n) for n in real)))
PYEOF
say "== g. conf ceiling: max_deleted_files=101 and max_deleted_fraction=0.02 (must be refused), 100 and 0.01 (accepted)"
fixture g; std_conf "max_deleted_files=101"; say "  101: rc=$(run "$(at 0 1 0)" r1) $(line r1 'numeric keys' 1 80)"
std_conf "max_deleted_fraction=0.02"; say "  0.02: rc=$(run "$(at 0 1 0)" r2) $(line r2 'numeric keys' 1 80)"
std_conf "max_deleted_files=100" "max_deleted_fraction=0.01"; say "  100 and 0.01: rc=$(run "$(at 0 1 0)" r3)"
std_conf "max_deleted_files=-1"; say "  -1: rc=$(run "$(at 0 1 1)" r4)"
say "== h. many deletions: 700 of 1000 files deleted mid-run at the ceiling conf; are ALL named in the last lines / manifest / state?"
fixture h; for i in $(seq 1 1000); do echo "f $i" > "$T/vol/WEDNESDAY/sub/t$i.txt"; done
for i in $(seq 1 70000); do :; done
"$PY" -c 'import os,sys
d=sys.argv[1]
for i in range(1001, 70001): open("%s/t%d.txt" % (d, i), "w").write("f")' "$T/vol/WEDNESDAY/sub"
CONF_RSYNC="$(mk_stub del650 'if [ "$N" = 1 ]; then for i in $(seq 60001 60650); do mv "$V/sub/t$i.txt" "$STUBDIR/taken/"; done; fi; "$REAL" "$@"; exit $?')"; CONF_CHUNK=70010
std_conf "max_deleted_files=100" "max_deleted_fraction=0.01"
rc=$(run "$(at 0 1 0)" r); say "  70,002 planned, 650 deleted (allowed 1% = 700): rc=$rc GOOD=$(good r)"
say "  DELETED AT SOURCE lines in the run's last lines: $(/usr/bin/grep -c -F '  DELETED AT SOURCE:' "$T/o/r.txt") ; 'and N more' line: $(line r '... and' 1 80)"
"$PY" -c 'import json,glob,sys
m=json.load(open(sorted(glob.glob(sys.argv[1]+"/lane/manifests/wednesday/*_run_manifest.json"))[-1]))
s=json.load(open(sys.argv[1]+"/lane/state/wednesday.json"))
print("  manifest deleted_during_run names: %d ; per-set deleted_count=%s names=%d ; state last_good.deleted_during_run names: %d" % (len(m["deleted_during_run"]), m["sets"][0].get("deleted_count"), len(m["sets"][0].get("deleted_during_run", [])), len((s.get("last_good") or {}).get("deleted_during_run", []))))' "$T"
date; uptime
