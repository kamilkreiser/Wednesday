#!/bin/bash
# Tests for rules_card.py. bash 3.2 compatible. Builds fixtures in a mktemp dir. Never discards stderr.
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL="$HERE/../rules_card.py"
PY=python3
T="$(printf '\t')"
TMP="$(mktemp -d)"
FAILS=0
trap 'rm -rf "$TMP"' EXIT

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS+1)); }

# run <args...> : sets OUT (stdout+stderr) and RC
run() { OUT="$($PY "$TOOL" "$@" 2>&1)"; RC=$?; }

# row file status seats family triggers enforced rule
row() { printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5" "$6" "$7"; }

ENF="2_Project_Files/tools/rules_card.py"

# mk <name> : fresh fixture dir in $D with 6 lesson files and a clean index
mk() {
  D="$TMP/$1"; mkdir -p "$D"
  for n in a b c d e f; do echo "# lesson $n" > "$D/2026-01-01_$n.md"; done
  {
    echo "# comment line"
    echo
    row 2026-01-01_a.md live all checks-that-can-fail verify,report - "When I report a count: state its source."
    row 2026-01-01_b.md live all kam-communication kam-message,card - "When I write to Kam: lead with the answer."
    row 2026-01-01_c.md live wednesday local-models usage - "When I pick a model on the Studio: use the local one."
    row 2026-01-01_d.md live all enforcement-in-the-path git,tooling "$ENF" "When I commit: the hook refuses secrets, so never bypass it."
    row 2026-01-01_e.md dead all other:retired wrap - "When wrapping: the old ritual."
    row 2026-01-01_f.md superseded all other:old lesson - "-> 2026-01-01_a.md: replaced."
  } > "$D/_rules_index.tsv"
  IDX="$D/_rules_index.tsv"
}

# mutate: sed on the index
mut() { sed "$1" "$IDX" > "$IDX.new" && mv "$IDX.new" "$IDX"; }

expect_fault() { # name expected-substring
  run --check --learnings-dir "$D"
  if [ "$RC" = 1 ] && echo "$OUT" | grep -q -- "$2"; then pass "$1"; else fail "$1 (rc=$RC out=$OUT)"; fi
}

# ---- clean fixture passes
mk clean
run --check --learnings-dir "$D"
if [ "$RC" = 0 ] && echo "$OUT" | grep -q '^OK'; then pass "clean fixture passes --check"; else fail "clean fixture passes --check (rc=$RC out=$OUT)"; fi

# ---- each fault
mk f1; echo "# x" > "$D/2026-01-07_g.md"
expect_fault "fault: lesson file with no index row" "no index row"

mk f2; row 2026-01-09_nope.md live all other:x wrap - "rule" >> "$IDX"
expect_fault "fault: row names missing file" "missing file"

mk f3; grep 2026-01-01_a.md "$IDX" >> "$IDX"
expect_fault "fault: duplicated file row" "duplicate"

mk f4; printf '2026-01-01_a.md\tlive\tall\tx\tverify\t-\n' >> "$IDX"
expect_fault "fault: row without 7 fields" "field count"

mk f5; mut "s/${T}live${T}all${T}kam-communication/${T}maybe${T}all${T}kam-communication/"
expect_fault "fault: bad status" "bad status"

mk f6; mut "s/${T}live${T}wednesday${T}/${T}live${T}saturday${T}/"
expect_fault "fault: bad seats value" "bad seats"

mk f7; mut "s/verify,report/verify,bogus/"
expect_fault "fault: trigger outside vocabulary" "bad trigger"

mk f8; mut "s#${T}${ENF}${T}#${T}2_Project_Files/tools/nope.sh${T}#"
expect_fault "fault: enforced_by path missing" "enforced_by path"

mk f9; LONG="$(printf 'x%.0s' $(seq 1 261))"; mut "s/state its source\./$LONG/"
expect_fault "fault: rule longer than 260" "too long"

mk f10; mut "s/${T}When I write to Kam: lead with the answer\.\$/${T}/"
expect_fault "fault: empty rule" "rule empty"

# boundary: exactly 260 is fine
mk f11; EX="$(printf 'y%.0s' $(seq 1 260))"; mut "s/When I report a count: state its source\./$EX/"
run --check --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "boundary: 260-char rule passes"; else fail "boundary: 260-char rule passes ($OUT)"; fi

# ---- card generation and seat filtering
mk card
run --seat friday --learnings-dir "$D"
CARD="$D/_rules_card_friday.md"
if [ "$RC" = 0 ] && [ -f "$CARD" ] && echo "$OUT" | grep -q 'rows on card: 2'; then pass "friday card written, summary line shows 2 rows"; else fail "friday card written (rc=$RC out=$OUT)"; fi
if head -6 "$CARD" | grep -q '^type: rules-card' && grep -q '^source: GENERATED' "$CARD" && grep -q '^status: live' "$CARD"; then pass "card frontmatter"; else fail "card frontmatter"; fi
if ! grep -q '^- .*`2026-01-01_c.md`$' "$CARD" && grep -q 'other seats only: 2026-01-01_c.md' "$CARD"; then pass "wednesday-only row absent from friday card, listed under other seats"; else fail "seat filtering friday"; fi
run --seat wednesday --learnings-dir "$D"
if grep -q '^- .*`2026-01-01_c.md`$' "$D/_rules_card_wednesday.md"; then pass "wednesday card includes wednesday-only row"; else fail "wednesday card includes row"; fi
SECT="$(sed -n '/^## Enforced by a tool/,/^## Not on this card/p' "$CARD")"
if echo "$SECT" | grep -q "enforced by \`$ENF\` — \`2026-01-01_d.md\`" && ! sed -n '/^## enforcement-in-the-path/p' "$CARD" | grep -q .; then pass "enforced row in enforced section, not in a family"; else fail "enforced section ($SECT)"; fi
if grep -q '^- dead: 2026-01-01_e.md' "$CARD" && grep -q '^- superseded: 2026-01-01_f.md' "$CARD"; then pass "dead and superseded listed under Not on this card"; else fail "not-on-card lists"; fi
if grep -q '^Counts: 6 lessons, 6 rule lines, 2 on this card, 1 enforced, 1 dead, 1 superseded, 1 other-seat-only' "$CARD"; then pass "counts line"; else fail "counts line: $(grep '^Counts' "$CARD")"; fi

# truncation to 120 in enforced section
mk trunc; LONG="$(printf 'z%.0s' $(seq 1 200))"; mut "s/When I commit: the hook refuses secrets, so never bypass it\./$LONG/"
run --seat friday --learnings-dir "$D"
Z="$(grep 'enforced by' "$D/_rules_card_friday.md" | grep -o 'z*' | sort | tail -1)"
if [ "${#Z}" = 120 ]; then pass "enforced rule truncated to 120 chars"; else fail "truncation (len ${#Z})"; fi

# family ordering: bigger family first
mk order
row 2026-01-01_a.md live all aaa-small verify - "x" > /dev/null
{ row 2026-01-01_a.md live all zzz-big verify - "r1"; row 2026-01-01_b.md live all zzz-big verify - "r2"; row 2026-01-01_c.md live all aaa-small verify - "r3"; } > "$D/_rules_index.tsv"
run --seat friday --learnings-dir "$D"
FIRST="$(grep '^## ' "$D/_rules_card_friday.md" | sed -n 2p)"
if [ "$FIRST" = "## zzz-big" ]; then pass "families sorted by row count descending"; else fail "family order ($FIRST)"; fi

# ---- --check with --seat: current / missing / stale
mk seatchk
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 1 ] && echo "$OUT" | grep -q 'card missing'; then pass "missing card fails --check --seat"; else fail "missing card (rc=$RC $OUT)"; fi
run --seat friday --learnings-dir "$D"
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "fresh card passes --check --seat"; else fail "fresh card (rc=$RC $OUT)"; fi
# date-only change is ignored
sed 's/^date: .*/date: 1999-01-01/' "$D/_rules_card_friday.md" > "$D/x" && mv "$D/x" "$D/_rules_card_friday.md"
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "date line ignored in card comparison"; else fail "date ignored ($OUT)"; fi
IDX="$D/_rules_index.tsv"; mut "s/lead with the answer/lead with the BLUF/"
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 1 ] && echo "$OUT" | grep -q 'card stale'; then pass "stale card fails --check --seat"; else fail "stale card (rc=$RC $OUT)"; fi

# ---- --at
mk at
run --at git --seat friday --learnings-dir "$D"
if [ "$RC" = 0 ] && echo "$OUT" | grep -q '^Rules for: git (1)' && echo "$OUT" | grep -q '^• \[[^]]*\] \[enforced\] .*(2026-01-01_d.md)'; then pass "--at includes enforced rows, marked"; else fail "--at git (rc=$RC $OUT)"; fi
run --at verify --seat friday --learnings-dir "$D"
if echo "$OUT" | grep -q '^Rules for: verify (1)' && echo "$OUT" | grep -q '(2026-01-01_a.md)' && ! echo "$OUT" | grep -q '2026-01-01_d.md'; then pass "--at filters by trigger"; else fail "--at verify ($OUT)"; fi
run --at usage --seat friday --learnings-dir "$D"
if echo "$OUT" | grep -q '^Rules for: usage (0)' && ! echo "$OUT" | grep -q '2026-01-01_c.md'; then pass "--at respects seat (wednesday-only absent for friday)"; else fail "--at usage friday ($OUT)"; fi
run --at usage --seat wednesday --learnings-dir "$D"
if echo "$OUT" | grep -q '^Rules for: usage (1)'; then pass "--at usage for wednesday finds the row"; else fail "--at usage wednesday ($OUT)"; fi
run --at wrap --seat friday --learnings-dir "$D"
if echo "$OUT" | grep -q '(0)' && ! echo "$OUT" | grep -q '2026-01-01_e.md'; then pass "--at excludes dead rows"; else fail "--at wrap ($OUT)"; fi
run --at bogus --seat friday --learnings-dir "$D"
if [ "$RC" = 2 ] && echo "$OUT" | grep -q 'kam-message'; then pass "unknown trigger exits 2 listing vocabulary"; else fail "unknown trigger (rc=$RC $OUT)"; fi
WED_SEAT=wednesday run --at usage --learnings-dir "$D"
if echo "$OUT" | grep -q '^Rules for: usage (1)'; then pass "--at seat from WED_SEAT"; else fail "WED_SEAT ($OUT)"; fi
OUT="$(WED_SEAT= $PY "$TOOL" --at usage --learnings-dir "$D" 2>&1)"; RC=$?
# tree here is not named FRIDAY/TUESDAY/WEDNESDAY unless the repo is; accept either exit 0 (derived) or 2 (not derivable)
if [ "$RC" = 0 ] || [ "$RC" = 2 ]; then pass "--at without seat derives from tree or exits 2 (rc=$RC)"; else fail "seat derive (rc=$RC $OUT)"; fi
mkdir -p "$TMP/noidx"
run --at git --seat friday --learnings-dir "$TMP/noidx"
if [ "$RC" = 0 ] && [ -z "$OUT" ]; then pass "missing index: --at silent, exit 0"; else fail "missing index (rc=$RC out=$OUT)"; fi

# ---- --stats
run --stats --learnings-dir "$D"
if [ "$RC" = 0 ] && echo "$OUT" | grep -q 'by status' && echo "$OUT" | grep -q 'by trigger' && echo "$OUT" | grep -q '^enforced: 1'; then pass "--stats prints groups and enforced count"; else fail "--stats (rc=$RC $OUT)"; fi

# ---- reinforcement weights
S=2026-02-01
mkw() {
  D="$TMP/$1"; mkdir -p "$D"
  for n in cite-link cite-md alpha-gate-keyed-on-tool-names beta-shared-prefix-aaa-one beta-shared-prefix-aaa-two twice plain conf old zeta; do echo "# l" > "$D/${S}_$n.md"; done
  {
    for n in cite-link cite-md alpha-gate-keyed-on-tool-names beta-shared-prefix-aaa-one beta-shared-prefix-aaa-two twice plain conf zeta; do
      row ${S}_$n.md live all checks-that-can-fail git - "rule $n."
    done
    row ${S}_old.md superseded all other:old git - "-> ${S}_cite-link.md: merged."
  } > "$D/_rules_index.tsv"
  cat > "$D/_ledger.md" <<EOF2
# ledger
| 2026-02-02 | x | see [[${S}_cite-link]] | w=1 |
| 2026-02-03 | a | b with | pipes | ${S}_cite-md.md | w=2 |
| 2026-02-04 | abbreviated ${S}_alpha-gate-keyed-on-tool-names…md here |
| 2026-02-05 | ambiguous ${S}_beta-shared-prefix-aaa-…md here |
| 2026-02-06 | [[${S}_twice]] and again ${S}_twice.md |
- 2026-02-07 a loose line naming [[${S}_plain]]
not a row: | 2026-02-08 | [[${S}_plain]] |
EOF2
  cat > "$D/_ledger_archive.md" <<EOF2
| 2026-01-20 | path/to/${S}_cite-md.md |
| 2026-01-21 | [[${S}_old]] |
| 2026-01-22 | [[${S}_old]] |
EOF2
  echo "| 2026-02-09 | [[${S}_conf]] |" > "$D/_ledger (conflict_on_2026-01-01).md"
  printf '| 2026-02-09 | [[%s_conf]] [[%s_cite-link]] |\n' $S $S > "$D/_ledger_x.pre-1.md"
  IDX="$D/_rules_index.tsv"
}
mkw wt
run --weights --learnings-dir "$D"
WOUT="$($PY "$TOOL" --weights --learnings-dir "$D" 2>/dev/null)"
wl() { echo "$WOUT" | grep "^${S}_$1.md${T}"; }
if [ "$(wl cite-link | cut -f2,3,4)" = "3${T}1${T}2026-02-02" ]; then pass "[[stem]] row counts; superseded -> target weight merged (1+2), last date"; else fail "cite-link ($(wl cite-link))"; fi
if [ "$(wl cite-md | cut -f2,3)" = "2${T}2" ]; then pass "stem.md and path citations count (resident + archive)"; else fail "cite-md ($(wl cite-md))"; fi
if [ "$(wl alpha-gate-keyed-on-tool-names | cut -f2)" = "1" ]; then pass "unique ellipsis-abbreviated citation counts"; else fail "alpha ($(wl alpha-gate-keyed-on-tool-names))"; fi
if [ "$(wl beta-shared-prefix-aaa-one | cut -f2)" = "0" ] && [ "$(wl beta-shared-prefix-aaa-two | cut -f2)" = "0" ]; then pass "ambiguous ellipsis prefix counts for neither"; else fail "ambiguous"; fi
if [ "$(wl twice | cut -f2)" = "1" ]; then pass "row naming the lesson twice counts once"; else fail "twice ($(wl twice))"; fi
if [ "$(wl plain | cut -f2)" = "0" ]; then pass "non-table lines do not count"; else fail "plain ($(wl plain))"; fi
if [ "$(wl conf | cut -f2)" = "0" ]; then pass "(conflict_on_ and .pre- ledger files ignored"; else fail "conf ($(wl conf))"; fi
if [ "$(wl old | cut -f2,3)" = "0${T}2" ]; then pass "merged row keeps own_rows, weight 0 after passing"; else fail "old ($(wl old))"; fi
if echo "$OUT" | grep -q '^weights: 0=.*ledger rows scanned: _ledger.md=5, _ledger_archive.md=3'; then pass "stderr summary with per-ledger rows scanned"; else fail "summary ($OUT)"; fi
if [ "$(echo "$WOUT" | head -1 | cut -f1)" = "${S}_cite-link.md" ]; then pass "--weights sorted by weight descending"; else fail "weights order"; fi
if [ ! -e "$D/_rules_weights.tsv" ] && ! ls "$D" | grep -qi weight; then pass "--weights writes nothing to disk"; else fail "weights wrote a file"; fi

run --seat friday --learnings-dir "$D"
CARD="$D/_rules_card_friday.md"
FAMLINES="$(sed -n '/^## checks-that-can-fail/,/^$/p' "$CARD" | grep '^- ')"
if [ "$(echo "$FAMLINES" | sed -n 1p | grep -c "^- \[×3\] .*cite-link")" = 1 ] && [ "$(echo "$FAMLINES" | sed -n 2p | grep -c "^- \[×2\] .*cite-md")" = 1 ] && [ "$(echo "$FAMLINES" | sed -n 3p | grep -c "^- \[×1\] .*alpha-gate")" = 1 ]; then pass "family order follows weight"; else fail "family order ($FAMLINES)"; fi
if echo "$FAMLINES" | grep -q '^- \[new\] .*plain'; then pass "[new] shown for weight zero"; else fail "[new] missing"; fi
MR="$(sed -n '/^## Most reinforced/,/^$/p' "$CARD" | grep '^- ')"
if [ "$(echo "$MR" | wc -l | tr -d ' ')" = 4 ] && echo "$MR" | sed -n 1p | grep -q '\[×3\]' && echo "$MR" | sed -n 4p | grep -q '\[×1\]'; then pass "Most reinforced section exists and is ordered"; else fail "most reinforced ($MR)"; fi
if grep -n '^Counts:' "$CARD" | head -1 | cut -d: -f1 | { read c; m="$(grep -n '^## Most reinforced' "$CARD" | cut -d: -f1)"; [ "$m" -gt "$c" ]; }; then pass "Most reinforced follows the counts line"; else fail "section position"; fi
if grep -q '^- These are weighted guidance, not absolute laws' "$CARD" && grep -q '^- Lessons that say the same thing are merged' "$CARD"; then pass "new how-to-use bullets"; else fail "bullets"; fi
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "--check --seat passes with weights"; else fail "check weights ($OUT)"; fi
echo "| 2026-02-10 | [[${S}_zeta]] |" >> "$D/_ledger.md"
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 1 ] && echo "$OUT" | grep -q 'card stale'; then pass "new ledger row makes the card stale"; else fail "stale on weight ($OUT)"; fi

run --at git --top 1 --seat friday --learnings-dir "$D"
if [ "$(echo "$OUT" | grep -c '^•')" = 1 ] && echo "$OUT" | grep '^•' | grep -q '^• \[×3\] .*cite-link' && echo "$OUT" | tail -1 | grep -q '^(+[0-9]* more: rules_card.py --at git)$'; then pass "--at --top 1: one rule plus the more line"; else fail "--top ($OUT)"; fi
run --at git --seat friday --learnings-dir "$D"
if echo "$OUT" | sed -n 2p | grep -q '^• \[×3\]' && ! echo "$OUT" | grep -q 'more:'; then pass "--at sorts by weight, prefix on each line, no more-line without --top"; else fail "--at weights ($OUT)"; fi

# ---- multi-rule lessons: <lesson>.md#<n>
A=2026-01-01_a.md
mk mr1; row "$A#2" live all other:second git - "When I run git: second rule of lesson a." >> "$IDX"
run --check --learnings-dir "$D"
if [ "$RC" = 0 ] && echo "$OUT" | grep -q '^OK'; then pass "multi: x.md plus x.md#2 is accepted (not a duplicate)"; else fail "multi accept (rc=$RC $OUT)"; fi

mk mr2; row "$A#2" live all other:second git - "r2" >> "$IDX"; row "$A#2" live all other:second git - "r2 again" >> "$IDX"
expect_fault "multi fault: x.md#2 twice is a duplicate" "duplicate row for $A#2"

mk mr3; echo "# g" > "$D/2026-01-07_g.md"; row 2026-01-07_g.md#2 live all other:x git - "r" >> "$IDX"
run --check --learnings-dir "$D"
if [ "$RC" = 1 ] && echo "$OUT" | grep -q 'no plain row for 2026-01-07_g.md' && ! echo "$OUT" | grep -q 'no index row'; then pass "multi fault: #n row without plain row named (base counts as indexed)"; else fail "multi no plain (rc=$RC $OUT)"; fi

mk mr4; row 2026-01-09_nope.md#2 live all other:x git - "r" >> "$IDX"
expect_fault "multi fault: #n row whose base lesson file is missing" "missing file 2026-01-09_nope.md (row 2026-01-09_nope.md#2)"

for bad in 1 0 x ""; do
  mk mr5; row "$A#$bad" live all other:x git - "r" >> "$IDX"
  expect_fault "multi fault: bad rule number '#$bad'" "bad rule number in $A#$bad"
done

mk mr6; row "$A#3" live all other:third git - "r3" >> "$IDX"
run --check --learnings-dir "$D"
if [ "$RC" = 1 ] && echo "$OUT" | grep -q 'no plain row'; then fail "multi: #3 with plain row present wrongly faulted ($OUT)"; else pass "multi: #3 (gap, plain present) accepted"; fi

# weights, card, --at, --stats on a multi-rule fixture
mk mr7
{ row $A live all checks-that-can-fail verify,report - "When I report a count: state its source."
  row "$A#2" live all other:second git - "When I run git: second rule of lesson a."
  row 2026-01-01_b.md live all kam-communication kam-message,card - "When I write to Kam: lead with the answer."
  row 2026-01-01_c.md live wednesday local-models usage - "When I pick a model: use the local one."
  row 2026-01-01_d.md live all enforcement-in-the-path git,tooling "$ENF" "When I commit: never bypass the hook."
  row "2026-01-01_d.md#2" live all enforcement-in-the-path wrap "$ENF" "When I wrap: second enforced rule."
  row 2026-01-01_e.md dead all other:retired wrap - "old."
  row "2026-01-01_e.md#2" dead all other:retired wrap - "old two."
  row 2026-01-01_f.md superseded all other:old lesson - "-> $A: replaced."
  row "2026-01-01_f.md#2" superseded all other:old lesson - "-> $A: replaced two."
} > "$IDX"
{ echo "| 2026-02-02 | [[2026-01-01_a]] |"; echo "| 2026-02-03 | [[2026-01-01_a]] and [[2026-01-01_b]] |"; echo "| 2026-02-04 | [[2026-01-01_a]] |"; } > "$D/_ledger.md"
run --check --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "multi: fixture with #2 rows (live, enforced, dead, superseded) passes --check"; else fail "multi fixture check ($OUT)"; fi
WOUT="$($PY "$TOOL" --weights --learnings-dir "$D" 2>"$D/werr")"; WERR="$(cat "$D/werr")"
if ! echo "$WOUT" | grep -q '#' && [ "$(echo "$WOUT" | grep -c .)" = 6 ] && echo "$WOUT" | head -1 | grep -q "^$A${T}3"; then pass "multi: --weights lists base files only (6 lessons)"; else fail "multi weights list ($WOUT)"; fi
if echo "$WERR" | grep -q 'lessons=5, excluding 1 merged'; then pass "multi: weight summary counts lessons, not rows"; else fail "multi weight summary ($WERR)"; fi
run --seat friday --learnings-dir "$D"
CARD="$D/_rules_card_friday.md"
if grep -q '^- \[×3\] When I run git: second rule of lesson a\. — `2026-01-01_a.md` (rule 2)$' "$CARD"; then pass "multi: #2 row shows base weight and '(rule 2)' in its own family"; else fail "multi card line ($(grep 'second rule' "$CARD"))"; fi
if sed -n '/^## other:second/,/^$/p' "$CARD" | grep -q 'rule 2'; then pass "multi: #2 row sits in its own family"; else fail "multi family"; fi
MR="$(sed -n '/^## Most reinforced/,/^$/p' "$CARD" | grep '^- ')"
if [ "$(echo "$MR" | grep -c "2026-01-01_a.md")" = 1 ] && ! echo "$MR" | grep -q 'rule 2'; then pass "multi: Most reinforced has one line per lesson (plain row only)"; else fail "multi top section ($MR)"; fi
if grep -q '^Counts: 6 lessons, 10 rule lines, 3 on this card, 2 enforced, 2 dead, 2 superseded, 1 other-seat-only' "$CARD"; then pass "multi: counts line has lessons and rule lines"; else fail "multi counts ($(grep '^Counts' "$CARD"))"; fi
if grep -q "enforced by \`$ENF\` — \`2026-01-01_d.md\` (rule 2)" "$CARD" && grep -q '^- dead: 2026-01-01_e.md, 2026-01-01_e.md (rule 2)' "$CARD" && grep -q '^- superseded: 2026-01-01_f.md, 2026-01-01_f.md (rule 2)' "$CARD"; then pass "multi: enforced/dead/superseded #2 rows labelled"; else fail "multi sections"; fi
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "multi: generated card is current for --check --seat"; else fail "multi card check ($OUT)"; fi
run --at git --seat friday --learnings-dir "$D"
if echo "$OUT" | grep -q '^Rules for: git (2)' && echo "$OUT" | grep -q "^• \[×3\] .*second rule of lesson a\..*($A, rule 2)" && ! echo "$OUT" | grep -q "($A)"; then pass "multi: --at matches #2 by its own trigger, prints (file, rule 2); base row not printed"; else fail "multi --at git ($OUT)"; fi
run --at verify --seat friday --learnings-dir "$D"
if echo "$OUT" | grep -q "($A)" && ! echo "$OUT" | grep -q 'rule 2'; then pass "multi: --at verify prints the base row only"; else fail "multi --at verify ($OUT)"; fi
run --stats --learnings-dir "$D"
if echo "$OUT" | grep -q '^lessons: 6, rule lines: 10$'; then pass "multi: --stats shows lessons vs rule lines"; else fail "multi stats ($OUT)"; fi

# ---- P4: seat weight beside fleet weight; --top never cuts a seat regression of the last 30 days
D5="$($PY -c 'import datetime;print((datetime.date.today()-datetime.timedelta(days=5)).isoformat())')"
D45="$($PY -c 'import datetime;print((datetime.date.today()-datetime.timedelta(days=45)).isoformat())')"
# mkp <name> <seat-ledger-date> <with-seat-ledger 1|0>: p0 fleet 9 (shared ledger), p1 fleet 3 / seat 1, p2 fleet 2 / seat 0,
# p3 fleet 3 / seat 3 (equal); friday's own ledger is _ledger_friday.md
mkp() {
  D="$TMP/$1"; mkdir -p "$D"
  for n in p0 p1 p2 p3; do echo "# l" > "$D/2026-03-01_$n.md"; done
  for n in p0 p1 p2 p3; do row 2026-03-01_$n.md live all checks-that-can-fail git - "When I do $n: rule $n."; done > "$D/_rules_index.tsv"
  IDX="$D/_rules_index.tsv"
  { for i in 1 2 3 4 5 6 7 8 9; do echo "| 2026-03-02 | [[2026-03-01_p0]] r$i |"; done
    echo "| 2026-03-02 | [[2026-03-01_p1]] |"; echo "| 2026-03-03 | [[2026-03-01_p1]] |"
    echo "| 2026-03-02 | [[2026-03-01_p2]] |"; echo "| 2026-03-03 | [[2026-03-01_p2]] |"; } > "$D/_ledger.md"
  if [ "$3" = 1 ]; then
    { echo "| 2026-03-04 | [[2026-03-01_p1]] |"
      for i in 1 2 3; do echo "| $2 | [[2026-03-01_p3]] s$i |"; done; } > "$D/_ledger_friday.md"
  fi
}
mkp sw1 "$D5" 1
run --seat friday --learnings-dir "$D"
CARD="$D/_rules_card_friday.md"
if grep -q '^- \[×3, seat ×1\] When I do p1: rule p1\. — `2026-03-01_p1.md`$' "$CARD" && grep -q '^- \[×2\] When I do p2' "$CARD"; then pass "P4 card: seat weight shown beside fleet weight when they differ"; else fail "P4 card differ ($(grep 'rule p' "$CARD"))"; fi
if grep -q '^- \[×3\] When I do p3: rule p3\. — `2026-03-01_p3.md`$' "$CARD" && grep -q '^- \[×9\] When I do p0: rule p0\. — `2026-03-01_p0.md`$' "$CARD"; then pass "P4 card: seat weight not shown when equal to fleet weight"; else fail "P4 card equal ($(grep 'rule p' "$CARD"))"; fi
run --check --seat friday --learnings-dir "$D"
if [ "$RC" = 0 ]; then pass "P4: --check --seat passes on a card with seat weights"; else fail "P4 check ($OUT)"; fi
run --at git --seat friday --learnings-dir "$D"
if echo "$OUT" | grep -q '^• \[×3, seat ×1\] .*p1' && echo "$OUT" | grep -q '^• \[×3\] .*p3'; then pass "P4 --at: seat weight shown when different, absent when equal"; else fail "P4 --at ($OUT)"; fi
run --at git --top 1 --seat friday --learnings-dir "$D"
if [ "$(echo "$OUT" | grep -c '^•')" = 2 ] && echo "$OUT" | grep -q '^• \[×3\] \[seat regression\] .*p3' && ! echo "$OUT" | grep '^•' | sed -n 1p | grep -q 'seat regression' && echo "$OUT" | tail -1 | grep -q '^(+2 more: rules_card.py --at git)$' && echo "$OUT" | grep -q '^Rules for: git (4)$'; then pass "P4: a recent seat regression survives --top 1, marked, more-line counts the rest"; else fail "P4 recent regression ($OUT)"; fi
run --at git --top 1 --seat tuesday --learnings-dir "$D"
if [ "$(echo "$OUT" | grep -c '^•')" = 1 ] && ! echo "$OUT" | grep -q 'seat' && echo "$OUT" | tail -1 | grep -q '^(+3 more: rules_card.py --at git)$'; then pass "P4: a seat with no ledger of its own is unchanged (no seat text, plain --top)"; else fail "P4 no ledger ($OUT)"; fi
run --seat tuesday --learnings-dir "$D"
if ! grep -q 'seat ×' "$D/_rules_card_tuesday.md"; then pass "P4: card of a seat with no own ledger carries no seat weights"; else fail "P4 tuesday card"; fi
mkp sw2 "$D45" 1
run --at git --top 1 --seat friday --learnings-dir "$D"
if [ "$(echo "$OUT" | grep -c '^•')" = 1 ] && ! echo "$OUT" | grep -q 'seat regression' && echo "$OUT" | tail -1 | grep -q '^(+3 more: rules_card.py --at git)$'; then pass "P4: a seat regression over 30 days old does not survive --top 1"; else fail "P4 old regression ($OUT)"; fi


echo
if [ "$FAILS" -gt 0 ]; then echo "$FAILS arm(s) FAILED"; exit 1; fi
echo "ALL ARMS PASSED"
