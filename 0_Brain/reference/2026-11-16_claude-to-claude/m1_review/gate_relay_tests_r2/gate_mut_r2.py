#!/usr/bin/env python3
"""Gate round-2 mutation runner. One mutation at a time in the `mut` clone, full
coagent-relay + coagent-ipc + coagent-cli suite, record CAUGHT/SURVIVED and the failing tests,
restore the file, and verify the tree is clean at the end (git diff --quiet)."""
import os, subprocess, sys, re

G = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_relay_r2"
REPO = G + "/mut"
R = "crates/coagent-relay/src/"
I = "crates/coagent-ipc/src/"

M = [
 ("X01", "eviction may pick LIVE channels (pending filter removed)", R+"state.rs",
  ".filter(|(_, c)| !c.registered)\n            .max_by_key", ".filter(|_| true)\n            .max_by_key"),
 ("X02", "eviction ignores the owner's channel count (oldest pending overall)", R+"state.rs",
  "per_owner.get(&c.owner).copied().unwrap_or(0),", "0usize,"),
 ("X03", "eviction picks the NEWEST pending channel of the top owner", R+"state.rs",
  "std::cmp::Reverse(c.created),", "c.created,"),
 ("X04", "pending TTL effectively disabled (x1000)", R+"state.rs",
  "clk.now.saturating_duration_since(ch.created) > pending_ttl", "clk.now.saturating_duration_since(ch.created) > pending_ttl * 1000"),
 ("X05", "live cap off by one (>= -> >)", R+"state.rs",
  ".count()\n                >= self.limits.max_channels_per_ip", ".count()\n                > self.limits.max_channels_per_ip"),
 ("X06", "a channel never becomes live (registered flag never set)", R+"state.rs",
  "ch.registered |= registers;", "ch.registered |= false;"),
 ("X07", "fairness comparison loosened (evict while big > mine)", R+"state.rs",
  "if big_bytes <= mine + need {", "if big_bytes <= mine {"),
 ("X08", "make_room evicts from the SMALLEST other channel", R+"state.rs",
  ".filter(|(i, _)| *i != requester)\n                .max_by_key(|(_, c)| c.bytes)", ".filter(|(i, _)| *i != requester)\n                .min_by_key(|(_, c)| c.bytes)"),
 ("X09", "last_seq allows an equal pair_seq (<= -> <)", R+"state.rs",
  ".is_some_and(|last| pair_seq <= *last)", ".is_some_and(|last| pair_seq < *last)"),
 ("X10", "last_seq not reset when a slot is retired", R+"state.rs",
  "ch.last_seq.retain(|(a, b), _| *a != slot && *b != slot);", ""),
 ("X11", "last_seq never recorded (check never fires)", R+"state.rs",
  "ch.last_seq.insert((from_slot, to_slot), pair_seq);", ""),
 ("X12", "FragTracker: control frames change in_frag (opcode <= 2 -> <= 10)", R+"meter.rs",
  "if opcode <= 2 {", "if opcode <= 10 {"),
 ("X13", "FragTracker: continuation frames ignored (only opcodes 1/2 count)", R+"meter.rs",
  "if opcode <= 2 {", "if opcode == 1 || opcode == 2 {"),
 ("X14", "FragTracker: 16-bit extended length mis-sized (2 -> 4 bytes)", R+"meter.rs",
  "126 => 2,\n        127 => 8,", "126 => 4,\n        127 => 8,"),
 ("X15", "FragTracker: mask key not counted in header length", R+"meter.rs",
  "2 + ext + if second & 0x80 != 0 { 4 } else { 0 }", "2 + ext"),
 ("X16", "lock: inode re-verification after locking skipped", I+"unix.rs",
  "Ok(md)\n                if md.file_type().is_file() && (md.dev(), md.ino()) == (mine.dev(), mine.ino()) =>",
  "_ if true =>"),
 ("X17", "lock: Drop unlinks the lock path without the inode check", I+"unix.rs",
  "if md.file_type().is_file() && (md.dev(), md.ino()) == self.lock_identity {", "if md.file_type().is_file() || true {"),
 ("X18", "holder check: any attached connection counts as the holder", R+"state.rs",
  ".map(|c| c.id)\n            == Some(conn_id)", ".map(|c| c.id)\n            .is_some()"),
 ("X19", "per-address mailbox cap off by one (>= -> >)", R+"state.rs",
  ">= self.limits.max_mailboxes_per_ip", "> self.limits.max_mailboxes_per_ip"),
 ("X20", "lock file owner check removed", I+"unix.rs",
  "check_owner(&lp, md.uid(), our_uid)?;", ""),
]

env = dict(os.environ)
env["CARGO_TARGET_DIR"] = G + "/target_mut"
env["CARGO_NET_OFFLINE"] = "true"

only = sys.argv[1:]
log = open(G + "/gate_mut_r2.log", "a")
for mid, what, f, old, new in M:
    if only and mid not in only:
        continue
    p = os.path.join(REPO, f)
    src = open(p).read()
    n = src.count(old)
    if n != 1:
        print(f"{mid} ANCHOR {n} times: PROBLEM", flush=True); log.write(f"{mid} ANCHOR {n}\n"); continue
    open(p, "w").write(src.replace(old, new))
    try:
        r = subprocess.run(["cargo", "test", "--locked", "--offline", "--manifest-path", REPO + "/Cargo.toml",
                            "-p", "coagent-relay", "-p", "coagent-ipc", "-p", "coagent-cli", "--no-fail-fast"],
                           env=env, capture_output=True, text=True, timeout=1500)
        out = r.stdout + r.stderr
        failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED$", out, re.M)))
        compile_err = "error[E" in out or "could not compile" in out
        if r.returncode == 0:
            verdict = "SURVIVED"
        elif compile_err:
            verdict = "COMPILE-ERROR"
        else:
            verdict = "CAUGHT"
        line = f"{mid} {verdict} | {what} | failed: {', '.join(failed) if failed else '-'}"
    except subprocess.TimeoutExpired:
        line = f"{mid} TIMEOUT(counted CAUGHT? no: inspect) | {what}"
    finally:
        open(p, "w").write(src)
    print(line, flush=True); log.write(line + "\n"); log.flush()
clean = subprocess.run(["git", "-C", REPO, "diff", "--quiet"]).returncode == 0
print("tree restored clean:", clean); log.write(f"tree restored clean: {clean}\n")
