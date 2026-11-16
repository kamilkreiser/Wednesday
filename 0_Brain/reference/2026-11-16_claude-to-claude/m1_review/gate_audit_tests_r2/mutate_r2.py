"""QA gate M3-AUDIT round 2 mutation driver. One mutant at a time on the pristine `mut` clone
(head 4c39916); the branch's full crate suite (`cargo test -p coagent-audit`, plus coagent-crypto
for mutants in that crate); revert with git checkout. Round-1 mutants (re-applied, adapted where
the source text changed) and new mutants on the delta (N..)."""
import os, re, subprocess, sys, json, importlib.util

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m3_audit_r2"
REPO = S + "/mut"
A = "crates/coagent-audit/src/"
C = "crates/coagent-crypto/src/"
TOOLS = "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
ENV = dict(os.environ, RUSTUP_HOME=TOOLS + "/rustup", CARGO_HOME=TOOLS + "/cargo",
           CARGO_TARGET_DIR=S + "/target_mut", PATH=TOOLS + "/cargo/bin:" + os.environ["PATH"])

# round-1 list, loaded from the round-1 driver (copied to tools/mutate_r1.py)
spec = importlib.util.spec_from_file_location("r1", S + "/tools/mutate_r1.py")
r1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r1)
R1 = {mid: (desc, [(A + f, old, new)]) for mid, f, desc, old, new in r1.M}

def cfgred(name):
    return ' && !cfg!(coagent_audit_red = "%s")' % name

ADAPT = {
 "M03": [(A+"bundle.rs", '    if h.author_seq != expect_seq' + cfgred("verify_no_seq_check") + ' {', '    if false {')],
 "M10": [(A+"bundle.rs", '        if !allowed {\n            return Err(at("countersigner not', '        if false {\n            return Err(at("countersigner not')],
 "M13": [(A+"bundle.rs", '        if out.len() == MAX_RECORDS + usize::from(cfg!(coagent_audit_red = "records_cap_plus_one"))', '        if out.len() == MAX_RECORDS + 1')],
 "M14": [(A+"bundle.rs", '        } else if n > MAX_RECORD_BYTES + usize::from(cfg!(coagent_audit_red = "frame_cap_plus_one"))', '        } else if n > MAX_RECORD_BYTES + 1')],
 "M15": [(A+"bundle.rs", '    if bytes.len() > cap {', '    if bytes.len() > cap + 1 {')],
 "M18": [(A+"bundle.rs", '        if &h.hash != expect' + cfgred("verify_no_own_head_hash") + ' {', '        if false {')],
 "M19": [(A+"bundle.rs", '                    if x != &h.hash' + cfgred("verify_no_peer_head_hash") + ' {', '                    if false {')],
 "M20": [(A+"bundle.rs", '            || (s.digest != digest_of(&bytes)' + cfgred("seal_count_only") + ')', '            || false')],
 "M24": [(A+"equivocation.rs", '                if x.seq().checked_add(1) != Some(later.author_seq)\n                    && !cfg!(coagent_audit_red = "link_no_adjacency")', '                if false')],
 "M25": [(A+"equivocation.rs", '                e.verify_sig(adev)\n                    .map_err(|_| EvidenceError::BadSignature)?;', '                let _ = e.verify_sig(adev);')],
 "M26": [(A+"received.rs", '        if h.author_seq > MAX_SEQ' + cfgred("accept_no_max_seq") + ' {', '        if false {')],
 "M28": [(A+"bundle.rs", '        if cs.by == exporter' + cfgred("verify_self_countersig") + ' {', '        if false {')],
 "M35": [(A+"equivocation.rs", '            let self_entry = a == self.from' + cfgred("hs_self_entry") + ';', '            let self_entry = false;')],
 "M40": [(A+"bundle.rs", '        if last_cs.is_some_and(|l| l >= key)' + cfgred("verify_dup_countersig") + ' {', '        if false {')],
 "M41": [(A+"bundle.rs", '            let out_of_order =\n                h.author_seq <= last' + cfgred("verify_dup_peer_head") + ';', '            let out_of_order = false;')],
 "M42": [(A+"session.rs", '        if hs.from == self.local' + cfgred("hs_accept_own") + ' {', '        if false {')],
}
for k, v in ADAPT.items():
    R1[k] = (R1[k][0] + " [adapted]", v)

NEW = {
 "N01": ("known_level: unknown pair defaults to Full instead of Nothing",
   [(A+"session.rs", "            .get(&(*author, *member))\n            .copied()\n            .unwrap_or_default()", "            .get(&(*author, *member))\n            .copied()\n            .unwrap_or(ShareLevel::Full)")]),
 "N02": ("receive_heads_seen: addressed-to-another record accepted", [(A+"session.rs", "        if hs.to.is_some_and(|t| t != self.local) {", "        if false {")]),
 "N03": ("verify_with_history: header in a broadcast record accepted", [(A+"equivocation.rs", "            if self.to.is_none()\n                && matches!(e, Statement::Header(_))", "            if false\n                && matches!(e, Statement::Header(_))")]),
 "N04": ("heads_seen_for: headers to a recipient at nothing", [(A+"session.rs", "                if self.known_level(&c.author(), recipient) >= ShareLevel::Summaries", "                if self.known_level(&c.author(), recipient) >= ShareLevel::Nothing")]),
 "N05": ("heads_seen_for: summaries recipient gets checkpoints only (> instead of >=)", [(A+"session.rs", "                if self.known_level(&c.author(), recipient) >= ShareLevel::Summaries", "                if self.known_level(&c.author(), recipient) > ShareLevel::Summaries")]),
 "N06": ("heads-seen: reporter member BY roster_v instead of AT roster_v", [(A+"equivocation.rs", "        if !hist.member_in(&self.from, at) {", "        if !hist.member_by(&self.from, at) {")]),
 "N07": ("heads-seen: entry author membership not checked", [(A+"equivocation.rs", "            if !hist.member_by(&a, at_entry) {", "            if false {")]),
 "N08": ("receive_heads_seen: RosterBehind check dropped", [(A+"session.rs", "        if !self.history.has_version(hs.roster_v) {", "        if false {")]),
 "N09": ("countersigner_ok: anchor may be AT v_join (<=)", [(A+"history.rs", "            .filter(|(_, rv)| *rv < v_join)", "            .filter(|(_, rv)| *rv <= v_join)")]),
 "N10": ("countersigner_ok: earliest pre-join checkpoint instead of latest", [(A+"history.rs", "            .map(|(s, _)| *s)\n            .max();", "            .map(|(s, _)| *s)\n            .min();")]),
 "N11": ("countersigner_ok: any pre-join checkpoint", [(A+"history.rs", "        latest_before == Some(head_seq)", "        latest_before.is_some()")]),
 "N12": ("MAX_HEADS_PER_AUTHOR off by one (>)", [(A+"received.rs", "        if self.heads.len() >= MAX_HEADS_PER_AUTHOR &&", "        if self.heads.len() > MAX_HEADS_PER_AUTHOR &&")]),
 "N13": ("StaleHead: equal sequence accepted (<)", [(A+"received.rs", "            if head.author_seq <= held &&", "            if head.author_seq < held &&")]),
 "N14": ("ensure_room: worst case counts frame headers only", [(A+"session.rs", "        let worst = n.saturating_mul(4 + MAX_RECORD_BYTES);", "        let worst = n.saturating_mul(4);")]),
 "N15": ("StoreLimits default bytes = full bundle cap", [(A+"session.rs", "            bytes: MAX_BUNDLE_BYTES / 8 * 7,", "            bytes: MAX_BUNDLE_BYTES,")]),
 "N16": ("export cap comparisons off by one", [(A+"bundle.rs", "    if (n > MAX_RECORDS || bytes.len() + seal_room > MAX_BUNDLE_BYTES)", "    if (n > MAX_RECORDS + 1 || bytes.len() + seal_room > MAX_BUNDLE_BYTES + 1)")]),
 "N17": ("summary pre-size check 64x instead of 4x", [(A+"chain.rs", "                if s.len() > 4 * MAX_SUMMARY_BYTES {", "                if s.len() > 64 * MAX_SUMMARY_BYTES {")]),
 "N18": ("crypto: AuditHeadsSeen label equal to AuditHead label", [(C+"identity.rs", '            SignDomain::AuditHeadsSeen => b"coagent-audit-heads-seen-v1",', '            SignDomain::AuditHeadsSeen => b"coagent-audit-head-v1",')]),
 "N19": ("receipts: summary to anyone entitled to the receiver's chain", [(A+"session.rs", "                    let entitled = m == x || self.known_level(&x, &m) >= ShareLevel::Summaries;", "                    let entitled = m == x || self.known_level(&x, &m) >= ShareLevel::Nothing;")]),
 "N20": ("accept_head: MAX_SEQ bound dropped", [(A+"received.rs", '        if head.author_seq > MAX_SEQ' + cfgred("head_no_max_seq") + ' {', '        if false {')]),
 "N21": ("verify: heads-seen addressed to another member accepted", [(A+"bundle.rs", "        if hs.from != exporter && hs.to.is_some_and(|t| t != exporter) {", "        if false {")]),
 "N22": ("verify: heads-seen naming a roster version not held accepted", [(A+"bundle.rs", "        if hs.roster_v > v_last || !book.has_version(hs.roster_v) {", "        if false {")]),
 "N23": ("heads_seen_for: recipient's own chain not excluded", [(A+"session.rs", "            .filter(|c| &c.author() != recipient)", "            .filter(|_c| true)")]),
 "N24": ("history.member_by: strictly before v", [(A+"history.rs", "        self.members.range(..=v).any(|(_, m)| m.contains(id))", "        self.members.range(..v).any(|(_, m)| m.contains(id))")]),
 "N25": ("crypto: AuditBundleSeal label equal to Binding label", [(C+"identity.rs", '            SignDomain::AuditBundleSeal => b"coagent-audit-bundle-seal-v1",', '            SignDomain::AuditBundleSeal => b"coagent-binding-v1",')]),
 "N26": ("A-M2 full revert to round 1: author checks CURRENT roster, verify checks head roster_v only",
   [(A+"chain.rs", "            hist.countersigner_ok(&cs.by, cs.author_seq, cs.roster_v, &heads)", "            hist.member_in(&cs.by, hist.range().1)"),
    (A+"bundle.rs", "            book.countersigner_ok(&cs.by, head.author_seq, head.roster_v, &own_head_list)", "            book.member_in(&cs.by, head.roster_v)")]),
 "N27": ("A-M2 author-side revert only (author checks CURRENT roster)",
   [(A+"chain.rs", "            hist.countersigner_ok(&cs.by, cs.author_seq, cs.roster_v, &heads)", "            hist.member_in(&cs.by, hist.range().1)")]),
}

ALL = dict(R1); ALL.update(NEW)

def run(only=None):
    results = []
    for mid in sorted(ALL):
        if only and mid not in only:
            continue
        desc, edits = ALL[mid]
        bad = None
        files = sorted({f for f, _, _ in edits})
        for f, old, new in edits:
            p = REPO + "/" + f
            src = open(p).read()
            n = src.count(old)
            if n != 1:
                bad = f"NOAPPLY ({f} matches={n})"; break
            open(p, "w").write(src.replace(old, new))
        if bad:
            subprocess.run(["git", "-C", REPO, "checkout", "--"] + files, check=True)
            results.append((mid, desc, bad, "")); print(mid, bad, flush=True); continue
        pk = ["-p", "coagent-audit"] + (["-p", "coagent-crypto"] if any(f.startswith(C) for f in files) else [])
        r = subprocess.run(["cargo", "test", "--offline", "--locked"] + pk + ["--no-fail-fast"],
                           cwd=REPO, env=ENV, capture_output=True, text=True)
        subprocess.run(["git", "-C", REPO, "checkout", "--"] + files, check=True)
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
    only = set(sys.argv[1:]) or None
    res = run(only)
    out = S + "/mutation_results_r2" + ("_partial" if only else "") + ".json"
    json.dump(res, open(out, "w"), indent=1)
    diff = subprocess.run(["git", "-C", REPO, "status", "--porcelain"], capture_output=True, text=True).stdout
    print("WORKTREE CLEAN" if not diff.strip() else "WORKTREE DIRTY:\n" + diff)
