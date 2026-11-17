#!/usr/bin/env python3
"""QA gate M3-ROSTER round 3 mutation driver (head 44662d5). Adapted from mutate_r2.py: the gate's
round-2 mutants re-anchored on the same checks, plus new X-mutants on the delta d88d5d7..44662d5.
One textual mutation at a time in a scratch copy; restores the file after each (checked by compare).
Modes:
  normal  : the BRANCH's whole coagent-roster suite (every test target on the branch, the gate files
            qa_gate.rs and qa_r2.rs included; NOT qa_r3.rs); if it survives, qa_r3.rs alone (info).
  ridoff  : COAGENT_RED_ROSTER=intake_roster_id_unchecked, targets gate_return_a5 + gate_return_a3
            (+ qa_r3 reported separately); the unmutated baseline's failing tests are discounted.
  OWN=1   : (second pass) qa_r3.rs alone, every listed mutant.
Usage: [OWN=1] mutate_r3.py <copy> <target_dir> <out.tsv> [ids...]"""
import os, subprocess, sys

WT, TARGET, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = set(sys.argv[4:])
I = "crates/coagent-roster/src/intake.rs"

M = [
 # the gate's round-2 mutants (same check; strings re-anchored where the head moved the code: *)
 ("N01", I, "        if !cfg!(coagent_red_roster = \"approve_no_validate\")\n            && !cfg!(coagent_red_roster = \"intake_keep_stale\")", "        if false", "approve: validator run removed", True),
 ("N02", I, "                .and_then(|_| crate::check_transition(roster, &next).map(|_| ()));", "                .map(|_| ());", "approve: transition rules not run", True),
 ("N03", I, "            let verdict = crate::validate_body(&next)\n", "            let verdict = Ok::<(), RosterError>(())\n", "approve: validate_body not run", True),
 ("N04", I, "                    r.outcome = Outcome::RefusedInvalid;\n                    r.proposal = None;", "                    let _ = r;", "refused approval leaves the proposal pending", True),
 ("N05", I, "                return Err(IntakeError::InvalidApproval(reason));", "                for r in self.records.values_mut() { if r.outcome == Outcome::Pending { r.outcome = Outcome::Stale; r.proposal = None; } }\n                return Err(IntakeError::InvalidApproval(reason));", "refused approval stales every other pending proposal", True),
 ("N06", I, "                return Err(IntakeError::InvalidApproval(reason));", "                for u in self.used.values_mut() { *u = u.saturating_add(1); }\n                return Err(IntakeError::InvalidApproval(reason));", "refused approval charges every proposer", True),
 ("N33", I, "                    r.outcome = Outcome::RefusedInvalid;", "                    r.outcome = Outcome::Declined;", "refused approval recorded as Declined", True),
 ("N17", I, ".retain(|k, _| roster.role_of(k) == Some(Role::Guest) && !roster.is_convener(k));", ".retain(|k, _| roster.role_of(k).is_some() && !roster.is_convener(k));", "crowded counters kept for observers", False),
 ("N18", I, "            return Err(IntakeError::ProposerHasPending);", "            *self.crowded.entry(s).or_insert(0) += 1;\n            return Err(IntakeError::ProposerHasPending);", "crowded counted on ProposerHasPending", False),
 ("N20", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "        if false && wire.len() > 2 * MAX_PROPOSAL_BYTES {", "receive_wire: string bound removed", False),
 ("N21", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "        if wire.len() >= 2 * MAX_PROPOSAL_BYTES {", "receive_wire: > -> >=", False),
 ("N22", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "        if wire.len() > 4 * MAX_PROPOSAL_BYTES {", "receive_wire: bound doubled", False),
 ("N25", I, "            if !cfg!(coagent_red_roster = \"wire_no_tick_too_large\") {\n                self.advance(roster, now, true);\n            }\n", "", "*receive_wire: no expiry pass on TooLarge", False),
 ("N38", I, "            if !cfg!(coagent_red_roster = \"wire_no_tick_malformed\") {\n                self.advance(roster, now, true);\n            }\n", "", "*receive_wire: no expiry pass on Malformed", False),
 ("N39", I, "        if !cfg!(coagent_red_roster = \"wire_no_roster_check\") {\n            self.check_roster(roster)?;\n        }\n", "", "*receive_wire: roster check removed", False),
 # new mutants on the delta
 ("X01", I, "let countable = (used < QUOTA_PER_PROPOSER && !self.muted.contains(&s))", "let countable = (used < QUOTA_PER_PROPOSER)", "counter: mute condition dropped (quota kept)", False),
 ("X02", I, "let countable = (used < QUOTA_PER_PROPOSER && !self.muted.contains(&s))", "let countable = (!self.muted.contains(&s))", "counter: quota condition dropped (mute kept)", False),
 ("X03", I, ".any(|m| m.proposal.as_ref().is_some_and(|p| p.proposal_id == id))", ".any(|m| m.proposal.as_ref().is_some_and(|p| p.proposal_id == id && p.proposer == s))", "roster id check only for the same proposer", False),
 ("X04", I, "            return Err(IntakeError::IdCarriedByRoster);", "            return Err(IntakeError::DuplicateId);", "roster id refused under the wrong (unnamed) error", False),
 ("X05", I, "            if !r.reported {\n                ended.push", "            if !r.reported && r.outcome == Outcome::Expired {\n                ended.push", "tick reports only expiries (staleness ends kept)", False),
 ("X06", I, "                    r.outcome = Outcome::Stale;\n", "                    r.outcome = Outcome::Stale;\n                    r.reported = false;\n", "approval's made_stale also reported again by tick", False),
 ("X07", I, "ended_unreported: self.records.values().filter(|r| !r.reported).count(),", "ended_unreported: 0,", "accounting: ended_unreported always 0", False),
 ("X08", I, "crowded_refusals: self.crowded.values().map(|c| u64::from(*c)).sum(),", "crowded_refusals: 0,", "accounting: crowded_refusals always 0", False),
 ("X09", I, "crowded_guests: self.crowded.len(),", "crowded_guests: 0,", "accounting: crowded_guests always 0", False),
 ("X10", I, "        self.check_roster(roster)?;\n        self.advance(roster, now, true);\n        // 1.", "        self.check_roster(roster)?;\n        // 1.", "receive: no expiry pass before checks", False),
 ("X11", I, "                reported: true,\n            },\n        );\n        Ok(id)", "                reported: false,\n            },\n        );\n        Ok(id)", "a new pending proposal is reported by the next tick", False),
]

BRANCH = ["admit_propose", "api_stability", "gate_return", "gate_return_a3", "gate_return_a5", "gate_roster",
          "intake", "lifetime", "limit", "mesh", "pinned_encoding", "proposal", "qa_gate", "qa_r2", "roles", "roster"]

def run(tests, red=None, lib=True):
    env = dict(os.environ, CARGO_TARGET_DIR=TARGET)
    env.pop("COAGENT_RED_ROSTER", None)
    if red:
        env["COAGENT_RED_ROSTER"] = red
    cmd = ["cargo", "test", "--locked", "--manifest-path", os.path.join(WT, "Cargo.toml"), "-p", "coagent-roster"] \
        + (["--lib"] if lib else []) + sum([["--test", t] for t in tests], []) + ["--no-fail-fast"]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    log = r.stdout + r.stderr
    if "error[E" in log or "could not compile" in log:
        return "COMPILE-ERROR", set()
    if not os.path.isdir("/Volumes/Laptop-DEV/FRIDAY"):
        return "ENV-ERROR", set()
    failed = {l.split()[1] for l in log.splitlines() if l.startswith("test ") and l.endswith("FAILED")}
    if r.returncode != 0 and not failed:
        return "ERROR(rc=%d)" % r.returncode, set()
    return ("KILLED" if failed else "SURVIVED"), failed

def fmt(res, failed):
    if res != "KILLED":
        return res
    f = sorted(failed)
    return "KILLED(" + ",".join(f[:4]) + ("" if len(f) <= 4 else f",+{len(f)-4}") + ")"

RID = "intake_roster_id_unchecked"
base_rid = None
out = open(OUT, "a")
for mid, f, old, new, what, rid in M:
    if ONLY and mid not in ONLY:
        continue
    path = os.path.join(WT, f)
    src = open(path).read()
    n = src.count(old)
    if n != 1:
        out.write(f"{mid}\tNOT-APPLIED(count={n})\t\t\t{what}\n"); out.flush(); continue
    open(path, "w").write(src.replace(old, new))
    try:
        if os.environ.get("OWN"):  # second pass: the gate's own round-3 tests only (qa_r3.rs)
            res, failed = run(["qa_r3"], lib=False)
            out.write(f"{mid}\tqa_r3-only\t{fmt(res, failed)}\t\t{what}\n"); out.flush()
            continue
        res, failed = run(BRANCH)
        main = fmt(res, failed)
        extra = fmt(*run(["qa_r3"], lib=False)) if res == "SURVIVED" else ""
        ridres = ""
        if rid:
            if base_rid is None:
                open(path, "w").write(src)
                base_rid = run(["gate_return_a5", "gate_return_a3", "qa_r3"], red=RID, lib=False)[1]
                out.write(f"BASE-ridoff\tfailing={sorted(base_rid)}\t\t\t(unmutated, receive id check off)\n"); out.flush()
                open(path, "w").write(src.replace(old, new))
            r2, fl = run(["gate_return_a5", "gate_return_a3", "qa_r3"], red=RID, lib=False)
            extra_f = fl - base_rid
            ridres = fmt("KILLED" if extra_f else r2 if r2 not in ("KILLED",) else "SURVIVED", extra_f)
    finally:
        open(path, "w").write(src)
        assert open(path).read() == src, "restore failed"
    out.write(f"{mid}\t{main}\t{extra}\t{ridres}\t{what}\n"); out.flush()
out.close()
