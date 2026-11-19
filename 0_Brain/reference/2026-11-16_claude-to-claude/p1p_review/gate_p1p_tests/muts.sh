W=/private/tmp/claude-501/qp1; S=$W/m/crates
m() { # m <label> <file> <from> <to> <tests...>
  local label=$1 f=$2 from=$3 to=$4; shift 4
  python3 -I - "$f" "$from" "$to" <<'PY' || { echo "[$label] MUTATION NOT APPLIED"; return; }
import sys
p,a,b=sys.argv[1:4]; s=open(p).read()
if s.count(a)!=1: sys.exit("anchor count %d" % s.count(a))
open(p,'w').write(s.replace(a,b))
PY
  bash $W/p/mut.sh "$label" "$@"
  git -C $W/m checkout -- "$f"
}
m M1_ttl_removed $S/coagent-daemon/src/gate.rs '.map(|w| now.saturating_duration_since(w.at) <= ttl)' '.map(|_w| true)' p1p_liveness
m M2_witness_on_deny $S/coagent-daemon/src/gate.rs 'if v.decision == "allow" || v.decision == "ask" {' 'if true {' p1p_liveness p1p_taint_persists p1p_deny_blocks p1p_unknown_tool_strict p1p_configchange p1p_ask_in_workspace
m M3_offtoken_none $S/coagent-daemon/src/engine.rs 'match (gate::off_token(g), ticket)' 'match (gate::off_token(&None), ticket)' release_audit p1p_liveness
m M4_taint_failure_ignored $S/coagent-daemon/src/engine.rs 'if g.taint(&c).is_err() {' 'if g.taint(&c).is_err() && false {' p1p_liveness p1p_taint_persists
m M5_taint_wrong_session $S/coagent-daemon/src/gate.rs 'let id = cut(&c.cc_session).to_string();' 'let id = String::from("wrong-session");' p1p_taint_persists
m M13_hook_halt_dropped $S/coagent-hook/src/main.rs '            if halt {
                if let Some(m) = o.as_object_mut() {' '            if false {
                if let Some(m) = o.as_object_mut() {' p1p_hook_mapping
m M14_hook_cc_as_pretooluse $S/coagent-hook/src/main.rs '"block" => Outcome::Print(json!({"decision": "block", "reason": reason})),' '"block" => Outcome::Print(pre_tool_use("deny", reason)),' p1p_configchange
