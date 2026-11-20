//! QA-RELAY-RECONNECT (independent check): probes of the Q1 fix (addendum 2) against real daemons.
//! Written by the checker; not part of the branch.
mod common;
mod rr_support;

use std::time::{Duration, Instant};

use common::*;
use rr_support::*;
use serde_json::json;

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
    send(&da, &format!("{tag}-a"));
    send(&db, &format!("{tag}-b"));
    exactly(&db, &[format!("{tag}-a").as_str()]);
    exactly(&da, &[format!("{tag}-b").as_str()]);
}

fn wait_ended_both(da: &std::path::Path, db: &std::path::Path) {
    wait_until("both ended, host relay stopped", Duration::from_secs(20), || {
        status_of(da)["session"]["ended"] == true
            && status_of(db)["session"]["ended"] == true
            && relay_pid(da).is_none()
    });
}

/// THE WINDOW: the guest ends; the host's invite is sent in a tight loop and accepted the moment the
/// host has seen the end, which is BEFORE the next 100 ms tick ran the ended session's clean-up
/// (the old relay is still running then and the invite reuses it). Then the clean-up runs.
/// Repeated `QRR_N` times (default 8); counts how often the invite landed in the window and
/// whether the new invitation's relay survived and the pair completed.
#[test]
fn qrr_q1_invite_inside_the_window_before_the_tick() {
    let n: usize = std::env::var("QRR_N").ok().and_then(|v| v.parse().ok()).unwrap_or(8);
    let mut run = Run::new("qq1w");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let mut in_window = 0;
    let mut failures = vec![];
    for round in 0..n {
        let old_relay = relay_pid(&da).expect("host relay");
        run.status(a);
        let db2 = db.clone();
        let ender = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(300));
            ctl(&db2, "end", json!({}))
        });
        let t0 = Instant::now();
        // QRR_FLOOD threads fire invites in parallel so one is queued in the daemon's IPC
        // channel the moment the end is processed (default 1 = the plain tight loop).
        let flood: usize = std::env::var("QRR_FLOOD").ok().and_then(|v| v.parse().ok()).unwrap_or(1);
        let got = std::sync::Arc::new(std::sync::Mutex::new(Vec::<serde_json::Value>::new()));
        let stop = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
        let mut hs = vec![];
        for _ in 0..flood {
            let (got, stop, da2) = (got.clone(), stop.clone(), da.clone());
            hs.push(std::thread::spawn(move || {
                while !stop.load(std::sync::atomic::Ordering::SeqCst) && t0.elapsed() < Duration::from_secs(20) {
                    let r = ctl(&da2, "invite", json!({}));
                    if r["ok"] == true {
                        got.lock().unwrap().push(r);
                        stop.store(true, std::sync::atomic::Ordering::SeqCst);
                    }
                }
            }));
        }
        for h in hs { h.join().unwrap(); }
        assert_eq!(ender.join().unwrap()["ok"], true);
        let oks = got.lock().unwrap().clone();
        assert_eq!(oks.len(), 1, "round {round}: exactly one invite accepted: {oks:?}");
        let inv = oks[0].clone();
        let after = status_of(&da);
        let reused = after["relay"]["relay_pid"].as_u64().map(|p| p as u32) == Some(old_relay);
        if reused {
            in_window += 1;
        }
        run.status(a);
        std::thread::sleep(Duration::from_millis(600));
        let alive_now = relay_pid(&da).is_some();
        let line = inv["result"]["line"].as_str().unwrap().to_string();
        let j = run.ctl(b, "join", json!({ "blob": line }));
        eprintln!(
            "QRR round {round}: invite reused the ended session's relay = {reused}; relay running 600 ms later = {alive_now}; join = {j}"
        );
        if j["ok"] != true || !alive_now {
            failures.push(format!(
                "round {round} (reused old relay: {reused}): relay alive {alive_now}; join {j}; host log tail: {}",
                tail(&run, 0)
            ));
            // recover for the next round: fresh invitation
            let _ = run.ctl(a, "end", json!({}));
            std::thread::sleep(Duration::from_millis(300));
            pair_talk(&mut run, a, b, &format!("recover{round}"));
            continue;
        }
        run.wait_connected(a, b);
        run.status(a);
        send(&da, &format!("w{round}"));
        exactly(&db, &[format!("w{round}").as_str()]);
    }
    eprintln!("QRR window summary: {in_window} of {n} invites landed inside the window; failures {}", failures.len());
    assert!(failures.is_empty(), "Q1 fault reachable: {failures:#?}");
    run.finish();
}

fn tail(run: &Run, i: usize) -> String {
    let s = String::from_utf8_lossy(&std::fs::read(&run.daemons[i].stderr).unwrap_or_default()).to_string();
    let l: Vec<&str> = s.lines().collect();
    l[l.len().saturating_sub(12)..].join(" | ")
}

/// Guest-side window: the host ends and invites at once; the guest joins in a tight loop the moment
/// it has seen the end (before its own tick's clean-up). The pair must complete and talk.
#[test]
fn qrr_q1_guest_joins_inside_its_window() {
    let mut run = Run::new("qq1g");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    for round in 0..4 {
        assert_eq!(run.ctl(a, "end", json!({}))["ok"], true);
        let inv = run.ctl(a, "invite", json!({}));
        assert_eq!(inv["ok"], true, "{inv}");
        run.status(a);
        let line = inv["result"]["line"].as_str().unwrap().to_string();
        let t0 = Instant::now();
        let j = loop {
            let j = run.ctl(b, "join", json!({ "blob": line }));
            if j["ok"] == true || j["error"]["code"] != "session_active" {
                break j;
            }
            assert!(t0.elapsed() < Duration::from_secs(20), "join never accepted: {j}");
        };
        assert_eq!(j["ok"], true, "round {round}: join {j}; guest log {}", tail(&run, 1));
        run.wait_connected(a, b);
        run.status(a);
        send(&db, &format!("g{round}"));
        exactly(&da, &[format!("g{round}").as_str()]);
    }
    run.finish();
}

/// Two ends in a row (host twice; then guest and host crossing), then a new invitation pairs.
#[test]
fn qrr_q1_two_ends_in_a_row_then_invite() {
    let mut run = Run::new("qq1e");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    assert_eq!(run.ctl(a, "end", json!({}))["ok"], true);
    let e2 = run.ctl(a, "end", json!({}));
    assert_eq!(e2["ok"], true, "{e2}");
    wait_ended_both(&da, &db);
    pair_talk(&mut run, a, b, "x1");
    // crossing ends
    let e_b = run.ctl(b, "end", json!({}));
    let e_a = run.ctl(a, "end", json!({}));
    assert_eq!(e_b["ok"], true);
    assert_eq!(e_a["ok"], true);
    wait_ended_both(&da, &db);
    std::thread::sleep(Duration::from_millis(400));
    pair_talk(&mut run, a, b, "x2");
    run.finish();
}

/// Four rounds alternating who ends, each followed by invite, pair, a message each way; the last
/// invitation is made 5 s (50 ticks) after its end.
#[test]
fn qrr_q1_four_rounds_alternating_and_late() {
    let mut run = Run::new("qq1r");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    for round in 0..4 {
        let by = if round % 2 == 0 { b } else { a };
        assert_eq!(run.ctl(by, "end", json!({}))["ok"], true);
        wait_ended_both(&da, &db);
        if round == 3 {
            std::thread::sleep(Duration::from_secs(5));
        }
        pair_talk(&mut run, a, b, &format!("r{round}"));
    }
    run.finish();
}

/// The protection: the guest ends the CURRENT session: the host's link closes and its relay stops;
/// and the HOST ends: the guest's link closes, and it does not keep reconnecting (reconnects and
/// attached stay put for 3 s).
#[test]
fn qrr_q1_protection_both_directions() {
    let mut run = Run::new("qq1p");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let old = relay_pids_of(&da);
    assert_eq!(run.ctl(b, "end", json!({}))["ok"], true);
    wait_until("host: ended, link closed, relay stopped", Duration::from_secs(20), || {
        let s = status_of(&da);
        s["session"]["ended"] == true && s["session"]["attached"] == false && s["relay"].is_null()
    });
    wait_gone(&old, "old relay gone");
    // now the other direction on a new session
    pair_talk(&mut run, a, b, "p2");
    let old = relay_pids_of(&da);
    assert_eq!(run.ctl(a, "end", json!({}))["ok"], true);
    wait_until("guest: ended, detached", Duration::from_secs(20), || {
        let s = status_of(&db);
        s["session"]["ended"] == true && s["session"]["attached"] == false
    });
    wait_gone(&old, "host relay gone after own end");
    let r0 = status_of(&db)["session"]["reconnects"].clone();
    std::thread::sleep(Duration::from_secs(3));
    let s = status_of(&db);
    assert_eq!(s["session"]["attached"], false, "guest re-attached after the host ended: {s}");
    assert_eq!(s["session"]["reconnects"], r0, "guest kept reconnecting after the end: {s}");
    eprintln!("QRR guest after host end: {}", s["session"]);
    run.finish();
}

/// Observe the window: after the guest ends, sample the host's status as fast as ctl allows and
/// record every (ended, relay present) pair seen, with the time since the end.
#[test]
fn qrr_q1_observe_the_window() {
    let mut run = Run::new("qq1o");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let da = run.dir(a);
    let mut seen_window = 0;
    for round in 0..5 {
        run.status(a);
        let db2 = run.dir(b);
        let ender = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(300));
            ctl(&db2, "end", json!({}))
        });
        let t0 = Instant::now();
        let mut samples = vec![];
        loop {
            let s = status_of(&da);
            let e = s["session"]["ended"] == true;
            let r = !s["relay"].is_null();
            samples.push((t0.elapsed().as_millis(), e, r));
            if e && r {
                seen_window += 1;
            }
            if !r || t0.elapsed() > Duration::from_secs(10) {
                break;
            }
        }
        assert_eq!(ender.join().unwrap()["ok"], true);
        let interesting: Vec<_> = samples.iter().filter(|x| x.1).collect();
        eprintln!("QRR observe round {round}: {} samples; those with ended=true: {interesting:?}", samples.len());
        pair_talk(&mut run, a, b, &format!("o{round}"));
    }
    eprintln!("QRR observe: samples inside the window (ended and relay present): {seen_window}");
    run.finish();
}

/// F1's identity side: an invite accepted inside the window carries the ENDED session's relay and
/// pin (R1: the identity is erased at the session's end).
#[test]
fn qrr_q1_window_invite_carries_the_old_pin() {
    let mut run = Run::new("qq1k");
    let a = run.daemon("a", &[]);
    let b = run.daemon("b", &[]);
    run.pair(a, b);
    let (da, db) = (run.dir(a), run.dir(b));
    let mut same_pin = 0;
    for round in 0..4 {
        let pin_old = host_pin(&da);
        run.status(a);
        let db2 = db.clone();
        let ender = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(300));
            ctl(&db2, "end", json!({}))
        });
        let t0 = Instant::now();
        let inv = loop {
            let r = run.ctl(a, "invite", json!({}));
            if r["ok"] == true { break r; }
            assert!(t0.elapsed() < Duration::from_secs(20));
        };
        ender.join().unwrap();
        let line = inv["result"]["line"].as_str().unwrap();
        let b64 = line.trim_start_matches("coagent join ");
        let raw = data_encoding::BASE64URL_NOPAD.decode(b64.as_bytes()).unwrap();
        let v: serde_json::Value = serde_json::from_slice(&raw).unwrap();
        let pin_new = v["relays"][0]["pin"].as_str().unwrap().to_string();
        eprintln!("QRR round {round}: old session pin {pin_old}; new invitation pin {pin_new}; same = {}", pin_new == pin_old);
        if pin_new == pin_old { same_pin += 1; }
        std::thread::sleep(Duration::from_millis(500));
        // fresh start for the next round
        let _ = run.ctl(a, "end", json!({}));
        pair_talk(&mut run, a, b, &format!("k{round}"));
    }
    eprintln!("QRR window invitations that carried the ended session's pin: {same_pin} of 4");
    run.finish();
}
