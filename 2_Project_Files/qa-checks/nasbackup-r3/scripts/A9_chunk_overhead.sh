#!/bin/bash
# A9 — measured per-chunk overhead on the fake NAS (a local APFS folder: NOT the SMB share). Same 20,000 small files copied
# three ways: one chunk, 100 chunks of 200 (the default), 400 chunks of 50. Overhead per chunk = (t_chunked - t_single) / (chunks - 1).
. "$(dirname "$0")/lib3.sh"; date; uptime
mk() { fixture "$1"; "$PY" -c 'import os,sys
d=sys.argv[1]
for i in range(20000):
    sub=os.path.join(d,"d%03d"%(i%100)); os.makedirs(sub,exist_ok=True); open(os.path.join(sub,"f%05d.txt"%i),"w").write("payload %d\n"%i)' "$T/vol/WEDNESDAY/bulk"; }
t() { local s e; s=$("$PY" -c 'import time; print(time.time())'); rc=$(run "$(at 0 1 0)" r); e=$("$PY" -c 'import time; print(time.time())')
  "$PY" -c 'import sys; print("%.1f" % (float(sys.argv[2])-float(sys.argv[1])))' "$s" "$e"; }
for spec in "one 30000" "c200 200" "c50 50" "one_again 30000" "c200_again 200"; do set -- $spec
  mk "$1"; CONF_CHUNK="$2"; CONF_MAXS=3000; std_conf; el=$(t)
  say "$(uptime | sed 's/.*load/load/') | chunk_files=$2: wall ${el} s, rc=$(tail -1 "$T/o/r.txt" >/dev/null; echo $RC) GOOD=$(good r) engine calls=$(/usr/bin/grep -c -F 'engine pass' "$T/o/r.txt") files proven=$(line r 'proven at the destination' 1 60 | sed 's/^ *//')"
done
date; uptime
