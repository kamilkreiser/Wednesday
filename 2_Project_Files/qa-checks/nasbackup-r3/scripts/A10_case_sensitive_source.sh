#!/bin/bash
# A10 — the real drive is Case-sensitive APFS and the share folds case; the lane's suite and both earlier checks ran on a case-FOLDING
# scratch volume. Here the SOURCE is a case-sensitive APFS disk image (a file under /private/tmp/qa3nb, mounted at <fixture>/vol,
# -nobrowse, detached at the end) and the fake NAS is the ordinary case-folding scratch volume.
. "$(dirname "$0")/lib3.sh"; date; uptime
IMG="$S/cs_$$.sparseimage"
T="$FXBASE/cs"; mkdir -p "$T/vol" "$T/nas/General" "$T/nas/Secuura" "$T/lane/seats" "$T/stub" "$T/o"
hdiutil create -size 300m -type SPARSE -fs "Case-sensitive APFS" -volname qa3cs "$IMG" > "$T/o/hdi_create.txt" 2>&1 || { cat "$T/o/hdi_create.txt"; exit 1; }
hdiutil attach "$IMG" -mountpoint "$T/vol" -nobrowse -owners on > "$T/o/hdi_attach.txt" 2>&1 || { cat "$T/o/hdi_attach.txt"; exit 1; }
trap 'hdiutil detach "$T/vol" > "$T/o/hdi_detach.txt" 2>&1; echo "image detached rc=$? ; still mounted: $(mount | /usr/bin/grep -c -F "$T/vol")"' EXIT
W="$T/vol/WEDNESDAY"; mkdir -p "$W/sub"; echo "content of a" > "$W/a.txt"; echo b > "$W/sub/b.txt"; echo 5000 > "$T/free_gib.txt"
say "source volume: $(diskutil info "$T/vol" | /usr/bin/grep -i 'File System Personality' | sed 's/^ *//') ; fake NAS volume folds case: $(touch "$T/nas/CaseProbe"; [ -e "$T/nas/caseprobe" ] && echo yes || echo no)"
echo one > "$W/Probe"; echo two > "$W/probe"; say "control: the source holds both Probe and probe: $(ls "$W" | /usr/bin/grep -c -i '^probe$')"
mkdir -p "$W/Logs" "$W/logs" "$W/pair"; echo L1 > "$W/Logs/x.txt"; echo l2 > "$W/logs/y.txt"; echo P1 > "$W/pair/Readme.md"; echo p2 > "$W/pair/README.md"; echo ok > "$W/pair/other.md"
"$PY" - "$W" <<'PYEOF'
import os, sys
W = sys.argv[1]; d = os.path.join(W, "fold"); os.makedirs(d)
pairs = [("ı.txt", "i.txt"), ("ıb.txt", "Ib.txt"), ("straße.txt", "strasse.txt"), ("ſx.txt", "sx.txt"), ("İc.txt", "i̇c.txt"), ("Kd.txt", "kd.txt"),
         ("ςe.txt", "σe.txt"), ("ﬁf.txt", "fif.txt"), ("ég.txt", "ég.txt"), ("ǅh.txt", "ǆh.txt"), ("ẞj.txt", "ßj.txt"), ("ͅk.txt", "ιk.txt")]
n = 0
for a, b in pairs:
    for x in (a, b):
        try:
            open(os.path.join(d, x), "x").write("FOLD %r\n" % x); n += 1
        except OSError as e:
            print("  source refused %r: %s" % (x, e.strerror))
print("  planted %d fold-probe files in %d pairs" % (n, len(pairs)))
PYEOF
std_conf; write_mounts
rc=$(run "$(at 0 1 0)" r0); say "night0 rc=$rc GOOD=$(good r0) ; $(line r0 'NOT BACKED UP' 1 200 | sed 's/^ *//')"
say "  $(line r0 'proven at the destination' 1 80 | sed 's/^ *//')"
"$PY" - "$W" "$(CURG)/WEDNESDAY" <<'PYEOF'
import os, sys, hashlib
src, dst = sys.argv[1], sys.argv[2]
def h(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
tot = miss = wrong = 0; bad = []
for dp, dn, fn in os.walk(src):
    for f in fn:
        p = os.path.join(dp, f); rel = os.path.relpath(p, src); tot += 1
        q = os.path.join(dst, rel)
        if not os.path.exists(q): miss += 1; bad.append("absent: %r" % rel)
        elif h(p) != h(q): wrong += 1; bad.append("OTHER CONTENT: %r" % rel)
print("  ORACLE: %d source files; at the destination path: %d absent, %d holding ANOTHER file's content" % (tot, miss, wrong))
for b in bad: print("     " + b)
PYEOF
say "  the manifest names the left-out names: $("$PY" -c 'import json,glob,sys
m=json.load(open(sorted(glob.glob(sys.argv[1]+"/lane/manifests/wednesday/*_run_manifest.json"))[-1])); s=m["sets"][0]; print(s["case_collision_files_not_backed_up"], sorted(s["case_collision_names"]))' "$T" | cut -c1-600)"
say "== a case-only rename between two nights (a.txt -> A.TXT, new content), then between plan and proof (sub/b.txt -> sub/B.txt)"
mv "$W/a.txt" "$W/A.TXT"; echo "content of A, changed and longer" > "$W/A.TXT"
CONF_RSYNC="$(mk_stub ren 'if [ "$N" = 1 ]; then mv "$V/sub/b.txt" "$V/sub/B.txt"; fi; exec "$REAL" "$@"')"; std_conf
rc=$(run "$(at 1 1 0)" r1); say "night1 rc=$rc GOOD=$(good r1) ; destination spelling: $(ls "$(CURG)/WEDNESDAY" | /usr/bin/grep -i '^a.txt$') holds: $(cat "$(CURG)/WEDNESDAY/a.txt") ; $(line r1 'DELETED AT SOURCE' 1 90 | sed 's/^ *//')"
CONF_RSYNC=""; std_conf; rc=$(run "$(at 2 1 0)" r2); say "night2 rc=$rc GOOD=$(good r2) ; sub/ at destination: $(ls "$(CURG)/WEDNESDAY/sub" | tr '\n' ' ') ; $(line r2 'to copy:' 1 60 | sed 's/^ *//')"
say "== the HOLD file spelled in another case on a case-SENSITIVE drive (hold_wednesday): is the run held?"
echo held > "$T/lane/hold_wednesday"; say "  (the lane's state folder is on the case-folding scratch volume here, as in every fixture: rc=$(run "$(at 3 1 0)" r3); on the real drive the lane itself is case-sensitive: NOT TESTED)"
date; uptime
