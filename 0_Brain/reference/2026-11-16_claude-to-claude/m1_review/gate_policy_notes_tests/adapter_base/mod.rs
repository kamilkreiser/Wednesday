//! QA-POLICY-NOTES D-B adapter, BASE (`f193620`): the owner entry point as main has it (no facts argument).
use coagent_policy::*;
pub fn owner(a: &Action, _hook: &HookInput, st: &State, m: Option<&OwnerAllow>, s: Surface, now: Timestamp) -> Decision {
    decide_with_owner_allow(a, st, m, s, now)
}
