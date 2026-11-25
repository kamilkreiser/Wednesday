#!/bin/bash
# QA-SCANNER-NEXT: two copies of the head with the FLAG rule loosened for the upper-case forms (scratch, never committed):
#   qa_loose_case = `-u`/`--user` tested on the bytes as written (so -U=/--USER= are not `user`)
#   qa_loose_b    = form (b) (`--user=a:b` / `-u=a:b`) switched off entirely
set -eu
C="$1"; T="$C/crates/coagent-scanner/tests"
for d in qa_loose_case qa_loose_b; do mkdir -p "$T/$d"; cp "$T/qa_headcopy/mod.rs" "$T/$d/mod.rs"; cp "$T/qa_headcopy/families.rs" "$T/$d/families.rs"; done
python3 -B -I -c 'import sys
def sub(p,o,n):
    s=open(p).read(); assert s.count(o)==1,(p,o); open(p,"w").write(s.replace(o,n))
sub(sys.argv[1]+"/qa_loose_case/families.rs", "let user = name == b\"-u\" || name == b\"--user\";", "let user = &b[i..e] == b\"-u\" || &b[i..e] == b\"--user\";")
sub(sys.argv[1]+"/qa_loose_b/families.rs", "if forms && user && b.get(e) == Some(&b'"'"'='"'"') {", "if false && user && b.get(e) == Some(&b'"'"'='"'"') {")' "$T"
for d in qa_loose_case qa_loose_b; do echo "$d: $(diff "$T/qa_headcopy/families.rs" "$T/$d/families.rs" | grep -c '^>') line(s) changed vs the head copy"; done
