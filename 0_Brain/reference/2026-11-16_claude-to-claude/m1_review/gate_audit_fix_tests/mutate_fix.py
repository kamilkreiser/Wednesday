#!/usr/bin/env python3
"""QA gate M3 AUDIT-FIX: plant one mutant at a time in crates/coagent-audit/src/session.rs of a scratch
copy, run the whole coagent-audit suite (--no-fail-fast; the copy also holds tests/qa_fix.rs), and
record which test binaries / tests fail. Usage: mutate_fix.py <pristine-copy> <mutant-copy> <logdir> [ids]
Environment: CARGO_HOME, RUSTUP_HOME, CARGO_TARGET_DIR, PATH set by the caller."""
import os, re, shutil, subprocess, sys, time

SRC = "crates/coagent-audit/src/session.rs"

MUTANTS = [
    ("M01", "rule (A) removed", "if !cfg!(coagent_audit_red = \"limits_strand_payer\") {", "if false {"),
    ("M02", "rule (A) bytes > -> >=", "if u.0 + CLOSING_CHECKPOINT_BYTES > alw.0", "if u.0 + CLOSING_CHECKPOINT_BYTES >= alw.0"),
    ("M03", "rule (A) records > -> >=", "|| u.1 + CLOSING_CHECKPOINT_RECORDS > alw.1", "|| u.1 + CLOSING_CHECKPOINT_RECORDS >= alw.1"),
    ("M04", "rule (A) bytes clause dropped", "if u.0 + CLOSING_CHECKPOINT_BYTES > alw.0", "if false"),
    ("M05", "rule (A) records clause dropped", "|| u.1 + CLOSING_CHECKPOINT_RECORDS > alw.1", "|| false"),
    ("M06", "owing range includes the last checkpoint's number", ".range(last.saturating_add(1)..)", ".range(last..)"),
    ("M07", "every allowance treated as owing", ".range(last.saturating_add(1)..)", ".range(0..)"),
    ("M08", "rule (A) asks the OLD limits", "let alw = new.requested_allowance();", "let alw = self.limits.requested_allowance();"),
    ("M09", "set_limits bypasses the rule", "let _ = self.try_set_limits(limits);",
     "let d = StoreLimits::default(); self.limits = StoreLimits { bytes: limits.bytes.min(d.bytes), records: limits.records.min(d.records) };"),
    ("M10", "hold-back one byte short", "if u.0 + CLOSING_CHECKPOINT_BYTES > alw.0", "if u.0 + CLOSING_CHECKPOINT_BYTES - 1 > alw.0"),
    ("M11", "store before check (no delete)", "        // 1. check: the roster crate's own answer",
     "        self.write(rkey, r)?;\n        // 1. check: the roster crate's own answer"),
    ("M12", "old chain not brought level after the swap",
     "        self.roster_check = match check.apply(next) {\n            Ok(Applied::Advanced { .. }) => Some(check),\n            _ => None,\n        };",
     "        self.roster_check = Some(check);"),
    ("M13", "rebuild skips a held version", "        for v in rest {\n            c.apply(v)?;", "        for v in rest.iter().skip(1) {\n            c.apply(v)?;"),
    ("M14", "accepted version not recorded among the held versions", "        self.roster_versions.push(next.clone());\n", ""),
    ("M15", "lifetime backstops removed (retired M11 rows)",
     "if (next.body.version > MAX_ROSTER_VERSIONS as u64 || keys.len() > MAX_KEYS_EVER)",
     "if false && (next.body.version > MAX_ROSTER_VERSIONS as u64 || keys.len() > MAX_KEYS_EVER)"),
    ("M16", "roster refusal mapped to LogFull", "            e => Err(e.into()),", "            _ => Err(AuditError::LogFull),"),
    ("M17", "failed write keeps the one-ahead check chain", "        self.write(rkey, r)?;\n        // 3. apply",
     "        if let Err(x) = self.write(rkey, r) {\n            self.roster_check = Some(check);\n            return Err(x);\n        }\n        // 3. apply"),
    ("M18", "refused path drops the check chain (rebuild next time)",
     "            Err(e) => {\n                self.roster_check = Some(check);\n                return self.roster_refused(next, e);",
     "            Err(e) => {\n                return self.roster_refused(next, e);"),
    ("M19", "held current number also routed through the check chain",
     "        if next.body.version > cur\n            && !store_first", "        if next.body.version >= cur\n            && !store_first"),
    ("M20", "write failure leaves member advanced (apply before write in apply_newer)",
     "        // 2. store: the one store call for an accepted version\n        self.write(rkey, r)?;\n        // 3. apply: the checked chain becomes this member's; the old one is brought level and kept\n        // as the next check chain\n        std::mem::swap(&mut self.roster, &mut check);",
     "        std::mem::swap(&mut self.roster, &mut check);\n        self.write(rkey, r)?;"),
]


def main():
    pristine, mut, logdir = sys.argv[1], sys.argv[2], sys.argv[3]
    only = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else None
    os.makedirs(logdir, exist_ok=True)
    base = open(os.path.join(pristine, SRC)).read()
    summary = open(os.path.join(logdir, "summary.txt"), "a")
    for mid, what, old, new in MUTANTS:
        if only and mid not in only:
            continue
        n = base.count(old)
        if n != 1:
            summary.write(f"{mid}\tNOT APPLIED (pattern found {n} times)\t{what}\n")
            summary.flush()
            continue
        open(os.path.join(mut, SRC), "w").write(base.replace(old, new))
        t0 = time.time()
        p = subprocess.run(
            ["cargo", "test", "--locked", "--offline", "--manifest-path", os.path.join(mut, "Cargo.toml"),
             "-p", "coagent-audit", "--no-fail-fast"],
            capture_output=True, text=True)
        out = p.stdout + p.stderr
        open(os.path.join(logdir, f"{mid}.log"), "w").write(out)
        failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", out, re.M)))
        built = "error[E" not in out and "could not compile" not in out
        qa = [f for f in failed if f.startswith("qa_")]
        branch = [f for f in failed if not f.startswith("qa_")]
        res = "BUILD FAILED" if not built else ("KILLED" if failed else "SURVIVED")
        summary.write(f"{mid}\t{res}\tbranch {len(branch)} qa {len(qa)}\t{int(time.time()-t0)}s\t{what}\n"
                      f"\tbranch: {branch}\n\tqa: {qa}\n")
        summary.flush()
    open(os.path.join(mut, SRC), "w").write(base)


if __name__ == "__main__":
    main()
