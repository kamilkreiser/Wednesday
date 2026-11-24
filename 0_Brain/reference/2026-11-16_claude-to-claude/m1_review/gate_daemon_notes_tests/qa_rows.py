#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 5: plant ONE change per row into a checkout of the head.
Usage: python3 -B qa_rows.py <checkout root> <row>   (exactly one occurrence of each old text required)
       python3 -B qa_rows.py --list"""
import sys

D = "crates/coagent-daemon/src/"
ROWS = {
    # property 1: the two start checks removed
    "r1": [(D + "main.rs", """            if url.trim().is_empty() {
                eprintln!("{RELAY_URL_EMPTY}");
                return 2;
            }
            if pin.is_empty() {
                eprintln!("{RELAY_PIN_EMPTY}");
                return 2;
            }
""", "")],
    # property 1: connect's no-candidate arm removed (empty join again)
    "r1b": [(D + "link.rs", """        Err(fails) if fails.is_empty() => Err(ConnectFail {
            why: NO_CANDIDATE.into(),
            pin_mismatch: false,
        }),
""", "")],
    # property 2: connect drops the relay client's pin_mismatch
    "r2": [(D + "link.rs", "            pin_mismatch: fails.iter().any(|f| f.error.pin_mismatch),\n",
            "            pin_mismatch: false,\n")],
    # property 2: status always says false (the engine still tracks it)
    "r8": [(D + "engine.rs", '"relay_identity_changed": s.relay_identity_changed,', '"relay_identity_changed": false,')],
    # property 3: both FR-3 branches removed (the on_mb arm and the on_relay_exited failure)
    "r3": [(D + "engine.rs", """            MbEvent::Down(_)
                if waiting
                    && p.role == PairingRole::Inviter
                    && self.cfg.external_relay.is_none()
                    && self.relay.is_some() =>
            {
                p.mb_down.get_or_insert_with(now);
            }
""", ""), (D + "engine.rs", """        if waiting_invite {
            self.fail_pairing_with(None, RELAY_STOPPED_INVITE_TEXT)
                .await;
        }
""", "        let _ = waiting_invite;\n")],
    # property 4: run no longer applies the gate rule
    "r4": [(D + "engine.rs", """    if let Some(t) = gate_refusal(cfg!(windows), cfg.gate.is_some()) {
        return Err(t.to_string());
    }
""", "")],
    # property 4: the help's Command Prompt lines removed
    "r4b": [(D + "main.rs", """  run on Windows).
  In the Command Prompt a ctl request is the JSON in double quotes, each inner \\" written \\\\\\":
  coagentd ctl --data-dir <dir> \\"{\\\\\\"v\\\\\\":1,\\\\\\"id\\\\\\":1,\\\\\\"cmd\\\\\\":\\\\\\"status\\\\\\"}\\"";""",
             """  run on Windows).";""")],
    # property 5: invite.rs's stale sentence back (a different file from the builder's lib.rs row)
    "r5": [(D + "invite.rs", """//! A second blob kind, `relay.moved`, carries new relay candidates for an existing session when the
//! joiner's stored candidate no longer reaches the convener's relay: after a restart of the
//! convener's whole program without `--keep-relay-identity` (a new certificate), when a saved
//! identity was replaced or moved away, or when the relay came back on another port. A relay child
//! restarted within the session keeps its certificate (`relay_child`), so it needs no line. It
//! carries no secret: a wrong pin can only send the joiner to a relay that cannot complete the
//! session's handshake.""", """//! A second blob kind, `relay.moved`, carries new relay candidates for an existing session after the
//! convener's relay restarted with a new certificate (the restarted `coagent relay` generates a new
//! one; see DESIGN QUESTIONS in STATUS). It carries no secret: a wrong pin can only send the joiner to
//! a relay that cannot complete the session's handshake.""")],
    # property 6 (R6-2): the refill leaves row 54's clock set
    "r6": [(D + "recovery.rs", """            self.skips_left = self.cfg.max_skips;
            self.skips_spent_at = None;
        }
        if m.seq == 0 {""", """            self.skips_left = self.cfg.max_skips;
        }
        if m.seq == 0 {""")],
    # property 8 (G29 / FR-9 b): a wrong timeout_s type falls back to the default again
    "r7": [("crates/coagent-mcp/src/main.rs", """            .map(|t| t.clamp(1, WAIT_MAX_S))
            .ok_or(WAIT_TIMEOUT_TYPE_TEXT),""", """            .map(|t| t.clamp(1, WAIT_MAX_S))
            .or(Some(WAIT_DEFAULT_S))
            .ok_or(WAIT_TIMEOUT_TYPE_TEXT),""")],
}

if sys.argv[1] == "--list":
    print(" ".join(ROWS))
    sys.exit(0)
root, row = sys.argv[1], sys.argv[2]
for path, old, new in ROWS[row]:
    p = f"{root}/{path}"
    s = open(p, encoding="utf-8").read()
    c = s.count(old)
    if c != 1:
        sys.exit(f"{row}: {path}: old text found {c} times")
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
print(f"{row}: planted {len(ROWS[row])} change(s)")
