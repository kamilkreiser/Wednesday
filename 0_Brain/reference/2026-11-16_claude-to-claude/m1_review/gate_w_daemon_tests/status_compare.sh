#!/bin/bash
# QA-W-DAEMON: Unix `status` reply and start/stop log of the BASE coagentd vs the HEAD coagentd,
# each in a fresh data folder; SIGTERM for one start and SIGINT for a second. Key ids, pids and
# the folder are masked; everything else must be byte-identical.
W=/private/tmp/claude-501/qwd; O=$W/sc; mkdir -p $O
one() { # $1 label $2 binary $3 signal
  d=$W/tools/tmp/sc-$1-$3; mkdir -p $(dirname $d)
  "$2" --data-dir "$d" --idle-exit-secs 60 2> $O/$1-$3.log & pid=$!
  for i in $(seq 1 100); do [ -S "$d/ipc/daemon.sock" ] && break; sleep 0.1; done
  "$2" ctl --data-dir "$d" '{"v":1,"id":7,"cmd":"status","args":{}}' > $O/$1-$3.status 2>&1
  kill -$3 $pid; wait $pid; echo "exit $?" >> $O/$1-$3.log
  sed -E -i '' "s/[0-9a-f]{64}/<KEY>/g; s/\"pid\":[0-9]+/\"pid\":<PID>/; s#$d#<DIR>#g" $O/$1-$3.status $O/$1-$3.log
}
for s in TERM INT; do one base $W/target-b/debug/coagentd $s; one head $W/target-hb/debug/coagentd $s; done
for s in TERM INT; do
  echo "== SIG$s status reply: $(cmp -s $O/base-$s.status $O/head-$s.status && echo BYTE-IDENTICAL || echo DIFFERENT)"; cat $O/head-$s.status | cut -c1-400
  echo "== SIG$s log: $(cmp -s $O/base-$s.log $O/head-$s.log && echo BYTE-IDENTICAL || echo DIFFERENT)"; cat $O/head-$s.log
done
echo "== positive control: a reply with one byte changed must show DIFFERENT"; sed 's/"gate":"off"/"gate":"of!"/' $O/head-TERM.status > $O/ctl.status; cmp -s $O/base-TERM.status $O/ctl.status && echo BYTE-IDENTICAL || echo DIFFERENT
