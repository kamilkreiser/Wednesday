//! QA-RELAY-RECONNECT-R2 (the short re-check): window probes of the RR-1 fix, wider than the
//! builder's `rr_window`. Written by the re-checker; NOT part of the branch.
//! Partly adapted from the first check's `gate_relay_reconnect_tests/qrr_q1.rs` (pair_talk,
//! the ender thread, the pin decoding), changed: every probe runs N rounds (default 20,
//! `QRR2_N`), counts losses and old pins instead of panicking at the first one, and recovers.
//!
//! A "loss": an accepted invite/join that does not end in a working pair (both connected and one
//! message each way, exactly once), or whose new relay is gone / restarted 600 ms later, or
//! (for joins) where the ENDED session's relay is still running 600 ms after the new pair.
//! An "old pin": a new invitation line carrying the ended session's relay pin.
mod common;
mod rr_support;

use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use common::*;
use rr_support::*;
use serde_json::{json, Value};

const APPLIED: &str = "the peer's end was applied before this command";

fn rounds() -> usize {
    std::env::var("QRR2_N")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(20)
}

fn log_of(run: &Run, i: usize) -> String {
    String::from_utf8_lossy(&std::fs::read(&run.daemons[i].stderr).unwrap_or_default()).to_string()
}

fn tail(run: &Run, i: usize) -> String {
    let s = log_of(run, i);
    let l: Vec<&str> = s.lines().collect();
    l[l.len().saturating_sub(10)..].join(" | ")
}

fn wait_for(t: Duration, mut f: impl FnMut() -> bool) -> bool {
    let t0 = Instant::now();
    while t0.elapsed() < t {
        if f() {
            return true;
        }
        std::thread::sleep(Duration::from_millis(50));
    }
    false
}

fn connected(d: &Path) -> bool {
    status_of(d)["session"]["connected"] == true
}

fn ended(d: &Path) -> bool {
    status_of(d)["session"]["ended"] == true
}

/// One message each way, each received exactly once (no panic: Err on a miss).
fn talk(dx: &Path, dy: &Path, tag: &str) -> Result<(), String> {
    for (from, to, t) in [(dx, dy, format!("{tag}-x")), (dy, dx, format!("{tag}-y"))] {
        let r = ctl(from, "send", json!({"kind": "chat", "text": t}));
        if r["ok"] != true {
            return Err(format!("send {t}: {r}"));
        }
        let mut got: Vec<String> = vec![];
        let t0 = Instant::now();
        while got.is_empty() && t0.elapsed() < Duration::from_secs(20) {
            got.extend(texts(&inbox(to)));
            std::thread::sleep(Duration::from_millis(50));
        }
        std::thread::sleep(Duration::from_millis(300));
        got.extend(texts(&inbox(to)));
        if got != vec![t.clone()] {
            return Err(format!("expected exactly [{t}], got {got:?}"));
        }
    }
    Ok(())
}

/// Invite on `a`, join on `b`, connected, talk (panics: used for set-up only).
fn pair_talk(run: &mut Run, a: usize, b: usize, tag: &str) {
    let (da, db) = (run.dir(a), run.dir(b));
    let inv = run.ctl(a, "invite", json!({}));
    assert_eq!(inv["ok"], true, "{tag}: invite {inv}");
    run.status(a);
    let line = inv["result"]["line"].as_str().unwrap().to_string();
    let j = run.ctl(b, "join", json!({ "blob": line }));
    assert_eq!(j["ok"], true, "{tag}: join {j}");
    run.wait_connected(a, b);
    run.status(a);
    talk(&da, &db, tag).unwrap_or_else(|e| panic!("{tag}: {e}"));
}

fn pin_of_line(line: &str) -> String {
    let b64 = line.trim_start_matches("coagent join ");
    let raw = data_encoding::BASE64URL_NOPAD
        .decode(b64.as_bytes())
        .expect("invite line decodes");
    let v: Value = serde_json::from_slice(&raw).expect("invite line is JSON");
    v["relays"][0]["pin"].as_str().unwrap().to_lowercase()
}

/// `ender` sends `end` 300 ms from now on its own thread; meanwhile `clients` threads call `op`
/// in a tight loop (starting at once) until one is accepted. A refusal other than
/// `session_active` is returned too (it is a finding). Returns (the first accepted or other
/// reply, the number of `session_active` refusals seen after the end's reply came back).
fn race(ender: &Path, clients: usize, op: Arc<dyn Fn() -> Value + Send + Sync>) -> (Value, usize) {
    let e = ender.to_path_buf();
    let end_done = Arc::new(AtomicBool::new(false));
    let ed = end_done.clone();
    let et = std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(300));
        let r = ctl(&e, "end", json!({}));
        ed.store(true, Ordering::SeqCst);
        r
    });
    let t0 = Instant::now();
    let got = Arc::new(Mutex::new(Vec::<Value>::new()));
    let stop = Arc::new(AtomicBool::new(false));
    let late_refusals = Arc::new(AtomicUsize::new(0));
    let mut hs = vec![];
    for _ in 0..clients {
        let (g, s, op, ed, lr) = (
            got.clone(),
            stop.clone(),
            op.clone(),
            end_done.clone(),
            late_refusals.clone(),
        );
        hs.push(std::thread::spawn(move || {
            while !s.load(Ordering::SeqCst) && t0.elapsed() < Duration::from_secs(20) {
                let r = op();
                if r["ok"] == true || r["error"]["code"] != "session_active" {
                    g.lock().unwrap().push(r);
                    s.store(true, Ordering::SeqCst);
                } else if ed.load(Ordering::SeqCst) {
                    lr.fetch_add(1, Ordering::SeqCst);
                }
            }
        }));
    }
    for h in hs {
        h.join().unwrap();
    }
    let er = et.join().unwrap();
    assert_eq!(er["ok"], true, "the end: {er}");
    let v = got.lock().unwrap().clone();
    assert!(!v.is_empty(), "nothing accepted within 20 s");
    (v[0].clone(), late_refusals.load(Ordering::SeqCst))
}

fn summary(name: &str, n: usize, losses: &[String], old_pins: &[String], reach: usize) {
    eprintln!(
        "QRR2 {name}: {n} rounds, {} lost, {} old pins; the end applied by the command itself (log line) {reach} times",
        losses.len(),
        old_pins.len()
    );
}

/// Item 2, probe 1: the guest ends; the HOST then calls `invite` back to back inside the window:
/// the first accepted, the second (sent at once) must be refused `session_active` and must not
/// touch the first one's relay. One client, so the second invite follows the first directly.
#[test]
fn qrr2_a_two_invites_back_to_back_inside_the_window() {
    let n = rounds();
    let mut run = Run::new("q2a");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let (mut losses, mut old_pins) = (vec![], vec![]);
    for round in 0..n {
        let pin_old = host_pin(&da).to_lowercase();
        run.status(a);
        let d2 = da.clone();
        let (inv, _) = race(&db, 1, Arc::new(move || ctl(&d2, "invite", json!({}))));
        let second = ctl(&da, "invite", json!({}));
        let rp = relay_pid(&da);
        run.status(a);
        let res = (|| -> Result<(), String> {
            if inv["ok"] != true {
                return Err(format!("first invite refused: {inv}"));
            }
            if second["error"]["code"] != "session_active" {
                return Err(format!("the second invite was not refused session_active: {second}"));
            }
            let line = inv["result"]["line"].as_str().unwrap().to_string();
            if pin_of_line(&line) == pin_old {
                old_pins.push(format!("round {round}: {pin_old}"));
            }
            std::thread::sleep(Duration::from_millis(600));
            if relay_pid(&da) != rp || rp.is_none() {
                return Err(format!("the invitation's relay {rp:?} is not the one running 600 ms later {:?}", relay_pid(&da)));
            }
            let j = ctl(&db, "join", json!({ "blob": line }));
            if j["ok"] != true {
                return Err(format!("join {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&da) && connected(&db)) {
                return Err("not connected within 30 s".into());
            }
            talk(&da, &db, &format!("a{round}"))
        })();
        if let Err(e) = res {
            losses.push(format!("round {round}: {e}; host log: {}", tail(&run, a)));
            let _ = ctl(&da, "end", json!({}));
            let _ = ctl(&db, "end", json!({}));
            std::thread::sleep(Duration::from_millis(400));
            pair_talk(&mut run, a, b, &format!("ra{round}"));
        }
    }
    let reach = log_of(&run, a).matches(APPLIED).count();
    summary("two_invites_back_to_back", n, &losses, &old_pins, reach);
    assert!(losses.is_empty() && old_pins.is_empty(), "losses {losses:#?} old pins {old_pins:#?}");
    assert!(reach > 0, "reach: no invite landed inside the window");
    run.finish();
}

/// Item 2, probe 2: invites already IN FLIGHT when the end is applied: four clients start firing
/// invites 300 ms BEFORE the guest's end, so requests are queued in the host's IPC channel across
/// the moment the end frame is applied (an invite cannot be mid-way inside the engine across the
/// end: while the session is live it is refused at once, READ `cmd_invite`). Exactly one accepted.
#[test]
fn qrr2_b_end_arrives_while_invites_are_in_flight() {
    let n = rounds();
    let mut run = Run::new("q2b");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let (mut losses, mut old_pins) = (vec![], vec![]);
    let mut queued_after_end = 0;
    for round in 0..n {
        let pin_old = host_pin(&da).to_lowercase();
        run.status(a);
        let d2 = da.clone();
        let (inv, late) = race(&db, 4, Arc::new(move || ctl(&d2, "invite", json!({}))));
        queued_after_end += late;
        let rp = relay_pid(&da);
        run.status(a);
        let res = (|| -> Result<(), String> {
            if inv["ok"] != true {
                return Err(format!("invite refused: {inv}"));
            }
            let line = inv["result"]["line"].as_str().unwrap().to_string();
            if pin_of_line(&line) == pin_old {
                old_pins.push(format!("round {round}: {pin_old}"));
            }
            std::thread::sleep(Duration::from_millis(600));
            if relay_pid(&da) != rp || rp.is_none() {
                return Err(format!("relay {rp:?} -> {:?} 600 ms later", relay_pid(&da)));
            }
            let j = ctl(&db, "join", json!({ "blob": line }));
            if j["ok"] != true {
                return Err(format!("join {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&da) && connected(&db)) {
                return Err("not connected within 30 s".into());
            }
            talk(&da, &db, &format!("b{round}"))
        })();
        if let Err(e) = res {
            losses.push(format!("round {round}: {e}; host log: {}", tail(&run, a)));
            let _ = ctl(&da, "end", json!({}));
            let _ = ctl(&db, "end", json!({}));
            std::thread::sleep(Duration::from_millis(400));
            pair_talk(&mut run, a, b, &format!("rb{round}"));
        }
    }
    let reach = log_of(&run, a).matches(APPLIED).count();
    summary("end_while_invites_in_flight", n, &losses, &old_pins, reach);
    eprintln!("QRR2 end_while_invites_in_flight: session_active refusals answered after the end's reply: {queued_after_end}");
    assert!(losses.is_empty() && old_pins.is_empty(), "losses {losses:#?} old pins {old_pins:#?}");
    assert!(reach > 0, "reach: no invite landed inside the window");
    run.finish();
}

/// Item 2, probe 3: the HOST ends. The window is then on the GUEST, which holds the ended
/// session's link: the guest calls `invite` in a tight loop and becomes the host of the next
/// session (roles swap each round). Its NEW relay must survive and the pair must talk.
#[test]
fn qrr2_c_host_ends_guest_invites_inside_its_window() {
    let n = rounds();
    let mut run = Run::new("q2c");
    let x = run.daemon("x", &[]);
    let y = run.daemon("y", &[]);
    run.pair(x, y);
    let (mut host, mut guest) = (x, y);
    let (mut losses, mut old_pins) = (vec![], vec![]);
    for round in 0..n {
        let (dh, dg) = (run.dir(host), run.dir(guest));
        let pin_old = host_pin(&dh).to_lowercase();
        run.status(host);
        let d2 = dg.clone();
        let (inv, _) = race(&dh, 1, Arc::new(move || ctl(&d2, "invite", json!({}))));
        let rp = relay_pid(&dg);
        run.status(guest);
        let res = (|| -> Result<(), String> {
            if inv["ok"] != true {
                return Err(format!("invite refused: {inv}"));
            }
            let line = inv["result"]["line"].as_str().unwrap().to_string();
            if pin_of_line(&line) == pin_old {
                old_pins.push(format!("round {round}: {pin_old}"));
            }
            std::thread::sleep(Duration::from_millis(600));
            if relay_pid(&dg) != rp || rp.is_none() {
                return Err(format!("the new host's relay {rp:?} -> {:?} 600 ms later", relay_pid(&dg)));
            }
            let j = ctl(&dh, "join", json!({ "blob": line }));
            if j["ok"] != true {
                return Err(format!("join {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&dh) && connected(&dg)) {
                return Err("not connected within 30 s".into());
            }
            talk(&dg, &dh, &format!("c{round}"))
        })();
        match res {
            Ok(()) => std::mem::swap(&mut host, &mut guest),
            Err(e) => {
                losses.push(format!("round {round}: {e}; new host log: {}", tail(&run, guest)));
                let _ = ctl(&dh, "end", json!({}));
                let _ = ctl(&dg, "end", json!({}));
                std::thread::sleep(Duration::from_millis(400));
                pair_talk(&mut run, host, guest, &format!("rc{round}"));
            }
        }
    }
    let reach = log_of(&run, x).matches(APPLIED).count() + log_of(&run, y).matches(APPLIED).count();
    summary("host_ends_guest_invites", n, &losses, &old_pins, reach);
    assert!(losses.is_empty() && old_pins.is_empty(), "losses {losses:#?} old pins {old_pins:#?}");
    assert!(reach > 0, "reach: no invite landed inside the window");
    run.finish();
}

/// Item 2, probe 4: `join` inside the window, on the HOST: the guest ends; the host (holding the
/// ended session's relay and link) joins a THIRD daemon's prepared invitation in a tight loop.
/// The new pair must talk, and the ended session's relay must be gone 600 ms after the pairing.
#[test]
fn qrr2_d_host_joins_a_third_party_inside_its_window() {
    let n = rounds();
    let mut run = Run::new("q2d");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    let c = run.daemon("c", &[]);
    run.pair(a, b);
    let (da, db, dc) = (run.dir(a), run.dir(b), run.dir(c));
    let mut losses = vec![];
    for round in 0..n {
        let invc = run.ctl(c, "invite", json!({}));
        assert_eq!(invc["ok"], true, "C's invite: {invc}");
        run.status(c);
        let line: String = invc["result"]["line"].as_str().unwrap().to_string();
        let old = relay_pids_of(&da);
        run.status(a);
        let (d2, l2) = (da.clone(), line.clone());
        let (j, _) = race(&db, 1, Arc::new(move || ctl(&d2, "join", json!({ "blob": l2 }))));
        let res = (|| -> Result<(), String> {
            if j["ok"] != true {
                return Err(format!("join refused: {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&da) && connected(&dc)) {
                return Err("A and C not connected within 30 s".into());
            }
            std::thread::sleep(Duration::from_millis(600));
            let alive_old: Vec<u32> = old.iter().copied().filter(|p| alive(*p)).collect();
            if !alive_old.is_empty() {
                return Err(format!("the ended session's relay/guard {alive_old:?} still running 600 ms after the new pair"));
            }
            talk(&dc, &da, &format!("d{round}"))
        })();
        if let Err(e) = res {
            losses.push(format!("round {round}: {e}; A log: {}", tail(&run, a)));
        }
        // Reset: A ends its session with C; A hosts B again.
        let _ = ctl(&da, "end", json!({}));
        let _ = ctl(&dc, "end", json!({}));
        wait_for(Duration::from_secs(10), || ended(&dc));
        std::thread::sleep(Duration::from_millis(300));
        pair_talk(&mut run, a, b, &format!("rd{round}"));
    }
    let reach = log_of(&run, a).matches(APPLIED).count();
    summary("host_joins_third_party", n, &losses, &[], reach);
    assert!(losses.is_empty(), "losses {losses:#?}");
    assert!(reach > 0, "reach: no join landed inside the window");
    run.finish();
}

/// Item 2, probe 5: `join` inside the window, on the GUEST: the host ends; the guest (holding the
/// ended session's link) joins a THIRD daemon's prepared invitation in a tight loop. The new pair
/// must talk; the old host's relay is gone (its own end).
#[test]
fn qrr2_e_guest_joins_a_third_party_inside_its_window() {
    let n = rounds();
    let mut run = Run::new("q2e");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    let c = run.daemon("c", &[]);
    run.pair(a, b);
    let (da, db, dc) = (run.dir(a), run.dir(b), run.dir(c));
    let mut losses = vec![];
    for round in 0..n {
        let invc = run.ctl(c, "invite", json!({}));
        assert_eq!(invc["ok"], true, "C's invite: {invc}");
        run.status(c);
        let line: String = invc["result"]["line"].as_str().unwrap().to_string();
        let old = relay_pids_of(&da);
        run.status(a);
        let (d2, l2) = (db.clone(), line.clone());
        let (j, _) = race(&da, 1, Arc::new(move || ctl(&d2, "join", json!({ "blob": l2 }))));
        let res = (|| -> Result<(), String> {
            if j["ok"] != true {
                return Err(format!("join refused: {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&db) && connected(&dc)) {
                return Err("B and C not connected within 30 s".into());
            }
            std::thread::sleep(Duration::from_millis(600));
            let alive_old: Vec<u32> = old.iter().copied().filter(|p| alive(*p)).collect();
            if !alive_old.is_empty() {
                return Err(format!("the old host's relay {alive_old:?} still running"));
            }
            if status_of(&da)["session"]["attached"] == true {
                return Err("the old host shows the guest attached after the end".into());
            }
            talk(&dc, &db, &format!("e{round}"))
        })();
        if let Err(e) = res {
            losses.push(format!("round {round}: {e}; B log: {}", tail(&run, b)));
        }
        let _ = ctl(&db, "end", json!({}));
        let _ = ctl(&dc, "end", json!({}));
        wait_for(Duration::from_secs(10), || ended(&dc));
        std::thread::sleep(Duration::from_millis(300));
        pair_talk(&mut run, a, b, &format!("re{round}"));
    }
    let reach = log_of(&run, b).matches(APPLIED).count();
    summary("guest_joins_third_party", n, &losses, &[], reach);
    assert!(losses.is_empty(), "losses {losses:#?}");
    assert!(reach > 0, "reach: no join landed inside the window");
    run.finish();
}

/// Item 2, probe 6: a restart of the HOST daemon between the end and the invite. The guest ends;
/// the moment the host's status shows the end applied, the host is stopped (even rounds SIGTERM,
/// odd rounds SIGKILL) and started again; then `invite` is called in a tight loop (20 s budget).
/// The invitation must be accepted, its relay must survive, carry a NEW pin, pair and talk.
#[test]
fn qrr2_f_host_restart_between_the_end_and_the_invite() {
    let n = rounds();
    let mut run = Run::new("q2f");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let (mut losses, mut old_pins) = (vec![], vec![]);
    let mut killed_with_relay = 0;
    for round in 0..n {
        let pin_old = host_pin(&da).to_lowercase();
        run.status(a);
        let db2 = db.clone();
        let et = std::thread::spawn(move || ctl(&db2, "end", json!({})));
        // Sample the host until the end is applied, then stop it at once.
        let t0 = Instant::now();
        let mut relay_present = false;
        while t0.elapsed() < Duration::from_secs(10) {
            let s = status_of(&da);
            if s["session"]["ended"] == true {
                relay_present = !s["relay"].is_null();
                break;
            }
        }
        if relay_present {
            killed_with_relay += 1;
        }
        if round % 2 == 0 {
            run.stop(a);
        } else {
            run.crash(a);
        }
        assert_eq!(et.join().unwrap()["ok"], true);
        run.start(a);
        run.status(a);
        let t1 = Instant::now();
        let inv = loop {
            let r = ctl(&da, "invite", json!({}));
            if r["ok"] == true || r["error"]["code"] != "session_active" || t1.elapsed() > Duration::from_secs(20) {
                break r;
            }
            std::thread::sleep(Duration::from_millis(20));
        };
        let rp = relay_pid(&da);
        run.status(a);
        let res = (|| -> Result<(), String> {
            if inv["ok"] != true {
                return Err(format!("invite after the restart not accepted within 20 s: {inv}"));
            }
            let line = inv["result"]["line"].as_str().unwrap().to_string();
            if pin_of_line(&line) == pin_old {
                old_pins.push(format!("round {round}: {pin_old}"));
            }
            std::thread::sleep(Duration::from_millis(600));
            if relay_pid(&da) != rp || rp.is_none() {
                return Err(format!("relay {rp:?} -> {:?} 600 ms later", relay_pid(&da)));
            }
            let j = ctl(&db, "join", json!({ "blob": line }));
            if j["ok"] != true {
                return Err(format!("join {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&da) && connected(&db)) {
                return Err("not connected within 30 s".into());
            }
            talk(&da, &db, &format!("f{round}"))
        })();
        if let Err(e) = res {
            losses.push(format!("round {round} ({}): {e}; host log: {}", if round % 2 == 0 { "SIGTERM" } else { "SIGKILL" }, tail(&run, a)));
            let _ = ctl(&da, "end", json!({}));
            let _ = ctl(&db, "end", json!({}));
            std::thread::sleep(Duration::from_millis(400));
            pair_talk(&mut run, a, b, &format!("rf{round}"));
        }
    }
    summary("host_restart_between_end_and_invite", n, &losses, &old_pins, 0);
    eprintln!("QRR2 host_restart: rounds where the host was stopped while ended with its relay still present: {killed_with_relay}");
    assert!(losses.is_empty() && old_pins.is_empty(), "losses {losses:#?} old pins {old_pins:#?}");
    run.finish();
}

/// Item 3: ordinary cycles, no race: invite, join, connected, one message each way, end
/// (alternating who ends), wait for both ended and the ticks to pass. The relay started for each
/// new invitation is the one still running after the pairing and the messages (never stopped by
/// the new block); each new invitation has a new pin; the new block's log line never appears.
#[test]
fn qrr2_g_ordinary_cycles_untouched() {
    let n = rounds();
    let mut run = Run::new("q2g");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    let (da, db) = (run.dir(a), run.dir(b));
    let mut losses = vec![];
    let mut pins: Vec<String> = vec![];
    for round in 0..n {
        let res = (|| -> Result<(), String> {
            let inv = ctl(&da, "invite", json!({}));
            if inv["ok"] != true {
                return Err(format!("invite {inv}"));
            }
            let rp = relay_pid(&da);
            let line = inv["result"]["line"].as_str().unwrap().to_string();
            let pin = pin_of_line(&line);
            if pins.contains(&pin) {
                return Err(format!("pin {pin} reused from an earlier session"));
            }
            pins.push(pin);
            let j = ctl(&db, "join", json!({ "blob": line }));
            if j["ok"] != true {
                return Err(format!("join {j}"));
            }
            if !wait_for(Duration::from_secs(30), || connected(&da) && connected(&db)) {
                return Err("not connected".into());
            }
            talk(&da, &db, &format!("g{round}"))?;
            if relay_pid(&da) != rp || rp.is_none() {
                return Err(format!("the invitation's relay {rp:?} is not the one running after the pairing: {:?}", relay_pid(&da)));
            }
            let by = if round % 2 == 0 { &db } else { &da };
            let e = ctl(by, "end", json!({}));
            if e["ok"] != true {
                return Err(format!("end {e}"));
            }
            if !wait_for(Duration::from_secs(20), || ended(&da) && ended(&db) && relay_pid(&da).is_none()) {
                return Err("not both ended with the host relay stopped".into());
            }
            std::thread::sleep(Duration::from_millis(300));
            Ok(())
        })();
        run.status(a);
        if let Err(e) = res {
            losses.push(format!("round {round}: {e}; host log: {}", tail(&run, a)));
            let _ = ctl(&da, "end", json!({}));
            let _ = ctl(&db, "end", json!({}));
            std::thread::sleep(Duration::from_millis(400));
        }
    }
    let applied = log_of(&run, a).matches(APPLIED).count() + log_of(&run, b).matches(APPLIED).count();
    eprintln!("QRR2 ordinary: {n} cycles, {} lost, distinct pins {}, new block's log line seen {applied} times", losses.len(), pins.len());
    assert!(losses.is_empty(), "losses {losses:#?}");
    assert_eq!(applied, 0, "the new block fired in an ordinary cycle");
    run.finish();
}

#[allow(dead_code)]
fn _unused(_: PathBuf) {}
