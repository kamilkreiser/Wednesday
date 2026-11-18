#!/usr/bin/env python3
"""QA gate r5: re-plant the r4 check's twelve surviving mutants (plus M12) with mutate4.py's own
replacement text, one at a time in the clone MUT_CLONE, run the test the builder names as the
killer, and restore the file byte for byte. Results: one line per mutant in results.tsv.
"""
import os, subprocess, sys, time, re, shutil

G = "/private/tmp/claude-501/gd5/m"
OUT = "/private/tmp/claude-501/gd5/mut"
TGT = "/private/tmp/claude-501/gd5/target_m"
REC = "crates/coagent-daemon/src/recovery.rs"
ENG = "crates/coagent-daemon/src/engine.rs"
RM = "recovery_model"
RR = "recovery_repro"

# id, file, old (mutate4.py's text unless marked), new, killer (target, test)
M = [
 ("M01", REC, "now.duration_since(*at) > self.cfg.rto)", "now.duration_since(*at) > self.cfg.rto * 2)", (RM, "r4_7_m01_t_rto_fires_at_15_s")),
 ("M03", REC, ".map(|t| now.duration_since(t) > self.cfg.held)", ".map(|t| now.duration_since(t) > self.cfg.held * 2)", (RM, "r4_7_m03_t_held_fires_at_30_s")),
 ("M04", REC, "self.blind_wait = (self.blind_wait * 2).min(self.cfg.blind_max);", "self.blind_wait = (self.blind_wait * 4).min(self.cfg.blind_max * 4);", (RM, "r4_7_m04_t_blind_waits_15_30_60_60")),
 ("M06", REC, "while self.tokens < self.cfg.bucket_size", "while self.tokens <= self.cfg.bucket_size", (RM, "r4_7_m06_the_bucket_holds_5")),
 ("M09", REC, "self.desync_out = missing > self.cfg.max_skips;", "self.desync_out = missing >= self.cfg.max_skips;", (RM, "r4_7_m09_256_missing_fit_one_round_of_skips_257_do_not")),
 ("M11", REC, "} else if n >= self.cfg.kk1_per_sec {", "} else if n > self.cfg.kk1_per_sec {", (RM, "r4_7_m11_m25_at_most_8_messages_1_examined_per_second")),
 # M12: the r4 text no longer occurs (the red control `no_clamp` was added to the same line); the
 # same change (the clamp never applies) on the line as it now stands.
 ("M12", REC, "        if n > top && !cfg!(coagent_red = \"no_clamp\") {", "        if false && n > top && !cfg!(coagent_red = \"no_clamp\") {", (RM, "row33_a_hostile_position_of_2_62_is_clamped_and_later_messages_flow")),
 ("M16", REC, "            self.unacked_since = None;\n            self.held_since = Some(now);", "            self.unacked_since = None;\n            self.held_since.get_or_insert(now);", (RM, "r4_7_m16_a_later_proven_full_rearms_t_held")),
 ("M17", ENG, "    rec.recv_upto = d.recv_floor;\n", "", (RR, "m17_the_receive_floor_is_in_session_json_and_holds_after_a_damaged_inbox")),
 ("M19", REC, "        let to = self.cfg.kk_timeout;", "        let to = self.cfg.kk_timeout * 2;", (RM, "r4_7_m19_the_key_exchange_clock_fires_at_5_s")),
 ("M20", REC, "            && self.pos.is_none()\n            && !self.ob.items.is_empty()", "            && false\n            && self.pos.is_none()\n            && !self.ob.items.is_empty()", (RM, "r4_7_m20_no_position_5_s_after_promotion_resyncs")),
 ("M23", REC, "            self.backoff = self.cfg.backoff_min;\n            self.keying_wait = self.cfg.keying;", "            self.keying_wait = self.cfg.keying;", (RM, "r4_7_m23_live_resets_the_backoff")),
 ("M25", REC, "            .map(|t| now.duration_since(t) >= Duration::from_secs(1))\n            .unwrap_or(true)\n        {\n            self.kk1_window = (Some(now), 0);", "            .map(|t| now.duration_since(t) >= Duration::from_secs(1))\n            .unwrap_or(true)\n        {\n            self.kk1_window = (None, 0);", (RM, "r4_7_m11_m25_at_most_8_messages_1_examined_per_second")),
]


def sh(cmd, log, timeout=None):
    with open(log, "a") as f:
        f.write(f"\n$ {cmd}\n"); f.flush()
        t0 = time.time()
        try:
            r = subprocess.run(["bash", "-c", f". /private/tmp/claude-501/gd5/env.sh; export CARGO_TARGET_DIR={TGT}; cd {G} && {cmd}"],
                               stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
            rc = r.returncode
        except subprocess.TimeoutExpired:
            rc = 124
        f.write(f"\n# rc={rc} {time.time()-t0:.0f}s\n")
    return rc


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
    res = open(f"{OUT}/results.tsv", "a")
    for (mid, path, old, new, (tgt, test)) in M:
        if only and mid not in only:
            continue
        p = os.path.join(G, path)
        src = open(p).read()
        n = src.count(old)
        log = f"{OUT}/{mid}.log"
        open(log, "w").close()
        if n != 1:
            res.write(f"{mid}\tNOT-APPLIED (text occurs {n} times)\t\t\n"); res.flush()
            continue
        open(p, "w").write(src.replace(old, new, 1))
        try:
            rc = sh(f"cargo build --locked --workspace --bins && cargo test --locked -p coagent-daemon --test {tgt} {test} -- --exact --nocapture", log, timeout=1800)
        finally:
            open(p, "w").write(src)
        txt = open(log).read()
        fails = re.findall(r"^test (\S+) \.\.\. FAILED$", txt, re.M)
        oks = re.findall(r"^test (\S+) \.\.\. ok$", txt, re.M)
        msg = ""
        mm = re.search(r"panicked at [^\n]*\n([^\n]*)", txt)
        if mm:
            msg = mm.group(1)[:300]
        verdict = "KILLED" if fails else ("SURVIVED" if oks else f"NO-RESULT rc={rc}")
        res.write(f"{mid}\t{verdict}\t{tgt}::{test}\t{msg}\n"); res.flush()
    rc = subprocess.run(["git", "-C", G, "status", "--porcelain"], capture_output=True, text=True).stdout
    res.write(f"# tree after: {'clean' if not rc.strip() else rc}\n")


if __name__ == "__main__":
    main()
