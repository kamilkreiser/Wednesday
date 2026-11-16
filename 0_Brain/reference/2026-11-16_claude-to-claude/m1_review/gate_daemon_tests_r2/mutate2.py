#!/usr/bin/env python3
"""Gate round-2 mutation runner: one mutation at a time over coagent-daemon / coagent-mcp at bb92225,
the builder's full suite of both crates (its gate_return tests included). Restores every file after
each run. Usage: mutate2.py [--dry] [--repo R --env E --out O] [names...]"""
import os, subprocess, sys, time, json

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_daemon_r2"
args = sys.argv[1:]
dry = "--dry" in args
def opt(k, d):
    if k in args:
        i = args.index(k); v = args[i + 1]; del args[i:i + 2]; return v
    return d
R = opt("--repo", S + "/mrepo")
ENV = opt("--env", S + "/menv.sh")
OUT = opt("--out", S + "/mut")
args = [a for a in args if a != "--dry"]
D = R + "/crates/coagent-daemon/src/"
M = R + "/crates/coagent-mcp/src/main.rs"
E = D + "engine.rs"

P = lambda *ps: list(ps)
MUTS = [
 # ---- round 1, re-anchored on bb92225 ----
 ("m01_escape_lt_gt_plain", P((M, "!matches!(c, '\"' | '\\\\' | '<' | '>' | '&')", "!matches!(c, '\"' | '\\\\' | '&')"))),
 ("m02_escape_controls_plain", P((M, "let plain = (' '..='~').contains(&c) &&", "let plain = (c < '\\u{7f}' && c != '\\n') &&"))),
 ("m03_escape_nonascii_plain", P((M, "let plain = (' '..='~').contains(&c) &&", "let plain = (c >= ' ' && c != '\\u{7f}') &&"))),
 ("m04_escape_amp_plain", P((M, "'>' | '&');", "'>');"))),
 ("m05_audience_unescaped", P((M, "                } else {\n                    esc_opt(s(\"audience\"))\n                };", "                } else {\n                    format!(\"\\\"{}\\\"\", s(\"audience\").unwrap_or(\"\"))\n                };"))),
 ("m06_nickname_unfiltered", P((M, ".and_then(|n| safe_token(n, 32))", ".and_then(|n| Some(n))"))),
 ("m07_release_ignores_witness", P((D+"release.rs", "    match witness.kind {\n        WitnessKind::UngatedM1 => {}\n    }\n", "    let _ = witness;\n"))),
 ("m08_status_serialises_inbox_serde", P((E, "\"unread_bytes\": s.ib.text_bytes(),", "\"unread_bytes\": s.ib.text_bytes(), \"inbox_dump\": serde_json::to_value(&s.ib.items).ok(),"))),
 ("m08b_status_reads_inbox_file", P((E, "\"unread_bytes\": s.ib.text_bytes(),", "\"unread_bytes\": s.ib.text_bytes(), \"inbox_dump\": std::fs::read_to_string(self.cfg.data_dir.join(\"inbox.json\")).ok(),"))),
 ("m08c_store_helper_leaks_text", P(
     (D+"store.rs", "impl InboxState {\n", "impl InboxState {\n    /// dump\n    pub fn dump(&self) -> Vec<String> { self.items.iter().filter_map(|i| i.text.as_ref().map(|t| t.to_store(&StoreKey(())))).collect() }\n"),
     (E, "\"unread_bytes\": s.ib.text_bytes(),", "\"unread_bytes\": s.ib.text_bytes(), \"inbox_dump\": s.ib.dump(),"))),
 ("m09_kk_ignores_persisted_hard_stop", P((E, "if s.rec.verify.hard_stop && !cfg!(coagent_red = \"no_hard_stop_initiator\") {", "if false {"))),
 ("m10_kk_respond_ignores_hard_stop", P((E, "if s.rec.verify.hard_stop && !cfg!(coagent_red = \"no_hard_stop_responder\") {", "if false {"))),
 ("m11_send_ignores_hard_stop", P((E, "        if s.rec.verify.hard_stop {\n            return Response::err(id, code::HARD_STOP, \"this pair hit a verify hard stop\");\n        }\n        if text.len() > max {", "        if text.len() > max {"))),
 ("m12_verify_start_no_cap", P((E, "if used >= MAX_ATTEMPTS && !cfg!(coagent_red = \"no_persisted_cap\") {", "if false {"))),
 ("m13_restore_base_attempts_zero", P((E, "        let base = rec.verify.attempts_used;", "        let base = 0;"))),
 ("m14_no_for_shown_words_not_hard_stop", P((E, "            Err(_) if !matched && shown => {", "            Err(_) if false && !matched && shown => {"))),
 ("m15_accept_seq0_chat", P((E, "            return;\n        }\n        if env.seq <= s.ib.recv_upto {", "            if env.kind != \"chat.msg\" { return; }\n        }\n        if env.seq <= s.ib.recv_upto {"))),
 ("m16_duplicates_delivered", P((E, "        if env.seq <= s.ib.recv_upto {\n            s.ack_due.get_or_insert(now() + ACK_DELAY);\n            return; // duplicate (redelivery after reconnect)\n        }\n", ""))),
 ("m17_app_gap_is_skip", P((E, "if env.seq > s.ib.recv_upto + 1 && !cfg!(coagent_red = \"app_gap_skip\") {", "if false {"))),
 ("m18_no_release_size_limit", P((E, "let oversize = text.len() > max_release;", "let oversize = text.len() > usize::MAX - max_release;"))),
 ("m19_temp_0644_then_chmod", P(
     (D+"datadir.rs", "            } else {\n                0o600\n            };", "            } else {\n                0o644\n            };"),
     (D+"datadir.rs", "        let (mut f, tmp) = self.open_temp(name)?;\n", "        let (mut f, tmp) = self.open_temp(name)?;\n        std::thread::sleep(std::time::Duration::from_millis(1));\n        f.set_permissions(std::os::unix::fs::PermissionsExt::from_mode(0o600)).map_err(io)?;\n"))),
 ("m20_relay_by_bare_name", P((D+"relay_child.rs", "    let mut relay = match Command::new(&coagent)", "    let _ = &coagent;\n    let mut relay = match Command::new(\"coagent\")"))),
 ("m21_relay_cwd_inherited", P((D+"relay_child.rs", "        .env_clear()\n        .current_dir(\"/\")\n        .stdin(Stdio::null())", "        .env_clear()\n        .stdin(Stdio::null())"))),
 ("m22_guard_env_inherited", P((D+"relay_child.rs", "            .env_clear()\n            .envs(if cfg!(coagent_red = \"guard_env_inherit\") {", "            .envs(if cfg!(coagent_red = \"guard_env_inherit\") {"))),
 ("m23_datadir_owner_mode_unchecked", P((D+"datadir.rs", "            check_dir_meta(md.file_type().is_dir(), md.uid(), md.mode(), uid)?;\n        }\n        Ok(DataDir {", "            let _ = (&md, uid);\n        }\n        Ok(DataDir {"))),
 ("m24_state_file_mode_unchecked", P((D+"datadir.rs", "            check_file_meta(md.file_type().is_file(), md.uid(), md.mode(), self.uid)?;", "            let _ = &md;"))),
 ("m25_reply_before_flush", P((E, "                Err(_) => Response::err(id, code::NOT_SAVED, \"state could not be saved\"),\n            };\n            let _ = r.reply.send(resp);", "                Err(_) => Response::err(id, code::NOT_SAVED, \"state could not be saved\"),\n            };\n            let _ = r.reply.send(resp);\n            tokio::time::sleep(Duration::from_millis(300)).await;\n            let _ = self.flush();"),
     (E, "            let resp = match self.flush() {\n                Ok(()) => resp,\n                Err(_) => Response::err(id, code::NOT_SAVED", "            let resp = match Ok::<(), String>(()) {\n                Ok(()) => resp,\n                Err(_) => Response::err(id, code::NOT_SAVED"))),
 ("m26_promote_on_kk1", P((E, "if cfg!(coagent_red = \"promote_on_kk1\") {", "if true {"))),
 ("m27_ipc_line_limit_off", P((E, "recv_json_line(&mut s, ipc::MAX_REQUEST_LINE)", "recv_json_line(&mut s, 64 * 1024 * 1024)"))),
 ("m28_contact_nickname_controls", P((E, "                nickname: nickname_of(&key),", "                nickname: format!(\"{}\\n\\u{1b}[31m\", nickname_of(&key)),"))),
 # ---- new, on the delta ----
 ("n02_persist_label_from_kk1", P((E, "                        s.pending.push((epoch, ch));", "                        s.rec.kk_label = s.rec.kk_label.max(epoch);\n                        self.dirty = true;\n                        s.pending.push((epoch, ch));"))),
 ("n03_pending_unbounded", P((E, "                        if s.pending.len() >= MAX_PENDING {", "                        if false {"))),
 ("n04_promote_without_proof", P((E, "                            Err(_) => {\n                                // Not authentic under this one: put it back, change nothing.\n                                s.pending.insert(pos, (epoch, ch));\n                                tried += 1;\n                            }", "                            Err(_) => {\n                                s.pending.clear();\n                                if self.install_channel(ch, epoch) {\n                                    self.on_channel_up();\n                                }\n                                return;\n                            }"))),
 ("n05_remove_on_handout", P((E, "if cfg!(coagent_red = \"ack_free_read\") {", "if true {"))),
 ("n06_drop_possibly_repeated", P((D+"release.rs", "possibly_repeated: it.handed_out > 0,", "possibly_repeated: false,"))),
 ("n07_handed_out_not_counted", P((E, "            it.handed_out = it.handed_out.saturating_add(1);\n", ""))),
 ("n08_ack_ignores_handout", P((E, ".retain(|i| !(i.local_seq <= upto && i.handed_out > 0));", ".retain(|i| i.local_seq > upto);"))),
 ("n09_inbox_items_off_by_one", P((E, "if (s.ib.items.len() >= limits::MAX_INBOX_ITEMS", "if (s.ib.items.len() > limits::MAX_INBOX_ITEMS"))),
 ("n10_inbox_bytes_off_by_one", P((E, "|| s.ib.text_bytes() + cost > limits::MAX_INBOX_TEXT_BYTES)", "|| s.ib.text_bytes() + cost > limits::MAX_INBOX_TEXT_BYTES + 1)"))),
 ("n11_page_items_off_by_one", P((E, "(page.len() >= limits::PAGE_ITEMS || bytes + len > limits::PAGE_TEXT_BYTES)", "(page.len() > limits::PAGE_ITEMS || bytes + len > limits::PAGE_TEXT_BYTES)"))),
 ("n12_page_bytes_unbounded", P((E, "(page.len() >= limits::PAGE_ITEMS || bytes + len > limits::PAGE_TEXT_BYTES)", "(page.len() >= limits::PAGE_ITEMS || bytes + len > usize::MAX / 2)"))),
 ("n13_outbox_items_off_by_one", P((E, "if s.ob.items.len() >= limits::MAX_OUTBOX_ITEMS", "if s.ob.items.len() > limits::MAX_OUTBOX_ITEMS"))),
 ("n14_writer_no_size_check", P((D+"store.rs", "        if b.len() as u64 > MAX_STATE_FILE {", "        if false {"))),
 ("n15_damaged_inbox_not_quarantined", P((D+"store.rs", "                quarantined: Some(self.dir.quarantine(INBOX_FILE)?),", "                quarantined: None,"))),
 ("n16_damaged_session_starts_fresh", P((D+"store.rs", "        self.load_json(SESSION_FILE)\n    }", "        Ok(self.load_json(SESSION_FILE).ok().flatten())\n    }"))),
 ("n17_dead_waiters_kept", P((E, "            self.waiters.retain(|w| !w.reply.is_closed());\n", ""))),
 ("n18_no_directory_sync", P((D+"datadir.rs", "        fs::rename(&tmp, self.root.join(name)).map_err(io)?;\n        fs::File::open(&self.root)\n            .and_then(|d| d.sync_all())\n            .map_err(io)?;\n", "        fs::rename(&tmp, self.root.join(name)).map_err(io)?;\n"))),
 ("n19_quarantine_deletes", P((D+"datadir.rs", "        fs::rename(self.root.join(name), self.root.join(&rel)).map_err(io)?;", "        fs::remove_file(self.root.join(name)).map_err(io)?;"))),
 ("n20_connected_without_channel", P((E, "s.attached && s.peer_present && s.chan_epoch.is_some() && !s.rec.ended", "s.attached && s.peer_present && !s.rec.ended"))),
 ("n21_room_never_signalled", P((E, "let room = s.refusing_full && self_has_room(&s.ib);", "let room = false;"))),
 ("n22_mcp_ack_without_write", P((M, "if drx.await.is_ok() {", "if true {"))),
 ("n23_mcp_ignores_cancel", P((M, "                        t.abort();", "                        let _ = t;"))),
 ("n24_ipc_does_not_watch_client", P((E, "_ = tokio::io::AsyncReadExt::read(&mut s, &mut probe) => {", "_ = std::future::pending::<usize>() => {"))),
 ("n25_guard_kill_orphans_relay", P((E, "if !cfg!(coagent_red = \"orphan_on_guard_kill\") {", "if false {"))),
 ("n26_peer_full_ignored", P((E, "if s.chan_epoch.is_none() || s.peer_full {", "if s.chan_epoch.is_none() {"))),
 ("n27_full_inbox_still_accepts_numbering", P((E, "            return; // full: neither accepted nor a gap; the sender keeps it and will be told \"room\"", "            s.ib.recv_upto = env.seq;\n            return;"))),
 ("n28_resume_room_ignored", P((E, "if env.body.get(\"room\").and_then(|v| v.as_bool()) == Some(true) && s.peer_full {", "if false {"))),
 ("n29_pending_not_cleared_on_promote", P((E, "                                s.pending.clear();\n                                if self.install_channel(ch, epoch) {\n                                    log!(", "                                if self.install_channel(ch, epoch) {\n                                    log!("))),
]

def sh(cmd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, cwd="/").returncode

env = f". {ENV}; "
os.makedirs(OUT, exist_ok=True)
results = []
for name, patches in MUTS:
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
            sh(env + f"cargo test --manifest-path {R}/Cargo.toml --locked -p coagent-daemon -p coagent-mcp --no-fail-fast", log)
            out = open(log).read()
            failed = [l for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
            if failed:
                res = "caught by " + ", ".join(l.split()[1] for l in failed)
            elif "test result: ok" in out:
                res = "SURVIVED"
            else:
                res = "HARNESS ERROR"
        results.append((name, res))
        print(f"{name}: {res} ({int(time.time()-t0)} s)", flush=True)
    finally:
        for path, txt in srcs.items():
            open(path, "w").write(txt)
if not dry:
    json.dump(results, open(f"{OUT}/results.json", "w"), indent=1)
