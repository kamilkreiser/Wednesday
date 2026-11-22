#!/bin/bash
# QA-WIN-FOLLOWUP item 1: the BASE (3337192) and HEAD (cf41a77) coagentd on macOS, each in a fresh
# data folder: one `status`, then a stop by signal (TERM, and INT as an extra). Key ids, pids and the
# folder masked; the reply and the whole stderr must be byte-identical. Also `--help` and one Unix
# refusal (a data folder that is a file). Positive control: one changed byte shows DIFFERENT.
W=/private/tmp/claude-501/qwf; O=$W/mc; rm -rf "$O" 2>/dev/null; mkdir -p $O $W/tools/tmp/mc
one() { # $1 label $2 binary $3 signal
  d=$W/tools/tmp/mc/$1-$3; [ -e "$d" ] && { echo "exists: $d"; exit 2; }
  "$2" --data-dir "$d" --idle-exit-secs 60 2> $O/$1-$3.log & pid=$!
  for i in $(seq 1 100); do [ -S "$d/ipc/daemon.sock" ] && break; sleep 0.1; done
  "$2" ctl --data-dir "$d" '{"v":1,"id":7,"cmd":"status","args":{}}' > $O/$1-$3.status 2>&1; echo "ctl exit $?" >> $O/$1-$3.status
  kill -$3 $pid; wait $pid; echo "exit $?" >> $O/$1-$3.log
  sed -E -i '' "s/[0-9a-f]{64}/<KEY>/g; s/\"pid\":[0-9]+/\"pid\":<PID>/; s#$d#<DIR>#g" $O/$1-$3.status $O/$1-$3.log
}
for s in TERM INT; do one base $W/t/b/debug/coagentd $s; one head $W/t/h/debug/coagentd $s; done
for b in b h; do $W/t/$b/debug/coagentd --help > $O/help-$b.txt 2>&1; echo "exit $?" >> $O/help-$b.txt; done
touch $W/tools/tmp/mc/afile
for b in b h; do $W/t/$b/debug/coagentd --data-dir $W/tools/tmp/mc/afile --idle-exit-secs 2 > $O/refuse-$b.txt 2>&1; echo "exit $?" >> $O/refuse-$b.txt; done
for s in TERM INT; do
  echo "== SIG$s status reply: $(cmp -s $O/base-$s.status $O/head-$s.status && echo BYTE-IDENTICAL || echo DIFFERENT)"; cat $O/head-$s.status
  echo "== SIG$s stderr: $(cmp -s $O/base-$s.log $O/head-$s.log && echo BYTE-IDENTICAL || echo DIFFERENT)"; cat $O/head-$s.log
done
echo "== --help: $(cmp -s $O/help-b.txt $O/help-h.txt && echo BYTE-IDENTICAL || echo DIFFERENT) ($(wc -l < $O/help-h.txt) lines)"
echo "== refusal (data folder is a file): $(cmp -s $O/refuse-b.txt $O/refuse-h.txt && echo BYTE-IDENTICAL || echo DIFFERENT)"; cat $O/refuse-h.txt
echo "== positive control: one changed byte must show DIFFERENT"
sed 's/"gate":"off"/"gate":"ofF"/' $O/head-TERM.status > $O/ctl.status; cmp -s $O/base-TERM.status $O/ctl.status && echo BYTE-IDENTICAL || echo DIFFERENT
sed 's/stopped/Stopped/' $O/head-TERM.log > $O/ctl.log; cmp -s $O/base-TERM.log $O/ctl.log && echo BYTE-IDENTICAL || echo DIFFERENT
