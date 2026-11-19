# probe helpers: start a gated daemon, feed hook events
W=/private/tmp/claude-501/qp1; B=$W/bin
REAL=$(cd $W && pwd -P)
RUNENV=(env -i PATH=/usr/bin:/bin HOME=$W/p/home TMPDIR=$W/p/tmp)
mkdir -p $W/p/home $W/p/tmp
startd() { # startd <datadir> <args...>
  local d=$1; shift
  "${RUNENV[@]}" $B/coagentd --data-dir $d --coagent $B/coagent --idle-exit-secs 600 "$@" </dev/null >/dev/null 2>>$d.log &
  echo $! > $d.pid
  for i in $(seq 1 100); do "${RUNENV[@]}" $B/coagentd ctl --data-dir $d '{"v":1,"id":1,"cmd":"status"}' >/dev/null 2>&1 && return 0; sleep 0.1; done; return 1
}
stopd() { kill -TERM $(cat $1.pid) 2>/dev/null; for i in $(seq 1 100); do kill -0 $(cat $1.pid) 2>/dev/null || return 0; sleep 0.1; done; kill -KILL $(cat $1.pid); }
ctl() { "${RUNENV[@]}" $B/coagentd ctl --data-dir $1 "$2"; }
ev() { # ev <session> <cwd> <mode> <tool> <input-json> [event-name]
  printf '{"session_id":"%s","transcript_path":"%s/t.jsonl","cwd":"%s","prompt_id":"p1","permission_mode":"%s","effort":{"level":"medium"},"hook_event_name":"%s","tool_name":"%s","tool_input":%s,"tool_use_id":"toolu_1"}' "$1" "$2" "$2" "$3" "${6:-PreToolUse}" "$4" "$5"
}
hk() { # hk <datadir> ; stdin = event ; prints rc/out/err
  local o e rc; o=$(mktemp $W/p/tmp/o.XXXX); e=$(mktemp $W/p/tmp/e.XXXX)
  "${RUNENV[@]}" $B/coagent-hook --data-dir $1 >$o 2>$e; rc=$?
  echo "rc=$rc out=$(cat $o) err=$(cat $e)"
}
san() { sed -e "s#$REAL#<qp1>#g" -e "s#$W#<qp1>#g"; }
