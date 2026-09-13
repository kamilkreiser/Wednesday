#!/bin/bash
# resume_qa_hpsm_composer_09c1591_combined.sh — RESUME one of the three combined tier-1 gates on HPSM
# Policy Composer 09c1591 in its OWN tmux pane, keeping the gate's context instead of re-deriving it.
#
# WHY (measured by Tuesday s12, 2026-09-13 16:5x AEST): at 16:48:28 the cockpit's `fleet` tmux session was
# recreated through Launch_Cockpit.command's Fresh branch (`kill-session -t fleet`). All three gate panes
# died with it, mid-run: no claude process remains; transcripts end 06:47–06:48Z. Gate A had written its
# report except the @@VERDICT@@ / @@MUTANT_HEADLINE@@ placeholders; gates B and C had no report dir yet;
# B's and C's compose stacks were still up. The original launcher cannot be re-used (gate A's report dir
# exists, guard 17), and a fresh launch would throw away ~1h of each gate's work.
#
# LAUNCH EACH IN ITS OWN TMUX PANE: cockpit.sh add 'QA/HPSM-C-A' "bash '<this file>' A" — NEVER nohup.
# Identity: HPSM's own az/gh dirs (as the original launcher). Config dir: Tuesday's project-local .claude,
# where the three sessions live.
# Usage: resume_qa_hpsm_composer_09c1591_combined.sh <A|B|C> [--check]
set -u

GATE="${1:-}"
case "$GATE" in
  A) SESSION='12eb20ba-8be5-49e0-83f6-c134004317e9'; SLUG='a-engine-content'; PROJ='policy-composer-qa-c-a'; PORTS='21080 / CI 21095'
     STATE='Your report.md is written through its evidence index; @@VERDICT@@ and @@MUTANT_HEADLINE@@ are still placeholders. Re-check anything you had not finished (e.g. the mutant run behind the headline) rather than assuming it completed.' ;;
  B) SESSION='258bef81-24c1-4e91-ab8d-fe9cfd527489'; SLUG='b-api-db'; PROJ='policy-composer-qa-c-b'; PORTS='21180 / CI 21195'
     STATE='Your last action (06:43Z) moved a 600 s command to the background (task b2a3ztpbc); it died with the pane, so re-run it IN THE FOREGROUND with a long timeout. Your report directory does not exist yet. Containers still up include your stack policy-composer-qa-c-b-* and `qa-gateb-m7-clone-fence-removed-89690-db` (started ~16:43, looks like your M7 mutant run). An unnamed container `musing_yonath` started ~16:48: inspect it before assuming it is yours; if it is not yours, leave it.' ;;
  C) SESSION='8aef64cf-68c0-4b92-8a4b-f7e24b657b19'; SLUG='c-web-renderers'; PROJ='policy-composer-qa-c-c'; PORTS='21280 / CI 21295'
     STATE='Your report directory does not exist yet. Your stack policy-composer-qa-c-c-* (including the Playwright container policy-composer-qa-c-c-pw) is still up.' ;;
  *) echo "usage: $0 <A|B|C> [--check]" >&2; exit 2 ;;
esac

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-combined-tier1.md"
REPORT_DIR="$QA_DIR/projects/hpsm/reports/2026-09-13-composer-09c1591-combined-$SLUG-tier1"
ID_ROOT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials'
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
TRANSCRIPT="$CLAUDE_CONFIG_DIR/projects/-Volumes-KK-T9-External-HDD--CODING-Testing-Agent-MAIN/$SESSION.jsonl"

[ -s "$TRANSCRIPT" ] || { echo "REFUSING: session transcript missing: $TRANSCRIPT" >&2; exit 3; }
grep -q "combined-$SLUG-tier1" "$TRANSCRIPT" || { echo "REFUSING: transcript does not belong to gate $GATE" >&2; exit 4; }
[ -s "$BRIEF" ] || { echo "REFUSING: brief missing: $BRIEF" >&2; exit 5; }
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || { echo "REFUSING: HPSM identity dirs missing under $ID_ROOT" >&2; exit 6; }
# A session that is still running must never be resumed a second time.
if ps -axo command | grep -F -- "--resume $SESSION" | grep -vq grep; then
  echo "REFUSING: gate $GATE session $SESSION is already running" >&2; exit 7
fi
docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding" >&2; exit 8; }

PROMPT="ultrathink. Tuesday here (coordinator), 2026-09-13. You are GATE $GATE of the combined tier-1 gate on HPSM Policy Composer @ 09c15918fadfee8a9bd590a1282113637f44515d.

WHAT HAPPENED: your tmux pane was KILLED at 16:48 AEST when the cockpit's fleet tmux session was restarted. It was not your fault and it says nothing about your work. Nothing of yours is running any more: no claude process, and every background command or task id you started before 16:48 is gone. What survived: your clone(s) under /tmp, your evidence on disk, and any containers named in the next paragraph. You are now resumed, same session, in a new tmux pane.

YOUR STATE AS TUESDAY MEASURED IT: $STATE

HOW TO FINISH:
1. Re-derive state from disk before acting: \`docker ps -a --filter name=$PROJ\`, your clone(s), your evidence folder, and $REPORT_DIR if it exists. Do NOT redo finished work.
2. Run long commands IN THE FOREGROUND with a long timeout. Never end a turn waiting on a background notice — a turn that ends to wait is how a gate dies.
3. Unchanged: your brief ($BRIEF), your head, your gate's scope, your compose project ($PROJ) and ports ($PORTS). Never touch the other two gates' compose projects or ports, pc-lane-a (18580), or the Azure demo.
4. HPSM's merge seat (session 42) died in the same restart. A successor, session 43, is being launched; it will not touch your projects or ports. Its local main may move, which does not affect you: you test 09c1591 in your own clone.
5. Fill every @@...@@ placeholder in your report, record this interruption in your report's frame section (one line: pane killed 16:48, resumed by Tuesday), clean up ONLY what you created, and MAIL YOUR VERDICT to tuesday-agent@agentmail.to exactly as your brief specifies."

if [ "${2:-}" = "--check" ]; then
  echo "guards passed for gate $GATE (session $SESSION); not launching (--check)"; exit 0
fi
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 9; }
exec claude --resume "$SESSION" --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
