#!/usr/bin/env python3
"""QA gate r4 mutation driver (M1 DAEMON). One mutant at a time in the clone `g`, restored with
`git checkout` after each. For each mutant: build, then the model/measure tests (tier A) and the
named process tests (tier B). A mutant no test of tier A or B kills is re-run against the whole
daemon suite (tier C) when --full is given. Results: one line per mutant in results.tsv.
Usage: mutate4.py [--only M01,M02] [--full]
"""
import os, subprocess, sys, time, re

G = os.environ.get("MUT_CLONE", "/private/tmp/claude-501/gd4/g")
OUT = "/private/tmp/claude-501/gd4/mut"
TGT = os.environ.get("MUT_TARGET", "/private/tmp/claude-501/gd4/target_g")
REC = "crates/coagent-daemon/src/recovery.rs"
ENG = "crates/coagent-daemon/src/engine.rs"

# id, file, old, new, what, tier-B process tests (target::name)
M = [
 ("M01", REC, "now.duration_since(*at) > self.cfg.rto)", "now.duration_since(*at) > self.cfg.rto * 2)", "T-RTO doubled", ["reconnect::test5c_a_gap_is_counted_and_the_senders_retransmit_clock_heals_it", "recovery_repro::measure_real_one_lost_packet_in_a_healthy_session"]),
 ("M02", REC, "now.duration_since(*at) > self.cfg.rto)", "now.duration_since(*at) > Duration::ZERO)", "T-RTO zeroed", ["reconnect::test5a_cut_connection_redelivers_exactly_once_in_order"]),
 ("M03", REC, ".map(|t| now.duration_since(t) > self.cfg.held)", ".map(|t| now.duration_since(t) > self.cfg.held * 2)", "T-HELD doubled", ["recovery_repro::fb_a_lost_room_message_does_not_hold_the_sender_for_ever"]),
 ("M04", REC, "self.blind_wait = (self.blind_wait * 2).min(self.cfg.blind_max);", "self.blind_wait = (self.blind_wait * 4).min(self.cfg.blind_max * 4);", "T-BLIND backoff doubled (x4, cap x4)", ["recovery_repro::fc_a_suppressed_peer_joined_does_not_leave_the_pair_without_a_key_exchange"]),
 ("M05", REC, "if now.duration_since(since) >= self.keying_wait", "if now.duration_since(since) >= Duration::ZERO", "T-KEYING zeroed", ["acceptance::test1_request_and_reply_through_the_relay_and_mcp", "recovery_repro::measure_real_a_healthy_looking_stale_channel"]),
 ("M06", REC, "while self.tokens < self.cfg.bucket_size", "while self.tokens <= self.cfg.bucket_size", "bucket size off by one (6 tokens)", ["recovery_repro::fg_a_relay_that_cuts_after_every_attach_gets_few_attachments"]),
 ("M07", REC, "&& now.duration_since(self.tokens_at) >= self.cfg.bucket_refill", "&& now.duration_since(self.tokens_at) >= self.cfg.bucket_refill / 2", "bucket refill halved (twice the tokens)", ["recovery_repro::fg_a_relay_that_cuts_after_every_attach_gets_few_attachments"]),
 ("M08", REC, "&& (self.in_flight.len() >= self.cfg.inflight_frames", "&& (self.in_flight.len() > self.cfg.inflight_frames", "in-flight frames off by one (129)", []),
 ("M09", REC, "self.desync_out = missing > self.cfg.max_skips;", "self.desync_out = missing >= self.cfg.max_skips;", "skip bound off by one (255)", ["recovery_repro::fd_a_damaged_outbox_does_not_leave_a_gap_for_ever"]),
 ("M10", REC, "if self.link_room <= LINK_MARGIN &&", "if self.link_room < LINK_MARGIN &&", "link margin off by one", ["recovery_repro::ff_a_stalled_link_queue_loses_no_frame_the_daemon_sealed"]),
 ("M11", REC, "} else if n >= self.cfg.kk1_per_sec {", "} else if n > self.cfg.kk1_per_sec {", "KK1 examined per second off by one (9)", ["delta::r2_2_a_relay_replaying_everything_cannot_stop_an_honest_exchange"]),
 ("M12", REC, "        if n > top {\n            self.n.clamped", "        if false && n > top {\n            self.n.clamped", "clamp of a proven ack/position removed (R8 row 33)", ["hardening::m17_an_application_sequence_gap_is_refused_and_shown_as_desync"]),
 ("M13", REC, "        self.held_since = None;\n        self.pos = None;\n        self.in_flight.clear();\n        if self.live.take().is_some() {", "        self.held_since = None;\n        self.in_flight.clear();\n        if self.live.take().is_some() {", "drop_link keeps the old channel's position (R4 POSITION per channel)", ["recovery_repro::fj_a_new_channel_sends_only_what_the_peer_lacks", "reconnect::test5a_cut_connection_redelivers_exactly_once_in_order"]),
 ("M14", REC, "        } else {\n            self.flush_due = true;\n        }", "        } else {\n        }", "no FLUSH when data arrives (only the 5 s idle one)", ["recovery_repro::ff_a_stalled_link_queue_loses_no_frame_the_daemon_sealed"]),
 ("M15", REC, ".map(|t| now.duration_since(t) >= self.cfg.flush_idle)", ".map(|t| now.duration_since(t) >= self.cfg.flush_idle * 2)", "idle FLUSH doubled", ["recovery_repro::measure_real_the_cost_of_the_idle_flush"]),
 ("M16", REC, "            self.unacked_since = None;\n            self.held_since = Some(now);", "            self.unacked_since = None;\n            self.held_since.get_or_insert(now);", "T-HELD not re-armed by later proven `full` (A4-Q6)", ["recovery_repro::fb_a_lost_room_message_does_not_hold_the_sender_for_ever"]),
 ("M17", ENG, "    rec.recv_upto = d.recv_floor;\n", "", "persisted field not written: recv floor (sync_rec)", ["restart::test6_identity_contact_attempts_and_hard_stops_survive_a_restart", "gate_r2::gr2::r2_g2_damaged_bulk_files_quarantined_damaged_session_fails_closed", "recovery_repro::d2_a_damaged_inbox_files_loss_is_told_to_the_assistant_once"]),
 ("M18", ENG, "        relay_send_seq: rec.relay_send_seq,\n", "        relay_send_seq: 1,\n", "persisted field not read back: relay send ceiling (durable_of)", ["reconnect::test5b_relay_restart_redelivers_exactly_once_in_order", "recovery_repro::r3_sigkill_between_the_save_and_the_send_delivers_once", "gate_r3::gr3::r3_sigkill_joiner_repeatedly_during_traffic"]),
 ("M19", REC, "        let to = self.cfg.kk_timeout;", "        let to = self.cfg.kk_timeout * 2;", "key-exchange clock doubled", ["delta::r2_2_one_dropped_frame_at_any_position_does_not_stall_the_session"]),
 ("M20", REC, "            && self.pos.is_none()\n            && !self.ob.items.is_empty()", "            && false\n            && self.pos.is_none()\n            && !self.ob.items.is_empty()", "row 27 'no position 5 s after promotion' removed", []),
 ("M21", REC, "            ob.send_next = ob.send_next.max(d.send_floor);", "", "restore drops the send floor only (half of restore_drops_floor)", ["recovery_repro::fd_a_damaged_outbox_does_not_leave_a_gap_for_ever"]),
 ("M22", REC, "                self.d.kk1_seen.remove(0);\n            }\n            out.push(Action::Dirty);", "                self.d.kk1_seen.remove(0);\n            }", "KK1 digest not marked for writing (R1 exception lazily persisted)", ["delta::r2_2_a_relay_replaying_everything_cannot_stop_an_honest_exchange"]),
 ("M23", REC, "            self.backoff = self.cfg.backoff_min;\n            self.keying_wait = self.cfg.keying;", "            self.keying_wait = self.cfg.keying;", "backoff never reset on LIVE", ["recovery_repro::measure_real_a_link_in_maximum_backoff"]),
 ("M24", REC, "        if m.seq <= self.ib.recv_upto && !cfg!(coagent_red = \"dup_accept\") {", "        if m.seq < self.ib.recv_upto && !cfg!(coagent_red = \"dup_accept\") {", "duplicate check off by one (accept seq == last received)", ["reconnect::test5a_cut_connection_redelivers_exactly_once_in_order"]),
 ("M25", REC, "            .map(|t| now.duration_since(t) >= Duration::from_secs(1))\n            .unwrap_or(true)\n        {\n            self.kk1_window = (Some(now), 0);", "            .map(|t| now.duration_since(t) >= Duration::from_secs(1))\n            .unwrap_or(true)\n        {\n            self.kk1_window = (None, 0);", "KK1 rate window never starts (no rate limit)", ["delta::n03_pending_exchanges_are_bounded_and_the_newest_survives"]),
 ("M26", REC, "            bucket_refill: Duration::from_secs(12),", "            bucket_refill: Duration::from_secs(6),", "bucket refill really halved (default 12 s -> 6 s)", ["recovery_repro::fg_a_relay_that_cuts_after_every_attach_gets_few_attachments"]),
]

SLOW ={"M02", "M08", "M10", "M14", "M06", "M09"}

def sh(cmd, log, timeout=None):
    with open(log, "a") as f:
        f.write(f"\n$ {cmd}\n"); f.flush()
        t0 = time.time()
        try:
            r = subprocess.run(["bash", "-c", f". {OUT}/../env.sh; export CARGO_TARGET_DIR={TGT}; cd {G} && {cmd}"],
                               stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
            rc = r.returncode
        except subprocess.TimeoutExpired:
            rc = 124
        f.write(f"\n# rc={rc} {time.time()-t0:.0f}s\n")
    return rc

def failed_tests(log, start):
    with open(log) as f:
        f.seek(start)
        txt = f.read()
    return sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED$", txt, re.M))), txt

def main():
    only = None; full = "--full" in sys.argv
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    res = open(os.environ.get("MUT_RESULTS", f"{OUT}/results.tsv"), "a")
    for (mid, path, old, new, what, procs) in M:
        if only and mid not in only:
            continue
        p = os.path.join(G, path)
        src = open(p).read()
        n = src.count(old)
        log = f"{OUT}/{mid}.log"
        open(log, "w").close()
        if n != 1:
            res.write(f"{mid}\tNOT APPLIED (old string occurs {n} times)\t{what}\n"); res.flush(); continue
        open(p, "w").write(src.replace(old, new))
        try:
            if sh("cargo build --workspace --bins --locked -q", log) != 0:
                res.write(f"{mid}\tDOES NOT COMPILE\t{what}\n"); res.flush(); continue
            pos = os.path.getsize(log)
            # Tier A: the model's properties except its two slowest (8-9 min together), which run only
            # for the mutants whose rule they guard (V12 quiet / V14 bounds).
            skip = "" if mid in SLOW else " -- --skip v12_honest_runs_are_quiet --skip v14_everything_bounded"
            sh("cargo test --locked -p coagent-daemon --no-fail-fast --test recovery_model --test recovery_measure" + skip, log, 2400)
            killers, _ = failed_tests(log, pos)
            for t in procs:
                tgt, name = t.split("::", 1)
                pos2 = os.path.getsize(log)
                sh(f"cargo test --locked -p coagent-daemon --test {tgt} -- --exact {name}", log, 900)
                k2, _ = failed_tests(log, pos2)
                killers += [f"{tgt}::{x}" for x in k2]
            tier = "A/B"
            if not killers and full:
                pos3 = os.path.getsize(log)
                sh("cargo test --locked -p coagent-daemon -p coagent-mcp --no-fail-fast", log, 3600)
                k3, _ = failed_tests(log, pos3)
                killers += k3; tier = "A/B/C(full suite)"
            verdict = "KILLED" if killers else "SURVIVED"
            res.write(f"{mid}\t{verdict}\t{what}\t{tier}\t{';'.join(killers)}\n"); res.flush()
        finally:
            subprocess.run(["git", "-C", G, "checkout", "--", path])
    res.close()

if __name__ == "__main__":
    main()
