//! QA GATE round 4 (M1 DAEMON, head feedc60): the gate's own attack tests. Findings only.
//! In-process daemons with a transport tap (the crate's `Tap`), in the style of `recovery_repro.rs`.
mod common;
#[rustfmt::skip]
#[path = "gate/gate_hostile/mod.rs"]
mod gate_hostile;

use std::path::Path;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering::SeqCst};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use coagent_daemon::link::{Dir, Tap, TapVerdict};
use common::*;
use serde_json::{json, Value};

/// A relay transport under the test's control (one daemon's links, mailbox and session).
#[derive(Default)]
struct G4 {
    /// Drop inbound SESSION presence lines (`peer.joined` carrying a slot; the mailbox's own
    /// `peer.joined` has no slot and passes).
    drop_session_joined: AtomicBool,
    dropped_joined: AtomicUsize,
    /// Cut the connection at every outbound `chan.open` / `chan.create` (the session link cannot
    /// attach; the mailbox is unaffected).
    refuse_session_attach: AtomicBool,
    opens: AtomicUsize,
    /// Hold the next outbound `chan.open` this long (once): the joiner's first attach then reaches
    /// the relay after the convener created the channel, so the pairing race of ruling (e) cannot
    /// happen and rescue the pair.
    delay_open_ms: std::sync::atomic::AtomicU64,
    log: Mutex<Vec<String>>,
}

impl Tap for G4 {
    fn frame(&self, dir: Dir, binary: bool, bytes: &[u8]) -> TapVerdict {
        if binary {
            return TapVerdict::Pass;
        }
        let s = String::from_utf8_lossy(bytes).to_string();
        match dir {
            Dir::Out => {
                if s.contains("chan.open") || s.contains("chan.create") {
                    self.opens.fetch_add(1, SeqCst);
                    let ms = self.delay_open_ms.swap(0, SeqCst);
                    if ms > 0 && s.contains("chan.open") {
                        std::thread::sleep(Duration::from_millis(ms));
                    }
                    if self.refuse_session_attach.load(SeqCst) {
                        return TapVerdict::Disconnect;
                    }
                }
            }
            Dir::In => {
                if s.contains("peer.joined") && s.contains("\"slot\"") {
                    self.log.lock().unwrap().push(s.clone());
                    if self.drop_session_joined.load(SeqCst) {
                        self.dropped_joined.fetch_add(1, SeqCst);
                        return TapVerdict::Drop;
                    }
                }
            }
        }
        TapVerdict::Pass
    }
}

fn start(run: &mut Run, name: &str, tap: &Arc<G4>) -> InProc {
    let t: Arc<dyn Tap> = tap.clone();
    InProc::start(run, name, Some(t), |c| {
        c.backoff_max = Duration::from_secs(2);
    })
}

fn st(dir: &Path) -> Value {
    ctl(dir, "status", json!({}))["result"].clone()
}

fn sess(dir: &Path) -> Value {
    st(dir)["session"].clone()
}

fn key_of(dir: &Path) -> String {
    st(dir)["key_id"].as_str().unwrap().to_string()
}

fn texts(ms: &[Value]) -> Vec<String> {
    ms.iter()
        .map(|m| m["text"].as_str().unwrap_or_default().to_string())
        .collect()
}

fn gather(dir: &Path, n: usize, t: Duration) -> Vec<Value> {
    let mut got = vec![];
    let t0 = Instant::now();
    while got.len() < n && t0.elapsed() < t {
        got.extend(inbox(dir));
        std::thread::sleep(Duration::from_millis(100));
    }
    got
}

/// Pair WITHOUT waiting for `connected` (the harness's `pair_dirs` waits 30 s for it).
fn pair_nowait(a: &Path, b: &Path) {
    let inv = ctl(a, "invite", json!({}));
    assert_eq!(inv["ok"], true, "invite: {inv}");
    let line = inv["result"]["line"].as_str().unwrap().to_string();
    let j = ctl(b, "join", json!({ "blob": line }));
    assert_eq!(j["ok"], true, "join: {j}");
}

/// G4-1 (design 09 §9 item 1, a SCRATCH state outside the model's generator). A fresh session
/// starts with the PAIRING channel as its live channel (label 0) and no position. In that state
/// T-BLIND (`live.is_none()`), T-KEYING (`live.is_none()`) and "no position" (`live_since`, which
/// `Machine::new` never sets) are all disarmed; only a `peer.joined` to the initiator starts the
/// first key exchange. The relay drops that ONE line (or every session presence line while the
/// pair attaches), then is honest. Safe (V4, V5): every queued message is delivered within 120 s
/// of the relay turning honest.
fn fresh_session_with_suppressed_first_presence(initiator_is_convener: bool, tag: &str) {
    fresh_session_case(initiator_is_convener, tag, false)
}

fn fresh_session_case(initiator_is_convener: bool, tag: &str, delay_joiner: bool) {
    loop {
        let mut run = Run::new(tag);
        let (tc, tj) = (Arc::new(G4::default()), Arc::new(G4::default()));
        let c = start(&mut run, "c", &tc);
        let j = start(&mut run, "j", &tj);
        let c_init = key_of(&c.dir) < key_of(&j.dir);
        if c_init != initiator_is_convener {
            c.stop();
            j.stop();
            run.finish();
            continue;
        }
        // The relay suppresses session presence toward the initiator while the pair attaches.
        let (ti, init_dir, resp_dir) = if c_init {
            (&tc, &c.dir, &j.dir)
        } else {
            (&tj, &j.dir, &c.dir)
        };
        ti.drop_session_joined.store(true, SeqCst);
        if delay_joiner {
            tj.delay_open_ms.store(3000, SeqCst);
        }
        pair_nowait(&c.dir, &j.dir);
        wait_until("both sessions attached", Duration::from_secs(30), || {
            sess(&c.dir)["attached"] == true && sess(&j.dir)["attached"] == true
        });
        std::thread::sleep(Duration::from_secs(3));
        // From here on the relay is honest.
        ti.drop_session_joined.store(false, SeqCst);
        let honest = Instant::now();
        let r1 = ctl(init_dir, "send", json!({"kind": "chat", "text": "MARKER-G4F-i"}));
        let r2 = ctl(resp_dir, "send", json!({"kind": "chat", "text": "MARKER-G4F-r"}));
        assert_eq!(r1["ok"], true, "{r1}");
        assert_eq!(r2["ok"], true, "{r2}");
        let mut got_r = vec![];
        let mut got_i = vec![];
        let mut connected_at = None;
        while honest.elapsed() < Duration::from_secs(150) && (got_r.is_empty() || got_i.is_empty()) {
            got_r.extend(inbox(resp_dir));
            got_i.extend(inbox(init_dir));
            if connected_at.is_none()
                && sess(init_dir)["connected"] == true
                && sess(resp_dir)["connected"] == true
            {
                connected_at = Some(honest.elapsed());
            }
            std::thread::sleep(Duration::from_millis(200));
        }
        let took = honest.elapsed();
        let (si, sr) = (sess(init_dir), sess(resp_dir));
        let dropped = ti.dropped_joined.load(SeqCst);
        eprintln!(
            "G4-1 ({tag}, initiator is the {}): presence lines dropped {dropped}; after the relay turned honest: \
             responder got {:?}, initiator got {:?} in {took:?}; connected at {connected_at:?}\n initiator {si}\n responder {sr}",
            if c_init { "convener" } else { "joiner" },
            texts(&got_r),
            texts(&got_i)
        );
        run.markers.push("MARKER-G4F".into());
        c.stop();
        j.stop();
        run.finish();
        assert!(dropped > 0, "the scenario did not suppress a presence line");
        assert!(
            texts(&got_r) == ["MARKER-G4F-i"] && texts(&got_i) == ["MARKER-G4F-r"],
            "V4/V5: a fresh session whose first peer.joined the relay suppressed did not recover within 150 s \
             of the relay turning honest (responder got {:?}, initiator got {:?}); initiator {si}; responder {sr}",
            texts(&got_r),
            texts(&got_i)
        );
        return;
    }
}

#[test]
fn g4_1a_fresh_session_first_presence_suppressed_initiator_convener() {
    fresh_session_with_suppressed_first_presence(true, "g4_f1a");
}

#[test]
fn g4_1b_fresh_session_first_presence_suppressed_initiator_joiner() {
    fresh_session_with_suppressed_first_presence(false, "g4_f1b");
}

/// G4-1d/e: as G4-1a/b, with the joiner's first `chan.open` held 3 s so the pairing race cannot
/// happen (the deterministic form of R4-1).
#[test]
fn g4_1d_fresh_session_no_race_initiator_convener() {
    fresh_session_case(true, "g4_f1d", true);
}

#[test]
fn g4_1e_fresh_session_no_race_initiator_joiner() {
    fresh_session_case(false, "g4_f1e", true);
}

/// Control for G4-1: the same, with nothing suppressed (positive control of the harness).
#[test]
fn g4_1c_fresh_session_control() {
    let mut run = Run::new("g4_f1c");
    let (tc, tj) = (Arc::new(G4::default()), Arc::new(G4::default()));
    let c = start(&mut run, "c", &tc);
    let j = start(&mut run, "j", &tj);
    let t0 = Instant::now();
    pair_nowait(&c.dir, &j.dir);
    let r1 = ctl(&c.dir, "send", json!({"kind": "chat", "text": "MARKER-G4C-c"}));
    let r2 = ctl(&j.dir, "send", json!({"kind": "chat", "text": "MARKER-G4C-j"}));
    assert_eq!(r1["ok"], true);
    assert_eq!(r2["ok"], true);
    let gj = gather(&j.dir, 1, Duration::from_secs(60));
    let gc = gather(&c.dir, 1, Duration::from_secs(60));
    eprintln!("G4-1c control: {:?} {:?} in {:?}", texts(&gj), texts(&gc), t0.elapsed());
    run.markers.push("MARKER-G4C".into());
    c.stop();
    j.stop();
    run.finish();
    assert_eq!(texts(&gj), ["MARKER-G4C-c"]);
    assert_eq!(texts(&gc), ["MARKER-G4C-j"]);
}

// ---------------------------------------------------------------------------------------------
// G4-0: the same state on the pure machine (no network): `Machine::new(.., live = Some(0), ..)`
// is exactly what `Engine::new_sess` builds for a fresh session (engine.rs `new_sess`).

struct NoCrypto {
    kk_starts: usize,
}
impl coagent_daemon::recovery::Crypto for NoCrypto {
    fn kk_initiate(&mut self) -> Option<(u64, Vec<u8>)> {
        self.kk_starts += 1;
        Some((1, vec![1, 2, 3]))
    }
    fn kk_respond(&mut self, _m: &[u8]) -> Option<(u64, Vec<u8>, String)> {
        None
    }
    fn kk_finish(&mut self, _i: u64, _m: &[u8]) -> Option<u64> {
        None
    }
    fn open(
        &mut self,
        _t: coagent_daemon::recovery::Target,
        _f: &[u8],
    ) -> Result<coagent_daemon::recovery::Content, coagent_daemon::recovery::OpenFail> {
        Err(coagent_daemon::recovery::OpenFail::Behind)
    }
    fn seal(
        &mut self,
        _t: coagent_daemon::recovery::Target,
        _w: coagent_daemon::recovery::Seal<'_>,
        _a: u64,
    ) -> Result<Vec<Vec<u8>>, coagent_daemon::recovery::SealFail> {
        Ok(vec![vec![0u8; 64]])
    }
    fn install(&mut self, _h: u64) -> bool {
        true
    }
    fn close_live(&mut self) {}
    fn forget(&mut self, _h: u64) {}
    fn set_aside(&mut self, _i: &coagent_daemon::store::OutboxItem) -> bool {
        true
    }
}

/// Both roles; each with a message queued right after pairing; the relay attaches the slot and
/// sends NO presence line (suppressed, then honest: an honest relay sends presence only at attach).
fn pure_fresh(initiator: bool) -> (bool, Option<Instant>, usize, usize, Vec<String>) {
    use coagent_daemon::recovery::{Action, Durable, Event, Machine, RecoveryConfig};
    use coagent_daemon::store::{InboxState, OutboxItem, OutboxState};
    let t0 = Instant::now();
    let d = Durable {
        relay_send_seq: 1,
        send_floor: 1,
        ..Default::default()
    };
    let ob = OutboxState {
        send_next: 1,
        items: vec![],
        unsendable: 0,
    };
    let mut m = Machine::new(RecoveryConfig::default(), initiator, d, InboxState::default(), ob, Some(0), t0);
    let mut c = NoCrypto { kk_starts: 0 };
    let mut log = vec![];
    let mut attaches = 0;
    let mut t = t0;
    let item = OutboxItem {
        seq: 1,
        id: "g4".into(),
        kind: "chat.msg".into(),
        re: None,
        body: json!({"text": "x"}),
        ts: "2026-01-01T00:00:00Z".into(),
    };
    let acts = m.step(Event::Queue(Box::new(item)), t, &mut c);
    log.push(format!("{acts:?}"));
    // 600 s of 100 ms ticks; the link attaches at once and stays up (an honest network).
    for k in 0..6000 {
        t = t0 + Duration::from_millis(100 * k);
        let acts = m.step(Event::Tick, t, &mut c);
        for a in &acts {
            if let Action::Attach { .. } = a {
                attaches += 1;
                let _ = m.step(Event::Attached, t, &mut c);
            }
            if let Action::Log(l) = a {
                log.push(l.clone());
            }
        }
    }
    (m.connected(), m.next_deadline(), c.kk_starts, attaches, log)
}

#[test]
fn g4_0_pure_fresh_session_without_presence_has_no_clock() {
    let mut fails = vec![];
    for initiator in [true, false] {
        let (connected, deadline, kk, att, log) = pure_fresh(initiator);
        eprintln!(
            "G4-0 initiator {initiator}: after 600 s attached: connected {connected}, next_deadline {deadline:?}, key exchanges started {kk}, attachments {att}, log {log:?}"
        );
        if !connected && (deadline.is_none() || kk == 0 && att <= 1) {
            fails.push(format!(
                "initiator {initiator}: connected {connected}, outbox 1, next_deadline {deadline:?}, key exchanges {kk}, attachments {att} in 600 s"
            ));
        }
    }
    assert!(
        fails.is_empty(),
        "V5: a fresh session (pairing channel live, no position, outbox not empty) waits with no clock: {fails:?}"
    );
}

/// G4-2 (ruling item e): the pairing race, forced. The convener's session link cannot attach for
/// a while (its `chan.open`/`chan.create` is cut), so the joiner's `chan.open` meets `not_found`
/// again and again, while BOTH sides queue messages. Then the convener may attach. Safe: every
/// message queued on either side arrives exactly once, in order, never labelled repeated; the
/// joiner's re-attachments stay inside the bucket (5 + T/12).
#[test]
fn g4_2_forced_pairing_race_loses_and_duplicates_nothing() {
    let mut run = Run::new("g4_race");
    let (tc, tj) = (Arc::new(G4::default()), Arc::new(G4::default()));
    let c = start(&mut run, "c", &tc);
    let j = start(&mut run, "j", &tj);
    tc.refuse_session_attach.store(true, SeqCst);
    pair_nowait(&c.dir, &j.dir);
    let t0 = Instant::now();
    let n = 20;
    for i in 0..n {
        let a = ctl(&c.dir, "send", json!({"kind": "chat", "text": format!("MARKER-G4R-c{i:02}")}));
        let b = ctl(&j.dir, "send", json!({"kind": "chat", "text": format!("MARKER-G4R-j{i:02}")}));
        assert_eq!(a["ok"], true, "{a}");
        assert_eq!(b["ok"], true, "{b}");
        std::thread::sleep(Duration::from_millis(500));
    }
    let window = t0.elapsed();
    let j_opens = tj.opens.load(SeqCst);
    let sj_mid = sess(&j.dir);
    tc.refuse_session_attach.store(false, SeqCst);
    let freed = Instant::now();
    let gj = gather(&j.dir, n, Duration::from_secs(150));
    let gc = gather(&c.dir, n, Duration::from_secs(60));
    let took = freed.elapsed();
    let reps = gj.iter().chain(gc.iter()).filter(|m| m["possibly_repeated"] == true).count();
    let (sc, sj) = (sess(&c.dir), sess(&j.dir));
    eprintln!(
        "G4-2: joiner chan.open attempts while the convener was held off {j_opens} in {window:?} (bucket bound {}); \
         joiner status then {sj_mid}\n after: joiner got {} convener got {} in {took:?}, repeats {reps}\n c {sc}\n j {sj}",
        5 + window.as_secs() / 12,
        gj.len(),
        gc.len()
    );
    run.markers.push("MARKER-G4R".into());
    c.stop();
    j.stop();
    run.finish();
    let want_j: Vec<String> = (0..n).map(|i| format!("MARKER-G4R-c{i:02}")).collect();
    let want_c: Vec<String> = (0..n).map(|i| format!("MARKER-G4R-j{i:02}")).collect();
    assert_eq!(texts(&gj), want_j, "pairing race: convener -> joiner not exactly once in order");
    assert_eq!(texts(&gc), want_c, "pairing race: joiner -> convener not exactly once in order");
    assert_eq!(reps, 0, "pairing race: a message labelled repeated");
    assert!(
        j_opens as u64 <= 5 + window.as_secs() / 12 + 1,
        "V11: the joiner attached {j_opens} times in {window:?}"
    );
}

// ---------------------------------------------------------------------------------------------
// G4-3 (design 09 row 33, §9 item 6): a HOSTILE PEER states a position far above anything sent.
// Safe: clamped to the highest number sent; the victim stays up and later messages still flow.

fn hostile_position(big: u64, kind: &str, tag: &str) {
    use gate_hostile::*;
    let mut run = Run::new(tag);
    let rs = run.root.join("relay.stderr");
    let relay = ExtRelay::start(&bin("coagent"), &run.home, std::fs::File::create(&rs).unwrap());
    run.extra_stderr.push(rs);
    let b = run.daemon("b", &["--relay-url", &relay.url, "--relay-pin", &relay.pin]);
    let mut a = [0u8; 32];
    hex::decode_to_slice(run.status(b)["key_id"].as_str().unwrap(), &mut a).unwrap();
    let victim = coagent_proto::bytes::KeyId(a);
    let inv = run.ctl(b, "invite", json!({}));
    let line = inv["result"]["line"].as_str().unwrap().to_string();
    let mut h = Hostile::start(line, victim, "honest".into());
    h.expect("paired", Duration::from_secs(30));
    h.expect("up ", Duration::from_secs(30));
    h.send(Cmd::Env {
        kind: kind.into(),
        seq: 0,
        re: None,
        crit: false,
        body: json!({"last_seq_received": big}),
        id: None,
    });
    let sent = h.expect("sent seq", Duration::from_secs(10));
    std::thread::sleep(Duration::from_secs(2));
    if kind == "full" {
        // a `room` afterwards, so the victim may send again
        h.send(Cmd::Env {
            kind: "resume".into(),
            seq: 0,
            re: None,
            crit: false,
            body: json!({"last_seq_received": big, "room": true}),
            id: None,
        });
        h.expect("sent seq", Duration::from_secs(10));
        std::thread::sleep(Duration::from_secs(1));
    }
    let r1 = run.ctl(b, "send", json!({"kind": "chat", "text": "MARKER-G4H-1"}));
    let r2 = run.ctl(b, "send", json!({"kind": "chat", "text": "MARKER-G4H-2"}));
    let t0 = Instant::now();
    let mut got = vec![];
    while t0.elapsed() < Duration::from_secs(20) && got.len() < 2 {
        h.drain();
        got = h.log.iter().filter(|l| l.starts_with("msg chat.msg seq")).cloned().collect();
        std::thread::sleep(Duration::from_millis(200));
    }
    let st = run.ctl(b, "status", json!({}));
    eprintln!("G4-3 {kind} {big}: hostile {sent}; victim send {r1} {r2}; hostile got {got:?}; victim status ok {} clamped {}", st["ok"], st["result"]["session"]["clamped"]);
    run.markers.push("MARKER-G4H".into());
    drop(h);
    run.finish();
    drop(relay);
    assert_eq!(st["ok"], true, "row 33: the victim daemon stopped answering after a peer stated position {big}");
    assert!(st["result"]["session"]["clamped"].as_u64().unwrap_or(0) >= 1, "row 33: the position {big} was not clamped: {st}");
    assert_eq!(got.len(), 2, "row 33: after a peer stated position {big} ({kind}) the victim's next messages did not flow: {got:?}");
}

#[test]
fn g4_3a_hostile_position_u64_max() {
    hostile_position(u64::MAX, "resume", "g4_h3a");
}

#[test]
fn g4_3b_hostile_position_2_62() {
    hostile_position(1 << 62, "resume", "g4_h3b");
}

#[test]
fn g4_3c_hostile_full_u64_max() {
    hostile_position(u64::MAX, "full", "g4_h3c");
}
