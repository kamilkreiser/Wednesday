//! QA GATE (M1 DAEMON) — a HOSTILE paired peer built from the library crates.
//!
//! It joins a real `coagentd` (the victim, convener) through a real `coagent relay` started by the
//! test itself (passed to the victim with --relay-url/--relay-pin so a victim restart does not
//! take the relay down), completes pairing with the link secret, takes the welcome, attaches its
//! slot, runs KK as the INITIATOR (its identity is generated until its key id is lower), and then
//! sends whatever envelopes / raw relay payloads the test asks for.
#![allow(dead_code)]

use std::io::{BufRead, BufReader};
use std::process::{Child, Command, Stdio};
use std::str::FromStr;
use std::sync::mpsc as smpsc;
use std::time::{Duration, Instant};

use coagent_crypto::channel::{Channel, Received};
use coagent_crypto::identity::DeviceIdentity;
use coagent_crypto::kk::{kk_initiate, KkInitiator, RosterView};
use coagent_crypto::pairing::{Paired, Pairing, PairingRole, Progress};
use coagent_crypto::pake::{FirstContact, PairingContext};
use coagent_daemon::invite::{self, Blob};
use coagent_daemon::link::{self, LinkEvent, LinkOut, LinkParams, MbEvent, MbOut};
use coagent_daemon::wire::{self, MailboxPayload, SessionPayload};
use coagent_proto::bytes::KeyId;
use coagent_proto::canonical;
use coagent_proto::envelope::EnvelopeDraft;
use coagent_proto::handshake::{Claims, PairingFrame};
use coagent_relay::client::Candidate;
use coagent_relay::{ChanId, Fingerprint, Token};
use coagent_roster::{RosterChain, SignedRoster};
use serde_json::Value;
use tokio::sync::mpsc;

/// A `coagent relay` process this test started (killed by pid on drop).
pub struct ExtRelay {
    pub child: Child,
    pub url: String,
    pub pin: String,
}

impl ExtRelay {
    pub fn start(coagent: &std::path::Path, home: &std::path::Path, stderr: std::fs::File) -> ExtRelay {
        let mut child = Command::new(coagent)
            .args(["relay", "--listen", "127.0.0.1:0", "--status-secs", "0"])
            .env_clear()
            .env("HOME", home)
            .current_dir("/")
            .stdin(Stdio::null())
            .stdout(Stdio::piped())
            .stderr(stderr)
            .spawn()
            .unwrap();
        let out = child.stdout.take().unwrap();
        let mut r = BufReader::new(out);
        let (mut url, mut pin) = (None, None);
        let t0 = Instant::now();
        while url.is_none() || pin.is_none() {
            assert!(t0.elapsed() < Duration::from_secs(10), "relay banner");
            let mut l = String::new();
            if r.read_line(&mut l).unwrap() == 0 {
                panic!("relay exited");
            }
            if let Some(v) = l.strip_prefix("url: ") {
                url = Some(v.trim().to_string());
            } else if let Some(v) = l.strip_prefix("fingerprint: ") {
                pin = Some(v.trim().to_string());
            }
        }
        std::thread::spawn(move || {
            let mut s = String::new();
            while r.read_line(&mut s).map(|n| n > 0).unwrap_or(false) {
                s.clear();
            }
        });
        ExtRelay {
            child,
            url: url.unwrap(),
            pin: pin.unwrap(),
        }
    }
}

impl Drop for ExtRelay {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

/// Commands to the hostile peer.
pub enum Cmd {
    /// Seal an envelope on the current channel and send it.
    Env {
        kind: String,
        seq: u64,
        re: Option<String>,
        crit: bool,
        body: Value,
        id: Option<String>,
    },
    /// Send raw relay payload bytes.
    Raw(Vec<u8>),
    /// Re-send the FIRST captured KK message 1 under a chosen epoch label (what a relay can do).
    ReplayKk1 { epoch: u64 },
    /// Run a fresh KK as an honest initiator (epoch = last used + 1).
    FreshKk,
    Stop,
}

pub struct Hostile {
    pub cmd: mpsc::UnboundedSender<Cmd>,
    pub out: smpsc::Receiver<String>,
    pub key_id: KeyId,
    thread: Option<std::thread::JoinHandle<()>>,
    pub log: Vec<String>,
}

impl Hostile {
    /// Pair with the victim using its invite `line`; the hostile key id is made LOWER than
    /// `victim` so that it is the KK initiator.
    pub fn start(line: String, victim: KeyId, claims_name: String) -> Hostile {
        let me = loop {
            let i = DeviceIdentity::generate().unwrap();
            if i.key_id() < victim {
                break i;
            }
        };
        let key_id = me.key_id();
        let (ctx, crx) = mpsc::unbounded_channel();
        let (otx, orx) = smpsc::channel();
        let thread = std::thread::spawn(move || {
            let rt = tokio::runtime::Builder::new_multi_thread()
                .worker_threads(2)
                .enable_all()
                .build()
                .unwrap();
            rt.block_on(hostile_main(line, me, crx, otx, claims_name));
        });
        Hostile {
            cmd: ctx,
            out: orx,
            key_id,
            thread: Some(thread),
            log: vec![],
        }
    }

    /// Wait for an output line starting with `prefix`.
    pub fn expect(&mut self, prefix: &str, t: Duration) -> String {
        let t0 = Instant::now();
        loop {
            let left = t.checked_sub(t0.elapsed()).unwrap_or_default();
            match self.out.recv_timeout(left) {
                Ok(l) => {
                    self.log.push(l.clone());
                    if l.starts_with(prefix) {
                        return l;
                    }
                }
                Err(_) => panic!("hostile: no {prefix:?} within {t:?}; log: {:?}", self.log),
            }
        }
    }

    pub fn drain(&mut self) {
        while let Ok(l) = self.out.try_recv() {
            self.log.push(l);
        }
    }

    pub fn send(&self, c: Cmd) {
        let _ = self.cmd.send(c);
    }

    pub fn chat(&self, seq: u64, text: &str) {
        self.send(Cmd::Env {
            kind: "chat.msg".into(),
            seq,
            re: None,
            crit: false,
            body: serde_json::json!({"audience": "agent", "author": "agent", "text": text}),
            id: None,
        });
    }
}

impl Drop for Hostile {
    fn drop(&mut self) {
        let _ = self.cmd.send(Cmd::Stop);
        if let Some(t) = self.thread.take() {
            let _ = t.join();
        }
    }
}

fn cands(r: &[coagent_daemon::store::RelayCandidate]) -> Vec<Candidate> {
    r.iter()
        .map(|c| Candidate {
            url: c.url.clone(),
            pin: Fingerprint::from_str(&c.pin).unwrap(),
        })
        .collect()
}

async fn hostile_main(
    line: String,
    me: DeviceIdentity,
    mut cmds: mpsc::UnboundedReceiver<Cmd>,
    out: smpsc::Sender<String>,
    claims_name: String,
) {
    let say = |s: String| {
        let _ = out.send(s);
    };
    let inv = match invite::parse(&line).unwrap() {
        Blob::Invite(i) => i,
        _ => panic!("not an invite"),
    };
    let cs = cands(&inv.relays);
    let (conn, idx) = link::mailbox_join(&cs, inv.mailbox, &None).await.unwrap();
    let (mbtx, mut mbrx) = mpsc::channel(64);
    let mb = link::spawn_mailbox(conn, 1, mbtx);
    let ctx = PairingContext {
        relay: format!("pin:{}", inv.relays[idx].pin.to_lowercase()),
        mailbox: hex::encode(inv.mailbox),
    };
    let claims = Claims {
        display_name: claims_name.clone(),
        client: claims_name.clone(),
        adapters: vec![],
    };
    let (mut pairing, first) = Pairing::start(
        PairingRole::Joiner,
        &me,
        &FirstContact::Link(inv.secret.clone()),
        &ctx,
        claims,
        None,
    )
    .unwrap();
    let send_pf = |f: &PairingFrame| {
        let j = canonical::encode(f).unwrap();
        wire::encode_mailbox(&MailboxPayload::Pairing(&j))
    };
    for f in first {
        mb.send(MbOut::Data(send_pf(&f))).await.unwrap();
    }
    let mut paired: Option<Paired> = None;
    let welcome: Value;
    loop {
        let (_, ev) = mbrx.recv().await.expect("mailbox events");
        let MbEvent::Data(b) = ev else { continue };
        match wire::decode_mailbox(&b).unwrap() {
            MailboxPayload::Pairing(j) => {
                let f: PairingFrame = canonical::decode(j).unwrap();
                match pairing.handle(&f).unwrap() {
                    Progress::Send(o) => {
                        for f in o {
                            mb.send(MbOut::Data(send_pf(&f))).await.unwrap();
                        }
                    }
                    Progress::Paired { send, paired: p } => {
                        for f in send {
                            mb.send(MbOut::Data(send_pf(&f))).await.unwrap();
                        }
                        paired = Some(*p);
                    }
                }
            }
            MailboxPayload::Frame(f) => {
                let p = paired.as_mut().expect("paired before welcome");
                match p.channel.open(f).unwrap() {
                    Received::Message(m) => {
                        welcome = m.envelope().body.clone();
                        break;
                    }
                    _ => panic!("welcome not a message"),
                }
            }
        }
    }
    let _ = mb.send(MbOut::Burn).await;
    let p = paired.unwrap();
    say(format!("paired {}", p.peer.key_id()));
    let signed: SignedRoster = serde_json::from_value(welcome["roster"].clone()).unwrap();
    let chain = RosterChain::start(&p.peer, p.session_id, &me.key_id(), &signed).unwrap();
    let chan = coagent_relay::frame::from_hex::<32>(welcome["chan_id"].as_str().unwrap()).unwrap();
    let my_slot = welcome["slot"].as_u64().unwrap() as u8;
    let mut tok = [0u8; 32];
    hex::decode_to_slice(welcome["slot_token"].as_str().unwrap(), &mut tok).unwrap();
    let peer_slot = chain.current().slot_of(&p.peer.key_id()).unwrap();
    let (ltx, mut lrx) = mpsc::channel(1024);
    let mk = |gen: u64, upto: u64, ltx: mpsc::Sender<(u64, LinkEvent)>| {
        link::spawn_link(
            LinkParams {
                cands: cs.clone(),
                chan_id: ChanId(chan),
                slot: my_slot,
                token: Token(tok),
                resume: vec![(peer_slot, upto)],
                create: None,
            },
            gen,
            ltx,
            None,
        )
    };
    let mut gen: u64 = 1;
    let mut recv_upto: u64 = 0;
    let mut link = mk(gen, 0, ltx.clone());
    let mut pair_seq: u64 = 1;
    let mut epoch: u64 = 0;
    let mut kk: Option<(u64, KkInitiator)> = None;
    let mut chanl: Option<(u64, Channel)> = None;
    let mut first_msg1: Option<Vec<u8>> = None;
    macro_rules! send_payload {
        ($p:expr) => {{
            let p: Vec<u8> = $p;
            let _ = link
                .send(LinkOut::Data {
                    to_slot: peer_slot,
                    pair_seq,
                    payload: p,
                })
                .await;
            pair_seq += 1;
        }};
    }
    macro_rules! fresh_kk {
        () => {{
            epoch += 1;
            let (init, msg1) = kk_initiate(&me, chain.current(), peer_slot).unwrap();
            if first_msg1.is_none() {
                first_msg1 = Some(msg1.clone());
            }
            kk = Some((epoch, init));
            send_payload!(wire::encode_session(&SessionPayload::Kk1 {
                epoch,
                msg: &msg1
            }));
            say(format!("kk1 sent {epoch}"));
        }};
    }
    loop {
        tokio::select! {
            ev = lrx.recv() => {
                let Some((g, ev)) = ev else { say("link gone".into()); return };
                if g != gen { continue; }
                match ev {
                    LinkEvent::Attached => say("attached".into()),
                    LinkEvent::PeerJoined(s) if s == peer_slot => {
                        say("peer joined".into());
                        fresh_kk!();
                    }
                    LinkEvent::PeerLeft(_) => say("peer left".into()),
                    LinkEvent::Data { from_slot, pair_seq: ps, payload } => {
                        recv_upto = recv_upto.max(ps);
                        let _ = link.send(LinkOut::Ack { from_slot, upto: ps }).await;
                        match wire::decode_session(&payload) {
                            Ok(SessionPayload::Kk2 { epoch: e, msg }) => {
                                say(format!("kk2 recv {e}"));
                                if let Some((ke, _)) = &kk {
                                    if *ke == e {
                                        let (_, init) = kk.take().unwrap();
                                        match init.finish(msg) {
                                            Ok(ch) => {
                                                chanl = Some((e, ch));
                                                say(format!("up {e}"));
                                            }
                                            Err(x) => say(format!("kk finish failed {x}")),
                                        }
                                    }
                                }
                            }
                            Ok(SessionPayload::Frame { epoch: e, frame }) => {
                                if let Some((ce, ch)) = chanl.as_mut() {
                                    if *ce == e {
                                        match ch.open(frame) {
                                            Ok(Received::Message(m)) => say(format!(
                                                "msg {} seq {} ack {}",
                                                m.kind(),
                                                m.envelope().seq,
                                                m.envelope().ack
                                            )),
                                            Ok(_) => {}
                                            Err(x) => say(format!("open err {x}")),
                                        }
                                    } else {
                                        say(format!("frame other epoch {e}"));
                                    }
                                }
                            }
                            Ok(SessionPayload::Kk1 { .. }) => say("kk1 recv (unexpected)".into()),
                            Err(_) => say("bad payload".into()),
                        }
                    }
                    LinkEvent::RelayError(c) => say(format!("relay error {c}")),
                    LinkEvent::Down(w) => {
                        say(format!("down {w}"));
                        tokio::time::sleep(Duration::from_millis(500)).await;
                        gen += 1;
                        link = mk(gen, recv_upto, ltx.clone());
                    }
                    _ => {}
                }
            }
            c = cmds.recv() => {
                match c {
                    None | Some(Cmd::Stop) => { let _ = link.send(LinkOut::Close).await; return; }
                    Some(Cmd::Env { kind, seq, re, crit, body, id }) => {
                        let Some((e, ch)) = chanl.as_mut() else { say("env: no channel".into()); continue };
                        let e = *e;
                        let d = EnvelopeDraft {
                            id: id.unwrap_or_else(|| coagent_daemon::util::new_id().unwrap()),
                            roster_v: chain.current().version(),
                            seq,
                            ack: 0,
                            ts: coagent_daemon::util::rfc3339_now(),
                            kind,
                            re,
                            crit,
                            chain: None,
                            body,
                            sig: None,
                        };
                        match ch.seal(d, Instant::now()) {
                            Ok(frames) => {
                                for f in frames {
                                    send_payload!(wire::encode_session(&SessionPayload::Frame { epoch: e, frame: &f }));
                                }
                                say(format!("sent seq {seq}"));
                            }
                            Err(x) => say(format!("seal refused seq {seq}: {x}")),
                        }
                    }
                    Some(Cmd::Raw(p)) => { send_payload!(p); say("raw sent".into()); }
                    Some(Cmd::ReplayKk1 { epoch: e }) => {
                        let m = first_msg1.clone().expect("a captured msg1");
                        send_payload!(wire::encode_session(&SessionPayload::Kk1 { epoch: e, msg: &m }));
                        say(format!("replayed kk1 as epoch {e}"));
                    }
                    Some(Cmd::FreshKk) => { fresh_kk!(); }
                }
            }
        }
    }
}
