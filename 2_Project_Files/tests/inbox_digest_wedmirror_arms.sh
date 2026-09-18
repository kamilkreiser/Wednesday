#!/bin/bash
# Arms for the Wednesday-seat mirror in fleet/inbox_digest.sh (2026-09-18): Datasec BODY PREVIEWS on coagent@
# are withheld from the Wednesday seat (subject kept); Tuesday's output is byte-identical. curl is a PATH stub,
# and each run gets a DISTINCT seen-file (a shared one makes the second run show 0 new, which is a vacuous pass;
# $RANDOM in sibling $(...) subshells repeats). The STRONG controls assert "3 new", not just the section header.
set -u
S=$(mktemp -d /private/tmp/claude-501/digest_arms.XXXX); mkdir -p "$S/bin"
cat > "$S/bin/curl" <<'C'
#!/bin/bash
case "$*" in
  *coagent*) printf '%s' '{"messages":[{"subject":"[Datasec/NexusAI -> Tuesday] STATUS: fixture","preview":"DATASEC-PREVIEW-TOKEN body","timestamp":"2026-09-18T02:50:00Z","message_id":"<d1@x>","from":"a@x","labels":[]},{"subject":"[Secuura/Blockchain -> Wednesday] STATUS: fixture","preview":"SECUURA-PREVIEW-TOKEN body","timestamp":"2026-09-18T02:50:01Z","message_id":"<s1@x>","from":"b@x","labels":[]},{"subject":"General note","preview":"GENERAL-PREVIEW-TOKEN body","timestamp":"2026-09-18T02:50:02Z","message_id":"<g1@x>","from":"c@x","labels":[]}]}' ;;
  *) echo '{"messages":[]}' ;;
esac
C
chmod +x "$S/bin/curl"
D=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet
run(){ PATH="$S/bin:$PATH" AGENTMAIL_API_KEY=dummy WED_AGENT=$2 INBOX_DIGEST_SEEN_FILE="$S/seen_$3.txt" bash "$1" 2>&1; }
W_NEW="$(run $D/inbox_digest.sh wednesday a)"; W_OLD="$(run $D/inbox_digest.sh.pre-0918-wedmirror wednesday b)"
T_NEW="$(run $D/inbox_digest.sh tuesday c)";   T_OLD="$(run $D/inbox_digest.sh.pre-0918-wedmirror tuesday d)"
c(){ printf '%s' "$1" | /usr/bin/grep -ci "$2"; }
F=0; chk(){ if [ "$2" = "$3" ]; then echo "PASS  $1"; else echo "FAIL  $1 (got $2, want $3)"; F=1; fi; }
chk "M0  strong control NEW 3 new"   "$(c "$W_NEW" 'coagent@agentmail.to — 3 new')" 1
chk "M0b strong control OLD 3 new"   "$(c "$W_OLD" 'coagent@agentmail.to — 3 new')" 1
chk "M1  RED-PROOF old leaks Datasec preview" "$(c "$W_OLD" DATASEC-PREVIEW-TOKEN)" 1
chk "M2  new withholds Datasec preview"  "$(c "$W_NEW" DATASEC-PREVIEW-TOKEN)" 0
chk "M3  new keeps Datasec subject"      "$(c "$W_NEW" 'Datasec/NexusAI')" 1
chk "M4  Secuura preview unchanged"      "$(c "$W_NEW" SECUURA-PREVIEW-TOKEN)" 1
chk "M5  general preview unchanged"      "$(c "$W_NEW" GENERAL-PREVIEW-TOKEN)" 1
chk "M7  Tuesday byte-identical"  "$([ "$T_NEW" = "$T_OLD" ] && echo same || echo differs)" same
chk "M8  Tuesday never sees Secuura preview" "$(c "$T_NEW" SECUURA-PREVIEW-TOKEN)" 0
exit $F
