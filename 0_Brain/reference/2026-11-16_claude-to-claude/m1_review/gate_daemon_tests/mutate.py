#!/usr/bin/env python3
"""Gate mutation runner: one mutation at a time over coagent-daemon / coagent-mcp, the builder's full
suite of both crates (gate_* tests skipped). Restores every file after each run."""
import os, subprocess, sys, time, json

S = "/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_daemon"
R = S + "/repo"
D = R + "/crates/coagent-daemon/src/"
M = R + "/crates/coagent-mcp/src/main.rs"

MUTS = [
 ("m01_escape_lt_gt_plain", M, "!matches!(c, '\"' | '\\\\' | '<' | '>' | '&')", "!matches!(c, '\"' | '\\\\' | '&')"),
 ("m02_escape_controls_plain", M, "let plain = (' '..='~').contains(&c) &&", "let plain = (c < '\\u{7f}' && c != '\\n') &&"),
 ("m03_escape_nonascii_plain", M, "let plain = (' '..='~').contains(&c) &&", "let plain = (c >= ' ' && c != '\\u{7f}') &&"),
 ("m04_escape_amp_plain", M, "'>' | '&');", "'>');"),
 ("m05_audience_unescaped", M, "esc_opt(s(\"audience\")),", "format!(\"\\\"{}\\\"\", s(\"audience\").unwrap_or(\"\")),"),
 ("m06_nickname_unfiltered", M, ".and_then(|n| safe_token(n, 32))", ".and_then(|n| Some(n))"),
 ("m07_release_ignores_witness", D+"release.rs", "    match witness {\n        GateWitness::UngatedM1 => {}\n    }\n", "    let _ = witness;\n"),
 ("m08_status_serialises_inbox", D+"engine.rs", "\"unread\": r.inbox.len(),", "\"unread\": r.inbox.len(), \"inbox_dump\": serde_json::to_value(&r.inbox).ok(),"),
 ("m09_kk_ignores_persisted_hard_stop", D+"engine.rs", "        if s.rec.verify.hard_stop {\n            log!(\"not starting a key exchange: hard stop\");\n            return;\n        }\n", ""),
 ("m10_kk_respond_ignores_hard_stop", D+"engine.rs", "                if s.rec.verify.hard_stop {\n                    s.refused += 1;", "                if false {\n                    s.refused += 1;"),
 ("m11_send_ignores_hard_stop", D+"engine.rs", "        if s.rec.verify.hard_stop {\n            return Response::err(id, code::HARD_STOP, \"this pair hit a verify hard stop\");\n        }\n        if text.len() > max {", "        if text.len() > max {"),
 ("m12_verify_start_no_cap", D+"engine.rs", "        if used >= MAX_ATTEMPTS {\n            return Response::err(id, code::LOCKED, \"no verify attempts left\");\n        }\n", ""),
 ("m13_restore_base_attempts_zero", D+"engine.rs", "        let base = rec.verify.attempts_used;", "        let base = 0;"),
 ("m14_no_for_shown_words_not_hard_stop", D+"engine.rs", "            Err(_) if !matched && shown => {", "            Err(_) if false && !matched && shown => {"),
 ("m15_accept_seq0_chat", D+"engine.rs", "                _ => s.refused += 1,\n            }\n            if s.rec.outbox.len() != before {\n                self.dirty = true;\n            }\n            return;\n        }", "                \"chat.msg\" => {}\n                _ => s.refused += 1,\n            }\n            if env.kind != \"chat.msg\" {\n            if s.rec.outbox.len() != before {\n                self.dirty = true;\n            }\n            return;\n            }\n        }"),
 ("m16_duplicates_delivered", D+"engine.rs", "        if env.seq <= s.rec.recv_upto {\n            s.ack_due.get_or_insert(now() + ACK_DELAY);\n            return; // duplicate (redelivery after reconnect)\n        }\n", ""),
 ("m17_app_gap_is_skip", D+"engine.rs", "        if env.seq > s.rec.recv_upto + 1 {", "        if false && env.seq > s.rec.recv_upto + 1 {"),
 ("m18_no_release_size_limit", D+"engine.rs", "let oversize = text.len() > max_release;", "let oversize = text.len() > usize::MAX - max_release;"),
 ("m19_state_chmod_after_create", D+"datadir.rs", "            .open(&tmp)\n            .map_err(io)?;\n        f.write_all(bytes).map_err(io)?;", "            .open(&tmp)\n            .map_err(io)?;\n        f.set_permissions(std::os::unix::fs::PermissionsExt::from_mode(0o644)).map_err(io)?;\n        std::thread::sleep(std::time::Duration::from_millis(1));\n        f.set_permissions(std::os::unix::fs::PermissionsExt::from_mode(0o600)).map_err(io)?;\n        f.write_all(bytes).map_err(io)?;"),
 ("m20_relay_by_bare_name", D+"relay_child.rs", "    let mut relay = match Command::new(&coagent)", "    let _ = &coagent;\n    let mut relay = match Command::new(\"coagent\")"),
 ("m21_relay_cwd_inherited", D+"relay_child.rs", "        .env_clear()\n        .current_dir(\"/\")\n        .stdin(Stdio::null())", "        .env_clear()\n        .stdin(Stdio::null())"),
 ("m22_relay_env_inherited", D+"relay_child.rs", "        .arg(format!(\"127.0.0.1:{port}\"))\n            .env_clear()", "        .arg(format!(\"127.0.0.1:{port}\"))"),
 ("m23_datadir_owner_mode_unchecked", D+"datadir.rs", "        let md = fs::symlink_metadata(root).map_err(io)?;\n        check_dir_meta(md.file_type().is_dir(), md.uid(), md.mode(), uid)?;", "        let md = fs::symlink_metadata(root).map_err(io)?;\n        let _ = (&md, uid);"),
 ("m24_state_file_mode_unchecked", D+"datadir.rs", "        check_file_meta(md.file_type().is_file(), md.uid(), md.mode(), self.uid)?;\n        if md.len() > max {", "        if md.len() > max {"),
 ("m25_reply_before_flush", D+"engine.rs", "            self.flush();\n            let _ = r.reply.send(resp);", "            let _ = r.reply.send(resp);\n            tokio::time::sleep(Duration::from_millis(300)).await;\n            self.flush();"),
 ("m26_kk_stale_epoch_accepted", D+"engine.rs", "                if epoch <= s.rec.epoch {", "                if false && epoch <= s.rec.epoch {"),
 ("m27_ipc_line_limit_off", D+"engine.rs", "recv_json_line(&mut s, ipc::MAX_REQUEST_LINE)", "recv_json_line(&mut s, 64 * 1024 * 1024)"),
 ("m28_contact_from_peer_claim", D+"engine.rs", "                nickname: nickname_of(&key),", "                nickname: format!(\"{}\\n\\u{1b}[31m\", nickname_of(&key)),"),
]

def sh(cmd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, cwd="/").returncode

only = sys.argv[1:]
env = f". {S}/env.sh; "
results = []
for name, path, old, new in MUTS:
    if only and name not in only:
        continue
    src = open(path).read()
    n = src.count(old)
    if n != 1:
        results.append((name, f"PATCH DID NOT APPLY ({n})"))
        print(name, results[-1][1], flush=True)
        continue
    open(path, "w").write(src.replace(old, new))
    try:
        log = f"{S}/mut/{name}.log"
        os.makedirs(f"{S}/mut", exist_ok=True)
        t0 = time.time()
        b = sh(env + f"cargo build --manifest-path {R}/Cargo.toml --workspace --bins --locked", log + ".build")
        if b != 0:
            res = "DOES NOT COMPILE"
        else:
            sh(env + f"cargo test --manifest-path {R}/Cargo.toml --locked -p coagent-daemon -p coagent-mcp --no-fail-fast -- --skip gate_", log)
            out = open(log).read()
            failed = [l for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
            if failed:
                res = "caught by " + ", ".join(l.split()[1] for l in failed)
            elif "test result: ok" in out and "error" not in out.split("test result")[-1][:0]:
                res = "SURVIVED"
            else:
                res = "HARNESS ERROR"
        results.append((name, res))
        print(f"{name}: {res} ({int(time.time()-t0)} s)", flush=True)
    finally:
        open(path, "w").write(src)
json.dump(results, open(f"{S}/mut/results.json", "w"), indent=1)
