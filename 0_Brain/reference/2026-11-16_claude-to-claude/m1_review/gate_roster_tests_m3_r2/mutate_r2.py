#!/usr/bin/env python3
"""QA gate M3-ROSTER round 2 mutation driver. One textual mutation at a time in a scratch copy, runs
the BRANCH's coagent-roster test suite (every test target on the branch, the gate file qa_gate.rs
included; NOT the round-2 QA tests), records killed / survived, restores the file. A second pass
(EXTRA) re-runs survivors against the round-2 QA tests only, for information.
Usage: mutate_r2.py <copy> <target_dir> <out.tsv> [ids...]"""
import os, subprocess, sys

WT, TARGET, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = set(sys.argv[4:])
L = "crates/coagent-roster/src/lib.rs"
I = "crates/coagent-roster/src/intake.rs"
P = "crates/coagent-roster/src/proposal.rs"

R1 = [  # round-1 mutants, re-applied (strings adapted where the head moved the code; marked *)
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
 ("M11", L, "let zero = p.at_version == 0 && !cfg", "let zero = false && p.at_version == 0 && !cfg", "*at_version 0 allowed (version-1 proposals)"),
 ("M12", L, "if (zero || (p.at_version != 0 && p.at_version.checked_add(1) != Some(m.added_in)))", "if (zero)", "*shape at_version+1==added_in removed"),
 ("M13", L, "if m.role == Role::Guest\n        && p.role == Role::Observer", "if false && m.role == Role::Guest\n        && p.role == Role::Observer", "*role upgrade allowed (now in check_admission_role)"),
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
 ("M32", I, "if body.members.len() + body.removed.len() + 1 > MAX_ENTRIES_EVER {", "if body.members.len() + body.removed.len() > MAX_ENTRIES_EVER {", "*intake lifetime off by one"),
 ("M33", I, "if pending_of(&s) >= PENDING_PER_PROPOSER", "if pending_of(&s) > PENDING_PER_PROPOSER", "per-proposer pending off by one"),
 ("M34", I, "if pending_all >= PENDING_PER_SESSION", "if pending_all > PENDING_PER_SESSION", "session pending off by one"),
 ("M35", I, "if used >= QUOTA_PER_PROPOSER &&", "if used > QUOTA_PER_PROPOSER &&", "quota off by one"),
 ("M36", I, "let expired = now.saturating_duration_since(r.received) >= PROPOSAL_TTL", "let expired = now.saturating_duration_since(r.received) > PROPOSAL_TTL", "expiry >= -> >"),
 ("M37", I, "let stale = (p.body.at_version != roster.version()\n                || p.body.at_hash.as_bytes() != &roster.hash())", "let stale = (p.body.at_version != roster.version())", "stale ignores hash"),
 ("M38", I, "        if role == Role::Guest && sp.body.role == Role::Observer {\n            return Err(IntakeError::RoleRaised);", "        if false {\n            return Err(IntakeError::RoleRaised);", "approve: role raise allowed"),
 ("M39", I, "                    r.outcome = Outcome::Stale;", "                    continue;", "*approve: others stay pending"),
 ("M40", I, "        if b.session_id != self.session_id {\n            return Err(IntakeError::WrongSession);", "        if false {\n            return Err(IntakeError::WrongSession);", "intake: session check removed"),
 ("M41", I, "        if roster.is_convener(&s) {\n            return Err(IntakeError::SenderIsStarter);", "        if false {\n            return Err(IntakeError::SenderIsStarter);", "intake: starter may propose"),
 ("M42", I, "let hash_differs = b.at_hash.as_bytes() != &roster.hash()", "let hash_differs = false && b.at_hash.as_bytes() != &roster.hash()", "*intake: stale ignores hash"),
 ("M43", I, "        if cand.key_id() != b.candidate.key_id {\n            return Err(IntakeError::BadCandidate);", "        if false {\n            return Err(IntakeError::BadCandidate);", "intake: candidate key id not checked"),
 ("M44", I, "        if roster.role_of(&cand.key_id()).is_some() {\n            return Err(IntakeError::CandidateIsMember);", "        if false {\n            return Err(IntakeError::CandidateIsMember);", "intake: member candidate allowed"),
 ("M45", I, "        if body.removed.iter().any(|r| r.key_id == cand.key_id()) {\n            return Err(IntakeError::CandidateRemoved);", "        if false {\n            return Err(IntakeError::CandidateRemoved);", "intake: removed candidate allowed"),
 ("M46", I, "        if self.records.len() >= MAX_REMEMBERED_IDS {\n            return Err(IntakeError::IdsFull);", "        if false {\n            return Err(IntakeError::IdsFull);", "intake: ids bound removed"),
 ("M47", I, "    roster.is_convener(key)\n}", "    let _ = (roster, key); true\n}", "may_approve always true"),
 ("M48", I, "if added_at.len() > 64 && !cfg", "if false && added_at.len() > 64 && !cfg", "*approve: added_at unchecked"),
 ("M49", I, "@@NA@@", "", "approve: lifetime re-check removed (code no longer exists; replaced by the validator run, see N01-N03)"),
 ("M50", I, "            self.muted.insert(r.proposer);", "            let _ = r.proposer;", "mute not recorded"),
 ("M51", I, "        self.used.insert(s, used.saturating_add(1));", "        self.used.insert(s, used);", "quota not charged"),
 ("M52", I, "        self.check_roster(roster)?;\n        self.tick(roster, now);\n        // 1.", "        self.tick(roster, now);\n        // 1.", "receive: roster/session/approver not checked"),
 ("M53", P, "    m.extend_from_slice(PROPOSAL_LABEL);\n    m.push(0);", "    m.extend_from_slice(b\"coagent-roster-proposal-v2\");\n    m.push(0);", "label bytes changed (consistently)"),
 ("M54", P, "    m.extend_from_slice(PROPOSAL_LABEL);\n    m.push(0);", "    m.extend_from_slice(PROPOSAL_LABEL);", "label separator dropped"),
 ("M55", P, "    m.extend_from_slice(PROPOSAL_LABEL);\n    m.push(0);", "", "label dropped entirely"),
 ("M56", P, "if bytes.len() > MAX_PROPOSAL_BYTES && !cfg", "if false && bytes.len() > MAX_PROPOSAL_BYTES && !cfg", "*SignedProposal::decode size check removed"),
 ("M57", P, "Some(Role::Observer) if !cfg!(coagent_red_roster = \"propose_observer_ok\") =>", "Some(Role::Observer) if false =>", "*propose(): observer allowed"),
 ("M58", P, "        return Err(ProposalError::CandidateRemoved);", "        let _ = 0;", "propose(): removed candidate allowed"),
 ("M59", P, "        if self.body.proposer != proposer.key_id() {\n            return Err(ProposalError::WrongProposer);", "        if false {\n            return Err(ProposalError::WrongProposer);", "verify(): WrongProposer removed"),
 ("M60", P, "if roster.is_convener(&me) && !cfg", "if false && roster.is_convener(&me) && !cfg", "*propose(): starter allowed"),
 ("M61", L, "                role: p.body.role,\n                sig: p.sig,", "                role,\n                sig: p.sig,", "Member::proposed records the entry role"),
]

N = [  # new mutants on code changed since 0a47fc9
 ("N01", I, "        if !cfg!(coagent_red_roster = \"approve_no_validate\")\n            && !cfg!(coagent_red_roster = \"intake_keep_stale\")", "        if false", "approve: validator run removed (receive checks intact)"),
 ("N02", I, "                .and_then(|_| crate::check_transition(roster, &next).map(|_| ()));", "                .map(|_| ());", "approve: transition rules not run"),
 ("N03", I, "            let verdict = crate::validate_body(&next)\n", "            let verdict = Ok::<(), RosterError>(())\n", "approve: single-version rules not run"),
 ("N04", I, "                    r.outcome = Outcome::RefusedInvalid;\n                    r.proposal = None;", "                    let _ = r;", "refused approval leaves the proposal pending"),
 ("N05", I, "                return Err(IntakeError::InvalidApproval(reason));", "                for r in self.records.values_mut() { if r.outcome == Outcome::Pending { r.outcome = Outcome::Stale; r.proposal = None; } }\n                return Err(IntakeError::InvalidApproval(reason));", "refused approval stales every other pending proposal"),
 ("N06", I, "                return Err(IntakeError::InvalidApproval(reason));", "                for u in self.used.values_mut() { *u = u.saturating_add(1); }\n                return Err(IntakeError::InvalidApproval(reason));", "refused approval charges every proposer"),
 ("N07", I, ".any(|m| m.sign_pub == b.candidate.sign_pub)", ".any(|m| false && m.sign_pub == b.candidate.sign_pub)", "receive: signing-key compare removed"),
 ("N08", I, ".any(|m| m.noise_static == b.candidate.noise_static)", ".any(|m| false && m.noise_static == b.candidate.noise_static)", "receive: Noise-key compare removed"),
 ("N09", I, ".any(|m| m.sign_pub == b.candidate.sign_pub)", ".any(|m| m.noise_static == b.candidate.sign_pub)", "receive: signing key compared with the wrong field"),
 ("N10", I, "if roster.version() >= MAX_VERSIONS\n", "if roster.version() > MAX_VERSIONS\n", "receive: version bound >= -> >"),
 ("N11", I, "if roster.version() >= MAX_VERSIONS\n", "if false && roster.version() >= MAX_VERSIONS\n", "receive: version bound removed"),
 ("N12", I, "                        made_stale.push((*k, r.proposer));", "                        let _ = k;", "made_stale never filled"),
 ("N13", I, "                        made_stale.push((*k, r.proposer));", "                        made_stale.push((*k, self.local));", "made_stale names the wrong proposer"),
 ("N14", I, "                *c = c.saturating_add(1);", "                *c = c.saturating_add(0);", "crowded counter not incremented"),
 ("N15", I, "                *c = c.saturating_add(1);", "                *c = c.saturating_add(2);", "crowded counter +2"),
 ("N16", I, ".retain(|k, _| roster.role_of(k) == Some(Role::Guest) && !roster.is_convener(k));", ".retain(|_, _| true);", "crowded counters never pruned"),
 ("N17", I, ".retain(|k, _| roster.role_of(k) == Some(Role::Guest) && !roster.is_convener(k));", ".retain(|k, _| roster.role_of(k).is_some() && !roster.is_convener(k));", "crowded counters kept for observers"),
 ("N18", I, "            return Err(IntakeError::ProposerHasPending);", "            *self.crowded.entry(s).or_insert(0) += 1;\n            return Err(IntakeError::ProposerHasPending);", "crowded counted on ProposerHasPending too"),
 ("N19", I, "        self.crowded.get(guest).copied().unwrap_or(0)", "        { let _ = guest; 0 }", "crowded_out always 0"),
 ("N20", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "        if false && wire.len() > 2 * MAX_PROPOSAL_BYTES {", "receive_wire: string bound removed (decode first)"),
 ("N21", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "        if wire.len() >= 2 * MAX_PROPOSAL_BYTES {", "receive_wire: > -> >="),
 ("N22", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "        if wire.len() > 4 * MAX_PROPOSAL_BYTES {", "receive_wire: bound doubled"),
 ("N23", P, "    if !b.len().is_multiple_of(2) || !b.iter().all(|c| matches!(c, b'0'..=b'9' | b'a'..=b'f')) {", "    if !b.len().is_multiple_of(2) || !b.iter().all(|c| matches!(c, b'0'..=b'9' | b'a'..=b'f' | b'A'..=b'F')) {", "wire: upper case accepted"),
 ("N24", P, "    if !b.len().is_multiple_of(2) || !b.iter().all(", "    if !b.iter().all(", "wire: odd length accepted"),
 ("N25", I, "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {\n            self.tick(roster, now);", "        if wire.len() > 2 * MAX_PROPOSAL_BYTES {", "receive_wire: no tick on TooLarge"),
 ("N26", P, "    bytes.iter().map(|b| format!(\"{b:02x}\")).collect()\n}\n\n/// Strict", "    bytes.iter().map(|b| format!(\"{b:02X}\")).collect()\n}\n\n/// Strict", "to_wire writes upper case"),
 ("N27", L, "    let p = &sp.body;\n    if let Some(rec) = &n.proposal {\n        check_admission_role(n, rec)?;", "    let p = &sp.body;\n    if let Some(rec) = &n.proposal {\n        let _ = check_admission_role(n, rec);", "transition: admission role rule skipped"),
 ("N28", L, "        if m.added_in == b.version {\n            if let Some(rec) = &m.proposal {", "        if false {\n            if let Some(rec) = &m.proposal {", "first roster: admission role rule skipped"),
 ("N29", L, "        if m.added_in == b.version {\n            if let Some(rec) = &m.proposal {", "        if true {\n            if let Some(rec) = &m.proposal {", "first roster: admission rule applied to every entry (F1 back)"),
 ("N30", L, "        if m.added_in == b.version {\n            if let Some(rec) = &m.proposal {", "        if m.added_in + 1 == b.version {\n            if let Some(rec) = &m.proposal {", "first roster: admission rule on the wrong version"),
 ("N31", I, "        next.version = cur.version.saturating_add(1);", "        next.version = cur.version.saturating_add(2);", "approve: version +2 (validator in approve does not check numbering)"),
 ("N32", I, "        next.prev_hash = Digest32(roster.hash());", "        next.prev_hash = Digest32([0; 32]);", "approve: wrong prev_hash"),
 ("N33", I, "                    r.outcome = Outcome::RefusedInvalid;", "                    r.outcome = Outcome::Declined;", "refused approval recorded as Declined"),
 ("N34", I, "if added_at.len() > 64 && !cfg", "if added_at.len() > 65 && !cfg", "approve: added_at bound off by one"),
 ("N35", I, "            .find(|s| cur.members.iter().all(|m| m.slot != *s))", "            .rfind(|s| cur.members.iter().all(|m| m.slot != *s))", "approve: last free slot instead of first"),
 ("N36", I, "        .retain(|k, _| roster.role_of(k) == Some(Role::Guest) && !roster.is_convener(k));", "        .retain(|k, _| roster.role_of(k) == Some(Role::Guest));", "crowded prune: convener term dropped"),
 ("N37", L, "    let zero = p.at_version == 0 && !cfg", "    let zero = p.at_version == 1 && !cfg", "version-zero rule on the wrong value"),
 ("N38", I, "        let Some(bytes) = from_wire_hex(wire) else {\n            self.tick(roster, now);\n            return Err(IntakeError::Malformed);\n        };", "        let Some(bytes) = from_wire_hex(wire) else {\n            return Err(IntakeError::Malformed);\n        };", "receive_wire: no tick on Malformed"),
 ("N39", I, "    pub fn receive_wire(\n        &mut self,\n        roster: &ValidRoster,\n        sender: &KeyId,\n        wire: &str,\n        now: Instant,\n    ) -> Result<ProposalId, IntakeError> {\n        self.check_roster(roster)?;", "    pub fn receive_wire(\n        &mut self,\n        roster: &ValidRoster,\n        sender: &KeyId,\n        wire: &str,\n        now: Instant,\n    ) -> Result<ProposalId, IntakeError> {", "receive_wire: roster check removed before its own tick"),
]

TESTS = ["admit_propose", "api_stability", "gate_return", "gate_return_a3", "gate_roster", "intake",
         "lifetime", "limit", "mesh", "pinned_encoding", "proposal", "qa_gate", "roles", "roster"]

def run(tests):
    env = dict(os.environ, CARGO_TARGET_DIR=TARGET)
    cmd = ["cargo", "test", "--locked", "--manifest-path", os.path.join(WT, "Cargo.toml"),
           "-p", "coagent-roster", "--lib"] + sum([["--test", t] for t in tests], []) + ["--no-fail-fast"]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    log = r.stdout + r.stderr
    if "error[E" in log or "could not compile" in log:
        return "COMPILE-ERROR"
    if "No such file" in log or "Network" in log or not os.path.isdir("/Volumes/Laptop-DEV/FRIDAY"):
        return "ENV-ERROR"
    if r.returncode != 0:
        failed = [l.split()[1] for l in log.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
        return "KILLED(" + ",".join(failed[:4]) + ("" if len(failed) <= 4 else f",+{len(failed)-4}") + ")"
    return "SURVIVED"

out = open(OUT, "a")
for mid, f, old, new, what in R1 + N:
    if ONLY and mid not in ONLY:
        continue
    path = os.path.join(WT, f)
    src = open(path).read()
    n = src.count(old)
    if n != 1:
        out.write(f"{mid}\tNOT-APPLIED(count={n})\t\t{what}\n"); out.flush(); continue
    open(path, "w").write(src.replace(old, new))
    try:
        res = run(TESTS)
        extra = run(["qa_r2"]) if res == "SURVIVED" and os.path.exists(os.path.join(WT, "crates/coagent-roster/tests/qa_r2.rs")) else ""
    finally:
        open(path, "w").write(src)
    out.write(f"{mid}\t{res}\t{extra}\t{what}\n"); out.flush()
out.close()
