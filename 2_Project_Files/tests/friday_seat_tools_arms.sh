#!/bin/bash
# friday_seat_tools_arms.sh — red-proof for the 2026-09-23 FRIDAY seat sweep (brief:
# fleet/briefs_staged/2026-09-23_friday_seat_tools_sweep.md; report: fleet/REPORT_2026-09-23_friday-seat-tools.md).
#
# For EACH changed tool: one run as the friday seat (a scratch tree literally named FRIDAY, or WED_AGENT=friday)
# proving it picks the FRIDAY names (inbox, stream, note dir, launcher, partition), and one Wednesday run comparing
# the NEW script with its pre-friday backup (<file>.pre-0923-HHMM-friday) on identical scratch inputs — Wednesday's
# behaviour must be byte-identical (after normalising the scratch path and wall-clock fields only).
# Unknown seats (THURSDAY tree / WED_AGENT=thursday) must still REFUSE.
#
# SAFETY — nothing here reaches a live system:
#   * every tool runs inside scratch trees under a mktemp dir (left in place: never-delete rule);
#   * curl is a PATH stub that records only the URL/subject/body (never headers — the Authorization key) and answers
#     from fixtures; no mail is sent and the live board is never called (LIVE_BOARD=0, or a stub python that only
#     echoes its argv; fake .pem files are the literal text "arms-fake");
#   * tmux is either a stub that always fails, or a wrapper onto a PRIVATE server (-L friday_tools_arms_$$) that is
#     killed at the end — the live `fleet` session is never listed for writing, tapped or respawned;
#   * rotate/liveness run only their refusal / test-mode paths (no launcher file exists in any scratch tree, and
#     LIVENESS_TEST=1 with stubs and an empty LIVENESS_LAUNCH_CMD);
#   * install_all_jobs.sh is run for real only with --check (read-only launchctl) on this tree; the friday install is
#     a no-op by construction and the WEDNESDAY installs are never run;
#   * nas_sync.sh is run ONLY as friday (it must refuse before anything); close_wednesday's inbox read goes through a
#     black-hole proxy (127.0.0.1:9) so the GET never leaves the machine.
# bash 3.2 (macOS): no declare -A, no ${var,,}, no timeout. Never cd.
set -u
SRC="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BASE="$(cd -P "$(mktemp -d "${TMPDIR:-/tmp}/friday_tools_arms.XXXXXX")" && pwd)"
O="$BASE/o"; BIN="$BASE/bin"; mkdir -p "$O" "$BIN"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "FAIL $1"; }
has() { [ -f "$2" ] && /usr/bin/grep -qF -- "$1" "$2"; }
echo "work dir: $BASE  (source: $SRC)"
unset WED_AGENT CLAUDE_CONFIG_DIR ROTATE_TMUX_SESSION ROTATE_LAUNCH_CMD LIVE_BOARD_PYTHON KAM_LIVE_BASE WEDNESDAY_TEST_HOUR \
      WEDNESDAY_DRYRUN DRYRUN AGENTMAIL_API_KEY CHAT_PROJECT
export WEDNESDAY_MUTE=1 WEDNESDAY_VOICE=arms-no-audio DEVMASTER=/nonexistent-devmaster

bk() { ls "$SRC/$1".pre-0923-*-friday 2>/dev/null | sort | head -1; }   # the EARLIEST backup = the pre-friday file
put() { # put <tree> <relpath> <new|old>
  local t="$1" p="$2" v="$3" from
  mkdir -p "$(dirname "$t/$p")"
  from="$SRC/$p"; if [ "$v" = old ] && [ -n "$(bk "$p")" ]; then from="$(bk "$p")"; fi
  cp -p "$from" "$t/$p"
}
FILES="2_Project_Files/tools/chat_reply.sh 2_Project_Files/tools/absence_claim_check.sh 2_Project_Files/tools/chat_streams.py
2_Project_Files/tools/_live_board.sh 2_Project_Files/tools/_kam_live.sh 2_Project_Files/tools/kam_msgs.sh
2_Project_Files/tools/kam_rulings_today.sh 2_Project_Files/tools/statusline_publish.sh 2_Project_Files/tools/decision_queue.sh
2_Project_Files/tools/_store_guard.sh 2_Project_Files/tools/chat_push.sh 2_Project_Files/tools/reconcile_rulings.py
2_Project_Files/tools/seat_note.sh 2_Project_Files/tools/tap_friday.sh 2_Project_Files/fleet/inbox_routing.conf
2_Project_Files/fleet/send_brief.sh 2_Project_Files/fleet/inbox_digest.sh 2_Project_Files/fleet/cockpit/seat_resolve.sh
2_Project_Files/fleet/cockpit/live_chat_poll.sh 2_Project_Files/fleet/cockpit/wake_watch.sh
2_Project_Files/fleet/cockpit/wednesday_rotate.sh 2_Project_Files/fleet/cockpit/rotate_liveness.sh
2_Project_Files/fleet/cockpit/dead_banner_check.sh 2_Project_Files/fleet/cockpit/exited_seat_check.sh
2_Project_Files/fleet/cockpit/pane_agent_live.sh 2_Project_Files/fleet/cockpit/cockpit.sh
2_Project_Files/scheduler/install_all_jobs.sh 2_Project_Files/scheduler/install_scheduler.command
2_Project_Files/scheduler/shift_change.sh 2_Project_Files/scheduler/nas_sync.sh 2_Project_Files/scheduler/close_wednesday.sh
2_Project_Files/fleet/hooks/pathguard.py 2_Project_Files/doctor.sh 2_Project_Files/voice/speak.sh 0_Brain/daily/_template.md"
mktree() { # mktree <tree> <new|old>
  local t="$1" v="$2" p
  mkdir -p "$t/0_Brain/dashboard/data" "$t/4_Credentials" "$t/2_Project_Files/fleet/state"
  for p in $FILES; do put "$t" "$p" "$v"; done
}
FR="$BASE/FRIDAY"; TH="$BASE/THURSDAY"; WN="$BASE/n/WEDNESDAY"; WO="$BASE/o_/WEDNESDAY"
mktree "$FR" new; mktree "$TH" new; mktree "$WN" new; mktree "$WO" old
norm() { sed -e "s#$WN#<ROOT>#g" -e "s#$WO#<ROOT>#g" -e "s#$FR#<ROOT>#g" "$1" | sed -E 's/20[0-9]{2}-[0-9]{2}-[0-9]{2}[T ][0-9:.]+([+-][0-9:]+|Z)?/<TS>/g'; }
same() { norm "$1" > "$1.n"; norm "$2" > "$2.n"; cmp -s "$1.n" "$2.n"; }

# ── stubs ────────────────────────────────────────────────────────────────────
# curl: records URL + -d body + subject (NEVER -H values), answers by URL. -w '%{http_code}' -> 200.
cat > "$BIN/curl" <<'EOF'
#!/bin/bash
url=""; data=""; w=""
while [ $# -gt 0 ]; do
  case "$1" in
    -H) shift ;;
    -d|--data) data="$2"; shift ;;
    -w) w="$2"; shift ;;
    -o|-m|--max-time|-X) shift ;;
    http*) url="$1" ;;
  esac; shift
done
printf 'URL %s\n' "$url" >> "${ARMS_CURL_LOG:-/dev/null}"
[ -n "$data" ] && printf 'DATA %s\n' "$data" >> "${ARMS_CURL_LOG:-/dev/null}"
if [ -n "$w" ]; then printf '200'; exit 0; fi
case "$url" in
  *friday-laptop-agent@*) printf '%s' '{"messages":[{"subject":"[Secuura/Blockchain -> Friday] STATUS: fx","preview":"FRI-IN","timestamp":"2026-09-23T01:00:00Z","message_id":"<f1@x>","from":"secuura-blockchain@agentmail.to"},{"subject":"[Wednesday -> Secuura/Blockchain] brief from friday","preview":"FRI-OWN","timestamp":"2026-09-23T01:00:01Z","message_id":"<f2@x>","from":"friday-laptop-agent@agentmail.to"}]}' ;;
  *wednesday-agent@*) printf '%s' '{"messages":[{"subject":"[Secuura/Blockchain -> Wednesday] STATUS: fx","preview":"WED-IN","timestamp":"2026-09-23T01:00:00Z","message_id":"<w1@x>","from":"secuura-blockchain@agentmail.to"},{"subject":"[Wednesday -> Secuura/Blockchain] brief","preview":"WED-OWN","timestamp":"2026-09-23T01:00:01Z","message_id":"<w2@x>","from":"wednesday-agent@agentmail.to"}]}' ;;
  *tuesday-agent@*) printf '%s' '{"messages":[{"subject":"[Datasec/NexusAI -> Tuesday] STATUS: fx","preview":"TUE-IN","timestamp":"2026-09-23T01:00:00Z","message_id":"<t1@x>","from":"datasec-nexusai@agentmail.to"}]}' ;;
  *coagent@*) printf '%s' '{"messages":[{"subject":"[Datasec/NexusAI -> Tuesday] gate","preview":"BUS-DS","timestamp":"2026-09-23T01:00:02Z","message_id":"<c1@x>","from":"a@x"},{"subject":"General","preview":"BUS-GEN","timestamp":"2026-09-23T01:00:03Z","message_id":"<c2@x>","from":"b@x"}]}' ;;
  *) printf '%s' '{"messages":[]}' ;;
esac
EOF
printf '#!/bin/bash\nexit 1\n' > "$BIN/tmux"
printf '#!/bin/bash\necho "STUBPY $*" >> "${ARMS_STUBPY_LOG:-/dev/null}"\necho "STUBPY $*"\nexit 1\n' > "$BIN/stubpy"
chmod +x "$BIN/curl" "$BIN/tmux" "$BIN/stubpy"
SPATH="$BIN:$PATH"
for t in "$FR" "$TH" "$WN" "$WO"; do printf 'AGENTMAIL_API_KEY=arms-fake-not-a-key\n' > "$t/4_Credentials/.env"; chmod 600 "$t/4_Credentials/.env"; done
TODAY="$(date +%F)"

# ═════ A. chat_reply.sh — stream name, project, refusal ═════════════════════════
LIVE_BOARD=0 bash "$FR/2_Project_Files/tools/chat_reply.sh" "friday arms hello A1" > "$O/A1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && has "appended to chat_friday.json" "$O/A1.out" && [ ! -e "$FR/0_Brain/dashboard/data/chat_wednesday.json" ] \
   && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); e=d[-1]; sys.exit(0 if e["text"]=="friday arms hello A1" and e["project"]=="Friday" else 1)' "$FR/0_Brain/dashboard/data/chat_friday.json" \
   && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if any(e.get("agent")=="friday" for e in d) else 1)' "$FR/0_Brain/dashboard/data/chat_log.json"; then
  ok "A1 chat_reply on a FRIDAY tree -> chat_friday.json (project Friday), derived chat_log agent=friday, no chat_wednesday.json"
else bad "A1 chat_reply friday: rc=$rc :: $(cat "$O/A1.out")"; fi
LIVE_BOARD=0 bash "$TH/2_Project_Files/tools/chat_reply.sh" "thursday A2" > "$O/A2.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && has "REFUSING" "$O/A2.out" && [ -z "$(ls "$TH/0_Brain/dashboard/data/" | /usr/bin/grep -i 'chat_')" ]; then
  ok "A2 chat_reply on a THURSDAY tree -> exit 2 REFUSING, no stream written"
else bad "A2 thursday: rc=$rc :: $(cat "$O/A2.out")"; fi
for v in n o_; do t="$BASE/$v/WEDNESDAY"
  LIVE_BOARD=0 bash "$t/2_Project_Files/tools/chat_reply.sh" "wednesday arms hello A3" > "$O/A3_$v.out" 2>&1; echo "rc=$?" >> "$O/A3_$v.out"
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); [e.pop("ts",None) for e in d]; print(json.dumps(d,sort_keys=True))' "$t/0_Brain/dashboard/data/chat_wednesday.json" > "$O/A3_$v.stream"
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); [e.pop("ts",None) for e in d]; print(json.dumps(d,sort_keys=True))' "$t/0_Brain/dashboard/data/chat_log.json" > "$O/A3_$v.log"
done
if same "$O/A3_n.out" "$O/A3_o_.out" && cmp -s "$O/A3_n.stream" "$O/A3_o_.stream" && cmp -s "$O/A3_n.log" "$O/A3_o_.log" && has "appended to chat_wednesday.json" "$O/A3_n.out"; then
  ok "A3 WEDNESDAY: new chat_reply == pre-friday chat_reply (stdout, chat_wednesday.json entry, derived chat_log; ts excluded)"
else bad "A3 wednesday byte-identity :: $(diff "$O/A3_n.out.n" "$O/A3_o_.out.n" | head -5) :: $(diff "$O/A3_n.stream" "$O/A3_o_.stream" | head -3)"; fi

# ═════ B. _live_board.sh — partition, holdings, the post command line ═══════════
lbm() { bash -c '. "$1/2_Project_Files/tools/_live_board.sh"
  for p in Secuura/Blockchain Datasec/NexusAI WED Fleet ""; do for s in wednesday tuesday; do printf "%s:%s=%s " "$s" "$p" "$(_lb_client "$p")"; done; done
  for s in wednesday tuesday; do for c in Secuura WED Datasec Friday; do _lb_seat_holds "$s" "$c"; printf "%s/%s=%s " "$s" "$c" "$?"; done; done' _ "$1"; }
R_F="$(bash -c '. "$1/2_Project_Files/tools/_live_board.sh"; printf "%s %s %s|" "$(_lb_client_for friday Datasec/NexusAI)" "$(_lb_client_for friday Secuura/Blockchain)" "$(_lb_client_for friday WED)"
  for c in Friday Secuura Datasec WED; do _lb_seat_holds friday "$c"; printf "%s=%s " "$c" "$?"; done
  for s in wednesday tuesday; do _lb_seat_holds "$s" Friday; printf "%s/Friday=%s " "$s" "$?"; done' _ "$FR")"
if [ "$R_F" = "Friday Friday Friday|Friday=0 Secuura=1 Datasec=1 WED=1 wednesday/Friday=1 tuesday/Friday=1 " ]; then
  ok "B1 _live_board: friday posts to partition Friday for every project; holds Friday only; wednesday/tuesday do not hold Friday"
else bad "B1 friday partition matrix: '$R_F'"; fi
lbm "$WN" > "$O/B2_n.out"; lbm "$WO" > "$O/B2_o_.out"
if cmp -s "$O/B2_n.out" "$O/B2_o_.out" && has "wednesday:Secuura/Blockchain=Secuura" "$O/B2_n.out"; then ok "B2 _live_board: wednesday/tuesday client + holdings matrix identical to the pre-friday file"
else bad "B2 matrix differs :: $(diff "$O/B2_n.out" "$O/B2_o_.out")"; fi
mkdir -p "$FR/4_Credentials/dashboard-cloud" "$WN/4_Credentials/dashboard-cloud" "$WO/4_Credentials/dashboard-cloud"
printf 'arms-fake\n' > "$FR/4_Credentials/dashboard-cloud/friday-seat.pem"
for t in "$WN" "$WO"; do printf 'arms-fake\n' > "$t/4_Credentials/dashboard-cloud/wednesday-seat.pem"; done
cat > "$BASE/cards.json" <<'EOF'
[{"id":"arms-card-ds","client_project":"Datasec/NexusAI","title":"t","status":"open"},{"id":"arms-card-sc","client_project":"Secuura/Blockchain","title":"t","status":"open"}]
EOF
ARMS_STUBPY_LOG="$O/B3.argv" LIVE_BOARD_PYTHON="$BIN/stubpy" bash -c '. "$1/2_Project_Files/tools/_live_board.sh"; live_board_post_message friday Datasec/NexusAI 2026-09-23T11:00:00+10:00 chat_friday.json "B3 text"; live_board_post_card friday "$2" arms-card-ds' _ "$FR" "$BASE/cards.json" > "$O/B3.out" 2>&1
FL="$FR/2_Project_Files/fleet/state/live_board_post_failures.log"
if has "message -> Friday failed: STUBPY - $FR friday Friday" "$FL" && has "card arms-card-ds -> Friday failed" "$FL" \
   && has "STUBPY $FR/2_Project_Files/dashboard-cloud/seat/post_card.py --seat friday --cert-dir $FR/4_Credentials/dashboard-cloud --from-store $BASE/cards.json --card-id arms-card-ds --client Friday" "$O/B3.argv"; then
  ok "B3 friday post: message -> partition Friday; card (client_project Datasec/…) -> Friday with --client Friday passed to post_card.py (stub python, no network)"
else bad "B3 friday post :: $(cat "$O/B3.out") :: $(cat "$FL" 2>&1)"; fi
for t in "$WN" "$WO"; do ARMS_STUBPY_LOG="$O/B4_$(basename "$(dirname "$t")").argv" LIVE_BOARD_PYTHON="$BIN/stubpy" bash -c '. "$1/2_Project_Files/tools/_live_board.sh"; live_board_post_message wednesday Secuura/Blockchain 2026-09-23T11:00:00+10:00 chat_wednesday.json "B4 text"; live_board_post_card wednesday "$2" arms-card-sc' _ "$t" "$BASE/cards.json" > "$O/B4_$(basename "$(dirname "$t")").out" 2>&1
  cut -d' ' -f2- "$t/2_Project_Files/fleet/state/live_board_post_failures.log" > "$O/B4_$(basename "$(dirname "$t")").log"; done
if same "$O/B4_n.argv" "$O/B4_o_.argv" && has "card arms-card-sc -> Secuura failed" "$O/B4_n.log" && has "--card-id arms-card-sc" "$O/B4_n.argv" && ! has "--client" "$O/B4_n.argv"; then
  ok "B4 WEDNESDAY post command lines (message + card, no --client) identical to the pre-friday file"
else bad "B4 wednesday post argv differ :: $(diff "$O/B4_n.argv.n" "$O/B4_o_.argv.n")"; fi

# ═════ C. _kam_live.sh — the seat guard and the certificate it picks ════════════
for t in "$FR" "$WN" "$WO"; do mkdir -p "$t/2_Project_Files/dashboard-cloud/.venv/bin"
  printf '#!/bin/bash\necho "$*" >> "%s/venv_args.log"\necho %s\n' "$t" "'{\"messages\":[]}'" > "$t/2_Project_Files/dashboard-cloud/.venv/bin/python"
  chmod +x "$t/2_Project_Files/dashboard-cloud/.venv/bin/python"; done
WED_AGENT=friday bash -c '. "$1/2_Project_Files/tools/_kam_live.sh"; kam_live_json --limit 5' _ "$FR" > "$O/C1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && [ "$(cat "$O/C1.out")" = "[]" ] && has "--seat friday --cert-dir $FR/4_Credentials/dashboard-cloud --decrypt --json --limit 5" "$FR/venv_args.log"; then
  ok "C1 _kam_live as friday: passes the seat guard, fetches with --seat friday and THIS tree's cert dir (stub venv)"
else bad "C1 kam_live friday: rc=$rc :: $(cat "$O/C1.out") :: $(cat "$FR/venv_args.log" 2>&1)"; fi
WED_AGENT=thursday bash -c '. "$1/2_Project_Files/tools/_kam_live.sh"; kam_live_json' _ "$FR" > "$O/C2.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && has "REFUSED" "$O/C2.out"; then ok "C2 _kam_live as thursday -> REFUSED rc 2"; else bad "C2 thursday: rc=$rc :: $(cat "$O/C2.out")"; fi
for v in n o_; do t="$BASE/$v/WEDNESDAY"; WED_AGENT=wednesday bash -c '. "$1/2_Project_Files/tools/_kam_live.sh"; kam_live_json --limit 5' _ "$t" > "$O/C3_$v.out" 2>&1; echo "rc=$?" >> "$O/C3_$v.out"; cp "$t/venv_args.log" "$O/C3_$v.args"; done
if same "$O/C3_n.out" "$O/C3_o_.out" && same "$O/C3_n.args" "$O/C3_o_.args"; then ok "C3 WEDNESDAY _kam_live output + fetch argv identical to the pre-friday file"
else bad "C3 differs :: $(diff "$O/C3_n.args.n" "$O/C3_o_.args.n")"; fi

# ═════ D/E. kam_rulings_today.sh / kam_msgs.sh --source local — whose tab ═══════
mkfx() { python3 - "$1" "$TODAY" "$2" <<'PY'
import json, sys
out, day, with_friday = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
rows = [("wednesday", "W-ROW to wednesday"), ("tuesday", "T-ROW to tuesday"), ("both", "B-ROW broadcast"), (None, "N-ROW untagged")]
if with_friday: rows.append(("friday", "F-ROW to friday"))
d = []
for i, (v, t) in enumerate(rows):
    e = {"role": "kam", "ts": "%sT09:0%d:00+10:00" % (day, i), "text": t}
    if v: e["view"] = v
    d.append(e)
json.dump(d, open(out, "w"))
PY
}
mkfx "$FR/0_Brain/dashboard/data/chat_log.json" 1; mkfx "$WN/0_Brain/dashboard/data/chat_log.json" 0; mkfx "$WO/0_Brain/dashboard/data/chat_log.json" 0
filt() { /usr/bin/grep -v -i -E 'FRESHNESS|STALE|min ago|newest' "$1"; }
WED_AGENT=friday bash "$FR/2_Project_Files/tools/kam_rulings_today.sh" --source local > "$O/D1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && has "F-ROW to friday" "$O/D1.out" && has "B-ROW" "$O/D1.out" && has "N-ROW" "$O/D1.out" && ! has "W-ROW" "$O/D1.out" && ! has "T-ROW" "$O/D1.out" && has "Showing 3 of 5" "$O/D1.out"; then
  ok "D1 kam_rulings_today as friday: shows view=friday + broadcast + untagged, withholds wednesday/tuesday tabs (3 of 5)"
else bad "D1 rulings friday: rc=$rc :: $(cat "$O/D1.out")"; fi
for v in n o_; do WED_AGENT=wednesday bash "$BASE/$v/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh" --source local > "$O/D2_$v.raw" 2>&1; filt "$O/D2_$v.raw" > "$O/D2_$v.out"; done
if same "$O/D2_n.out" "$O/D2_o_.out" && has "W-ROW" "$O/D2_n.out"; then ok "D2 WEDNESDAY kam_rulings_today identical to the pre-friday file (fixture with no friday rows; freshness lines excluded)"
else bad "D2 differs :: $(diff "$O/D2_n.out.n" "$O/D2_o_.out.n")"; fi
mkfx "$WN/0_Brain/dashboard/data/chat_log.json" 1; mkfx "$WO/0_Brain/dashboard/data/chat_log.json" 1
for v in n o_; do WED_AGENT=wednesday bash "$BASE/$v/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh" --source local > "$O/D3_$v.out" 2>&1; done
if ! has "F-ROW" "$O/D3_n.out" && has "F-ROW" "$O/D3_o_.out" && has "Showing 3 of 5" "$O/D3_n.out"; then
  ok "D3 INTENDED CHANGE: with a view=friday row present, Wednesday now withholds it (old file showed it as an unknown tag)"
else bad "D3 friday-row routing :: new=$(/usr/bin/grep -c F-ROW "$O/D3_n.out") old=$(/usr/bin/grep -c F-ROW "$O/D3_o_.out")"; fi
WED_AGENT=friday bash "$FR/2_Project_Files/tools/kam_msgs.sh" 10 --source local > "$O/E1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && /usr/bin/grep -F "view=wednesday" "$O/E1.out" | /usr/bin/grep -qF "NOT addressed to Friday" && ! /usr/bin/grep -F "view=friday" "$O/E1.out" | /usr/bin/grep -qF "NOT addressed"; then
  ok "E1 kam_msgs as friday: a view=wednesday row is flagged NOT addressed to Friday; the view=friday row is not flagged"
else bad "E1 kam_msgs friday: rc=$rc :: $(cat "$O/E1.out")"; fi
for v in n o_; do WED_AGENT=wednesday bash "$BASE/$v/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh" 10 --source local > "$O/E2_$v.out" 2>&1; done
if cmp -s "$O/E2_n.out" "$O/E2_o_.out" && /usr/bin/grep -F "view=friday" "$O/E2_n.out" | /usr/bin/grep -qF "NOT addressed to Wednesday"; then
  ok "E2 WEDNESDAY kam_msgs byte-identical to the pre-friday file (incl. a view=friday row flagged NOT addressed to Wednesday)"
else bad "E2 differs :: $(diff "$O/E2_n.out" "$O/E2_o_.out")"; fi

# ═════ F. statusline_publish.sh — usage_<seat>.json ═════════════════════════════
SLJ='{"rate_limits":{"seven_day":{"used_percentage":42.4,"resets_at":4102444800}}}'
printf '%s' "$SLJ" | sh "$FR/2_Project_Files/tools/statusline_publish.sh" LBL friday > "$O/F1.out" 2>&1
printf '%s' "$SLJ" | sh "$FR/2_Project_Files/tools/statusline_publish.sh" LBL thursday > "$O/F2.out" 2>&1
if python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d["agent"]=="friday" and d["pct"]==42 else 1)' "$FR/0_Brain/dashboard/data/usage_friday.json" \
   && [ ! -e "$FR/0_Brain/dashboard/data/usage_thursday.json" ] && has "not wednesday, tuesday or friday" "$FR/2_Project_Files/logs/statusline_publish.log"; then
  ok "F1 statusline_publish: friday -> usage_friday.json (pct 42); thursday publishes nothing and logs why"
else bad "F1 statusline friday :: $(cat "$O/F1.out" "$O/F2.out") :: $(cat "$FR/2_Project_Files/logs/statusline_publish.log" 2>&1)"; fi
for v in n o_; do printf '%s' "$SLJ" | sh "$BASE/$v/WEDNESDAY/2_Project_Files/tools/statusline_publish.sh" LBL wednesday > "$O/F3_$v.out" 2>&1
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d.pop("ts"); print(json.dumps(d,sort_keys=True))' "$BASE/$v/WEDNESDAY/0_Brain/dashboard/data/usage_wednesday.json" > "$O/F3_$v.json"; done
if cmp -s "$O/F3_n.json" "$O/F3_o_.json" && cmp -s "$O/F3_n.out" "$O/F3_o_.out"; then ok "F3 WEDNESDAY statusline_publish output + usage_wednesday.json identical (ts excluded)"
else bad "F3 differs :: $(diff "$O/F3_n.json" "$O/F3_o_.json")"; fi

# ═════ G. decision_queue.sh — seat stamp + ruling ownership (LIVE_BOARD=0) ══════
DQ="2_Project_Files/tools/decision_queue.sh"
addcard() { LIVE_BOARD=0 bash "$1/$DQ" add --id "$2" --client-project "$3" --title "arms $2" --bluf "b" --option a:A --option b:B --recommended a --default-action "none"; }
addcard "$FR" arms-fri-card Datasec/NexusAI > "$O/G1.out" 2>&1; rc=$?
FS="$FR/0_Brain/dashboard/data/decisions.json"
if [ "$rc" = 0 ] && python3 -c 'import json,sys; c=[x for x in json.load(open(sys.argv[1])) if x["id"]=="arms-fri-card"][0]; sys.exit(0 if c.get("seat")=="friday" else 1)' "$FS"; then
  ok "G1 decision_queue add on a FRIDAY tree stamps seat=friday"
else bad "G1 add friday: rc=$rc :: $(cat "$O/G1.out")"; fi
LIVE_BOARD=0 WED_AGENT=wednesday DQ_FILE="$FS" bash "$FR/$DQ" rule arms-fri-card a > "$O/G2.out" 2>&1; rc=$?
LIVE_BOARD=0 WED_AGENT=tuesday DQ_FILE="$FS" bash "$FR/$DQ" rule arms-fri-card a > "$O/G2t.out" 2>&1; rc2=$?
if [ "$rc" = 2 ] && [ "$rc2" = 2 ] && has "FRIDAY-seat card" "$O/G2.out" && has "FRIDAY-seat card" "$O/G2t.out" \
   && python3 -c 'import json,sys; c=[x for x in json.load(open(sys.argv[1])) if x["id"]=="arms-fri-card"][0]; sys.exit(0 if c["status"]=="open" else 1)' "$FS"; then
  ok "G2 wednesday AND tuesday are refused ruling a seat=friday card (card still open)"
else bad "G2 cross-seat rule: rc=$rc/$rc2 :: $(cat "$O/G2.out" "$O/G2t.out")"; fi
LIVE_BOARD=0 bash "$FR/$DQ" rule arms-fri-card a > "$O/G3.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && has "ruled: arms-fri-card -> a" "$O/G3.out"; then ok "G3 the friday seat rules its own card"
else bad "G3 friday rule: rc=$rc :: $(cat "$O/G3.out")"; fi
addcard "$WN" arms-wed-card Secuura/Blockchain > "$O/G4a.out" 2>&1
LIVE_BOARD=0 WED_AGENT=friday DQ_FILE="$WN/0_Brain/dashboard/data/decisions.json" bash "$WN/$DQ" rule arms-wed-card a > "$O/G4.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && has "not a friday-seat card" "$O/G4.out"; then ok "G4 the friday seat is refused ruling a card it did not create"
else bad "G4 friday on wednesday card: rc=$rc :: $(cat "$O/G4.out")"; fi
addcard "$WO" arms-wed-card Secuura/Blockchain > "$O/G5a_o.out" 2>&1
for v in n o_; do LIVE_BOARD=0 bash "$BASE/$v/WEDNESDAY/$DQ" rule arms-wed-card b > "$O/G5_$v.out" 2>&1; echo "rc=$?" >> "$O/G5_$v.out"
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); [c.pop(k,None) for c in d for k in ("ts","ruled_ts")]; print(json.dumps(d,sort_keys=True))' "$BASE/$v/WEDNESDAY/0_Brain/dashboard/data/decisions.json" > "$O/G5_$v.json"; done
if cmp -s "$O/G5_n.json" "$O/G5_o_.json" && same "$O/G4a.out" "$O/G5a_o.out" && cmp -s "$O/G5_n.out" "$O/G5_o_.out" && ! /usr/bin/grep -q '"seat"' "$O/G5_n.json"; then
  ok "G5 WEDNESDAY add + rule identical to the pre-friday file (no seat field written; ts excluded)"
else bad "G5 differs :: $(diff "$O/G5_n.json" "$O/G5_o_.json" | head -4) :: $(diff "$O/G5_n.out" "$O/G5_o_.out")"; fi

# ═════ H. reconcile_rulings.py — whose card each seat rules ═════════════════════
mkdir -p "$BASE/rr"
cat > "$BASE/rr/cards.json" <<'EOF'
[{"id":"rr-secuura","client_project":"Secuura/Blockchain","status":"open","title":"s","bluf":"b","options":[{"key":"a","label":"A"},{"key":"b","label":"B"}],"recommended":"a","default_action":"x"},
 {"id":"rr-datasec","client_project":"Datasec/NexusAI","status":"open","title":"d","bluf":"b","options":[{"key":"a","label":"A"},{"key":"b","label":"B"}],"recommended":"a","default_action":"x"},
 {"id":"rr-friday","client_project":"Datasec/NexusAI","seat":"friday","status":"open","title":"f","bluf":"b","options":[{"key":"a","label":"A"},{"key":"b","label":"B"}],"recommended":"a","default_action":"x"}]
EOF
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); json.dump([c for c in d if c.get("seat")!="friday"], open(sys.argv[2],"w"))' "$BASE/rr/cards.json" "$BASE/rr/cards_nofri.json"
printf '[{"role":"kam","ts":"%sT09:00:00+10:00","text":"Decision rr-secuura: a — A"},{"role":"kam","ts":"%sT09:01:00+10:00","text":"Decision rr-datasec: a — A"},{"role":"kam","ts":"%sT09:02:00+10:00","text":"Decision rr-friday: b — B"}]' "$TODAY" "$TODAY" "$TODAY" > "$BASE/rr/kam.json"
rr() { WED_AGENT="$1" RECONCILE_SOURCE=local RECONCILE_CHAT="$BASE/rr/kam.json" RECONCILE_DECISIONS="$2" LIVE_BOARD=0 python3 "$3" ${4:-} 2>&1; }
rr friday "$BASE/rr/cards.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" > "$O/H1.out"
rr wednesday "$BASE/rr/cards.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" > "$O/H2.out"
rr tuesday "$BASE/rr/cards.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" > "$O/H3.out"
wr() { /usr/bin/grep -c "WOULD RULE  $2 " "$1"; }
if [ "$(wr "$O/H1.out" rr-friday)$(wr "$O/H1.out" rr-secuura)$(wr "$O/H1.out" rr-datasec)" = "100" ] \
   && [ "$(wr "$O/H2.out" rr-friday)$(wr "$O/H2.out" rr-secuura)$(wr "$O/H2.out" rr-datasec)" = "010" ] \
   && [ "$(wr "$O/H3.out" rr-friday)$(wr "$O/H3.out" rr-secuura)$(wr "$O/H3.out" rr-datasec)" = "001" ] \
   && /usr/bin/grep "rr-friday" "$O/H2.out" | /usr/bin/grep -q "OUT OF SCOPE" && /usr/bin/grep "rr-friday" "$O/H3.out" | /usr/bin/grep -q "OUT OF SCOPE"; then
  ok "H1 reconcile: friday would rule ONLY the seat=friday card; wednesday only Secuura; tuesday only Datasec; the friday card is OUT OF SCOPE for both"
else bad "H1 reconcile scope :: F=[$(cat "$O/H1.out")] W=[$(cat "$O/H2.out")] T=[$(cat "$O/H3.out")]"; fi
OLDRR="$(bk 2_Project_Files/tools/reconcile_rulings.py)"
rr tuesday "$BASE/rr/cards.json" "$OLDRR" > "$O/H4.out"
if [ "$(wr "$O/H4.out" rr-friday)" = 1 ]; then ok "H4 NEGATIVE: the pre-friday reconciler as tuesday WOULD rule the seat=friday card (H1 can fail)"
else bad "H4 negative did not reproduce :: $(cat "$O/H4.out")"; fi
rr wednesday "$BASE/rr/cards_nofri.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" > "$O/H5_n.out"; rr wednesday "$BASE/rr/cards_nofri.json" "$OLDRR" > "$O/H5_o.out"
rr tuesday "$BASE/rr/cards_nofri.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" > "$O/H5t_n.out"; rr tuesday "$BASE/rr/cards_nofri.json" "$OLDRR" > "$O/H5t_o.out"
if cmp -s "$O/H5_n.out" "$O/H5_o.out" && cmp -s "$O/H5t_n.out" "$O/H5t_o.out"; then ok "H5 WEDNESDAY (and tuesday) reconcile reports byte-identical to the pre-friday file on non-friday cards"
else bad "H5 differs :: $(diff "$O/H5_n.out" "$O/H5_o.out") :: $(diff "$O/H5t_n.out" "$O/H5t_o.out")"; fi
rr thursday "$BASE/rr/cards.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" > "$O/H6.out"; rc=$?
if /usr/bin/grep -q "REFUSING" "$O/H6.out"; then ok "H6 reconcile as thursday -> REFUSING"; else bad "H6 thursday :: $(cat "$O/H6.out")"; fi
cp "$BASE/rr/cards.json" "$BASE/rr/cards_apply.json"
rr friday "$BASE/rr/cards_apply.json" "$FR/2_Project_Files/tools/reconcile_rulings.py" --apply > "$O/H7.out"
if /usr/bin/grep -q "RULED  rr-friday -> b" "$O/H7.out" && python3 -c 'import json,sys; d={c["id"]:c for c in json.load(open(sys.argv[1]))}; sys.exit(0 if d["rr-friday"]["status"]=="ruled" and d["rr-secuura"]["status"]=="open" and d["rr-datasec"]["status"]=="open" else 1)' "$BASE/rr/cards_apply.json"; then
  ok "H7 reconcile --apply as friday (fixture, LIVE_BOARD=0): rules rr-friday through decision_queue.sh, leaves the other two open"
else bad "H7 apply :: $(cat "$O/H7.out")"; fi

# ═════ I. chat_streams.py — the friday stream in the derived log ═══════════════
D_N="$WN/0_Brain/dashboard/data"; D_O="$WO/0_Brain/dashboard/data"
for d in "$D_N" "$D_O"; do
  printf '[{"role":"wednesday","ts":"2026-09-23T09:00:00+10:00","text":"w1","seat":"Studio"}]' > "$d/chat_wednesday.json"
  printf '[{"role":"wednesday","ts":"2026-09-23T09:01:00+10:00","text":"t1","seat":"mini","project":"Datasec"}]' > "$d/chat_tuesday.json"
  printf '[{"role":"kam","ts":"2026-09-23T09:02:00+10:00","text":"k1","view":"wednesday"}]' > "$d/chat_kam.json"
  mv "$d/chat_log.json" "$d/chat_log.json.fixture-before-I" 2>/dev/null
done
python3 "$WN/2_Project_Files/tools/chat_streams.py" > "$O/I2_n.out" 2>&1; python3 "$WO/2_Project_Files/tools/chat_streams.py" > "$O/I2_o.out" 2>&1
if cmp -s "$O/I2_n.out" "$O/I2_o.out" && cmp -s "$D_N/chat_log.json" "$D_O/chat_log.json" && ! has "friday" "$O/I2_n.out"; then
  ok "I1 WEDNESDAY chat_streams (no chat_friday.json): stdout + chat_log.json byte-identical to the pre-friday file"
else bad "I1 differs :: $(diff "$O/I2_n.out" "$O/I2_o.out")"; fi
printf '[{"role":"wednesday","ts":"2026-09-23T09:03:00+10:00","text":"f1","seat":"Kamils-MBP","project":"Friday"}]' > "$D_N/chat_friday.json"
python3 "$WN/2_Project_Files/tools/chat_streams.py" > "$O/I3.out" 2>&1
if has "chat_friday.json 1" "$O/I3.out" && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if [e["agent"] for e in d if e["text"]=="f1"]==["friday"] else 1)' "$D_N/chat_log.json"; then
  ok "I3 chat_streams: chat_friday.json merged, its entry carries agent=friday (derived from the FILE)"
else bad "I3 friday stream :: $(cat "$O/I3.out")"; fi
python3 - "$D_N/chat_log.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d.append({"role": "wednesday", "ts": "2026-09-23T09:04:00+10:00", "text": "orphan-f", "seat": "Kamils-MBP", "agent": "friday", "agent_source": "stream"})
json.dump(d, open(p, "w"))
PY
python3 "$WN/2_Project_Files/tools/chat_streams.py" --harvest > "$O/I4.out" 2>&1
if has "harvested 1 into chat_friday.json" "$O/I4.out" && has "orphan-f" "$D_N/chat_friday.json" && ! has "orphan-f" "$D_N/chat_tuesday.json"; then
  ok "I4 --harvest routes an orphan the derived file named agent=friday into chat_friday.json (not tuesday's, despite the MBP seat)"
else bad "I4 harvest :: $(cat "$O/I4.out")"; fi

# ═════ K. chat_push.sh — a view=friday panel message is mailed to Friday's inbox ═
for t in "$FR" "$WN" "$WO"; do printf '#!/bin/bash\necho "TAP $*" >> "%s/tap.log"\nexit 0\n' "$t" > "$t/2_Project_Files/tools/tap_wednesday.sh"; chmod +x "$t/2_Project_Files/tools/tap_wednesday.sh"
  printf '[{"role":"kam","ts":"2026-09-23T10:00:00+10:00","text":"K panel words","view":"x"}]' > "$t/0_Brain/dashboard/data/chat_kam.json"; done
ARMS_CURL_LOG="$O/K1.curl" PATH="$SPATH" bash "$FR/2_Project_Files/tools/chat_push.sh" "2026-09-23T10:00:00+10:00" friday > "$O/K1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && has "URL https://api.agentmail.to/v0/inboxes/friday-laptop-agent@agentmail.to/messages/send" "$O/K1.curl" && has "[Kam -> Friday] panel message" "$O/K1.curl" \
   && has "on the Friday tab" "$O/K1.curl" && has "friday-push: friday-laptop-agent@agentmail.to -> HTTP 200" "$FR/2_Project_Files/logs/chat_push.log" && has "TAP" "$FR/tap.log"; then
  ok "K1 chat_push view=friday -> mailed (stub) FROM+TO friday-laptop-agent@, subject [Kam -> Friday], 'Friday tab' body; Wednesday still tapped"
else bad "K1 chat_push friday: rc=$rc :: $(cat "$O/K1.out" "$O/K1.curl" 2>&1)"; fi
for v in n o_; do t="$BASE/$v/WEDNESDAY"; for view in tuesday both wednesday ""; do
  ARMS_CURL_LOG="$O/K2_$v.curl" PATH="$SPATH" bash "$t/2_Project_Files/tools/chat_push.sh" "2026-09-23T10:00:00+10:00" "$view" >> "$O/K2_$v.out" 2>&1; echo "rc=$?" >> "$O/K2_$v.out"; done
  cut -d' ' -f2- "$t/2_Project_Files/logs/chat_push.log" > "$O/K2_$v.log"; cp "$t/tap.log" "$O/K2_$v.tap"; done
if cmp -s "$O/K2_n.curl" "$O/K2_o_.curl" && cmp -s "$O/K2_n.log" "$O/K2_o_.log" && cmp -s "$O/K2_n.out" "$O/K2_o_.out" && cmp -s "$O/K2_n.tap" "$O/K2_o_.tap" && has "tuesday-agent@" "$O/K2_n.curl"; then
  ok "K2 WEDNESDAY chat_push for views tuesday/both/wednesday/none: curl argv, push log, taps identical to the pre-friday file"
else bad "K2 differs :: $(diff "$O/K2_n.curl" "$O/K2_o_.curl" | head -4) :: $(diff "$O/K2_n.log" "$O/K2_o_.log")"; fi

# ═════ L. _store_guard.sh guard_data_dir — chat_friday.json is irreplaceable ════
mkdir -p "$BASE/sg"; printf '[\n<<<<<<< HEAD\n{}\n=======\n{}\n>>>>>>> x\n]\n' > "$BASE/sg/chat_friday.json"
bash -c '. "$1"; guard_data_dir "$2"' _ "$FR/2_Project_Files/tools/_store_guard.sh" "$BASE/sg" > "$O/L1.out" 2>&1; rc=$?
bash -c '. "$1"; guard_data_dir "$2"' _ "$(bk 2_Project_Files/tools/_store_guard.sh)" "$BASE/sg" > "$O/L2.out" 2>&1; rc2=$?
if [ "$rc" != 0 ] && has "chat_friday.json" "$O/L1.out" && [ "$rc2" = 0 ]; then ok "L1 guard_data_dir refuses conflict markers in chat_friday.json (rc $rc); the pre-friday file did not look (rc 0, negative)"
else bad "L1 store guard: rc=$rc rc2=$rc2 :: $(cat "$O/L1.out")"; fi

# ═════ M. inbox_digest.sh — the seat's own inbox ════════════════════════════════
for s in friday; do ARMS_CURL_LOG="$O/M1.curl" PATH="$SPATH" WED_AGENT=$s INBOX_DIGEST_SEEN_FILE="$BASE/seen_M1" bash "$FR/2_Project_Files/fleet/inbox_digest.sh" > "$O/M1.out" 2>&1; echo "rc=$?" >> "$O/M1.out"; done
if has "URL https://api.agentmail.to/v0/inboxes/friday-laptop-agent@agentmail.to/messages?limit=50" "$O/M1.curl" && ! has "wednesday-agent@" "$O/M1.curl" \
   && /usr/bin/grep -F "[INBOUND]" "$O/M1.out" | /usr/bin/grep -qF "Secuura/Blockchain -> Friday" && /usr/bin/grep -F "[OUTBOUND]" "$O/M1.out" | /usr/bin/grep -qF "brief from friday" && has "BUS-DS" "$O/M1.out"; then
  ok "M1 inbox_digest as friday reads friday-laptop-agent@ (+ the bus), never wednesday-agent@; [X -> Friday] = INBOUND, own-sent = OUTBOUND; no client filter (both clients)"
else bad "M1 digest friday :: $(cat "$O/M1.out" "$O/M1.curl")"; fi
mkdir -p "$BASE/norow/FRIDAY/2_Project_Files/fleet" "$BASE/norow/FRIDAY/4_Credentials"; cp -p "$FR/4_Credentials/.env" "$BASE/norow/FRIDAY/4_Credentials/"
cp -p "$FR/2_Project_Files/fleet/inbox_digest.sh" "$BASE/norow/FRIDAY/2_Project_Files/fleet/"; /usr/bin/grep -v '^Friday|' "$FR/2_Project_Files/fleet/inbox_routing.conf" > "$BASE/norow/FRIDAY/2_Project_Files/fleet/inbox_routing.conf"
ARMS_CURL_LOG="$O/M2.curl" PATH="$SPATH" WED_AGENT=friday INBOX_DIGEST_SEEN_FILE="$BASE/seen_M2" bash "$BASE/norow/FRIDAY/2_Project_Files/fleet/inbox_digest.sh" > "$O/M2.out" 2>&1; rc=$?
if [ "$rc" != 0 ] && has "no 'Friday' row" "$O/M2.out" && [ ! -s "$O/M2.curl" ]; then ok "M2 inbox_digest as friday with no Friday routing row -> refuses (rc $rc) before any fetch"
else bad "M2 no-row: rc=$rc :: $(cat "$O/M2.out")"; fi
for s in wednesday tuesday; do for v in n o_; do
  ARMS_CURL_LOG="$O/M3_${s}_$v.curl" PATH="$SPATH" WED_AGENT=$s INBOX_DIGEST_SEEN_FILE="$BASE/seen_M3_${s}_$v" bash "$BASE/$v/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh" > "$O/M3_${s}_$v.out" 2>&1; echo "rc=$?" >> "$O/M3_${s}_$v.out"; done; done
if cmp -s "$O/M3_wednesday_n.out" "$O/M3_wednesday_o_.out" && cmp -s "$O/M3_tuesday_n.out" "$O/M3_tuesday_o_.out" && cmp -s "$O/M3_wednesday_n.curl" "$O/M3_wednesday_o_.curl" && has "WED-IN" "$O/M3_wednesday_n.out"; then
  ok "M3 WEDNESDAY (and tuesday) inbox_digest output + fetched URLs byte-identical to the pre-friday file"
else bad "M3 differs :: $(diff "$O/M3_wednesday_n.out" "$O/M3_wednesday_o_.out" | head -4) :: $(diff "$O/M3_tuesday_n.out" "$O/M3_tuesday_o_.out" | head -4)"; fi

# ═════ N. send_brief.sh — the sending inbox (trace; exits at the usage check, nothing sent) ═
PATH="$SPATH" WED_AGENT=friday bash -x "$FR/2_Project_Files/fleet/send_brief.sh" > "$O/N1.out" 2> "$O/N1.trace"; rc=$?
PATH="$SPATH" WED_AGENT=friday bash "$WN/2_Project_Files/fleet/send_brief.sh" > "$O/N2.out" 2>&1; rc2=$?
PATH="$SPATH" WED_AGENT=thursday bash "$FR/2_Project_Files/fleet/send_brief.sh" > "$O/N3.out" 2>&1; rc3=$?
if /usr/bin/grep -q "INBOX=friday-laptop-agent@agentmail.to" "$O/N1.trace" && [ "$rc" != 0 ] && [ "$rc2" = 2 ] && has "DISAGREE" "$O/N2.out" && [ "$rc3" = 2 ] && has "REFUSING" "$O/N3.out"; then
  ok "N1 send_brief: friday on a FRIDAY tree sends FROM friday-laptop-agent@ (trace); friday on a WEDNESDAY tree and thursday anywhere REFUSE"
else bad "N1 send_brief :: rc=$rc/$rc2/$rc3 :: $(/usr/bin/grep INBOX= "$O/N1.trace") :: $(cat "$O/N2.out" "$O/N3.out")"; fi
for v in n o_; do PATH="$SPATH" WED_AGENT=wednesday bash -x "$BASE/$v/WEDNESDAY/2_Project_Files/fleet/send_brief.sh" > "$O/N4_$v.out" 2> "$O/N4_$v.trace"; echo "rc=$?" >> "$O/N4_$v.out"
  /usr/bin/grep -E '^\++ (INBOX|SEAT_KEY|TREE_SEAT)=' "$O/N4_$v.trace" > "$O/N4_$v.vars"; done
if cmp -s "$O/N4_n.vars" "$O/N4_o_.vars" && same "$O/N4_n.out" "$O/N4_o_.out" && has "INBOX=wednesday-agent@agentmail.to" "$O/N4_n.vars"; then
  ok "N4 WEDNESDAY send_brief: SEAT_KEY/TREE_SEAT/INBOX and the usage exit identical to the pre-friday file"
else bad "N4 differs :: $(diff "$O/N4_n.vars" "$O/N4_o_.vars")"; fi

# ═════ O. wake_watch.sh — the seat's inbox + Kam tag (stub curl/tmux; stopped after 4 s) ═
ww() { # ww <tree> <outtag> [WED_AGENT]
  ( env ARMS_CURL_LOG="$O/$2.curl" PATH="$SPATH" ${3:+WED_AGENT=$3} bash "$1/2_Project_Files/fleet/cockpit/wake_watch.sh" "2026-09-23T00:00" 9999 1 > "$O/$2.out" 2>&1 ) &
  local p=$!; sleep 4; kill "$p" > "$O/$2.kill" 2>&1; pkill -P "$p" > "$O/$2.kill2" 2>&1; wait "$p" > "$O/$2.wait" 2>&1; true; }
ww "$FR" O1
if has "URL https://api.agentmail.to/v0/inboxes/friday-laptop-agent@agentmail.to/messages?limit=10" "$O/O1.curl" && ! has "wednesday-agent@" "$O/O1.curl"; then
  ok "O1 wake_watch on a FRIDAY tree (WED_AGENT unset) polls friday-laptop-agent@, never wednesday-agent@"
else bad "O1 wake_watch friday :: $(cat "$O/O1.out" "$O/O1.curl" 2>&1 | head -8)"; fi
mkdir -p "$BASE/norow/FRIDAY/2_Project_Files/fleet/cockpit"; for f in wake_watch.sh seat_resolve.sh dead_banner_check.sh exited_seat_check.sh; do cp -p "$FR/2_Project_Files/fleet/cockpit/$f" "$BASE/norow/FRIDAY/2_Project_Files/fleet/cockpit/"; done
ARMS_CURL_LOG="$O/O2.curl" PATH="$SPATH" bash "$BASE/norow/FRIDAY/2_Project_Files/fleet/cockpit/wake_watch.sh" "2026-09-23T00:00" 9999 1 > "$O/O2.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && has "REFUSED" "$O/O2.out" && [ ! -s "$O/O2.curl" ]; then ok "O2 wake_watch as friday with no Friday routing row -> REFUSED rc 2, no poll (never falls back to Wednesday's inbox)"
else bad "O2 no-row: rc=$rc :: $(cat "$O/O2.out")"; fi
ww "$WN" O3_n; ww "$WO" O3_o_
if [ -s "$O/O3_n.curl" ] && [ "$(sort -u "$O/O3_n.curl")" = "$(sort -u "$O/O3_o_.curl")" ] && has "wednesday-agent@agentmail.to" "$O/O3_n.curl"; then
  ok "O3 WEDNESDAY wake_watch polls the same URL set as the pre-friday file (wednesday-agent@)"
else bad "O3 differs :: $(sort -u "$O/O3_n.curl") :: $(sort -u "$O/O3_o_.curl")"; fi

# ═════ P. live_chat_poll.sh — seat guard + default tap ═════════════════════════
PATH="$SPATH" bash -x "$FR/2_Project_Files/fleet/cockpit/live_chat_poll.sh" --seat friday --once --dry-run > "$O/P1.out" 2> "$O/P1.trace"; rc=$?
PATH="$SPATH" bash "$FR/2_Project_Files/fleet/cockpit/live_chat_poll.sh" --seat thursday --once --dry-run > "$O/P2.out" 2>&1; rc2=$?
if /usr/bin/grep -q "TAP=$FR/2_Project_Files/tools/tap_friday.sh" "$O/P1.trace" && ! /usr/bin/grep -qi "REFUSING" "$O/P1.out" && [ "$rc2" = 2 ] && has "REFUSING" "$O/P2.out"; then
  ok "P1 live_chat_poll --seat friday passes the seat guard and defaults its tap to tools/tap_friday.sh; --seat thursday REFUSES"
else bad "P1 poll :: rc=$rc/$rc2 :: $(/usr/bin/grep 'TAP=' "$O/P1.trace") :: $(cat "$O/P1.out" "$O/P2.out")"; fi
for v in n o_; do PATH="$SPATH" bash -x "$BASE/$v/WEDNESDAY/2_Project_Files/fleet/cockpit/live_chat_poll.sh" --seat wednesday --once --dry-run > "$O/P3_$v.out" 2> "$O/P3_$v.trace"; echo "rc=$?" >> "$O/P3_$v.out"
  /usr/bin/grep -E '^\++ (TAP|STATE|SEAT)=' "$O/P3_$v.trace" > "$O/P3_$v.vars"; done
if same "$O/P3_n.vars" "$O/P3_o_.vars" && same "$O/P3_n.out" "$O/P3_o_.out" && /usr/bin/grep -q 'tap_wednesday.sh' "$O/P3_n.vars"; then
  ok "P3 WEDNESDAY live_chat_poll: TAP/STATE/SEAT and the dry-run output identical to the pre-friday file (tap_wednesday.sh)"
else bad "P3 differs :: $(diff "$O/P3_n.vars.n" "$O/P3_o_.vars.n") :: $(diff "$O/P3_n.out.n" "$O/P3_o_.out.n")"; fi

# ═════ Q. wednesday_rotate.sh — the seat launcher (refusal path only: no launcher exists in scratch) ═
env -u ROTATE_TMUX_SESSION -u ROTATE_LAUNCH_CMD WED_AGENT=friday bash "$FR/2_Project_Files/fleet/cockpit/wednesday_rotate.sh" --self > "$O/Q1.out" 2>&1; rc=$?
env -u ROTATE_TMUX_SESSION -u ROTATE_LAUNCH_CMD WED_AGENT=thursday bash "$FR/2_Project_Files/fleet/cockpit/wednesday_rotate.sh" --self > "$O/Q2.out" 2>&1; rc2=$?
if [ "$rc" = 2 ] && has "seat 'friday' but its launcher is missing: $FR/Launch_Friday.command" "$O/Q1.out" && [ "$rc2" = 2 ] && has "(wednesday|tuesday|friday)" "$O/Q2.out"; then
  ok "Q1 wednesday_rotate: friday maps to Launch_Friday.command (refused here only because the scratch tree has none); thursday REFUSED"
else bad "Q1 rotate :: rc=$rc/$rc2 :: $(cat "$O/Q1.out" "$O/Q2.out")"; fi
for v in n o_; do env -u ROTATE_TMUX_SESSION -u ROTATE_LAUNCH_CMD bash "$BASE/$v/WEDNESDAY/2_Project_Files/fleet/cockpit/wednesday_rotate.sh" --self > "$O/Q3_$v.out" 2>&1; echo "rc=$?" >> "$O/Q3_$v.out"; done
if same "$O/Q3_n.out" "$O/Q3_o_.out" && has "Launch_Wednesday.command" "$O/Q3_n.out"; then ok "Q3 WEDNESDAY wednesday_rotate launcher resolution identical to the pre-friday file"
else bad "Q3 differs :: $(diff "$O/Q3_n.out.n" "$O/Q3_o_.out.n")"; fi

# ═════ R. rotate_liveness.sh — the seat named in the alarm (TEST MODE, stubs, no relaunch) ═
for t in "$FR" "$WN" "$WO"; do mkdir -p "$t/stubs"; printf '#!/bin/bash\necho "SPEAK $*" >> "%s/stubs/said.log"\n' "$t" > "$t/stubs/speak.sh"; printf '#!/bin/bash\necho "PANEL $*" >> "%s/stubs/said.log"\n' "$t" > "$t/stubs/chat_reply.sh"; chmod +x "$t/stubs/"*.sh
  printf '%%99 [x] title 1 dead=0\n' > "$t/stubs/before.txt"; done
rl() { env LIVENESS_TEST=1 LIVENESS_DELAY=0 LIVENESS_STUB_DIR="$1/stubs" LIVENESS_LAUNCH_CMD= ${2:+WED_AGENT=$2} bash "$1/2_Project_Files/fleet/cockpit/rotate_liveness.sh" "armsnosuch_friday_$$" "$1/stubs/before.txt" "%99" > "$1/stubs/rl.out" 2>&1; echo "rc=$?" >> "$1/stubs/rl.out"; }
rl "$FR" friday
if has "PANEL --project WED Friday: the fleet tmux session DIED" "$FR/stubs/said.log" && has "(seat friday," "$FR/2_Project_Files/fleet/cockpit/logs/rotate_wednesday.log" && has "RELAUNCH SKIPPED" "$FR/2_Project_Files/fleet/cockpit/logs/rotate_wednesday.log"; then
  ok "R1 rotate_liveness (test mode) names seat friday and mirrors 'Friday: …' to the (stub) panel; no relaunch"
else bad "R1 liveness friday :: $(cat "$FR/stubs/rl.out" "$FR/stubs/said.log" 2>&1)"; fi
rl "$WN" wednesday; rl "$WO" wednesday
for v in n o_; do t="$BASE/$v/WEDNESDAY"; cut -d' ' -f3- "$t/2_Project_Files/fleet/cockpit/logs/rotate_wednesday.log" | sed -E 's/ROTATE_LOSS_[0-9_]+/ROTATE_LOSS_<N>/g; s/[0-9]{2}:[0-9]{2}/<HM>/g' > "$O/R2_$v.log"; sed -E 's/ROTATE_LOSS_[0-9_]+/ROTATE_LOSS_<N>/g; s/[0-9]{2}:[0-9]{2}/<HM>/g' "$t/stubs/said.log" > "$O/R2_$v.said"; done
if same "$O/R2_n.log" "$O/R2_o_.log" && cmp -s "$O/R2_n.said" "$O/R2_o_.said" && has "Wednesday: the fleet tmux session DIED" "$O/R2_n.said"; then
  ok "R2 WEDNESDAY rotate_liveness log + alarm wording identical to the pre-friday file"
else bad "R2 differs :: $(diff "$O/R2_n.log.n" "$O/R2_o_.log.n" | head -4) :: $(diff "$O/R2_n.said" "$O/R2_o_.said")"; fi

# ═════ S/T. installers — friday gets NO scheduled jobs (a no-op, exit 0) ═════════
env -u WED_AGENT bash "$FR/2_Project_Files/scheduler/install_all_jobs.sh" > "$O/S1.out" 2>&1; rc=$?
env -u WED_AGENT bash "$FR/2_Project_Files/scheduler/install_all_jobs.sh" --check > "$O/S2.out" 2>&1; rc2=$?
WED_AGENT=wednesday bash "$FR/2_Project_Files/scheduler/install_all_jobs.sh" --check > "$O/S3.out" 2>&1; rc3=$?
env -u WED_AGENT bash "$TH/2_Project_Files/scheduler/install_all_jobs.sh" --check > "$O/S4.out" 2>&1; rc4=$?
if [ "$rc" = 0 ] && [ "$rc2" = 0 ] && [ "$(cat "$O/S1.out")" = "friday seat: no scheduled jobs are installed on the laptop" ] && [ "$(cat "$O/S2.out")" = "friday seat: no scheduled jobs are installed on the laptop" ] \
   && [ "$rc3" = 2 ] && has "REFUSED" "$O/S3.out" && [ "$rc4" = 2 ] && has "not WEDNESDAY, TUESDAY or FRIDAY" "$O/S4.out"; then
  ok "S1 install_all_jobs: FRIDAY tree -> the no-op line, exit 0 (install and --check); env/tree disagreement and THURSDAY -> REFUSED"
else bad "S1 installer :: rc=$rc/$rc2/$rc3/$rc4 :: $(cat "$O/S1.out" "$O/S2.out" "$O/S3.out" "$O/S4.out")"; fi
env -u WED_AGENT bash "$SRC/2_Project_Files/scheduler/install_all_jobs.sh" --check > "$O/S5_n.out" 2>&1; echo "rc=$?" >> "$O/S5_n.out"
env -u WED_AGENT bash "$(bk 2_Project_Files/scheduler/install_all_jobs.sh)" --check > "$O/S5_o.out" 2>&1; echo "rc=$?" >> "$O/S5_o.out"
if cmp -s "$O/S5_n.out" "$O/S5_o.out" && has "jobs for seat 'wednesday'" "$O/S5_n.out"; then ok "S5 WEDNESDAY (this tree) install_all_jobs --check byte-identical to the pre-friday file (read-only launchctl)"
else bad "S5 differs :: $(diff "$O/S5_n.out" "$O/S5_o.out")"; fi
WED_AGENT=friday bash "$FR/2_Project_Files/scheduler/install_scheduler.command" > "$O/T1.out" 2>&1; rc=$?
if [ "$rc" = 0 ] && [ "$(cat "$O/T1.out")" = "friday seat: no scheduled jobs are installed on the laptop" ]; then ok "T1 install_scheduler.command as friday -> the same no-op line, exit 0"
else bad "T1 install_scheduler friday: rc=$rc :: $(cat "$O/T1.out")"; fi

# ═════ U/V. job scripts — refuse friday BY NAME ═══════════════════════════════
PATH="$SPATH" WEDNESDAY_TEST_HOUR=5 WEDNESDAY_DRYRUN=1 bash "$FR/2_Project_Files/scheduler/shift_change.sh" > "$O/U1.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && has "seat friday: the laptop runs no scheduled jobs" "$O/U1.out"; then ok "U1 shift_change on a FRIDAY tree -> REFUSING by name (rc 2)"
else bad "U1 shift_change friday: rc=$rc :: $(cat "$O/U1.out")"; fi
for v in n o_; do PATH="$SPATH" WEDNESDAY_TEST_HOUR=5 WEDNESDAY_DRYRUN=1 bash "$BASE/$v/WEDNESDAY/2_Project_Files/scheduler/shift_change.sh" > "$O/U2_$v.out" 2>&1; echo "rc=$?" >> "$O/U2_$v.out"
  cut -d' ' -f3- "$BASE/$v/WEDNESDAY/2_Project_Files/scheduler/logs/shift_change_$TODAY.log" > "$O/U2_$v.log" 2>&1; done
if same "$O/U2_n.out" "$O/U2_o_.out" && same "$O/U2_n.log" "$O/U2_o_.log"; then ok "U2 WEDNESDAY shift_change (dry run, no tmux) output + log identical to the pre-friday file"
else bad "U2 differs :: $(diff "$O/U2_n.log.n" "$O/U2_o_.log.n") :: $(diff "$O/U2_n.out.n" "$O/U2_o_.out.n")"; fi
# U3 — the tree-path fix in shift_change.sh (it passed ".../2_Project_Files/.." whose basename is "..", so NO tree ever
# decided). On a TUESDAY tree with WED_AGENT unset (how launchd runs it) the new file addresses wraps to tuesday-agent@;
# the pre-friday file addressed them to wednesday-agent@ (the defect, reproduced as the negative).
TU="$BASE/TUESDAY"; mkdir -p "$TU/2_Project_Files/scheduler" "$TU/2_Project_Files/fleet/cockpit"; cp -p "$SRC/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$TU/2_Project_Files/fleet/cockpit/"
cp -p "$SRC/2_Project_Files/scheduler/shift_change.sh" "$TU/2_Project_Files/scheduler/shift_change.sh"; cp -p "$(bk 2_Project_Files/scheduler/shift_change.sh)" "$TU/2_Project_Files/scheduler/shift_change_old.sh"
PATH="$SPATH" WEDNESDAY_TEST_HOUR=5 WEDNESDAY_DRYRUN=1 bash -x "$TU/2_Project_Files/scheduler/shift_change.sh" > "$O/U3n.out" 2> "$O/U3n.trace"
PATH="$SPATH" WEDNESDAY_TEST_HOUR=5 WEDNESDAY_DRYRUN=1 bash -x "$TU/2_Project_Files/scheduler/shift_change_old.sh" > "$O/U3o.out" 2> "$O/U3o.trace"
if /usr/bin/grep -q '^+ WRAP_INBOX=tuesday-agent@agentmail.to' "$O/U3n.trace" && /usr/bin/grep -q '^+ WRAP_INBOX=wednesday-agent@agentmail.to' "$O/U3o.trace"; then
  ok "U3 shift_change on a TUESDAY tree (WED_AGENT unset): wraps now addressed to tuesday-agent@; the pre-friday file said wednesday-agent@ (negative)"
else bad "U3 tree-path fix :: new=$(/usr/bin/grep 'WRAP_INBOX=' "$O/U3n.trace") old=$(/usr/bin/grep 'WRAP_INBOX=' "$O/U3o.trace")"; fi
WED_AGENT=friday bash "$FR/2_Project_Files/scheduler/nas_sync.sh" > "$O/V1.out" 2>&1; rc=$?
if [ "$rc" = 2 ] && has "REFUSED — seat friday" "$O/V1.out" && [ -z "$(ls "$FR/2_Project_Files/scheduler/logs" 2>/dev/null | /usr/bin/grep -i nas_sync)" ]; then
  ok "V1 nas_sync as friday -> REFUSED rc 2 before any log, state or engine call"
else bad "V1 nas_sync friday: rc=$rc :: $(cat "$O/V1.out")"; fi

# ═════ Y. pathguard.py — FRIDAY is a sister tree ═══════════════════════════════
pg() { printf '%s' "$2" | HOOK_OWN_ROOT="$1" python3 "$3" 2>&1; }
PG="$FR/2_Project_Files/fleet/hooks/pathguard.py"; PGO="$(bk 2_Project_Files/fleet/hooks/pathguard.py)"
r1="$(pg /Volumes/DevMASTER/WEDNESDAY 'cp a /Volumes/DevMASTER/FRIDAY/b' "$PG")"; r2="$(pg /Volumes/DevMASTER/FRIDAY 'cp a /Volumes/DevMASTER/FRIDAY/b' "$PG")"
r3="$(pg /Volumes/DevMASTER/FRIDAY 'cp a /Volumes/DevMASTER/WEDNESDAY/b' "$PG")"; r4="$(pg /Volumes/DevMASTER/FRIDAY 'echo x > /Volumes/DevMASTER/TUESDAY/b' "$PG")"
r5="$(pg /Volumes/DevMASTER/WEDNESDAY 'cp a /Volumes/DevMASTER/FRIDAY/b' "$PGO")"
if [ "$r1" = "cp|/Volumes/DevMASTER/FRIDAY/b" ] && [ -z "$r2" ] && [ "$r3" = "cp|/Volumes/DevMASTER/WEDNESDAY/b" ] && [ "$r4" = "redirect|/Volumes/DevMASTER/TUESDAY/b" ] && [ -z "$r5" ]; then
  ok "Y1 pathguard: Wednesday is refused writes into FRIDAY/; Friday passes its own tree and is refused WEDNESDAY/ + TUESDAY/; the pre-friday file let FRIDAY/ through (negative)"
else bad "Y1 pathguard :: [$r1] [$r2] [$r3] [$r4] [$r5]"; fi
: > "$O/Y2_n.out"; : > "$O/Y2_o.out"
for c in 'cp a /Volumes/DevMASTER/TUESDAY/b' 'cp a /Volumes/DevMASTER/WEDNESDAY/b' 'cp a /Volumes/X/!CODING/p/f' 'echo > "/Volumes/DevMASTER/Notes (MASTER)/x"' 'cat /Volumes/DevMASTER/TUESDAY/x' 'rm /tmp/x'; do
  pg /Volumes/DevMASTER/WEDNESDAY "$c" "$PG" >> "$O/Y2_n.out"; echo "|" >> "$O/Y2_n.out"; pg /Volumes/DevMASTER/WEDNESDAY "$c" "$PGO" >> "$O/Y2_o.out"; echo "|" >> "$O/Y2_o.out"; done
if cmp -s "$O/Y2_n.out" "$O/Y2_o.out" && has "cp|/Volumes/DevMASTER/TUESDAY/b" "$O/Y2_n.out"; then ok "Y2 WEDNESDAY pathguard verdicts on the existing probe set identical to the pre-friday file"
else bad "Y2 differs :: $(diff "$O/Y2_n.out" "$O/Y2_o.out")"; fi

# ═════ Z. tap_friday.sh — resolves the pane, delegates to cockpit.sh say (PRIVATE tmux server) ═
TB="$BASE/tbin"; mkdir -p "$TB"; REAL_TMUX="$(command -v tmux || echo /opt/homebrew/bin/tmux)"; SOCK="friday_tools_arms_$$"
printf '#!/bin/bash\nexec %s -L %s "$@"\n' "$REAL_TMUX" "$SOCK" > "$TB/tmux"; chmod +x "$TB/tmux"
PATH="$TB:$PATH" tmux new-session -d -s fleet -n main "env PS1='❯ ' bash --norc --noprofile -i"
ZP="$(PATH="$TB:$PATH" tmux list-panes -t fleet:0 -F '#{pane_id}' | head -1)"; PATH="$TB:$PATH" tmux set -p -t "$ZP" @cockpit_name friday
sleep 1
PATH="$TB:$PATH" bash "$FR/2_Project_Files/tools/tap_friday.sh" "friday-arms-Z1" > "$O/Z1.out" 2>&1; rc=$?
sleep 1; PATH="$TB:$PATH" tmux capture-pane -p -t "$ZP" > "$O/Z1.cap" 2>&1
PATH="$TB:$PATH" tmux set -p -t "$ZP" @cockpit_name wednesday
PATH="$TB:$PATH" bash "$FR/2_Project_Files/tools/tap_friday.sh" "friday-arms-Z2" > "$O/Z2.out" 2>&1; rc2=$?
sleep 1; PATH="$TB:$PATH" tmux capture-pane -p -t "$ZP" > "$O/Z2.cap" 2>&1
PATH="$TB:$PATH" bash "$WN/2_Project_Files/tools/tap_friday.sh" "friday-arms-Z3" > "$O/Z3.out" 2>&1; rc3=$?
PATH="$TB:$PATH" tmux kill-server > "$O/Z.kill" 2>&1
if [ "$rc" = 0 ] && has "friday-arms-Z1" "$O/Z1.cap" && [ "$rc2" = 0 ] && has "friday-arms-Z2" "$O/Z2.cap" && [ "$rc3" = 2 ] && has "not a FRIDAY tree" "$O/Z3.out"; then
  ok "Z1 tap_friday: delivers to the pane named 'friday', and to the legacy 'wednesday' pane on a FRIDAY tree (private tmux server); refuses on a WEDNESDAY tree"
else bad "Z1 tap_friday :: rc=$rc/$rc2/$rc3 :: $(cat "$O/Z1.out" "$O/Z2.out" "$O/Z3.out") :: cap=$(tail -3 "$O/Z2.cap")"; fi

# ═════ X. doctor.sh — friday checks + skips; Wednesday unchanged ══════════════════
mkdir -p "$FR/2_Project_Files/scheduler" "$FR/4_Credentials/dashboard-cloud"; chmod 644 "$FR/4_Credentials/dashboard-cloud/friday-seat.pem"
env -u WED_AGENT -u CLAUDE_CONFIG_DIR bash "$FR/2_Project_Files/doctor.sh" > "$O/X1.out" 2>&1; rc=$?
if has "friday: AGENTMAIL_API_KEY in 4_Credentials/.env" "$O/X1.out" && has "friday: friday-seat.pem mode 644 (must be 0600)" "$O/X1.out" && has "friday: CLAUDE_CONFIG_DIR unset" "$O/X1.out" \
   && has "run Launch_Friday.command — it runs first-time setup" "$O/X1.out" && has "scheduler launchd jobs: friday seat" "$O/X1.out" && has "chat_sync: friday seat" "$O/X1.out" \
   && has "scheduler per-job sweep: friday seat" "$O/X1.out" && has "NAS staleness: friday seat" "$O/X1.out" && has "scheduled jobs: friday seat" "$O/X1.out" && has "ornith night job: not this seat" "$O/X1.out" \
   && ! has "com.friday." "$O/X1.out"; then
  ok "X1 doctor on a FRIDAY tree: key present, pem-mode FAIL at 0644, CLAUDE_CONFIG_DIR + first-run marker WARN; launchd/chatsync/job-sweep/NAS/jobs/Ornith all skipped by name"
else bad "X1 doctor friday :: $(/usr/bin/grep -i -E 'friday|com\.' "$O/X1.out")"; fi
chmod 600 "$FR/4_Credentials/dashboard-cloud/friday-seat.pem"; : > "$FR/4_Credentials/.friday_configured"
env -u WED_AGENT CLAUDE_CONFIG_DIR="$FR/4_Credentials/.claude" bash "$FR/2_Project_Files/doctor.sh" > "$O/X2.out" 2>&1
env -u WED_AGENT CLAUDE_CONFIG_DIR="/Users/elsewhere/.claude" bash "$FR/2_Project_Files/doctor.sh" > "$O/X3.out" 2>&1
if has "friday: live-board seat key friday-seat.pem present, mode 0600" "$O/X2.out" && has "friday: CLAUDE_CONFIG_DIR is under this tree" "$O/X2.out" && has "friday: first-run setup done" "$O/X2.out" \
   && has "friday: CLAUDE_CONFIG_DIR is OUTSIDE this tree" "$O/X3.out"; then
  ok "X2 doctor friday green path (0600, config dir under tree, marker) and an OUTSIDE config dir is a FAIL"
else bad "X2 doctor friday green :: $(/usr/bin/grep -i 'friday' "$O/X2.out" "$O/X3.out")"; fi
for v in n o_; do env -u CLAUDE_CONFIG_DIR WED_AGENT=wednesday bash "$BASE/$v/WEDNESDAY/2_Project_Files/doctor.sh" > "$O/X4_$v.raw" 2>&1; echo "rc=$?" >> "$O/X4_$v.raw"
  /usr/bin/grep -v -E 'preflight — |last exit|log [0-9]+s|s old|ago|probe|docker|tailscale|min\)|PREFLIGHT:' "$O/X4_$v.raw" > "$O/X4_$v.out"; done
if same "$O/X4_n.out" "$O/X4_o_.out" && ! /usr/bin/grep -qE '(✓|⚠|✗) +(friday|.*friday seat)' "$O/X4_n.raw"; then ok "X4 WEDNESDAY doctor (scratch tree) identical to the pre-friday doctor (volatile lines excluded); no friday line"
else bad "X4 doctor differs :: $(diff "$O/X4_n.out.n" "$O/X4_o_.out.n" | head -8)"; fi

# ═════ W. close_wednesday.sh — friday's inbox, through a black-hole proxy (~3 min of the tool's own backoff) ═
if [ "${ARMS_SKIP_SLOW:-0}" = 1 ]; then echo "SKIP W1 close_wednesday inbox (ARMS_SKIP_SLOW=1)"; else
  mkdir -p "$FR/0_Brain/daily_friday"; sed "s/{{date}}/$TODAY/" "$FR/0_Brain/daily/_template.md" > "$FR/0_Brain/daily_friday/$TODAY.md"
  https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 WEDNESDAY_TEST_HOUR=23 WEDNESDAY_DRYRUN=1 bash "$FR/2_Project_Files/scheduler/close_wednesday.sh" > "$O/W1.out" 2>&1
  CL="$FR/2_Project_Files/scheduler/logs/close_$TODAY.log"
  if has "inbox check friday-laptop-agent@agentmail.to attempt 1/4" "$CL" && ! has "friday-agent@agentmail.to attempt" "$CL" && ! has "wednesday-agent@" "$CL"; then
    ok "W1 close bell on a FRIDAY tree reads friday-laptop-agent@ (+ the bus) — never a composed friday-agent@ or wednesday-agent@ (GETs black-holed at 127.0.0.1:9)"
  else bad "W1 close inbox :: $(/usr/bin/grep -i 'inbox' "$CL" | head -4) :: $(cat "$O/W1.out")"; fi
fi

echo "RESULT: $PASS passed, $FAIL failed (work dir $BASE)"
[ "$FAIL" = 0 ]
