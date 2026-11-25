//! QA-POLICY-NOTES D-B adapter, HEAD (`b6af26c`, also `535b017`): the facts read from the SAME hook input the action
//! was classified from, by the crate's own `owner_input_facts` (the call the daemon lane is meant to make).
use coagent_policy::*;
pub fn owner(a: &Action, hook: &HookInput, st: &State, m: Option<&OwnerAllow>, s: Surface, now: Timestamp) -> Decision {
    decide_with_owner_allow(a, st, m, &owner_input_facts(hook), s, now)
}
