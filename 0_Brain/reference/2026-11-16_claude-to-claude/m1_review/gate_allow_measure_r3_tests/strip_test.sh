#!/bin/bash
# QA-R3: does scan_bytes.py's stripping of SYNTHETIC literals (only in files named redact.py / scan_bytes.py) hide a real hit?
# usage: strip_test.sh <spike dir of my clone at head> <work dir>
S=$1; D=$2/striptest; mkdir -p "$D/a" "$D/b"
for d in a b; do cp "$S/redact.py" "$D/$d/$( [ $d = a ] && echo redact.py || echo other_name.py)"; done
for f in "$D/a/redact.py" "$D/b/other_name.py"; do
  { echo '# QA-R3 plant 1 (real-shaped mail, other domain): planted.qa3@example.net'
    echo "# QA-R3 plant 2 (config dir, a workspace class of redact.py): $CLAUDE_CONFIG_DIR/x"
    echo '# QA-R3 plant 3 (adversarial: a value that CONTAINS a synthetic literal): alex@example.org msg_01ABCDEFGHIJKLMNtail9'
  } >> "$f"; done
python3 -I -B "$S/scan_bytes.py" --control "$D/a/redact.py" "$D/b/other_name.py"
echo "-- plant 3 alone, in a file named redact.py:"
printf '# alex@example.org msg_01ABCDEFGHIJKLMNtail9\n' > "$D/a/only3/redact.py" 2>/dev/null || { mkdir -p "$D/a/only3"; printf '# alex@example.org msg_01ABCDEFGHIJKLMNtail9\n' > "$D/a/only3/redact.py"; }
python3 -I -B "$S/scan_bytes.py" --control "$D/a/only3/redact.py"; echo "exit $?"
