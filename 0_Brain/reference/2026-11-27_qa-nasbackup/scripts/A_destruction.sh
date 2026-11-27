#!/bin/bash
# A_destruction.sh — can any path lose content at the destination? Oracle: oracle.py (every content hash that was
# under the fake NAS before a run must still be somewhere under it after).
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
tailmsg() { /usr/bin/grep -E 'GOOD:|FAILED|PROBLEM|  - |REFUSED|Traceback|Error' "$T/out/$1.txt" | head -8 | cut -c1-330; }

say "### A0 POSITIVE CONTROL of the oracle: a destination file taken away by hand must be reported LOST"
fixture A0; rc=$(run "$(at 0 1 0)" r1); snap a
mkdir -p "$T/held"; mv -n "$(CUR)/a.txt" "$T/held/a.txt"
lost a | tail -2; verdict "A0 oracle fires on a removed file (rc of oracle)" 1 "${PIPESTATUS[0]}"

say; say "### A1-A4 changed / shrunk to zero / same-size change / removed at source"
fixture A1; printf 'AAAA' > "$T/vol/WEDNESDAY/same.txt"; echo "will shrink" > "$T/vol/WEDNESDAY/z.txt"
rc=$(run "$(at 0 1 0)" r1); verdict "A1 first run rc" 0 "$rc"; snap a
echo "new longer content of a" > "$T/vol/WEDNESDAY/a.txt"; : > "$T/vol/WEDNESDAY/z.txt"; sleep 1; printf 'BBBB' > "$T/vol/WEDNESDAY/same.txt"
mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/sub/b.txt" "$T/held/"
rc=$(run "$(at 1 1 0)" r2); verdict "A1-4 second run rc" 0 "$rc"; lost a | tail -1; verdict "A1-4 nothing lost" 0 "${PIPESTATUS[0]}"
verdict "A2 zero-byte now current" 0 "$(stat -f %z "$(CUR)/z.txt")"
verdict "A4 removed-at-source still at dest" yes "$([ -f "$(CUR)/sub/b.txt" ] && echo yes || echo no)"
find "$(VER)" -type f | sed "s|$T/||" | sort

say; say "### A5 a source FILE replaced by a DIRECTORY of the same name (with a child)"
fixture A5; echo "i was a file" > "$T/vol/WEDNESDAY/thing"
rc=$(run "$(at 0 1 0)" r1); snap a
mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/thing" "$T/held/thing"; mkdir "$T/vol/WEDNESDAY/thing"; echo "child" > "$T/vol/WEDNESDAY/thing/child.txt"
rc=$(run "$(at 1 1 0)" r2); say "A5 run rc=$rc"; tailmsg r2; lost a | tail -2; verdict "A5 nothing lost" 0 "${PIPESTATUS[0]}"
say "A5 dest 'thing' is now: $(stat -f %HT "$(CUR)/thing" 2>&1)"; find "$T/nas/General" -path '*thing*' | sed "s|$T/||"
rc=$(run "$(at 2 1 0)" r3); say "A5 NEXT night rc=$rc (state last_attempt=$(state last_attempt.status), last_good=$(state last_good.time_local))"; tailmsg r3
rc=$(run "$(at 3 1 0)" r4); say "A5 night after rc=$rc (state last_attempt=$(state last_attempt.status), last_good=$(state last_good.time_local))"

say; say "### A6 a source DIRECTORY replaced by a FILE of the same name"
fixture A6; mkdir "$T/vol/WEDNESDAY/thing"; echo "child" > "$T/vol/WEDNESDAY/thing/child.txt"
rc=$(run "$(at 0 1 0)" r1); snap a
mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/thing" "$T/held/thing"; echo "now a file" > "$T/vol/WEDNESDAY/thing"
rc=$(run "$(at 1 1 0)" r2); say "A6 run rc=$rc"; tailmsg r2; lost a | tail -2; verdict "A6 nothing lost" 0 "${PIPESTATUS[0]}"
rc=$(run "$(at 2 1 0)" r3); say "A6 NEXT night rc=$rc last_attempt=$(state last_attempt.status) last_good=$(state last_good.time_local)"
say "A6 is the new file content anywhere on the NAS? $(/usr/bin/grep -r -l 'now a file' "$T/nas" 2>&1 | wc -l | tr -d ' ') file(s)"

say; say "### A7 a source file replaced by a SYMLINK (to an in-scope file, and to a secret)"
fixture A7; echo "real" > "$T/vol/WEDNESDAY/r.txt"; mkdir "$T/vol/WEDNESDAY/4_Credentials"; echo "TOPSECRET-A7" > "$T/vol/WEDNESDAY/4_Credentials/k"
rc=$(run "$(at 0 1 0)" r1); snap a
mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/r.txt" "$T/held/"; ln -s 4_Credentials/k "$T/vol/WEDNESDAY/r.txt"; ln -s 4_Credentials "$T/vol/WEDNESDAY/creds_link"
rc=$(run "$(at 1 1 0)" r2); verdict "A7 rc" 0 "$rc"; lost a | tail -1; verdict "A7 nothing lost" 0 "${PIPESTATUS[0]}"
verdict "A7 secret content on NAS (grep -r count)" 0 "$(/usr/bin/grep -r -l 'TOPSECRET-A7' "$T/nas" 2>/dev/null | wc -l | tr -d ' ')"
verdict "A7 control: the secret IS findable at the source by the same grep" 1 "$(/usr/bin/grep -r -l 'TOPSECRET-A7' "$T/vol/WEDNESDAY/4_Credentials" 2>/dev/null | wc -l | tr -d ' ')"

say; say "### A8 a rename that differs ONLY BY CASE (scratch volume is case-insensitive, like the share), content changed"
fixture A8; echo "report v1" > "$T/vol/WEDNESDAY/report.txt"; printf 'SAME1' > "$T/vol/WEDNESDAY/keep.txt"; mkdir "$T/vol/WEDNESDAY/logs"; echo l1 > "$T/vol/WEDNESDAY/logs/l.txt"
rc=$(run "$(at 0 1 0)" r1); snap a
mv "$T/vol/WEDNESDAY/report.txt" "$T/vol/WEDNESDAY/tmp1"; mv "$T/vol/WEDNESDAY/tmp1" "$T/vol/WEDNESDAY/REPORT.txt"; echo "report v2 longer" > "$T/vol/WEDNESDAY/REPORT.txt"
mv "$T/vol/WEDNESDAY/keep.txt" "$T/vol/WEDNESDAY/tmp2"; mv "$T/vol/WEDNESDAY/tmp2" "$T/vol/WEDNESDAY/KEEP.txt"; sleep 1; printf 'SAME2' > "$T/vol/WEDNESDAY/KEEP.txt"
mv "$T/vol/WEDNESDAY/logs" "$T/vol/WEDNESDAY/tmp3"; mv "$T/vol/WEDNESDAY/tmp3" "$T/vol/WEDNESDAY/Logs"; echo l2-new > "$T/vol/WEDNESDAY/Logs/new.txt"; echo "l1 changed" > "$T/vol/WEDNESDAY/Logs/l.txt"
rc=$(run "$(at 1 1 0)" r2); verdict "A8 rc" 0 "$rc"; tailmsg r2; lost a | tail -2; verdict "A8 nothing lost" 0 "${PIPESTATUS[0]}"
say "A8 names at dest now: $($PY -c 'import os,sys; print(sorted(os.listdir(sys.argv[1])))' "$(CUR)")"
verdict "A8 current content of the renamed file" "report v2 longer" "$(cat "$(CUR)/REPORT.txt")"
verdict "A8 same-size renamed file current content" SAME2 "$(cat "$(CUR)/KEEP.txt")"

say; say "### A9 Unicode: the same name in NFC then NFD at the source, content changed"
fixture A9
"$PY" - "$T/vol/WEDNESDAY" <<'PYEOF'
import os,sys,unicodedata
d=sys.argv[1]; n=unicodedata.normalize("NFC","café.txt"); open(os.path.join(d,n),"w").write("nfc v1\n")
PYEOF
rc=$(run "$(at 0 1 0)" r1); snap a
"$PY" - "$T/vol/WEDNESDAY" <<'PYEOF'
import os,sys,unicodedata
d=sys.argv[1]; nfc=unicodedata.normalize("NFC","café.txt"); nfd=unicodedata.normalize("NFD","café.txt")
os.rename(os.path.join(d,nfc), os.path.join(d,"tmp9")); os.rename(os.path.join(d,"tmp9"), os.path.join(d,nfd))
open(os.path.join(d,nfd),"w").write("nfd v2 longer\n")
print("source names now:", [ascii(x) for x in os.listdir(d) if x.startswith("caf")])
PYEOF
rc=$(run "$(at 1 1 0)" r2); verdict "A9 rc" 0 "$rc"; tailmsg r2; lost a | tail -2; verdict "A9 nothing lost" 0 "${PIPESTATUS[0]}"
"$PY" -c 'import os,sys; print("dest names:", [ascii(x) for x in os.listdir(sys.argv[1]) if x.startswith("caf")])' "$(CUR)"

say; say "### A12 source folders named like the tool's own (versions, current, _tmp_incoming, manifests, runs) and a second-night change"
fixture A12; for n in versions current _tmp_incoming manifests runs nightly-backup; do mkdir -p "$T/vol/WEDNESDAY/$n"; echo "src $n v1" > "$T/vol/WEDNESDAY/$n/f.txt"; done
rc=$(run "$(at 0 1 0)" r1); verdict "A12 rc" 0 "$rc"; snap a
for n in versions current _tmp_incoming manifests runs nightly-backup; do echo "src $n v2 changed" > "$T/vol/WEDNESDAY/$n/f.txt"; done
rc=$(run "$(at 1 1 0)" r2); verdict "A12 rc2" 0 "$rc"; lost a | tail -1; verdict "A12 nothing lost" 0 "${PIPESTATUS[0]}"
verdict "A12 six previous copies kept" 6 "$(find "$(VER)" -name f.txt | wc -l | tr -d ' ')"

say; say "### A13 the versions/ folder is not writable when a changed file must be versioned"
fixture A13; rc=$(run "$(at 0 1 0)" r1); snap a
echo "changed content, longer" > "$T/vol/WEDNESDAY/a.txt"; chmod 555 "$(VER)"
rc=$(run "$(at 1 1 0)" r2); chmod 755 "$(VER)"; say "A13 rc=$rc"; tailmsg r2; lost a | tail -2; verdict "A13 nothing lost" 0 "${PIPESTATUS[0]}"
verdict "A13 the run is NOT recorded good" "failed" "$(state last_attempt.status)"

say; say "### A14 DRY run against an existing destination with pending changes writes nothing to the NAS"
fixture A14; rc=$(run "$(at 0 1 0)" r1); echo "changed" > "$T/vol/WEDNESDAY/a.txt"; echo new > "$T/vol/WEDNESDAY/n.txt"
b="$(find "$T/nas" -exec stat -f '%N|%z|%m|%c' {} + | shasum -a 256)"
nb --dry > "$T/out/dry.txt" 2>&1; rc=$?; nb > "$T/out/dry2.txt" 2>&1
a="$(find "$T/nas" -exec stat -f '%N|%z|%m|%c' {} + | shasum -a 256)"
verdict "A14 dry rc" 0 "$rc"; verdict "A14 NAS tree stat-listing unchanged by two dry runs" "$b" "$a"
echo x > "$T/nas/General/touched"; a2="$(find "$T/nas" -exec stat -f '%N|%z|%m|%c' {} + | shasum -a 256)"
verdict "A14 CONTROL: the listing hash changes when a file is added (differs=yes)" yes "$([ "$b" != "$a2" ] && echo yes || echo no)"
/usr/bin/grep -c 'to copy: 2 files' "$T/out/dry.txt"
