#!/bin/bash
# QA-MEASURE-2 4.7: E3 rehearsal (NO model) in MY OWN private tmux server qm2-<random>, created and killed here.
# Two reader panes (windows A, B) stand for the dialog: `read -r -t 20`, result to a file in my work dir.
# Routes from this process: r1 tmux send-keys, r2 TIOCSTI on the pane's device opened by path, r3 a plain write to it.
# Negative control: each route is first aimed at B with B's token; A must never get it.  usage: bash qm2_e3.sh <work dir>
W="$1/e3"; mkdir -p "$W"; TS="qm2-$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 6)"; TM=(tmux -L "$TS")
echo "runner tty=$(tty 2>&1) ps_tt=$(ps -o tt= -p $$) server=qm2-<random>"
TIOC='import errno,fcntl,os,sys,termios
dev,s=sys.argv[1],sys.argv[2].encode()+b"\r"
try: fd=os.open(dev,os.O_RDWR|os.O_NOCTTY)
except OSError as e: print("TIOCSTI open failed errno=%d (%s)"%(e.errno,errno.errorcode.get(e.errno))); sys.exit(0)
ok=0
for ch in s:
    try: fcntl.ioctl(fd,termios.TIOCSTI,bytes([ch])); ok+=1
    except OSError as e: print("TIOCSTI ioctl failed after %d bytes errno=%d (%s)"%(ok,e.errno,errno.errorcode.get(e.errno))); break
else: print("TIOCSTI ok for all %d bytes"%ok)'
for r in r1 r2 r3; do
  echo "## route $r"
  "${TM[@]}" new-session -d -s "$TS" -n A -x 100 -y 20 "cd '$W' && printf 'reader A: '; IFS= read -r -t 20 L; echo \"A_GOT=[\$L] rc=\$?\" >> A.$r.out; sleep 60"
  "${TM[@]}" new-window -t "$TS" -n B "cd '$W' && printf 'reader B: '; IFS= read -r -t 20 L; echo \"B_GOT=[\$L] rc=\$?\" >> B.$r.out; sleep 60"
  sleep 1; PTA=$("${TM[@]}" display -p -t "$TS:A" '#{pane_tty}'); PTB=$("${TM[@]}" display -p -t "$TS:B" '#{pane_tty}')
  echo "  pane modes: A $(ls -l "$PTA" | awk '{print $1}') B $(ls -l "$PTB" | awk '{print $1}')"
  for tgt in B A; do
    tok="QA${r}${tgt}"; [ $tgt = A ] && t=$PTA || t=$PTB
    case $r in
      r1) "${TM[@]}" send-keys -t "$TS:$tgt" -l "$tok"; "${TM[@]}" send-keys -t "$TS:$tgt" Enter; echo "  r1 send-keys to $tgt exit=$?";;
      r2) echo "  r2 to $tgt: $(python3 -I -B -c "$TIOC" "$t" "$tok" 2>&1)";;
      r3) if printf '%s\r' "$tok" > "$t" 2>/dev/null; then echo "  r3 write to $tgt ok"; else echo "  r3 write to $tgt failed"; fi;;
    esac; sleep 1.5
  done
  "${TM[@]}" send-keys -t "$TS:A" -l "RUNNERA"; "${TM[@]}" send-keys -t "$TS:A" Enter; "${TM[@]}" send-keys -t "$TS:B" -l "RUNNERB"; "${TM[@]}" send-keys -t "$TS:B" Enter; sleep 1.5
  echo "  screen A: $("${TM[@]}" capture-pane -t "$TS:A" -p | grep -v '^\s*$' | tr '\n' '|')"
  echo "  $(cat "$W/A.$r.out" 2>/dev/null || echo 'A: no line')   $(cat "$W/B.$r.out" 2>/dev/null || echo 'B: no line')"
  "${TM[@]}" kill-server; sleep 0.5
done
echo "server after kill: $("${TM[@]}" list-sessions 2>&1 | sed -E 's#/[^ ]*tmux-[0-9]+/#<tmux dir>/#')"
echo "socket file left: $(ls /private/tmp/tmux-$(id -u)/ 2>/dev/null | grep -c "^$TS$")"
echo "(after each route the readers' line is my own r1 typing RUNNERA/RUNNERB: it shows the reader was still waiting if the route delivered nothing)"
