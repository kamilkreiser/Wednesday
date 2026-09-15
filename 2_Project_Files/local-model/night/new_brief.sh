#!/bin/bash
# new_brief.sh <KS-id> [--split A|B] — write a brief SKELETON for Ornith with the clock stamped by the SHELL.
# 2026-09-15 (ledger +5 the same day: five brief headers carried a typed clock). The writer fills the sections;
# the header's time comes from `date`, never from the writer. Refuses to overwrite an existing brief (quarantine
# by mv first — never delete). Output: night/briefs/<id>.md, or night/briefs/split_<id><A|B>/<id>.md with --split.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ID="${1:-}"; SPLIT=""; [ "${2:-}" = "--split" ] && SPLIT="${3:-}"
case "$ID" in KS-[0-9]*) ;; *) echo "usage: new_brief.sh KS-<n> [--split A|B]" >&2; exit 2;; esac
if [ -n "$SPLIT" ]; then DIR="$HERE/briefs/split_${ID#KS-}$SPLIT"; else DIR="$HERE/briefs"; fi
OUT="$DIR/$ID.md"; mkdir -p "$DIR"
if [ -e "$OUT" ]; then echo "new_brief: REFUSED — $OUT exists; mv it to $OUT.<why>-$(date +%F) first (never delete)" >&2; exit 3; fi
NOW="$(date '+%H:%M')"; TODAY="$(date +%F)"
cat > "$OUT" <<TPL
# $ID — Wednesday's task for Ornith${SPLIT:+, PART $SPLIT of two} (written $NOW on $TODAY from the file at develop <TIP> — <lines read whole>)

## What is wrong (one paragraph)
<what the ticket says, in Wednesday's words, with the line numbers at the tip; what is NOT in this task>

## The exact change — <N> SMALL EDITS (≤ 3 per task; > 3 → split), each its own hunk with 3 lines of context
E1 — line <n> becomes (context: line <n-1> is \`…\`; line <n+1> is \`…\`):
\`\`\`
-<exact line at the tip>
+<the new line>
\`\`\`

## The test — one new vitest file, in-process
File: \`services/<svc>/src/__tests__/<id>-<slug>.test.ts\`
<copy instruction naming EVERY file-scope declaration of the reference by name, or the driver given as TEXT TO COPY>
Cells (every cell 🔴 or CONTROL, nothing optional):
- 🔴 \`it('🔴 $ID — …')\`: … (Untouched code: … — the red.)
- CONTROL \`it('$ID control — …')\`: … — green on both trees.

## Where (parsed into the checklist — every **must change** line must appear as a \`-\` line in your diff)
* \`:<n>\` — **must change**: \`<exact line>\`
* \`:<m>\` — (correct) \`<exact line>\` — stays   (an INSERT-ONLY edit names its anchor here as (correct) and has NO must-change line — A3b cannot see an insertion; 2026-09-15 KS-747)

## Tamper (TEST-ONLY mode only — delete this section for a product fix)
line: <n>
from: \`<exact line at the tip>\`
to: \`<replacement> // TAMPER: …\`
statement_ok: <required when the line sits mid-statement: name the enclosing statement's lines and why the rest cannot veto; read at the tip by Wednesday $NOW>

## Output
Exactly ONE \`\`\`diff block; paths repo-relative (\`Blockchain/Dev/services/...\`); correct hunk counts; blank context lines keep their leading space.
TPL
echo "new_brief: wrote $OUT (stamped $NOW)"
