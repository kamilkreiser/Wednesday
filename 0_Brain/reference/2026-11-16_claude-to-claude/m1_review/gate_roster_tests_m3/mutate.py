#!/usr/bin/env python3
"""QA gate M3-ROSTER mutation driver. Applies one textual mutation at a time to the head source in a
scratch worktree, runs the BUILDER's coagent-roster test suite (not the QA tests), records killed or
survived, and restores the file. Usage: mutate.py <worktree> <target_dir> <out.tsv> [ids...]"""
import os, subprocess, sys

WT, TARGET, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = set(sys.argv[4:])
L = "crates/coagent-roster/src/lib.rs"
I = "crates/coagent-roster/src/intake.rs"
P = "crates/coagent-roster/src/proposal.rs"

M = [
 ("M01", L, "if b.cap > CAP {", "if b.cap > CAP + 1 {", "cap above max -> CapExceeded"),
 ("M02", L, "if b.cap != CAP_DEFAULT && b.cap != CAP && !cfg", "if b.cap != CAP_DEFAULT && b.cap != CAP && b.cap != 2 && !cfg", "cap 2 accepted"),
 ("M03", L, "if b.members.len() > count_limit(b) {", "if b.members.len() >= count_limit(b) + 1 + 0 && false {", "count rule removed"),
 ("M04", L, "        usize::from(b.cap)\n    }", "        usize::from(b.cap) + 1\n    }", "count limit off by one"),
 ("M05", L, "if m.slot >= slot_limit(b) &&", "if m.slot > slot_limit(b) &&", "slot >= -> >"),
 ("M06", L, "if b.version > MAX_VERSIONS &&", "if b.version > MAX_VERSIONS + 1 &&", "version bound off by one"),
 ("M07", L, "if b.members.len() + b.removed.len() > MAX_ENTRIES_EVER\n", "if b.members.len() + b.removed.len() > MAX_ENTRIES_EVER + 1\n", "entries bound off by one up"),
 ("M08", L, "if b.members.len() + b.removed.len() > MAX_ENTRIES_EVER\n", "if b.members.len() + b.removed.len() >= MAX_ENTRIES_EVER\n", "entries bound off by one down"),
 ("M09", L, "if p.proposer == m.key_id && !cfg", "if false && p.proposer == m.key_id && !cfg", "proposer==candidate removed"),
 ("M10", L, "if p.proposer == b.convener && !cfg", "if false && p.proposer == b.convener && !cfg", "proposer==starter removed"),
 ("M11", L, "if (p.at_version == 0 || p.at_version.checked_add(1)", "if (p.at_version.checked_add(1)", "at_version 0 allowed (version-1 proposals)"),
 ("M12", L, "if (p.at_version == 0 || p.at_version.checked_add(1) != Some(m.added_in))", "if (p.at_version == 0)", "shape at_version+1==added_in removed"),
 ("M13", L, "if m.role == Role::Guest\n        && p.role == Role::Observer", "if false && m.role == Role::Guest\n        && p.role == Role::Observer", "role upgrade allowed"),
 ("M14", L, ".any(|r| r.key_id == m.key_id && r.at_version <= p.at_version)", ".any(|r| r.key_id == m.key_id && r.at_version < p.at_version)", "I-6 <= -> <"),
 ("M15", L, "if !seen_ids.insert(p.proposal_id) && !cfg", "if false && !seen_ids.insert(p.proposal_id) && !cfg", "dup id removed"),
 ("M16", L, "            None => {\n                unchecked.insert(m.key_id);\n            }", "            None => {}", "unchecked not reported"),
 ("M17", L, "                .map_err(|_| RosterError::BadProposalSignature(m.key_id))?,", "                .map_err(|_| RosterError::BadProposalSignature(m.key_id)).unwrap_or(()),", "first-roster sig error ignored"),
 ("M18", L, ".filter(|k| valid.by_key.contains_key(k))", ".filter(|k| valid.by_key.contains_key(k) && false)", "unchecked report dropped on next version"),
 ("M19", L, "let cap_change = (before != after &&", "let cap_change = (before != after && false &&", "cap change never reported"),
 ("M20", L, "                from: before,\n                to: after,", "                from: after,\n                to: before,", "cap change from/to swapped"),
 ("M21", L, "if held.role_of(&p.proposer) != Some(Role::Guest)\n", "if held.role_of(&p.proposer) == None\n", "observer proposer allowed (transition)"),
 ("M22", L, "if (p.at_version != held.version() || p.at_hash.as_bytes() != &held.hash())", "if (p.at_version != held.version())", "transition at_hash not checked"),
 ("M23", L, "if (p.at_version != held.version() || p.at_hash.as_bytes() != &held.hash())", "if (p.at_hash.as_bytes() != &held.hash())", "transition at_version not checked"),
 ("M24", L, "    &body.convener == key\n}", "    let _ = (body, key); true\n}", "is_roster_signer always true"),
 ("M25", L, "fn next_with_cap(current: &ValidRoster, cap: u8) -> Result<RosterBody, RosterError> {\n    if cap == current.cap() {", "fn next_with_cap(current: &ValidRoster, cap: u8) -> Result<RosterBody, RosterError> {\n    if false && cap == current.cap() {", "helper CapUnchanged removed"),
 ("M26", L, "    validate_body(&next)?;\n    check_transition(current, &next)?;\n    Ok(next)", "    check_transition(current, &next)?;\n    Ok(next)", "helper does not validate the body"),
 ("M27", L, "        \"member.propose\" => !cfg!(coagent_red_roster = \"admit_observer_propose\"),", "        \"member.propose\" => false,", "admit: observer may propose"),
 ("M28", L, "        && !intake::may_approve(roster, &from)\n", "        && false && !intake::may_approve(roster, &from)\n", "admit: anyone sends result"),
 ("M29", L, "            None if removed_now.contains(&m.key_id) => {}", "            None => {}", "silent drop allowed (existing rule, control)"),
 ("M30", L, "            if let Some(sp) = n.rebuilt_proposal(&next.session_id) {\n                check_added_proposal(held, n, &sp)?;", "            if let Some(sp) = n.rebuilt_proposal(&next.session_id) {\n                let _ = check_added_proposal(held, n, &sp);", "transition proposal rules skipped"),
 ("M31", I, "if body.members.len() >= usize::from(seats) {", "if body.members.len() > usize::from(seats) {", "free seat >= -> >"),
 ("M32", I, "if body.members.len() + body.removed.len() + 1 > MAX_ENTRIES_EVER {\n            return Err(IntakeError::LifetimeFull);\n        }\n        // 9.", "if body.members.len() + body.removed.len() > MAX_ENTRIES_EVER {\n            return Err(IntakeError::LifetimeFull);\n        }\n        // 9.", "intake lifetime off by one"),
 ("M33", I, "if pending_of(&s) >= PENDING_PER_PROPOSER", "if pending_of(&s) > PENDING_PER_PROPOSER", "per-proposer pending off by one"),
 ("M34", I, "if pending_all >= PENDING_PER_SESSION", "if pending_all > PENDING_PER_SESSION", "session pending off by one"),
 ("M35", I, "if used >= QUOTA_PER_PROPOSER &&", "if used > QUOTA_PER_PROPOSER &&", "quota off by one"),
 ("M36", I, "let expired = now.saturating_duration_since(r.received) >= PROPOSAL_TTL", "let expired = now.saturating_duration_since(r.received) > PROPOSAL_TTL", "expiry >= -> >"),
 ("M37", I, "let stale = (p.body.at_version != roster.version()\n                || p.body.at_hash.as_bytes() != &roster.hash())", "let stale = (p.body.at_version != roster.version())", "stale ignores hash"),
 ("M38", I, "        if role == Role::Guest && sp.body.role == Role::Observer {\n            return Err(IntakeError::RoleRaised);", "        if false {\n            return Err(IntakeError::RoleRaised);", "approve: role raise allowed"),
 ("M39", I, "                r.outcome = if k == id {\n                    Outcome::Approved\n                } else {\n                    Outcome::Stale\n                };\n                r.proposal = None;", "                if k == id {\n                    r.outcome = Outcome::Approved;\n                    r.proposal = None;\n                }", "approve: others stay pending"),
 ("M40", I, "        if b.session_id != self.session_id {\n            return Err(IntakeError::WrongSession);", "        if false {\n            return Err(IntakeError::WrongSession);", "intake: session check removed"),
 ("M41", I, "        if roster.is_convener(&s) {\n            return Err(IntakeError::SenderIsStarter);", "        if false {\n            return Err(IntakeError::SenderIsStarter);", "intake: starter may propose"),
 ("M42", I, "        if b.at_version != roster.version() || b.at_hash.as_bytes() != &roster.hash() {\n            return Err(IntakeError::Stale);", "        if b.at_version != roster.version() {\n            return Err(IntakeError::Stale);", "intake: stale ignores hash"),
 ("M43", I, "        if cand.key_id() != b.candidate.key_id {\n            return Err(IntakeError::BadCandidate);", "        if false {\n            return Err(IntakeError::BadCandidate);", "intake: candidate key id not checked"),
 ("M44", I, "        if roster.role_of(&cand.key_id()).is_some() {\n            return Err(IntakeError::CandidateIsMember);", "        if false {\n            return Err(IntakeError::CandidateIsMember);", "intake: member candidate allowed"),
 ("M45", I, "        if body.removed.iter().any(|r| r.key_id == cand.key_id()) {\n            return Err(IntakeError::CandidateRemoved);", "        if false {\n            return Err(IntakeError::CandidateRemoved);", "intake: removed candidate allowed"),
 ("M46", I, "        if self.records.len() >= MAX_REMEMBERED_IDS {\n            return Err(IntakeError::IdsFull);", "        if false {\n            return Err(IntakeError::IdsFull);", "intake: ids bound removed"),
 ("M47", I, "    roster.is_convener(key)\n}", "    let _ = (roster, key); true\n}", "may_approve always true"),
 ("M48", I, "        if added_at.len() > 64 {\n            return Err(IntakeError::FieldLimit);", "        if false {\n            return Err(IntakeError::FieldLimit);", "approve: added_at unchecked"),
 ("M49", I, "        if cur.members.len() + cur.removed.len() + 1 > MAX_ENTRIES_EVER {\n            return Err(IntakeError::LifetimeFull);\n        }\n        let slot", "        let slot", "approve: lifetime re-check removed"),
 ("M50", I, "            self.muted.insert(r.proposer);", "            let _ = r.proposer;", "mute not recorded"),
 ("M51", I, "        self.used.insert(s, used.saturating_add(1));", "        self.used.insert(s, used);", "quota not charged"),
 ("M52", I, "        self.check_roster(roster)?;\n        self.tick(roster, now);\n        // 1.", "        self.tick(roster, now);\n        // 1.", "receive: roster/session/approver not checked"),
 ("M53", P, "    m.extend_from_slice(PROPOSAL_LABEL);\n    m.push(0);", "    m.extend_from_slice(b\"coagent-roster-proposal-v2\");\n    m.push(0);", "label bytes changed (consistently)"),
 ("M54", P, "    m.extend_from_slice(PROPOSAL_LABEL);\n    m.push(0);", "    m.extend_from_slice(PROPOSAL_LABEL);", "label separator dropped"),
 ("M55", P, "    m.extend_from_slice(PROPOSAL_LABEL);\n    m.push(0);", "", "label dropped entirely"),
 ("M56", P, "        if bytes.len() > MAX_PROPOSAL_BYTES {\n            return Err(ProposalError::TooLarge);\n        }\n        Ok(canonical::decode(bytes)?)", "        Ok(canonical::decode(bytes)?)", "SignedProposal::decode size check removed"),
 ("M57", P, "        Some(Role::Observer) => return Err(ProposalError::Observer),", "        Some(Role::Observer) => {}", "propose(): observer allowed"),
 ("M58", P, "        return Err(ProposalError::CandidateRemoved);", "        let _ = 0;", "propose(): removed candidate allowed"),
 ("M59", P, "        if self.body.proposer != proposer.key_id() {\n            return Err(ProposalError::WrongProposer);", "        if false {\n            return Err(ProposalError::WrongProposer);", "verify(): WrongProposer removed"),
 ("M60", P, "    if roster.is_convener(&me) {\n        return Err(ProposalError::IsStarter);", "    if false {\n        return Err(ProposalError::IsStarter);", "propose(): starter allowed"),
 ("M61", L, "                role: p.body.role,\n                sig: p.sig,", "                role,\n                sig: p.sig,", "Member::proposed records the entry role"),
]

TESTS = ["admit_propose", "api_stability", "gate_return", "gate_roster", "intake", "lifetime",
         "limit", "mesh", "pinned_encoding", "proposal", "roles", "roster"]

env = dict(os.environ, CARGO_TARGET_DIR=TARGET)
out = open(OUT, "a")
for mid, f, old, new, what in M:
    if ONLY and mid not in ONLY:
        continue
    path = os.path.join(WT, f)
    src = open(path).read()
    n = src.count(old)
    if n != 1:
        out.write(f"{mid}\tNOT-APPLIED(count={n})\t{what}\n"); out.flush(); continue
    open(path, "w").write(src.replace(old, new))
    try:
        cmd = ["cargo", "test", "--locked", "--manifest-path", os.path.join(WT, "Cargo.toml"),
               "-p", "coagent-roster", "--lib"] + sum([["--test", t] for t in TESTS], []) + ["--no-fail-fast"]
        r = subprocess.run(cmd, env=env, capture_output=True, text=True)
        log = r.stdout + r.stderr
        if "error[E" in log or "could not compile" in log:
            res = "COMPILE-ERROR"
        elif r.returncode != 0:
            failed = [l.split()[1] for l in log.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
            res = "KILLED(" + ",".join(failed[:4]) + ")"
        else:
            res = "SURVIVED"
    finally:
        open(path, "w").write(src)
    out.write(f"{mid}\t{res}\t{what}\n"); out.flush()
out.close()
