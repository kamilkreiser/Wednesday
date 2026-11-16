"""QA gate M3-AUDIT round 3 mutation driver (head 882e094).
Round-1 mutants (from the reference `gate_audit_tests/mutate.py`), round-2 mutants (the ADAPT and NEW
tables of `gate_audit_tests_r2/mutate_r2.py`, re-adapted below where the source changed) and new
mutants P01.. on code changed since 4c39916. One mutant at a time on a pristine clone; the branch's
full crate suite (`cargo test -p coagent-audit`, plus coagent-crypto for crypto mutants); revert with
git checkout.

usage: mutate_r3.py <clone> <target_dir> <logdir> <out.json> [--check] [--suite gate_r3] [ids...]
"""
import os, re, subprocess, sys, json, importlib.util

REF = "/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review"
A = "crates/coagent-audit/src/"
C = "crates/coagent-crypto/src/"
TOOLS = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"

# round 1
spec = importlib.util.spec_from_file_location("r1", REF + "/gate_audit_tests/mutate.py")
r1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r1)
R1 = {mid: (desc, [(A + f, old, new)]) for mid, f, desc, old, new in r1.M}

def cfgred(name):
    return ' && !cfg!(coagent_audit_red = "%s")' % name

# round 2 tables (ADAPT and NEW), executed from the reference driver's text
src2 = open(REF + "/gate_audit_tests_r2/mutate_r2.py").read()
block = src2[src2.index("ADAPT = {"):src2.index("ALL = dict(R1)")]
ns = {"A": A, "C": C, "R1": R1, "cfgred": cfgred}
exec(block, ns)
R2 = ns["NEW"]  # R1 already updated in place with round-2 adaptations

# round 3 re-adaptations: same semantics, source text changed at 882e094
ADAPT3 = {
 "N01": [(A+"session.rs", "            .map(|(_, l)| *l)\n            .unwrap_or_default()", "            .map(|(_, l)| *l)\n            .unwrap_or(ShareLevel::Full)")],
 "N07": [(A+"equivocation.rs", "            if !member_ok && !cfg!(coagent_audit_red = \"hs_no_entry_member\") {", "            if false {")],
 "N14": [(A+"session.rs", "        self.ensure(Payer::Own, n.saturating_mul(4 + MAX_RECORD_BYTES), n)", "        self.ensure(Payer::Own, n.saturating_mul(4), n)")],
 "N16": [(A+"bundle.rs", "    if (n > MAX_RECORDS + slack || bytes.len() + seal_room > MAX_BUNDLE_BYTES + slack)", "    if (n > MAX_RECORDS + 1 || bytes.len() + seal_room > MAX_BUNDLE_BYTES + 1)")],
 "N17": [(A+"chain.rs", "                if s.len() > factor * MAX_SUMMARY_BYTES {", "                if s.len() > 64 * MAX_SUMMARY_BYTES {")],
 "N21": [(A+"bundle.rs", "            && hs.to.is_some_and(|t| t != exporter)\n            && !cfg!(coagent_audit_red = \"verify_hs_other_recipient\")", "            && false")],
 "N22": [(A+"bundle.rs", "        if (hs.roster_v > v_last || !book.has_version(hs.roster_v))\n            && !cfg!(coagent_audit_red = \"verify_hs_unheld_version\")", "        if false")],
}
for k, v in ADAPT3.items():
    R2[k] = (R2[k][0] + " [adapted r3]", v)

R1["M38"] = (R1["M38"][0] + " [adapted r3]", [(A+"session.rs",
  "                self.store_evidence(&ev)?;\n                return Err(AuditError::Receive(ReceiveError::Fork(ev)));",
  "                self.store_evidence(&ev)?;\n                return Ok(head.countersign(id)?);")])

S_ = A + "session.rs"
NEW3 = {
 "P01": ("ensure: per-peer RECORD quota dropped (bytes only)", [(S_, "            && (u_b.saturating_add(bytes) > q_b || u_r.saturating_add(records) > q_r)", "            && (u_b.saturating_add(bytes) > q_b)")]),
 "P02": ("ensure: peers' pool RECORD limit dropped", [(S_, "            && (peers_b.saturating_add(bytes) > pool_b || peers_r.saturating_add(records) > pool_r)", "            && (peers_b.saturating_add(bytes) > pool_b)")]),
 "P03": ("persist: payer's bytes never charged", [(S_, "        e.0 += 4 + bytes.len();", "        e.0 += 0;")]),
 "P04": ("receive: receipt charged to Own instead of the author", [(S_, "                    self.persist(&Record::OwnEvent(r), payer)?;", "                    self.persist(&Record::OwnEvent(r), Payer::Own)?;")]),
 "P05": ("receive: no byte reserve for the receipt", [(S_, "            + if receipt { RECEIPT_RECORD_MAX } else { 0 };", "            + 0;")]),
 "P06": ("receive: record count reserves 1 instead of 2", [(S_, "        self.ensure(payer, need, 1 + usize::from(receipt))?;", "        self.ensure(payer, need, 1)?;")]),
 "P07": ("advances: always true", [(S_, "    strictly || newm.len() > old.len()\n}", "    true\n}")]),
 "P08": ("advances: any roster_v change advances (also lower)", [(S_, "        return new.roster_v > last.roster_v;", "        return true;")]),
 "P09": ("advances: a lower number for a held author still advances", [(S_, "            Some(n) if n >= s => strictly |= n > s,", "            Some(n) => strictly |= n > s,")]),
 "P10": ("receive_heads_seen: last_hs never updated", [(S_, "        self.last_hs.insert(key, hs.clone());", "        let _ = key;")]),
 "P11": ("receive_heads_seen: latest-state key ignores the recipient", [(S_, "        let key = (hs.from, hs.to);", "        let key = (hs.from, None);")]),
 "P12": ("note_share_level: an older statement replaces a newer one", [(S_, "            .is_none_or(|(seq, _)| *seq < h.author_seq)", "            .is_none_or(|_| true)")]),
 "P13": ("note_share_level: version-range membership loop dropped", [(S_, "            if self.history.has_version(v)\n                && !(self.history.member_in(&h.author, v)", "            if false\n                && !(self.history.member_in(&h.author, v)")]),
 "P14": ("note_share_level: session check dropped", [(S_, "        if h.session_id != self.session_id {\n            return Err(AuditError::WrongSession);\n        }\n        if h.author == self.local {", "        if h.author == self.local {")]),
 "P15": ("note_share_level: author==member check dropped", [(S_, "        if body.member == h.author {", "        if false {")]),
 "P16": ("note_share_level: kind check dropped", [(S_, "        if h.kind != SHARE_LEVEL_KIND {", "        if false {")]),
 "P17": ("note_share_level: summary commitment check dropped", [(S_, "        check_tiers(stmt).map_err(AuditError::Receive)?;", "        let _ = check_tiers(stmt);")]),
 "P18": ("apply_roster: levels FROM a removed author kept", [(S_, "                    .retain(|(a, m), _| !removed.contains(a) && !removed.contains(m));", "                    .retain(|(_a, m), _| !removed.contains(m));")]),
 "P19": ("store_evidence: duplicate evidence stored again", [(S_, "        if self.evidence_stored.contains(&enc) {\n            return Ok(());\n        }", "        if false {\n            return Ok(());\n        }")]),
 "P20": ("add_countersignature: exact-duplicate short-cut dropped", [(S_, "        if had {\n            return Ok(()); // an exact duplicate: nothing stored\n        }", "        if false {\n            return Ok(());\n        }")]),
 "P21": ("receive_heads_seen: digest set never filled (claimed redundant)", [(S_, "        self.hs_digests.insert(digest);", "        let _ = digest;")]),
 "P22": ("note_share_level: roster_v not held accepted (has_version check dropped)", [(S_, "        if !self.history.has_version(body.roster_v) {\n            return Err(AuditError::RosterBehind(body.roster_v));\n        }", "")]),
 "P23": ("store_evidence: per-author counter never incremented", [(S_, "        self.evidence_per_author.insert(ev.author(), n + 1);", "        let _ = n;")]),
 "P24": ("receive_heads_seen: removed reporter's record stored (reporter_current forced true)", [(S_, "        let reporter_current = self.roster.current().role_of(&hs.from).is_some()", "        let reporter_current = true")]),
 "P25": ("own reserve divisor 4 -> 1 (peers' pool is 0)... inverted: OWN_SHARE_DIVISOR 4 -> 2", [(S_, "pub const OWN_SHARE_DIVISOR: usize = 4;", "pub const OWN_SHARE_DIVISOR: usize = 2;")]),
 "P26": ("PEER_QUOTA_DIVISOR 7 -> 3", [(S_, "pub const PEER_QUOTA_DIVISOR: usize = 7;", "pub const PEER_QUOTA_DIVISOR: usize = 3;")]),
 "P27": ("EVIDENCE_PER_AUTHOR 4 -> 1000", [(S_, "pub const EVIDENCE_PER_AUTHOR: usize = 4;", "pub const EVIDENCE_PER_AUTHOR: usize = 1000;")]),
 "P28": ("set_limits: may RAISE limits above the defaults", [(S_, "            bytes: limits.bytes.min(d.bytes),", "            bytes: limits.bytes,")]),
 "P29": ("start: existing records not counted", [(S_, "        let used_bytes = existing.iter().map(|r| 4 + r.len()).sum();", "        let used_bytes = 0;")]),
 "P30": ("ShareLevelBody: unknown fields allowed", [(A+"chain.rs", "#[serde(deny_unknown_fields)]\npub struct ShareLevelBody {", "pub struct ShareLevelBody {")]),
}

ALL = dict(R1); ALL.update(R2); ALL.update(NEW3)

def main():
    args = sys.argv[1:]
    repo, target, logdir, outp = args[:4]
    rest = args[4:]
    check = "--check" in rest
    suite = None
    if "--suite" in rest:
        suite = rest[rest.index("--suite") + 1]
    ids = [a for a in rest if re.match(r"^[MNP]\d\d$", a)]
    env = dict(os.environ, RUSTUP_HOME=TOOLS + "/rustup", CARGO_HOME=TOOLS + "/cargo",
               CARGO_TARGET_DIR=target, PATH=TOOLS + "/cargo/bin:" + os.environ["PATH"])
    env.pop("COAGENT_AUDIT_RED", None)
    os.makedirs(logdir, exist_ok=True)
    results = []
    for mid in sorted(ALL):
        if ids and mid not in ids:
            continue
        desc, edits = ALL[mid]
        files = sorted({f for f, _, _ in edits})
        bad = None
        for f, old, new in edits:
            p = repo + "/" + f
            s = open(p).read()
            n = s.count(old)
            if n != 1:
                bad = f"NOAPPLY ({f} matches={n})"; break
            open(p, "w").write(s.replace(old, new))
        if bad or check:
            subprocess.run(["git", "-C", repo, "checkout", "--"] + files, check=True)
            results.append((mid, desc, bad or "APPLIES", "")); print(mid, bad or "APPLIES", flush=True)
            continue
        pk = ["-p", "coagent-audit"] + (["-p", "coagent-crypto"] if any(f.startswith(C) for f in files) else [])
        cmd = ["cargo", "test", "--offline", "--locked"] + pk + ["--no-fail-fast"]
        if suite:
            cmd = ["cargo", "test", "--offline", "-p", "coagent-audit", "--test", suite]
        r = subprocess.run(cmd, cwd=repo, env=env, capture_output=True, text=True)
        subprocess.run(["git", "-C", repo, "checkout", "--"] + files, check=True)
        out = r.stdout + r.stderr
        open(f"{logdir}/{mid}.log", "w").write(out)
        if "error[E" in out or "could not compile" in out:
            status, by = "COMPILE-ERROR", ""
        else:
            failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
            status = "KILLED" if failed else ("SURVIVED" if r.returncode == 0 else "KILLED?(no test named)")
            by = ", ".join(failed)
        results.append((mid, desc, status, by))
        print(mid, status, by[:300], flush=True)
    json.dump(results, open(outp, "w"), indent=1)
    diff = subprocess.run(["git", "-C", repo, "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True).stdout
    print("WORKTREE CLEAN" if not diff.strip() else "WORKTREE DIRTY:\n" + diff)

if __name__ == "__main__":
    main()
