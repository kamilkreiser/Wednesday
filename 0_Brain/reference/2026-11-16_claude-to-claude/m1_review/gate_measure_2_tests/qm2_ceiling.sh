#!/bin/bash
# QA-MEASURE-2 4.7: the committed count_run (extracted from m2.sh at the head, nothing else of m2.sh runs) against fake
# ledgers in MY work dir. Never touches the committed runs.log. usage: bash qm2_ceiling.sh <spike dir> <work dir>
S="$1"; W="$2"; mkdir -p "$W/ceil"
FN="$(sed -n '/^count_run() {/,/^}/p' "$S/m2.sh")"
printf '#!/bin/bash\necho "2.1.332 (fake claude for the ceiling test)"\n' > "$W/ceil/fakeclaude"; chmod +x "$W/ceil/fakeclaude"
for have in 19 20 25; do
  seq "$have" | sed 's/^/run=fake/' > "$W/ceil/ledger-$have.log"; cp "$W/ceil/ledger-$have.log" "$W/ceil/ledger-$have.before"
  echo "## ledger holds $have lines:"
  RUNS="$W/ceil/ledger-$have.log" CEIL=20 MODEL=claude-haiku-5-5 CLAUDE_BIN="$W/ceil/fakeclaude" bash -c "$FN"'
count_run would-be-next test; echo "(allowed; nothing was started)"'
  echo "exit=$? ; ledger lines now: $(grep -c . "$W/ceil/ledger-$have.log") ; last line: $(tail -1 "$W/ceil/ledger-$have.log" | cut -c1-60)"
done
echo "committed runs.log untouched: $(git -C "$S" status --porcelain -- runs.log | wc -l | tr -d ' ') changes"
