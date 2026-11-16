#!/usr/bin/env python3
"""Mutation driver (gate r2). One mutation at a time in repo-mut; full suite of the three CORE crates;
file restored with `git checkout -- <file>` after each. Usage: mut.py <set: r1|new|all> [ids...]"""
import os, re, subprocess, sys

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_core_r2"
R = S + "/repo-mut"
LOG = S + "/mutlogs"
os.makedirs(LOG, exist_ok=True)
C = "crates/coagent-crypto/src/"
RO = "crates/coagent-roster/src/lib.rs"

R1 = [
    ("M01", C + "pairing.rs", 'PairingRole::Joiner => b"joiner\\0",', 'PairingRole::Joiner => b"inviter",'),
    ("M02", C + "pairing.rs", "        mac.update(h);\n", ""),
    ("M03", C + "sas.rs", 'if !cfg!(coagent_red = "sas_commit_no_h") {\n        d.update(h);\n    }', ""),
    ("M04", C + "sas.rs", "    d.update(r_r);\n", ""),
    ("M05", C + "channel.rs", "if self.recv_in_epoch >= REKEY_AFTER_MESSAGES", "if self.recv_in_epoch > REKEY_AFTER_MESSAGES"),
    ("M06", RO, "            if got != have + 1 {\n                return Err(RosterError::Gap { have, got });\n            }\n", ""),
    ("M07", RO, "            if next.body.prev_hash.as_bytes() != &self.current.hash() {\n                return Err(RosterError::BrokenChain);\n            }\n", ""),
    ("M08", RO, "                m.added_in <= r.at_version\n            };", "                m.added_in < r.at_version\n            };"),
    ("M09", C + "kk.rs", 'if !cfg!(coagent_red = "kk_prologue_no_roster_hash") {\n        p.extend_from_slice(roster_hash);\n    }', ""),
    ("M10", C + "kk.rs", 'if !cfg!(coagent_red = "kk_prologue_no_slots") {\n        p.push(initiator_slot);\n        p.push(responder_slot);\n    }', ""),
    ("M11", C + "channel_map.rs", "                v.abort();\n", ""),
    ("M12", "crates/coagent-proto/src/envelope.rs", "    if e.to != b.local {", "    if false && e.to != b.local {"),
    ("M13", C + "pake.rs", "        id_a.extend_from_slice(&c);\n        id_b.extend_from_slice(&c);\n", ""),
    ("M14", C + "pake.rs", "            info.extend_from_slice(ctx);\n", ""),
    ("M15", C + "channel.rs", 'if !self.awaiting_confirm && !cfg!(coagent_red = "keyconfirm_after_confirm")', 'if false && !self.awaiting_confirm'),
    ("M16", C + "channel_map.rs", "            Some(VerifyStatus::HardStop)\n        ) {\n            return Err(CryptoError::VerifyHardStop);", "            Some(VerifyStatus::Locked)\n        ) {\n            return Err(CryptoError::VerifyHardStop);"),
    ("M17", C + "pairing.rs", 'if hello.session_id.is_some() && !cfg!(coagent_red = "joiner_hello_session_ok")', "if false && hello.session_id.is_some()"),
    ("M18", RO, "    if &b.session_id != session {\n        return Err(RosterError::WrongSession);\n    }\n", ""),
    ("M19", RO, 'if dev.key_id() != m.key_id && !cfg!(coagent_red = "roster_no_keyid_check")', "if false && dev.key_id() != m.key_id"),
    ("M20", RO, "                return Err(RosterError::Fork(Box::new(ForkEvidence {\n                    held: held.clone(),\n                    offered: next.clone(),\n                })));", "                return Err(RosterError::Stale { have, got });"),
]

NEW = [
    # arming window comparison: expiry ignored
    ("N01", C + "sas.rs", "(Some(until), Some(now)) => now <= until,", "(Some(_until), Some(_now)) => true,"),
    # unknown time (None) counts as armed
    ("N02", C + "sas.rs", "(Some(until), Some(now)) => now <= until,\n            _ => false,", "(Some(until), Some(now)) => now <= until,\n            (Some(_), None) => true,\n            _ => false,"),
    # un-count on decline also after the reveal (free guess for a middleman)
    ("N03", C + "sas.rs", "            (true, SasStep::Decline) => match self.state {\n                // The other side was not armed and did not use our commitment. r_C was never\n                // revealed, so un-counting this attempt gives a middleman nothing.\n                State::CommitSent { .. } => {",
            "            (true, SasStep::Decline) => match self.state {\n                // The other side was not armed and did not use our commitment. r_C was never\n                // revealed, so un-counting this attempt gives a middleman nothing.\n                State::CommitSent { .. } | State::AwaitingHuman { .. } => {"),
    # no un-count on decline (liveness)
    ("N04", C + "sas.rs", "                    self.attempts = self.attempts.saturating_sub(1);\n", ""),
    # responder press not used up by an accepted commitment (one press, many ceremonies)
    ("N05", C + "sas.rs", "                    self.armed_until = None; // the press is used up\n                    let r_r", "                    let r_r"),
    # committer press not used up at the reveal
    ("N06", C + "sas.rs", "                    self.armed_until = None; // the press is used up\n                    Ok(SasOutput {", "                    Ok(SasOutput {"),
    # an unarmed committer counts the declined request
    ("N07", C + "sas.rs", "                State::Idle => Ok(SasOutput::decline()),", "                State::Idle => {\n                    self.attempts += 1;\n                    Ok(SasOutput::decline())\n                }"),
    # words binding compares only the first word
    ("N08", C + "sas.rs", 'if &pending != words && !cfg!(coagent_red = "confirm_unbound")', "if pending[0] != words[0]"),
    # a "no" for stale words is honoured (hard stop) -- this is the direction r2 recommends; expect SURVIVE or the f3 test to flag
    ("N09", C + "sas.rs", 'if &pending != words && !cfg!(coagent_red = "confirm_unbound") {', 'if matched && &pending != words {'),
    # slot inheritance: an existing per-key record is not raised to the slot's count
    ("N10", C + "channel_map.rs", "            if v.attempts_used() < inherited {\n                *v = PairVerification::with_attempts_used(inherited);\n            }\n", ""),
    # slot hard-stop check removed at insert
    ("N11", C + "channel_map.rs", 'if rec.hard_stop && !cfg!(coagent_red = "slot_ignore") {', "if false && rec.hard_stop {"),
    # sync_slot does not record the hard stop
    ("N12", C + "channel_map.rs", "        rec.hard_stop |= v.status() == VerifyStatus::HardStop;\n", ""),
    # sync_slot does not record attempts
    ("N13", C + "channel_map.rs", "        rec.attempts_used = rec.attempts_used.max(v.attempts_used()).min(MAX_ATTEMPTS);\n", ""),
    # small-order check removed from verify_device (independent of the red-control branch)
    ("N14", C + "identity.rs", "    if is_small_order(keys.noise_static.as_bytes()) {\n        return Err(CryptoError::BadKey);", "    if false && is_small_order(keys.noise_static.as_bytes()) {\n        return Err(CryptoError::BadKey);"),
    # small-order: ignore the top bit handling by masking -- uses only canonical 0 / 1 / p-1 spellings? (compare top byte only)
    ("N15", C + "identity.rs", "        .to_bytes()\n        == [0u8; 32]", "        .to_bytes()[0]\n        == 0"),
    # ephemeral offset wrong
    ("N16", C + "noise.rs", "        .get(..32)", "        .get(1..33)"),
    # KK initiator does not check the responder's ephemeral (msg2)
    ("N17", C + "kk.rs", "        noise::read_starting_with_e(&mut self.hs, msg2)?;", "        noise::read(&mut self.hs, msg2)?;"),
    # XX inviter does not check the joiner's ephemeral (msg2)
    ("N18", C + "pairing.rs", "                let payload = noise::read_starting_with_e(&mut hs, bytes)?;", "                let payload = noise::read(&mut hs, bytes)?;"),
    # XX joiner does not check the inviter's ephemeral (msg1)
    ("N19", C + "pairing.rs", "                noise::read_starting_with_e(&mut hs, bytes)?;\n                let payload = canonical::encode(&self.hello)?;", "                noise::read(&mut hs, bytes)?;\n                let payload = canonical::encode(&self.hello)?;"),
    # self-membership checks the convener instead of the local device
    ("N20", RO, "if current.role_of(local).is_none()", "if current.role_of(&convener.key_id()).is_none()"),
    # duplicate check: sign_pub not checked
    ("N21", RO, "(!noise_keys.insert(m.noise_static) || !sign_keys.insert(m.sign_pub))", "(!noise_keys.insert(m.noise_static) || (false && !sign_keys.insert(m.sign_pub)))"),
    # duplicate check: noise_static not checked
    ("N22", RO, "(!noise_keys.insert(m.noise_static) || !sign_keys.insert(m.sign_pub))", "((false && !noise_keys.insert(m.noise_static)) || !sign_keys.insert(m.sign_pub))"),
    # MAX_FRAME off by one (refuses a legitimate maximum-size frame)
    ("N23", C + "channel.rs", 'if frame.len() > MAX_FRAME && !cfg!(coagent_red = "open_no_len_cap")', "if frame.len() >= MAX_FRAME"),
    # MAX_FRAME too loose (cap at twice the size)
    ("N24", C + "channel.rs", 'if frame.len() > MAX_FRAME && !cfg!(coagent_red = "open_no_len_cap")', "if frame.len() > 2 * MAX_FRAME"),
    # role_changed reported only for the first changed member
    ("N25", RO, "                    role_changed.push(m.key_id);", "                    if role_changed.is_empty() {\n                        role_changed.push(m.key_id);\n                    }"),
    # tick allows time to go backwards
    ("N26", C + "channel_map.rs", "            Some(t) if t > now => t, // time never goes backwards here\n", ""),
    # committer re-commits on a request that crosses its own commitment (extra attempt)
    ("N27", C + "sas.rs", "                State::CommitSent { .. } => Ok(SasOutput::nothing()),", "                State::CommitSent { .. } => {\n                    self.state = State::Idle;\n                    self.commit(h)\n                }"),
    # test-seam guard in build.rs never fires (checked with the runner's release row, not the suite)
    ("N28", "crates/coagent-crypto/build.rs", 'std::env::var("PROFILE").as_deref() != Ok("release"),\n            "the test-seam feature', 'std::env::var("PROFILE").as_deref() != Ok("bench"),\n            "the test-seam feature'),
]


def run(mid, path, old, new):
    full = os.path.join(R, path)
    src = open(full).read()
    n = src.count(old)
    if n != 1:
        return f"{mid}: NOT APPLIED (anchor count {n})"
    open(full, "w").write(src.replace(old, new))
    try:
        p = subprocess.run(
            ["cargo", "test", "--locked", "--offline", "--no-fail-fast", "-p", "coagent-proto", "-p", "coagent-crypto", "-p", "coagent-roster"],
            cwd=R, capture_output=True, text=True)
        out = p.stdout + p.stderr
        open(f"{LOG}/{mid}.log", "w").write(out)
        if "error[E" in out or "could not compile" in out:
            return f"{mid}: BUILD ERROR"
        failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
        okc = len(re.findall(r"^test \S+ \.\.\. ok$", out, re.M))
        if failed:
            return f"{mid}: CAUGHT by {', '.join(failed)} (ok={okc})"
        return f"{mid}: SURVIVED (ok={okc})"
    finally:
        subprocess.run(["git", "checkout", "--", path], cwd=R)


if __name__ == "__main__":
    which = sys.argv[1]
    ids = set(sys.argv[2:])
    muts = (R1 if which in ("r1", "all") else []) + (NEW if which in ("new", "all") else [])
    for m in muts:
        if ids and m[0] not in ids:
            continue
        print(run(*m), flush=True)
    st = subprocess.run(["git", "status", "--porcelain"], cwd=R, capture_output=True, text=True).stdout
    print("clean after run:", st.strip() == "", flush=True)
