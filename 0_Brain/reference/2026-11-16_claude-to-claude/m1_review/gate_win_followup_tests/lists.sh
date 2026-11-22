#!/bin/bash
# QA-WIN-FOLLOWUP items 7-8: `cargo test --locked -p <crate> -- --list` per target, base and head, on the Mac.
W=/private/tmp/claude-501/qwf; O=$W/logs/list; mkdir -p $O
for t in b h; do for c in coagent-cli coagent-relay coagent-daemon; do
  $W/run.sh $W/$t $t cargo test --locked -p $c -- --list > $O/$t-$c.raw 2>&1; echo "$t $c exit $?"
  # keep: "Running <target>" lines and "<name>: test|bench" lines
  grep -E '^\s+Running |: (test|bench)$|^[0-9]+ tests?, ' $O/$t-$c.raw | sed -E 's#\(.*target/[^/]+/debug/deps/##; s#-[0-9a-f]{16}\)##' > $O/$t-$c.txt
done; done
for c in coagent-cli coagent-relay coagent-daemon; do
  echo "== $c: $(cmp -s $O/b-$c.txt $O/h-$c.txt && echo IDENTICAL || echo DIFFERENT); tests base $(grep -c ': test$' $O/b-$c.txt) head $(grep -c ': test$' $O/h-$c.txt)"
  diff $O/b-$c.txt $O/h-$c.txt | head -40
done
