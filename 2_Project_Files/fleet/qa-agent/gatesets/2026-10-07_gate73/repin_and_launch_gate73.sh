#!/bin/bash
# repin_and_launch_gate73.sh — the LAUNCH ACTION for gate73 (batched T2: #1407 KS-998, #1409 KS-1313, #1408 KS-1435, #1410 KS-591 custody).
# NOT RUN BY THE DRAFTER except `--dry-run`. Carried from repin_and_launch_gate72.sh, widened to FOUR rows + a landing order.
# EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT, compared with kit.json (the drafter's pin) AND with what this script reads live:
#   (V)  --order a,b,c,d (each row once) --head-1407 --head-1409 --head-1408 --head-1410 --develop, all present and well-formed — rc 9
#        each head == kit.json                                                                                     — rc 11 (WRONG VALUE)
#   (A)  each READY names its heads in full and #<pr>                                                              — rc 18
#   (2)  ONE `git ls-remote` of develop + 4 refs/pull/<n>/head + 4 branches, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the GitHub URL (a read verb); each head == pull/head == branch      — rc 11 (MISMATCH)
#   (1)  gh_gate73.py api for each row (rc 3 API failure; rc 11 not open / not develop / head differs) + census (REPORTED, not refused).
#        `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared --no-checkout` of the checkout, origin = the GitHub URL, the
#        checkout's core.sshCommand, NEVER an exported GIT_SSH_COMMAND): fetch heads / develop / base BY SHA only if absent; any still
#        absent refused BY NAME — rc 19. c1 for each row with EVERY required pin and --others must pass — rc 13 (a c1 FAIL is a re-draft).
#        c4 chain for --order on the develop read NOW: printed as the launch-time PREDICTION; at the draft develop its trees must equal
#        kit.json predicted_chain (rc 13 on a mismatch: the kit's composed docs would not be what the gate measures).
#   (S)  the merge seat is RULED (kit.json merge_seat non-null, not an author seat) — rc 8 (a dry run REPORTS it instead)
#   (R)  render prompt_gate73.txt -> prompt_gate73.rendered.txt + head_at_launch.txt (P x4 / B / D / O / S)          — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (4)  G73_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: V, A, 2, 1 (or --no-api), 3b, 3c, S (reported), R, 0 (reported) and the launcher's --check, then stops. Outputs: launch_<HHMMSS>.*
# (dry: dry_<HHMMSS>.*). Controls-only overrides (DRY RUN ONLY): G73_ROUTING (routing stand-in), G73_LSFILE (ls-remote stand-in),
# G73_KITJSON (a kit stand-in, e.g. with a ruled merge seat, for the launcher arm).
# Usage (run under `script -q /dev/null`):
#   repin_and_launch_gate73.sh --order 1407,1409,1408,1410 --head-1407 <40-hex> --head-1409 <40-hex> --head-1408 <40-hex> --head-1410 <40-hex>
#                              --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KITJSON="${G73_KITJSON:-$GS/kit.json}"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
ROUTING="${G73_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"; ROWS='1407 1409 1408 1410'
USAGE="usage: repin_and_launch_gate73.sh --order <a,b,c,d> --head-1407 <40-hex> --head-1409 <40-hex> --head-1408 <40-hex> --head-1410 <40-hex> --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]"
ORD=""; H1407=""; H1409=""; H1408=""; H1410=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --order) ORD="${2:-}"; shift 2 2>/dev/null || shift;;
    --head-1407) H1407="${2:-}"; shift 2 2>/dev/null || shift;;   --head-1409) H1409="${2:-}"; shift 2 2>/dev/null || shift;;
    --head-1408) H1408="${2:-}"; shift 2 2>/dev/null || shift;;   --head-1410) H1410="${2:-}"; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;       --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;;
    *) echo "$USAGE"; exit 9;;
  esac
done
hd() { eval "printf '%s' \"\$H$1\""; }
echo "--- V. required arguments, each well-formed and == the kit's pin (a wrong value refuses BY NAME)"
for _a in ORD H1407 H1409 H1408 H1410 DEV; do eval "_v=\$$_a"; [ -n "$_v" ] || { echo "REFUSING: a REQUIRED argument is missing ($_a)"; echo "$USAGE"; exit 9; }; done
for _a in H1407 H1409 H1408 H1410 DEV; do eval "_v=\$$_a"; printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_a must be the FULL 40-hex sha, got '$_v'"; exit 9; }; done
[ "$(printf '%s' "$ORD" | tr ',' '\n' | sort | tr '\n' ' ')" = "1407 1408 1409 1410 " ] || { echo "REFUSING: --order must name each of 1407 1409 1408 1410 exactly once, got '$ORD'"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
for _r in $ROWS; do [ "$(hd $_r)" = "$(KJ rows.$_r.head_expected)" ] || { echo "REFUSING: WRONG VALUE --head-$_r '$(hd $_r)' != kit.json $(KJ rows.$_r.head_expected) — the kit's figures are for that head; re-draft"; exit 11; }; done
[ "$DEV" = "$(KJ develop_at_draft)" ] || { echo "REFUSING: WRONG VALUE --develop '$DEV' != kit.json develop_at_draft $(KJ develop_at_draft) (pass the draft develop; a moved develop is handled by --repin-develop)"; exit 11; }
echo "  order $ORD + 4 heads + develop present, well-formed and == kit.json"
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate73$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | order $ORD | develop $DEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- A. each head must be the one its READY names"
for _r in $ROWS; do
  READY="$(KJ rows.$_r.ready)"; _h="$(hd $_r)"
  [ -s "$READY" ] || { echo "REFUSING: READY missing or empty ('$READY')"; exit 18; }
  _n="$(/usr/bin/grep -c -F "$_h" "$READY")"; _p="$(/usr/bin/grep -c -F "#$_r" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY' "$READY")"
  echo "  #$_r $(basename "$READY") (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$_r $_p | CONTROL lines naming 'READY' $_c"
  [ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the READY does not name $_h in full (or #$_r)"; exit 18; }
done

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop"; for _r in $ROWS; do REFS="$REFS refs/pull/$_r/head refs/heads/$(KJ rows.$_r.branch)"; done
if [ -n "${G73_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G73_LSFILE is a dry-run control only"; exit 16; }
  cp "$G73_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G73_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
for _r in $ROWS; do
  _h="$(hd $_r)"; _p="$(get "refs/pull/$_r/head")"; _b="$(get "refs/heads/$(KJ rows.$_r.branch)")"
  echo "  #$_r pull/head $_p | branch $_b"
  [ "$_p" = "$_h" ] && [ "$_b" = "$_h" ] || { echo "REFUSING TO LAUNCH: #$_r origin pull/head '$_p' / branch '$_b' != --head-$_r $_h — MISMATCH"; exit 11; }
done

echo "--- 1. PULLS API x4 + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  for _r in $ROWS; do
    python3 "$GS/gh_gate73.py" api --pr "$_r" --head "$(hd $_r)" > "$OUTP.api_$_r.out" 2> "$OUTP.api_$_r.err"; arc=$?
    echo "  api #$_r rc=$arc | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.api_$_r.out" | tr '\n' ' ')"; grep -E '^(FAIL|INFO)' "$OUTP.api_$_r.out" | sed 's/^/    /' | cut -c1-240
    [ "$arc" -eq 3 ] && { echo "REFUSING: API failure"; exit 3; }
    [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$_r open, unmerged, on develop at $(hd $_r) with the kit's shape"; exit 11; }
  done
  python3 "$GS/gh_gate73.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; echo "  census rc=$crc (REPORTED, not refused)"
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED (== the batch's base: the first lander's squash tree is its END_TREE; the kit's predicted chain applies)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (3c checks descent, that the advance touches no row's code / tooling, and RE-PREDICTS the chain)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, C1 x4 on the develop read now, the chain prediction"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
for s in $H1407 $H1409 $H1408 $H1410 "$CUR_DEV" "$(KJ base)" "$(KJ trailer_control)"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
OTH="1407=$H1407,1409=$H1409,1408=$H1408,1410=$H1410"
for _r in $ROWS; do
  python3 "$GS/c1_pin_gate73.py" --pr "$_r" --repo "$CL" --head "$(hd $_r)" --base "$(KJ base)" --parents-n 1 --end-tree "$(KJ rows.$_r.end_tree)" --develop "$CUR_DEV" --others "$OTH" > "$OUTP.c1_$_r.out" 2> "$OUTP.c1_$_r.err"; rc1=$?
  echo "  c1 #$_r rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_$_r.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_$_r.out" | sed 's/^/    /' | cut -c1-240
  [ "$rc1" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED for #$_r at its head (a pin moved: re-draft)"; exit 13; }
done
mkdir -p "$OUTP.chain"
python3 "$GS/c4_docs_gate73.py" chain --repo "$CL" --order "$ORD" --develop "$CUR_DEV" --heads "$OTH" --out "$OUTP.chain" > "$OUTP.c4chain.out" 2> "$OUTP.c4chain.err"; rc4=$?
grep -E '^(STEP|FINAL|CHAIN|REFUSED)' "$OUTP.c4chain.out" | sed 's/^/    /' | cut -c1-240; echo "  c4 chain rc=$rc4"
[ "$rc4" -eq 0 ] || { echo "REFUSING TO LAUNCH: the docs merge-in chain does not predict cleanly on develop $CUR_DEV for order $ORD (read $OUTP.c4chain.out)"; exit 13; }
PRED="$(python3 -c 'import json,sys; print(" | ".join("%s %s" % (s["pr"], s["tree"]) for s in json.load(open(sys.argv[1]))["steps"]))' "$OUTP.chain/chain.json")"
if [ "$DEV_MOVED" = 0 ] && [ "$ORD" = "$(KJ merge_order_default | tr ' ' ',')" ]; then
  KPRED="$(python3 -c 'import json,sys; print(" | ".join("%s %s" % (s["pr"], s["tree"]) for s in json.load(open(sys.argv[1]))["predicted_chain"]["steps"]))' "$KITJSON")"
  [ "$PRED" = "$KPRED" ] || { echo "REFUSING TO LAUNCH: the chain read now ($PRED) != kit.json predicted_chain ($KPRED): the composed docs in the kit are not what the gate will measure"; exit 13; }
  echo "  the chain read now == kit.json predicted_chain (the composed_2026-10-07/ docs apply VERBATIM)"
else
  echo "  NOTE: develop moved or a non-default order: the kit's composed_2026-10-07/ docs do NOT apply; the merge seat composes from $OUTP.chain/ (or re-runs c4 chain on the real develop)"
fi
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 says it touched none of the rows' paths / tooling; the chain is RE-PREDICTED above). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV; chain $PRED" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- S. the merge seat must be RULED (RULINGS Q-SEAT)"
SEAT="$(KJ merge_seat)"
if [ -z "$SEAT" ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: REPORTED, not refused — kit.json merge_seat is null; a real run refuses rc 8 and the launcher refuses rc 8)"; SEAT="Seat UNRULED"
  else echo "REFUSING TO LAUNCH: RULING NEEDED — kit.json merge_seat is null (RULINGS Q-SEAT)"; exit 8; fi
else echo "  merge seat: $SEAT"; fi

echo "--- R. render the prompt (four heads, develop $CUR_DEV, order $ORD, merge seat $SEAT)"
python3 - "$GS/prompt_gate73.txt" "$GS/prompt_gate73.rendered.txt" "$GS/head_at_launch.txt" "$KITJSON" "$CUR_DEV" "$ORD" "$SEAT" "$PRED" "$H1407" "$H1409" "$H1408" "$H1410" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import json, sys
src, dst, hf, kj, dev, order, seat, pred, h7, h9, h8, h0 = sys.argv[1:13]
K = json.load(open(kj)); t = open(src, encoding='utf-8').read()
heads = {'1407': h7, '1409': h9, '1408': h8, '1410': h0}
need = {'{{HEAD_%s}}' % r: 1 for r in heads}; need.update({'{{DEVELOP}}': 2, '{{ORDER}}': 2, '{{ORDER_CSV}}': 1, '{{MERGE_SEAT}}': 5, '{{PREDICTED_TREES}}': 1})
low = ['%s x%d' % (k, t.count(k)) for k, n in need.items() if t.count(k) < n]
if low: raise SystemExit('template tokens below their floor: %s' % low)
ord_txt = ' -> '.join(order.split(','))
for r, h in heads.items(): t = t.replace('{{HEAD_%s}}' % r, h)
t = t.replace('{{DEVELOP}}', dev).replace('{{ORDER_CSV}}', order).replace('{{ORDER}}', ord_txt).replace('{{MERGE_SEAT}}', seat).replace('{{PREDICTED_TREES}}', pred)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
lines = ['P %s %s %s %s' % (r, K['rows'][r]['branch'], heads[r], K['rows'][r]['end_tree']) for r in ('1407', '1409', '1408', '1410')]
lines += ['B %s 1' % K['base'], 'D %s' % dev, 'O %s' % order, 'S %s' % seat]
open(hf, 'w').write('\n'.join(lines) + '\n')
print('  rendered -> %s (%d bytes); head file %s (P x4 / B / D / O / S)' % (dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  G73_KITJSON="$KITJSON" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — order $ORD, develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G73_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G73_* override is set"; exit 16; }
echo "--- 5. usage gate"
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"; rc=$?
sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"; echo "  usage_gate rc=$rc (WED_USAGE_STOP=${WED_USAGE_STOP:-unset})"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (WED_USAGE_STOP only with Kam's recorded authority)"; exit 12; }
echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }
echo "--- 7. cockpit.sh add (the fleet's own tooling, never raw send-keys)"
"$(KJ cockpit)" add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2> "$OUTP.cockpit_add.err"; rc=$?
sed 's/^/    /' "$OUTP.cockpit_add.out" "$OUTP.cockpit_add.err"; echo "  cockpit.sh add rc=$rc"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') order $ORD; develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §8)"
