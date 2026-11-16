"""QA gate M3-AUDIT mutation driver. One mutant at a time on the pristine `mut` clone; the
builder's full crate suite (`cargo test -p coagent-audit`); revert with git checkout."""
import os, re, subprocess, sys, json

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m3_audit"
REPO = S + "/mut"
SRC = REPO + "/crates/coagent-audit/src/"
TOOLS = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
ENV = dict(os.environ, RUSTUP_HOME=TOOLS + "/rustup", CARGO_HOME=TOOLS + "/cargo",
           CARGO_TARGET_DIR=S + "/target-mut", PATH=TOOLS + "/cargo/bin:" + os.environ["PATH"])

M = [
 ("M01", "header.rs", "drop outer prev_hash prefix from chain hash",
  "        h.update(self.prev_hash.as_bytes());\n        h.update(canonical::encode(self)?);",
  "        h.update(canonical::encode(self)?);"),
 ("M02", "header.rs", "chain hash ignores the header (hash = H(prev_hash))",
  "        h.update(canonical::encode(self)?);\n", "        let _ = canonical::encode(self)?;\n"),
 ("M03", "bundle.rs", "verify: drop own/peer author_seq check",
  "    if h.author_seq != expect_seq {", "    if false && h.author_seq != expect_seq {"),
 ("M04", "header.rs", "drop `type` from the signed header bytes",
  "    #[serde(rename = \"type\")]\n    pub kind: String,\n    /// Salted commitments to each tier (`None`: the event has no such tier).",
  "    #[serde(rename = \"type\", skip)]\n    pub kind: String,\n    /// Salted commitments to each tier (`None`: the event has no such tier)."),
 ("M05", "checkpoint.rs", "countersignature attests: drop session comparison",
  "        self.session_id == head.session_id\n            && (self.author", "        true\n            && (self.author"),
 ("M06", "received.rs", "accept: compare only 4-byte prefix of head hash",
  "            if head.hash != hash {", "            if head.hash.0[..4] != hash.0[..4] {"),
 ("M07", "received.rs", "accept: seq == next-1 treated as next (off-by-one on held range)",
  "        if seq < next {", "        if seq + 1 < next {"),
 ("M08", "received.rs", "skip summary-tier commitment check",
  "    tier_ok(\n        &e.summary,\n        &e.header.tiers.summary,\n        Tier::Summary,\n        MAX_SUMMARY_BYTES,\n    )?;",
  "    let _ = tier_ok(\n        &e.summary,\n        &e.header.tiers.summary,\n        Tier::Summary,\n        MAX_SUMMARY_BYTES,\n    );"),
 ("M09", "chain.rs", "send the full-tier salt (no body) to a summaries recipient",
  "                } else {\n                    None\n                },\n            }),",
  "                } else {\n                    e.full.as_ref().map(|o| TierOpening { salt: o.salt.clone(), body: String::new() })\n                },\n            }),"),
 ("M10", "bundle.rs", "verify: skip countersigner roster-membership check",
  "        if cs.by == exporter || !book.member_in(&cs.by, head.roster_v) {", "        if cs.by == exporter {"),
 ("M11", "chain.rs", "author: store countersignature from a non-member",
  "            None => return Err(AuditError::NotMember(cs.by)),\n        };", "            None => return self.store_cs(cs),\n        };"),
 ("M12", "equivocation.rs", "evidence verify: accept two identical statements",
  "                if hx == hy && !cfg!", "                if false && hx == hy && !cfg!"),
 ("M13", "bundle.rs", "off-by-one MAX_RECORDS", "        if out.len() == MAX_RECORDS {", "        if out.len() == MAX_RECORDS + 1 {"),
 ("M14", "bundle.rs", "off-by-one MAX_RECORD_BYTES", "        } else if n > MAX_RECORD_BYTES {", "        } else if n > MAX_RECORD_BYTES + 1 {"),
 ("M15", "bundle.rs", "off-by-one MAX_BUNDLE_BYTES", "    if bytes.len() > MAX_BUNDLE_BYTES {", "    if bytes.len() > MAX_BUNDLE_BYTES + 1 {"),
 ("M16", "chain.rs", "skip redaction on the summary tier",
  "                let red = self.redactor.redact(s);", "                let red = s.to_string();"),
 ("M17", "bundle.rs", "verify: skip countersignature signature check",
  "        if cs.verify_sig(dev).is_err() {", "        if false && cs.verify_sig(dev).is_err() {"),
 ("M18", "bundle.rs", "verify: skip own checkpoint-hash-vs-chain check",
  "        if &h.hash != expect {", "        if false && &h.hash != expect {"),
 ("M19", "bundle.rs", "verify: skip peer checkpoint-hash-vs-chain check",
  "                    if x != &h.hash {", "                    if false && x != &h.hash {"),
 ("M20", "bundle.rs", "verify: seal digest not compared (count only)",
  "        if s.records != n || s.digest != digest_of(&bytes) {", "        if s.records != n {"),
 ("M21", "received.rs", "joiner: accept a header AT the anchor number",
  "        if seq <= self.base_seq {", "        if seq < self.base_seq {"),
 ("M22", "received.rs", "joiner: accept heads before the anchor",
  "        if head.author_seq < self.base_seq || head.author_seq == 0 {", "        if head.author_seq == 0 {"),
 ("M23", "equivocation.rs", "evidence verify: drop session check",
  "        if x.session() != keys.session() || y.session() != keys.session() {", "        if false {"),
 ("M24", "equivocation.rs", "link evidence: drop adjacency check",
  "                if x.seq().checked_add(1) != Some(later.author_seq) {\n                    return Err(EvidenceError::WrongSequence);",
  "                if false {\n                    return Err(EvidenceError::WrongSequence);"),
 ("M25", "equivocation.rs", "heads-seen: entry signatures not checked",
  "            e.verify_sig(adev)\n                .map_err(|_| EvidenceError::BadSignature)?;", "            let _ = e.verify_sig(adev);"),
 ("M26", "received.rs", "accept: drop MAX_SEQ bound",
  "        if h.author_seq > MAX_SEQ {\n            return Err(ReceiveError::BadField(\"author_seq\"));\n        }\n", ""),
 ("M27", "chain.rs", "author: accept its own countersignature",
  "        if cs.by == self.author {\n            return Err(AuditError::CountersignByAuthor);\n        }\n", ""),
 ("M28", "bundle.rs", "verify: accept countersignature by the exporter itself",
  "        if cs.by == exporter || !book.member_in", "        if !book.member_in"),
 ("M29", "bundle.rs", "verify_together: omitted_own off-by-one",
  "            .filter(|(au, q)| *au == me && *q > have)", "            .filter(|(au, q)| *au == me && *q > have + 1)"),
 ("M30", "domain.rs", "seal label collides with head label",
  "            AuditDomain::BundleSeal => b\"coagent-audit-bundle-seal-v1\",", "            AuditDomain::BundleSeal => b\"coagent-audit-head-v1\","),
 ("M31", "bundle.rs", "verify: joiner anchor signature not checked",
  "            Some(s) => {\n                check_head(s, &session, &a, &dev)?;", "            Some(s) => {\n                let _ = check_head(s, &session, &a, &dev);"),
 ("M32", "received.rs", "accept: prev_hash link not checked",
  "        if h.prev_hash != self.last_hash() && !cfg!(coagent_audit_red = \"recv_accept_gap\") {", "        if false {"),
 ("M33", "received.rs", "accept_head: never compares with held statements",
  "        let theirs = Statement::Head(head.clone());\n        let held = HeldOne(self);",
  "        let theirs = Statement::Head(SignedHead { author_seq: u64::MAX - 5, ..head.clone() });\n        let held = HeldOne(self);"),
 ("M34", "received.rs", "accept: drop author check (key is the author's anyway)",
  "        if h.author != self.author {\n            return Err(ReceiveError::WrongAuthor);\n        }\n        // RED CONTROL `recv_no_sig_check`",
  "        // RED CONTROL `recv_no_sig_check`"),
 ("M35", "equivocation.rs", "heads-seen: entry about the reporter itself allowed",
  "            if a == self.from || prev.is_some_and(|p| p >= a) {", "            if prev.is_some_and(|p| p >= a) {"),
 ("M36", "bundle.rs", "export: countersignatures dropped",
  "                countersigs.entry((x.author_seq, x.by)).or_insert(x);", "                let _ = x;"),
 ("M37", "tiers.rs", "tier commitment uses only half the salt (128 bits)",
  "        h.update(salt);", "        h.update(&salt[..16]);"),
 ("M38", "session.rs", "receive_head: countersign even a refused (forked) head",
  "                self.persist(&Record::Evidence((*ev).clone()))?;\n                return Err(AuditError::Receive(ReceiveError::Fork(ev)));",
  "                self.persist(&Record::Evidence((*ev).clone()))?;\n                return Ok(head.countersign(id)?);"),
]

def run(only=None):
    results = []
    for mid, f, desc, old, new in M:
        if only and mid not in only:
            continue
        p = SRC + f
        src = open(p).read()
        n = src.count(old)
        if n != 1:
            results.append((mid, desc, f"NOAPPLY (matches={n})", ""))
            print(mid, "NOAPPLY", n, flush=True)
            continue
        open(p, "w").write(src.replace(old, new))
        r = subprocess.run(["cargo", "test", "--offline", "--locked", "-p", "coagent-audit", "--no-fail-fast"],
                           cwd=REPO, env=ENV, capture_output=True, text=True)
        subprocess.run(["git", "-C", REPO, "checkout", "--", "crates/coagent-audit/src/" + f], check=True)
        out = r.stdout + r.stderr
        open(f"{S}/mutlogs/{mid}.log", "w").write(out)
        if "error[E" in out or "could not compile" in out:
            status, by = "COMPILE-ERROR", ""
        else:
            failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
            status = "KILLED" if failed else ("SURVIVED" if r.returncode == 0 else "KILLED?(no test named)")
            by = ", ".join(failed)
        results.append((mid, desc, status, by))
        print(mid, status, by, flush=True)
    return results

if __name__ == "__main__":
    os.makedirs(S + "/mutlogs", exist_ok=True)
    res = run(set(sys.argv[1:]) or None)
    json.dump(res, open(S + "/mutation_results.json", "w"), indent=1)
    diff = subprocess.run(["git", "-C", REPO, "status", "--porcelain"], capture_output=True, text=True).stdout
    print("WORKTREE CLEAN" if not diff.strip() else "WORKTREE DIRTY:\n" + diff)
