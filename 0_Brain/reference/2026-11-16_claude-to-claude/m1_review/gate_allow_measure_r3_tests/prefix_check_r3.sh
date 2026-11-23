#!/bin/bash
# usage: prefix_check_r3.sh <clone> <base> <head> <path> <tmpdir>
# PREFIX if the base file is a byte-for-byte prefix of the head file; plus a 1-byte-flip control.
# Adapted from the r2 check's prefix_check.sh (tmp dir passed in instead of mktemp; python -I -B).
C=$1; B=$2; H=$3; F=$4; T=$5; mkdir -p "$T"
git -C "$C" show "$B:$F" > "$T/b"; git -C "$C" show "$H:$F" > "$T/h"
python3 -I -B - "$T/b" "$T/h" "$F" <<'PY'
import sys
b=open(sys.argv[1],'rb').read(); h=open(sys.argv[2],'rb').read(); f=sys.argv[3]
print(("PREFIX" if h.startswith(b) else "NOT-PREFIX"), f, "base=%d head=%d appended=%d"%(len(b),len(h),len(h)-len(b)))
c=bytearray(b); c[len(c)//2]^=1
print("  control (1 byte flipped in base copy):", "detected OK" if not h.startswith(bytes(c)) else "CONTROL FAILED")
PY
rm "$T/b" "$T/h"
