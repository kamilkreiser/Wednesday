#!/usr/bin/env python3
"""Gate round-3 mutation runner (M1 DAEMON @ d8b5b4b). One mutation at a time over coagent-daemon /
coagent-mcp; the builder's suite of both crates (gate_r2 / gate_return included; the gate's own gr3
excluded). A targeted filter runs first when one is given; a mutant it does not catch then gets the
FULL suite before it is called a survivor. Every file is restored after each run.
Usage: mutate3.py --repo R --env E --out O [--dry] [names...]"""
import os, subprocess, sys, time, json

args = sys.argv[1:]
dry = "--dry" in args
def opt(k, d):
    if k in args:
        i = args.index(k); v = args[i + 1]; del args[i:i + 2]; return v
    return d
R = opt("--repo", None)
ENV = opt("--env", None)
OUT = opt("--out", None)
args = [a for a in args if a != "--dry"]
D = R + "/crates/coagent-daemon/src/"
M = R + "/crates/coagent-mcp/src/main.rs"
E = D + "engine.rs"
L = D + "limits.rs"
ST = D + "store.rs"
DD = D + "datadir.rs"
RC = D + "relay_child.rs"
REL = D + "release.rs"

def P(*ps): return list(ps)
# (name, patches, quick filter or None)
MUTS = [
 # ---- round 1 (m), re-anchored on d8b5b4b ----
 ("m01_escape_lt_gt_plain", P((M, "!matches!(c, '\"' | '\\\\' | '<' | '>' | '&')", "!matches!(c, '\"' | '\\\\' | '&')")), "escaping test7 containment m05"),
 ("m02_escape_controls_plain", P((M, "let plain = (' '..='~').contains(&c) &&", "let plain = (c < '\\u{7f}' && c != '\\n') &&")), "escaping test7 containment"),
 ("m03_escape_nonascii_plain", P((M, "let plain = (' '..='~').contains(&c) &&", "let plain = (c >= ' ' && c != '\\u{7f}') &&")), "escaping test7 containment"),
 ("m04_escape_amp_plain", P((M, "'>' | '&');", "'>');")), "escaping test7"),
 ("m05_audience_unescaped", P((M, "                } else {\n                    esc_opt(s(\"audience\"))\n                };", "                } else {\n                    format!(\"\\\"{}\\\"\", s(\"audience\").unwrap_or(\"\"))\n                };")), "m05 test7"),
 ("m06_nickname_unfiltered", P((M, ".and_then(|n| safe_token(n, 32))", ".and_then(|n| Some(n))")), None),
 ("m07_release_ignores_witness", P((REL, "    match witness.kind {\n        WitnessKind::UngatedM1 => {}\n    }\n", "    let _ = witness;\n")), "test8 release"),
 ("m08_status_serialises_inbox_serde", P((E, "\"unread_bytes\": s.ib.text_bytes(),", "\"unread_bytes\": s.ib.text_bytes(), \"inbox_dump\": serde_json::to_value(&s.ib.items).ok(),")), None),
 ("m08b_status_reads_inbox_file", P((E, "\"unread_bytes\": s.ib.text_bytes(),", "\"unread_bytes\": s.ib.text_bytes(), \"inbox_dump\": std::fs::read_to_string(self.cfg.data_dir.join(\"inbox.json\")).ok(),")), "r2_7 status"),
 ("m08c_store_helper_leaks_text", P(
     (ST, "impl InboxState {\n", "impl InboxState {\n    /// dump\n    pub fn dump(&self) -> Vec<String> { self.items.iter().filter_map(|i| i.text.as_ref().map(|t| t.to_store(&StoreKey(())))).collect() }\n"),
     (E, "\"unread_bytes\": s.ib.text_bytes(),", "\"unread_bytes\": s.ib.text_bytes(), \"inbox_dump\": s.ib.dump(),")), "r2_7 status"),
 ("m09_kk_ignores_persisted_hard_stop", P((E, "if s.rec.verify.hard_stop && !cfg!(coagent_red = \"no_hard_stop_initiator\") {", "if false {")), "m09 hard_stop"),
 ("m10_kk_respond_ignores_hard_stop", P((E, "if s.rec.verify.hard_stop && !cfg!(coagent_red = \"no_hard_stop_responder\") {", "if false {")), "m10 hard_stop"),
 ("m11_send_ignores_hard_stop", P((E, "        if s.rec.verify.hard_stop {\n            return Response::err(id, code::HARD_STOP, \"this pair hit a verify hard stop\");\n        }\n        if text.len() > max {", "        if text.len() > max {")), "hard_stop m11 test6"),
 ("m12_verify_start_no_cap", P((E, "if used >= MAX_ATTEMPTS && !cfg!(coagent_red = \"no_persisted_cap\") {", "if false {")), "m12 test6"),
 ("m13_restore_base_attempts_zero", P((E, "        let base = rec.verify.attempts_used;", "        let base = 0;")), "m12 test6"),
 ("m14_no_for_shown_words_not_hard_stop", P((E, "            Err(_) if !matched && shown => {", "            Err(_) if false && !matched && shown => {")), "hard_stop test6"),
 ("m15_accept_seq0_chat", P((E, "        if env.seq == 0 {\n            match env.kind.as_str() {", "        if env.seq == 0 && env.kind != \"chat.msg\" {\n            match env.kind.as_str() {")), None),
 ("m16_duplicates_delivered", P((E, "        if env.seq <= s.ib.recv_upto {\n            s.ack_due.get_or_insert(now() + ACK_DELAY);\n            return; // duplicate (redelivery after reconnect)\n        }\n", "")), "test5 reconnect"),
 ("m17_app_gap_is_skip", P((E, "if env.seq > s.ib.recv_upto + 1 && !cfg!(coagent_red = \"app_gap_skip\") {", "if false {")), "m17"),
 ("m18_no_release_size_limit", P((E, "let oversize = text.len() > max_release;", "let oversize = text.len() > usize::MAX - max_release;")), "test7"),
 ("m19_temp_0644_then_chmod", P(
     (DD, "            } else {\n                0o600\n            };", "            } else {\n                0o644\n            };"),
     (DD, "        let (mut f, tmp) = self.open_temp(name)?;\n", "        let (mut f, tmp) = self.open_temp(name)?;\n        std::thread::sleep(std::time::Duration::from_millis(1));\n        f.set_permissions(std::os::unix::fs::PermissionsExt::from_mode(0o600)).map_err(io)?;\n")), "m19"),
 ("m20_relay_by_bare_name", P((RC, "    let mut relay = match Command::new(&coagent)", "    let _ = &coagent;\n    let mut relay = match Command::new(\"coagent\")")), "test1"),
 ("m21_relay_cwd_inherited", P((RC, "        .env_clear()\n        .current_dir(\"/\")\n        .stdin(Stdio::null())", "        .env_clear()\n        .stdin(Stdio::null())")), "m22"),
 ("m22_guard_env_inherited", P((RC, "            .env_clear()\n            .envs(if cfg!(coagent_red = \"guard_env_inherit\") {", "            .envs(if cfg!(coagent_red = \"guard_env_inherit\") {")), "m22"),
 ("m23_datadir_owner_mode_unchecked", P((DD, "            check_dir_meta(md.file_type().is_dir(), md.uid(), md.mode(), uid)?;\n        }\n        Ok(DataDir {", "            let _ = (&md, uid);\n        }\n        Ok(DataDir {")), "m23"),
 ("m24_state_file_mode_unchecked", P((DD, "            check_file_meta(md.file_type().is_file(), md.uid(), md.mode(), self.uid)?;", "            let _ = &md;")), "m24"),
 ("m25_reply_before_flush", P(
     (E, "                Err(_) => Response::err(id, code::NOT_SAVED, \"state could not be saved\"),\n            };\n            let _ = r.reply.send(resp);", "                Err(_) => Response::err(id, code::NOT_SAVED, \"state could not be saved\"),\n            };\n            let _ = r.reply.send(resp);\n            tokio::time::sleep(Duration::from_millis(300)).await;\n            let _ = self.flush();"),
     (E, "            let resp = match self.flush() {\n                Ok(()) => resp,\n                Err(_) => Response::err(id, code::NOT_SAVED", "            let resp = match Ok::<(), String>(()) {\n                Ok(()) => resp,\n                Err(_) => Response::err(id, code::NOT_SAVED")), None),
 ("m26_promote_on_kk1", P((E, "if cfg!(coagent_red = \"promote_on_kk1\") {", "if true {")), "g1 gate_b"),
 ("m27_ipc_line_limit_off", P((E, "recv_json_line(&mut s, ipc::MAX_REQUEST_LINE)", "recv_json_line(&mut s, 64 * 1024 * 1024)")), "test9"),
 ("m28_contact_nickname_controls", P((E, "                nickname: nickname_of(&key),", "                nickname: format!(\"{}\\n\\u{1b}[31m\", nickname_of(&key)),")), None),
 # ---- round 2 (n), re-anchored ----
 ("n02_persist_label_from_kk1", P((E, "                s.pending.push((epoch, ch, now()));", "                s.rec.kk_label = s.rec.kk_label.max(epoch);\n                s.pending.push((epoch, ch, now()));")), "g1 gate_b r2_g1"),
 ("n03_pending_unbounded", P((E, "if s.pending.len() >= MAX_PENDING && !cfg!(coagent_red = \"pending_unbounded\") {", "if false {")), "n03"),
 ("n04_promote_without_proof", P((E, "                    Err(_) if cfg!(coagent_red = \"promote_without_proof\") => None,\n                    Err(_) => continue,", "                    Err(_) => None,")), "n04"),
 ("n05_remove_on_handout", P((E, "if cfg!(coagent_red = \"ack_free_read\") {", "if true {")), "g3"),
 ("n06_drop_possibly_repeated", P((REL, "possibly_repeated: it.handed_out > 0,", "possibly_repeated: false,")), "g3 n22"),
 ("n07_handed_out_not_counted", P((E, "            it.handed_out = it.handed_out.saturating_add(1);\n", "")), "g3 n22"),
 ("n08_ack_ignores_handout", P((E, ".retain(|i| !(i.local_seq <= upto && i.handed_out > 0));", ".retain(|i| i.local_seq > upto);")), "r2_g3 g3"),
 ("n09_inbox_items_off_by_one", P((ST, "self.items.len() < crate::limits::MAX_INBOX_ITEMS + xi", "self.items.len() <= crate::limits::MAX_INBOX_ITEMS + xi")), "n09"),
 ("n10_inbox_bytes_off_by_one", P((ST, "self.text_bytes() + text <= crate::limits::MAX_INBOX_TEXT_BYTES + xb", "self.text_bytes() + text <= crate::limits::MAX_INBOX_TEXT_BYTES + xb + 1")), "n09"),
 ("n11_page_items_off_by_one", P((E, "&& (page.len() >= limits::PAGE_ITEMS + usize::from", "&& (page.len() > limits::PAGE_ITEMS + usize::from")), "n09"),
 ("n12_page_text_unbounded", P((E, "                    || bytes + len > limits::PAGE_TEXT_BYTES\n", "                    || bytes + len > usize::MAX / 2\n")), None),
 ("n13_outbox_items_off_by_one", P((E, "            >= limits::MAX_OUTBOX_ITEMS + usize::from(cfg!(coagent_red = \"outbox_items_off_by_one\"))", "            > limits::MAX_OUTBOX_ITEMS + usize::from(cfg!(coagent_red = \"outbox_items_off_by_one\"))")), "n09"),
 ("n14_writer_no_size_check", P((ST, "if b.len() as u64 > MAX_STATE_FILE && !cfg!(coagent_red = \"writer_no_size_check\") {", "if false {")), "n14 g2"),
 ("n15_damaged_inbox_not_quarantined", P((ST, "                quarantined: Some(self.dir.quarantine(INBOX_FILE)?),", "                quarantined: None,")), "damaged g2"),
 ("n16_damaged_session_starts_fresh", P((ST, "        self.load_json(SESSION_FILE)\n    }", "        Ok(self.load_json(SESSION_FILE).ok().flatten())\n    }")), "damaged g2"),
 ("n17_dead_waiters_kept_at_wake", P((E, "        if !red {\n            self.waiters.retain(|w| !w.reply.is_closed());\n        }\n", "")), None),
 ("n18_no_directory_sync", P((DD, "        fs::rename(&tmp, self.root.join(name)).map_err(io)?;\n        fs::File::open(&self.root)\n            .and_then(|d| d.sync_all())\n            .map_err(io)?;\n", "        fs::rename(&tmp, self.root.join(name)).map_err(io)?;\n")), None),
 ("n19_quarantine_deletes", P((DD, "            fs::rename(self.root.join(name), self.root.join(&rel)).map_err(io)?;", "            fs::remove_file(self.root.join(name)).map_err(io)?;")), "damaged quarantine"),
 ("n20_connected_without_channel", P((E, "            && s.chan_epoch.is_some()\n", "")), None),
 ("n21_room_never_signalled", P((E, "let room = s.refusing_full && self_has_room(&s.ib);", "let room = false;")), "g2 gate_c"),
 ("n22_mcp_ack_without_write", P((M, "if drx.await.is_ok() {", "if true {")), "n22"),
 ("n23_mcp_ignores_cancel", P((M, "                        t.abort();", "                        let _ = t;")), "g4 g3"),
 ("n24_ipc_does_not_watch_client", P((E, "                        let _ = tokio::io::AsyncReadExt::read(&mut s, &mut probe).await;", "                        std::future::pending::<()>().await;")), "g4 gate_d"),
 ("n25_guard_kill_orphans_relay", P((E, "if !cfg!(coagent_red = \"orphan_on_guard_kill\") {", "if false {")), "g9"),
 ("n26_peer_full_ignored", P((E, "let held = s.peer_full && !cfg!(coagent_red = \"transmit_while_full\");", "let held = false;")), None),
 ("n27_full_inbox_still_numbers", P((E, "            s.arrived_while_full += 1;\n            return; // full: neither", "            s.arrived_while_full += 1;\n            s.ib.recv_upto = env.seq;\n            return; // full: neither")), "g2 gate_c"),
 ("n28_resume_room_ignored", P((E, "if env.body.get(\"room\").and_then(|v| v.as_bool()) == Some(true) && s.peer_full {", "if false {")), "g2 gate_c"),
 ("n29_pending_not_cleared_on_install", P((E, "                s.chan_epoch = Some(epoch);\n                s.pending.clear();", "                s.chan_epoch = Some(epoch);")), None),
 # ---- round 3 (x): new, on code changed since bb92225 ----
 ("x01_install_channel_no_hard_stop", P((E, "        if Self::hard_stopped(s) {\n            log!(\"channel refused: hard stop\");\n            return false;\n        }\n", "")), "hard_stop"),
 ("x02_on_kk2_no_hard_stop", P((E, "        if Self::hard_stopped(s) || ch.peer_key_id() != s.rec.peer {", "        if ch.peer_key_id() != s.rec.peer {")), "hard_stop"),
 ("x03_on_frame_no_hard_stop", P((E, "        if Self::hard_stopped(s) {\n            s.refused += 1;\n            return;\n        }\n        // Initiator: the responder's first frame", "        // Initiator: the responder's first frame")), "hard_stop"),
 ("x04_channel_up_no_hard_stop", P((E, "        let Some(s) = self.sess.as_mut() else { return };\n        if Self::hard_stopped(s) {\n            return;\n        }\n        log!(\n            \"channel up:", "        let Some(s) = self.sess.as_mut() else { return };\n        log!(\n            \"channel up:")), "hard_stop"),
 ("x05_seal_no_hard_stop", P((E, "        if Self::hard_stopped(s) {\n            return Err(CryptoError::NoChannel);\n        }\n", "")), "hard_stop"),
 ("x06_send_frame_no_hard_stop", P((E, "        if self.sess.as_ref().map(Self::hard_stopped).unwrap_or(true) {\n            return;\n        }\n", "")), "hard_stop"),
 ("x07_transmit_no_hard_stop", P((E, "if s.chan_epoch.is_none() || held || Self::hard_stopped(s) {", "if s.chan_epoch.is_none() || held {")), "hard_stop"),
 ("x08_on_inbound_no_hard_stop", P((E, "        if Self::hard_stopped(s) {\n            s.refused += 1;\n            return;\n        }\n        let env = m.envelope();", "        let env = m.envelope();")), "hard_stop"),
 ("x09_hard_stop_keeps_pending", P((E, "            s.pending.clear();\n            s.unconfirmed = None;\n        }\n        s.awaiting_rekey = None;", "            s.unconfirmed = None;\n        }\n        s.awaiting_rekey = None;")), "hard_stop"),
 ("x10_hard_stop_keeps_unconfirmed", P((E, "            s.pending.clear();\n            s.unconfirmed = None;\n        }\n        s.awaiting_rekey = None;", "            s.pending.clear();\n        }\n        s.awaiting_rekey = None;")), "hard_stop"),
 ("x11_hard_stop_keeps_map_channel", P((E, "        self.map.close(&sid, &peer);\n        self.dirty = true;\n        log!(\"HARD STOP", "        let _ = (sid, peer);\n        self.dirty = true;\n        log!(\"HARD STOP")), "hard_stop"),
 ("x12_hard_stop_not_marked_dirty", P((E, "        self.dirty = true;\n        log!(\"HARD STOP", "        log!(\"HARD STOP")), "hard_stop test6 m09 m10"),
 ("x13_connected_ignores_hard_stop", P((E, "            && !Self::hard_stopped(s)\n            && !s.rec.ended", "            && !s.rec.ended")), "hard_stop"),
 ("x14_kk_timeout_600s", P((E, "pub const KK_TIMEOUT: Duration = Duration::from_secs(5);", "pub const KK_TIMEOUT: Duration = Duration::from_secs(600);")), "r2_2 r2_g1"),
 ("x15_unanswered_kk1_never_retried", P((E, "                        .kk\n                        .as_ref()\n                        .map(|(_, _, at)| at.elapsed() > KK_TIMEOUT)", "                        .kk\n                        .as_ref()\n                        .map(|(_, _, at)| at.elapsed() > Duration::MAX)")), "r2_2 r2_g1"),
 ("x16_unconfirmed_never_retried", P((E, "                            .unconfirmed\n                            .as_ref()\n                            .map(|(_, _, at)| at.elapsed() > KK_TIMEOUT)", "                            .unconfirmed\n                            .as_ref()\n                            .map(|(_, _, at)| at.elapsed() > Duration::MAX)")), "r2_2 r2_g1"),
 ("x17_rekey_stall_1500s", P((E, "const REKEY_STALL: Duration = Duration::from_secs(15);", "const REKEY_STALL: Duration = Duration::from_secs(1500);")), "r2_2 r2_g1"),
 ("x18_retransmit_1500s", P((E, "const RETRANSMIT_AFTER: Duration = Duration::from_secs(15);", "const RETRANSMIT_AFTER: Duration = Duration::from_secs(1500);")), "r2_2"),
 ("x19_pending_ttl_zero", P((E, "const PENDING_TTL: Duration = Duration::from_secs(30);", "const PENDING_TTL: Duration = Duration::from_millis(0);")), "r2_2 r2_g1 test1"),
 ("x20_replays_never_answered_again", P((E, "const REPLAY_ANSWER_GAP: Duration = Duration::from_millis(500);", "const REPLAY_ANSWER_GAP: Duration = Duration::from_secs(3600);")), None),
 ("x21_unconfirmed_promoted_without_open", P((E, "            match ch.open(frame) {\n                Ok(received) => {\n                    if self.install_channel(ch, l) {", "            match Ok::<Received, CryptoError>(Received::Rekeyed) {\n                Ok(received) => {\n                    if self.install_channel(ch, l) {")), "r2_2 r2_g1 n04"),
 ("x22_kk1_digest_never_recorded", P((E, "                if !s.rec.kk1_seen.contains(&digest) {\n                    s.rec.kk1_seen.push(digest);", "                if false {\n                    s.rec.kk1_seen.push(digest);")), "r2_g1 r2_2 g1"),
 ("x23_kk1_seen_kept_2", P((ST, "pub const KK1_SEEN_KEPT: usize = 256;", "pub const KK1_SEEN_KEPT: usize = 2;")), "r2_g1 r2_2 g1"),
 ("x24_kk1_digest_1_byte", P((E, "let digest = hex::encode(&msg[..msg.len().min(16)]);", "let digest = hex::encode(&msg[..msg.len().min(1)]);")), "r2_g1 r2_2 g1"),
 ("x25_pending_evicts_newest", P((E, "                    s.pending.remove(0);", "                    s.pending.pop();")), "r2_g1 n03"),
 ("x26_audience_bound_64k", P((L, "pub const MAX_PEER_AUDIENCE: usize = 8 * 1024;", "pub const MAX_PEER_AUDIENCE: usize = 64 * 1024;")), "r2_3 bulky"),
 ("x27_re_bound_unchecked", P((REL, "            && self\n                .re\n                .as_ref()\n                .map(|r| r.len() <= MAX_PEER_ID)\n                .unwrap_or(true)", "")), None),
 ("x28_overbound_item_keeps_text", P((REL, "            re: None,\n            text: None,\n            audience: None,\n            ..self", "            re: None,\n            audience: None,\n            ..self")), "r2_3"),
 ("x29_load_not_bounded", P((ST, "                        // from an older version): anything over them becomes a count-only notice.\n                        .bounded()", "                        // from an older version): anything over them becomes a count-only notice.\n")), None),
 ("x30_item_cost_unescaped", P((L, "    peer_bytes * EXPANSION + ITEM_FIXED", "    peer_bytes + ITEM_FIXED")), "r2_3 bulky"),
 ("x31_page_cost_off_by_one_item", P((E, "let over_cost = cost + c > limits::PAGE_BYTES && !cfg!(coagent_red = \"page_text_only\");", "let over_cost = cost > limits::PAGE_BYTES && !cfg!(coagent_red = \"page_text_only\");")), "r2_3"),
 ("x32_sealable_small_ack", P((E, "            ack: u64::MAX,\n            ..Self::draft(", "            ack: 0,\n            ..Self::draft(")), None),
 ("x33_sealable_limit_doubled", P((E, ".map(|v| v.len() <= coagent_crypto::channel::MAX_RECORD_BODY)", ".map(|v| v.len() <= 2 * coagent_crypto::channel::MAX_RECORD_BODY)")), "r2_4 control_heavy"),
 ("x34_set_aside_without_quarantine", P((E, "        match self.store.quarantine_unsendable(&s.ob.items[pos]) {", "        match Ok::<String, crate::store::StoreError>(String::new()) {")), "r2_4"),
 ("x35_unsendable_not_counted", P((E, "        s.ob.unsendable += 1;\n", "")), "r2_4"),
 ("x36_not_confirmed_set_aside", P((E, "            Err(CryptoError::NoChannel) | Err(CryptoError::NotConfirmed) => {}", "            Err(CryptoError::NoChannel) => {}")), None),
 ("x37_max_waiters_1", P((E, "const MAX_WAITERS: usize = 64;", "const MAX_WAITERS: usize = 1;")), "g4 wait"),
 ("x38_busy_without_prune", P((E, "                    self.waiters.retain(|w| !w.reply.is_closed());\n                    if self.waiters.len() >= MAX_WAITERS {", "                    if self.waiters.len() >= MAX_WAITERS {")), "g4 wait"),
 ("x39_quarantine_name_seconds_only", P((DD, "                format!(\n                    \"quarantine/{name}.{}.{}\",\n                    crate::util::unix_now(),\n                    hex::encode(&r[..8])\n                )", "                {\n                    let _ = &r;\n                    format!(\"quarantine/{name}.{}\", crate::util::unix_now())\n                }")), "r2_5 quarantine damaged"),
 ("x40_relay_ack_duplicates", P((E, "let new = pair_seq > s.rec.relay_recv_upto;", "let new = pair_seq >= s.rec.relay_recv_upto;")), None),
 ("x41_full_without_flush", P((E, "            let _ = self.flush();\n            let last = self.sess.as_ref().map(|s| s.rec.recv_upto).unwrap_or(0);\n            self.send_control(\"full\"", "            let last = self.sess.as_ref().map(|s| s.rec.recv_upto).unwrap_or(0);\n            self.send_control(\"full\"")), None),
 ("x42_ack_sent_unconditional", P((E, "            if s.rec.recv_upto >= s.ib.recv_upto {\n                s.ack_due = None;\n            }", "            s.ack_due = None;")), None),
 ("x43_outbox_load_fail_open", P((E, "        let mut ob = match self.store.load_outbox() {", "        let mut ob = match self.store.load_outbox().or_else(|_| Ok::<_, crate::store::StoreError>(Default::default())) {")), None),
 ("x44_channel_up_keeps_peer_full", P((E, "        s.peer_full = false;\n        let full = s.refusing_full;", "        let full = s.refusing_full;")), "g2 gate_c n09"),
 ("x45_connected_ignores_unconfirmed", P((E, "            && s.unconfirmed.is_none()\n", "")), None),
 ("x46_connected_ignores_awaiting_rekey", P((E, "            && s.awaiting_rekey.is_none()\n", "")), None),
 ("x47_page_may_be_empty", P((E, "            if !page.is_empty()\n", "            if true\n")), None),
 ("x48_pending_tries_ignore_label", P((E, "                .filter(|(_, (l, _, _))| *l == epoch)\n", "")), None),
 ("x49_send_checks_raw_text_only_again", P((E, "if !cfg!(coagent_red = \"send_no_size_check\") && !Self::sealable(s, &self.id, &item) {", "if false {")), "r2_4"),
 ("x50_mcp_no_ack_gate", P((M, "                drop(gate.lock().await);", "")), "r2_7 count_bound"),
]

def sh(cmd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, cwd="/").returncode

env = f". {ENV}; . {R}/scripts/env.sh; "
os.makedirs(OUT, exist_ok=True)
results = []
def failed_in(out):
    return [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
for name, patches, quick in MUTS:
    if args and name not in args:
        continue
    srcs = {}
    ok = True
    for path, old, new in patches:
        src = srcs.get(path, open(path).read())
        if path not in srcs:
            srcs[path] = src
        n = src.count(old)
        if n != 1:
            ok = False
            print(name, f"PATCH DID NOT APPLY ({path.split('/')[-1]}: {n})", flush=True)
    if dry or not ok:
        if not ok:
            results.append((name, "PATCH DID NOT APPLY"))
        else:
            print(name, "applies", flush=True)
        continue
    cur = dict(srcs)
    for path, old, new in patches:
        cur[path] = cur[path].replace(old, new)
    try:
        for path, txt in cur.items():
            open(path, "w").write(txt)
        log = f"{OUT}/{name}.log"
        t0 = time.time()
        b = sh(env + f"cargo build --manifest-path {R}/Cargo.toml --workspace --bins --tests --locked", log + ".build")
        if b != 0:
            res = "DOES NOT COMPILE"
        else:
            res = None
            if quick:
                sh(env + f"cargo test --manifest-path {R}/Cargo.toml --locked -p coagent-daemon -p coagent-mcp --no-fail-fast -- {quick}", log + ".quick")
                f = failed_in(open(log + ".quick").read())
                if f:
                    res = "caught (targeted) by " + ", ".join(f)
            if res is None:
                sh(env + f"cargo test --manifest-path {R}/Cargo.toml --locked -p coagent-daemon -p coagent-mcp --no-fail-fast", log)
                out = open(log).read()
                f = failed_in(out)
                if f:
                    res = "caught (full) by " + ", ".join(f)
                elif "test result: ok" in out:
                    res = "SURVIVED (full suite)"
                else:
                    res = "HARNESS ERROR"
        results.append((name, res))
        print(f"{name}: {res} ({int(time.time()-t0)} s)", flush=True)
    finally:
        for path, txt in srcs.items():
            open(path, "w").write(txt)
if not dry:
    json.dump(results, open(f"{OUT}/results.json", "w"), indent=1)
