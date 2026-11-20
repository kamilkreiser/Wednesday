#!/usr/bin/env python3
"""QA-AUDIT-HOST: mutations of my own in coagent-audit-host. Each mutation is (id, file, old, new,
what). For each: apply to the `mut` worktree, run the crate's tests (debug) except the two long ones
(`stop_anywhere`, `property`), record failing tests; restore with `git checkout`. With --long, a
survivor is also run against the two long tests. Usage: mutate.py [--long] [ids...]"""
import os, subprocess, sys, re, time

W = "/private/tmp/claude-501/qah"
MUT = f"{W}/mut"
CR = "crates/coagent-audit-host"
ENV = dict(os.environ, COAGENT_TOOLS=f"{W}/tools", CARGO_TARGET_DIR=f"{W}/target-mut")
for k in ("COAGENT_AUDIT_RED", "COAGENT_RED", "COAGENT_RED_ROSTER", "COAGENT_AUDIT_HOST_RED"):
    ENV.pop(k, None)
TC = f"{W}/tools/cargo/bin"
ENV["RUSTUP_HOME"] = f"{W}/tools/rustup"
ENV["CARGO_HOME"] = f"{W}/tools/cargo"
ENV["PATH"] = TC + ":" + ENV["PATH"]

MUTS = [
    ("M1", f"{CR}/src/fsio.rs",
     "            if durable {\n                self.sync_for(name).map_err(WriteError::After)?;\n            }\n            Ok(())",
     "            Ok(())",
     "skip the directory sync after a put's rename/link"),
    ("M2", f"{CR}/src/fsio.rs",
     "cfg!(coagent_audit_host_red = \"open_ignores_file_rights\") || mode & 0o077 == 0",
     "cfg!(coagent_audit_host_red = \"open_ignores_file_rights\") || mode & 0o033 == 0",
     "accept group/other READ rights (a 0644 file, a 0755 directory)"),
    ("M3", f"{CR}/src/host.rs",
     "        (Some(Ok(())), _) => Some((pending.unwrap_or_else(|| unreachable!()), Opened::Pending)),\n        (_, Some(Ok(()))) => Some((current.unwrap_or_else(|| unreachable!()), Opened::Current)),",
     "        (_, Some(Ok(()))) => Some((current.unwrap_or_else(|| unreachable!()), Opened::Current)),\n        (Some(Ok(())), _) => Some((pending.unwrap_or_else(|| unreachable!()), Opened::Pending)),",
     "check CURRENT before pending at open (order of design 10 §2.8 swapped)"),
    ("M4", f"{CR}/src/host.rs",
     "        if self.window.is_some() && !cfg!(coagent_audit_host_red = \"seal_interleaved\") {",
     "        if self.window.is_some() && !self.queue.is_empty() && !cfg!(coagent_audit_host_red = \"seal_interleaved\") {",
     "let the FIRST call of a window through to the member"),
    ("M5", f"{CR}/src/dir.rs",
     "            let Some((sid, key)) = parse_name(&e.name) else {\n                return Err(DirError::UnknownFile(rel));\n            };",
     "            let Some((sid, key)) = parse_name(&e.name) else {\n                continue;\n            };",
     "ignore (instead of refusing) an unknown file in the store"),
    ("M6", f"{CR}/src/dir.rs",
     "        if leftovers > MAX_LEFTOVER_TEMPS {\n            return Err(DirError::TooManyLeftovers(leftovers));\n        }",
     "",
     "drop the 64-leftover bound in the store"),
    ("M7", f"{CR}/src/host.rs",
     "        self.write_archive(\"rel\", segment, &bytes)?;\n        write_anchor(&self.anchors, PENDING, &post)?;",
     "        self.write_archive(\"rel\", segment, &bytes)?;",
     "release: do not save the post-release anchor as pending before deleting"),
    ("M8", f"{CR}/src/host.rs",
     "            Err(e) if m.store().is_poisoned() => {",
     "            Err(e) if m.store().is_poisoned() && false => {",
     "P-4 in the host: a poisoned store is NOT re-opened (the error returned as is)"),
    ("M9", f"{CR}/src/host.rs",
     "    fn ensure_anchor(&mut self) -> Result<(), HostError> {\n        if self.anchor_dirty {\n            self.save_current()?;\n        }\n        Ok(())",
     "    fn ensure_anchor(&mut self) -> Result<(), HostError> {\n        if self.anchor_dirty {\n            let _ = self.save_current();\n        }\n        Ok(())",
     "DQ-H4: a failed anchor save never refuses the next change"),
    ("M10", f"{CR}/src/host.rs",
     "                    if self.save_current().is_ok() {\n                        let _ = self.anchors.remove(PENDING);\n                    }",
     "                    let _ = self.anchors.remove(PENDING);\n                    let _ = self.save_current();",
     "seal step 4: drop pending BEFORE current is saved (and whatever the save does)"),
    ("M11", f"{CR}/src/fsio.rs",
     "            if let Err(e) = ck(fault::Op::Write).and_then(|_| f.write_all(data)) {",
     "            if let Err(e) = ck(fault::Op::Write).and_then(|_| f.write_all(&data[..data.len().saturating_sub(usize::from(data.len() > 100))])) {",
     "a torn write: the last byte of a file over 100 bytes not written"),
    ("M12", f"{CR}/src/dir.rs",
     "    matches!(\n        part,\n        Part::Fixed(Table::Segment) | Part::Fixed(Table::Anchor)\n    ) || (files <= MAX_FILES_PER_SESSION && bytes <= MAX_RECORD_BYTES_PER_SESSION)",
     "    let _ = (part, files, bytes);\n    true",
     "drop the store's per-session bounds"),
    ("M13", f"{CR}/src/host.rs",
     "        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),",
     "        Err(_) => return Ok(None),",
     "an anchor file that cannot be read is treated as absent"),
    ("M14", f"{CR}/src/host.rs",
     "                Causer::Member(k) => m.record_for(id, k, e, now)?,",
     "                Causer::Member(k) => match m.record_for(id, k, e.clone(), now) { Ok(n) => n, Err(_) => m.record(id, e, now)? },",
     "P-6: a refused record_for retried as a local record"),
]


def run(cmd, log):
    with open(log, "w") as f:
        return subprocess.call(cmd, cwd=MUT, env=ENV, stdout=f, stderr=subprocess.STDOUT)


def failing(log):
    return sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", open(log).read(), re.M)))


def main():
    args = sys.argv[1:]
    long = "--long" in args
    ids = [a for a in args if not a.startswith("--")]
    os.makedirs(f"{W}/logs/mut", exist_ok=True)
    for mid, path, old, new, what in MUTS:
        if ids and mid not in ids:
            continue
        full = f"{MUT}/{path}"
        src = open(full).read()
        if src.count(old) != 1:
            print(f"{mid} NOT APPLIED (pattern count {src.count(old)}): {what}", flush=True)
            continue
        open(full, "w").write(src.replace(old, new))
        t0 = time.time()
        log = f"{W}/logs/mut/{mid}.log"
        rc = run(["cargo", "test", "--locked", "-p", "coagent-audit-host", "--", "--skip", "stop_anywhere", "--skip", "property"], log)
        fl = failing(log)
        compiled = "error[E" not in open(log).read() and "could not compile" not in open(log).read()
        verdict = "KILLED" if fl else ("NO-COMPILE" if not compiled else ("SURVIVED" if rc == 0 else f"rc={rc}"))
        extra = ""
        if long and verdict == "SURVIVED":
            log2 = f"{W}/logs/mut/{mid}.long.log"
            rc2 = run(["cargo", "test", "--locked", "-p", "coagent-audit-host", "--lib", "--", "stop_anywhere", "property"], log2)
            fl2 = failing(log2)
            if fl2:
                verdict = "KILLED (long)"
                fl = fl2
            extra = f" long rc={rc2}"
        subprocess.call(["git", "checkout", "--", path], cwd=MUT)
        print(f"{mid} {verdict} ({time.time()-t0:.0f}s{extra}): {what} :: {', '.join(fl[:6])}", flush=True)


main()
