//! QA-AUDIT-HOST (independent check): MY OWN stop-anywhere scenario, run through the builder's stop
//! machinery (its fault injector, `copy_tree`, `revert_unsynced`; copied from `stop_anywhere.rs` and
//! changed). Adds: two seals in a row, restarts (so stops land INSIDE `open`), a seal right after a
//! restart, a removed peer's events still arriving around its release, and more peers.
//! (Builder's text follows.) Section 4 item 7: the STOP-ANYWHERE test. A fixed scenario (create; a mixed run of recording and
//! receiving; an own checkpoint and its countersignatures; a full seal; a roster change; a release;
//! more recording) runs once to count every filesystem operation the host makes. Then, for every j,
//! it runs again with the process STOPPED at operation j (j and every later operation fail, as a
//! dead process makes none): the folder is copied as the disk holds it and opened by a FRESH host,
//! and (a) the open succeeds, (b) no acknowledged own record is lost or re-used, nor an
//! acknowledged peer event lost, (c) the archive and the store verify together
//! (`verify_segments`), (d) re-running the interrupted step and the rest completes the scenario to
//! the very anchor the run without a stop reaches. Every stop between a directory change and its
//! directory sync (a temporary file written, a rename, a link, an unlink) is checked a second time
//! with that change undone: the other disk such a stop can leave (P-4: "after the temporary file is
//! written, after the rename, before the directory sync").

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

use coagent_audit::anchor::AuditAnchor;
use coagent_audit::bundle::{verify, verify_segments, Bundle};
use coagent_audit::checkpoint::SignedHead;
use coagent_audit::session::SessionAudit;
use coagent_audit::store::MemStore;
use coagent_audit::AuditError;
use coagent_proto::bytes::KeyId;
use coagent_proto::canonical;

use super::common::*;
use super::{copy_tree, revert_unsynced};
use crate::fsio::fault::{self, Rule};
use crate::{AuditHost, Causer, HostError, Input, Outcome, SealTrigger};

const V: usize = 1;
const BASE: u8 = 170;

#[derive(Clone, Copy, Debug)]
enum Step {
    Create,
    Rec(Who),
    PeerRec(usize),
    PeerCp(usize),
    OwnCp,
    Seal,
    RosterRemove(usize),
    Release(usize),
    /// Seal to reach this segment number.
    SealTo(u64),
    /// Drop the host (a clean shutdown) and open it again.
    Restart,
    /// Peer `j` makes an event now but it is held back (delivered by `Late`).
    PeerHold(usize),
    /// The held-back event of peer `j` arrives now (any answer accepted; acknowledged only if stored).
    Late(usize),
}

#[derive(Clone, Copy, Debug)]
enum Who {
    Local,
    Member(usize),
}

const SCENARIO: &[Step] = &[
    Step::Create,
    Step::Rec(Who::Local),
    Step::PeerRec(0),
    Step::PeerRec(3),
    Step::Rec(Who::Member(2)),
    Step::PeerRec(4),
    Step::OwnCp,
    Step::PeerCp(0),
    Step::SealTo(1),
    Step::Rec(Who::Local),
    Step::PeerRec(0),
    Step::SealTo(2),
    Step::Rec(Who::Member(4)),
    Step::Restart,
    Step::SealTo(3),
    Step::PeerRec(3),
    Step::PeerHold(3),
    Step::RosterRemove(3),
    Step::Late(3),
    Step::PeerRec(0),
    Step::Release(3),
    Step::PeerRec(4),
    Step::Late(3),
    Step::Restart,
    Step::Rec(Who::Local),
];

/// One run of the scenario: the world, the peers (in memory, never stopped), the host.
struct Run {
    w: World,
    peers: BTreeMap<usize, SessionAudit<MemStore>>,
    root: PathBuf,
    host: Option<AuditHost>,
    /// What the host acknowledged: own (number, header bytes), and peer (author, number).
    acked_own: BTreeMap<u64, Vec<u8>>,
    acked_peer: Vec<(KeyId, u64)>,
    /// Per step, the peer's half of it already done (it is done once; the host's half re-runs).
    peer_done: Vec<bool>,
    /// The object a peer made for the host in a step, kept for a re-run.
    pending_event: BTreeMap<usize, coagent_audit::chain::AuditEvent>,
    pending_head: BTreeMap<usize, SignedHead>,
    own_cs: BTreeMap<usize, Vec<coagent_audit::checkpoint::Countersignature>>,
    held: BTreeMap<usize, coagent_audit::chain::AuditEvent>,
    late_refused: u64,
    release_rerun_refused: u64,
}

/// The own sequence number after step `i` in the run without a stop.
fn expected_seq(i: usize) -> u64 {
    SCENARIO[..=i]
        .iter()
        .filter(|s| matches!(s, Step::Rec(_)))
        .count() as u64
}

fn now_of(i: usize) -> u64 {
    10 * (i as u64 + 1)
}

impl Run {
    fn new(root: PathBuf) -> Run {
        let w = World::new(BASE, 5, 5);
        let mut peers = BTreeMap::new();
        for i in [0usize, 2, 3, 4] {
            peers.insert(i, mem_member(&w, i));
        }
        Run {
            w,
            peers,
            root,
            host: None,
            acked_own: BTreeMap::new(),
            acked_peer: Vec::new(),
            peer_done: vec![false; SCENARIO.len()],
            pending_event: BTreeMap::new(),
            pending_head: BTreeMap::new(),
            own_cs: BTreeMap::new(),
            held: BTreeMap::new(),
            late_refused: 0,
            release_rerun_refused: 0,
        }
    }

    fn h(&mut self) -> &mut AuditHost {
        self.host.as_mut().expect("a host")
    }

    fn ack_own(&mut self, seq: u64) {
        let e = self
            .host
            .as_ref()
            .unwrap()
            .member()
            .unwrap()
            .own()
            .event(seq)
            .unwrap()
            .clone();
        self.acked_own
            .insert(seq, canonical::encode(&e.header).unwrap());
    }

    /// Run step `i`; `Err` when the host's answer is a failure (the stop shows as one).
    fn step(&mut self, i: usize) -> Result<(), String> {
        let id = fixed_identity(BASE + V as u8);
        let now = t(now_of(i));
        match SCENARIO[i] {
            Step::Create => {
                if self.host.is_some() {
                    return Ok(()); // created before the stop
                }
                let (h, _) = AuditHost::create(
                    &self.root,
                    cfg(&self.w),
                    &id,
                    &self.w.ids[0].verified(),
                    &self.w.rosters[0],
                    redactor(),
                    now,
                )
                .map_err(|e| format!("{e:?}"))?;
                self.host = Some(h);
            }
            Step::Rec(who) => {
                let causer = match who {
                    Who::Local => Causer::LocalHuman,
                    Who::Member(g) => Causer::Member(self.w.key(g)),
                };
                let want = expected_seq(i);
                let have = self.h().member().map_err(|e| format!("{e:?}"))?.own().seq();
                let seq = if have >= want {
                    want // landed before the stop: never recorded twice
                } else {
                    let out = self
                        .h()
                        .apply(
                            &id,
                            Input::Record {
                                causer,
                                input: owned("host.ev", None, None),
                            },
                            now,
                        )
                        .map_err(|e| format!("{e:?}"))?;
                    let Outcome::Recorded(seq) = out else {
                        return Err(format!("{out:?}"));
                    };
                    seq
                };
                assert_eq!(seq, want, "own numbering");
                self.ack_own(seq);
                // delivered to every peer (a re-delivery is a replay, ignored)
                let outgoing = self.host.as_ref().unwrap().member().unwrap().outgoing(seq);
                for (to, e) in outgoing {
                    if let Some(j) = self.w.ids.iter().position(|d| d.key_id() == to) {
                        if let Some(p) = self.peers.get_mut(&j) {
                            let _ = p.receive(&self.w.ids[j], &e, now);
                        }
                    }
                }
            }
            Step::PeerRec(j) => {
                if !self.peer_done[i] {
                    let p = self.peers.get_mut(&j).unwrap();
                    let seq = p.record(&self.w.ids[j], bare("p.ev"), now).unwrap();
                    let e = p
                        .outgoing(seq)
                        .into_iter()
                        .find(|(to, _)| *to == self.w.key(V))
                        .unwrap()
                        .1;
                    self.pending_event.insert(i, e);
                    self.peer_done[i] = true;
                }
                let e = self.pending_event[&i].clone();
                match self.h().apply(&id, Input::Receive(e.clone()), now) {
                    Ok(_) => {}
                    // already stored before the stop: a re-delivery is a replay
                    Err(HostError::Audit(AuditError::Receive(
                        coagent_audit::received::ReceiveError::Replay { .. },
                    ))) => {}
                    Err(x) => return Err(format!("{x:?}")),
                }
                self.acked_peer.push((e.header.author, e.header.author_seq));
            }
            Step::PeerCp(j) => {
                if !self.peer_done[i] {
                    let h = self
                        .peers
                        .get_mut(&j)
                        .unwrap()
                        .checkpoint_now(&self.w.ids[j], now)
                        .unwrap();
                    self.pending_head.insert(i, h);
                    self.peer_done[i] = true;
                }
                let h = self.pending_head[&i].clone();
                match self.h().apply(&id, Input::ReceiveHead(h), now) {
                    Ok(Outcome::Countersigned(cs)) => {
                        let _ = self.peers.get_mut(&j).unwrap().add_countersignature(&cs);
                    }
                    Ok(o) => return Err(format!("{o:?}")),
                    Err(x) => return Err(format!("{x:?}")),
                }
            }
            Step::OwnCp => {
                let out = self
                    .h()
                    .apply(&id, Input::Checkpoint, now)
                    .map_err(|e| format!("{e:?}"))?;
                let Outcome::Checkpoint(h) = out else {
                    return Err(format!("{out:?}"));
                };
                if !self.peer_done[i] {
                    let mut css = Vec::new();
                    for (j, p) in self.peers.iter_mut() {
                        if let Ok(cs) = p.receive_head(&self.w.ids[*j], &h) {
                            css.push(cs);
                        }
                    }
                    self.own_cs.insert(i, css);
                    self.peer_done[i] = true;
                }
                for cs in self.own_cs[&i].clone() {
                    self.h()
                        .apply(&id, Input::Countersignature(cs), now)
                        .map_err(|e| format!("{e:?}"))?;
                }
            }
            Step::Seal => {
                let target = 1;
                if self.h().member().map_err(|e| format!("{e:?}"))?.segment() < target {
                    self.h()
                        .seal(&id, SealTrigger::OwnerCommand, now)
                        .map_err(|e| format!("{e:?}"))?;
                }
            }
            Step::RosterRemove(k) => {
                if !self.peer_done[i] {
                    let r = self.w.remove(k);
                    for (j, p) in self.peers.iter_mut() {
                        if *j != k {
                            p.apply_roster(&r).unwrap();
                        }
                    }
                    self.peer_done[i] = true;
                }
                let r = self.w.rosters.last().unwrap().clone();
                self.h()
                    .apply(&id, Input::Roster(r), now)
                    .map_err(|e| format!("{e:?}"))?;
            }
            Step::Release(k) => {
                let key = self.w.key(k);
                match self.h().apply(&id, Input::Release(key), now) {
                    Ok(_) => {}
                    Err(e) => {
                        // a release that landed before the stop: re-running it may be refused;
                        // accepted only if nothing of k's seat is left in the store
                        let m = self.h().member().map_err(|x| format!("{x:?}"))?;
                        let left = m.seat_usage(k as u8).1;
                        if left != 0 {
                            return Err(format!("release re-run: {e:?} with {left} records left"));
                        }
                        self.release_rerun_refused += 1;
                    }
                }
            }
            Step::SealTo(target) => {
                if self.h().member().map_err(|e| format!("{e:?}"))?.segment() < target {
                    self.h()
                        .seal(&id, SealTrigger::OwnerCommand, now)
                        .map_err(|e| format!("{e:?}"))?;
                }
            }
            Step::Restart => {
                self.host = None;
                let (h, _) = open_host(&self.w, V, &self.root, cfg(&self.w), now_of(i))
                    .map_err(|e| format!("{e:?}"))?;
                self.host = Some(h);
            }
            Step::PeerHold(j) => {
                if !self.peer_done[i] {
                    let p = self.peers.get_mut(&j).unwrap();
                    let seq = p.record(&self.w.ids[j], bare("p.held"), now).unwrap();
                    let e = p
                        .outgoing(seq)
                        .into_iter()
                        .find(|(to, _)| *to == self.w.key(V))
                        .unwrap()
                        .1;
                    self.held.insert(j, e);
                    self.peer_done[i] = true;
                }
            }
            Step::Late(j) => {
                if let Some(e) = self.held.get(&j).cloned() {
                    match self.h().apply(&id, Input::Receive(e.clone()), now) {
                        Ok(Outcome::Received(_)) => {
                            self.acked_peer.push((e.header.author, e.header.author_seq))
                        }
                        Ok(o) => return Err(format!("{o:?}")),
                        Err(HostError::Audit(_)) => self.late_refused += 1,
                        Err(x) => return Err(format!("{x:?}")),
                    }
                }
            }
        }
        Ok(())
    }
}

/// Own events by number (header bytes) and peer events (author, number).
type Held = (BTreeMap<u64, Vec<u8>>, Vec<(KeyId, u64)>);

/// Every own event and peer event held in a folder: the segment files, the release files and the
/// current export. Returns (own: number → header bytes, distinct per number or an error; peers).
fn union(files: &[Bundle], export: &Bundle) -> Result<Held, String> {
    let mut own: BTreeMap<u64, Vec<u8>> = BTreeMap::new();
    let mut peer = Vec::new();
    for b in files.iter().chain(std::iter::once(export)) {
        for e in &b.own_events {
            let hb = canonical::encode(&e.header).unwrap();
            if let Some(prev) = own.get(&e.header.author_seq) {
                if *prev != hb {
                    return Err(format!("own number {} signed twice", e.header.author_seq));
                }
            }
            own.insert(e.header.author_seq, hb);
        }
        for p in &b.peers {
            for e in &p.events {
                peer.push((e.header.author, e.header.author_seq));
            }
        }
    }
    Ok((own, peer))
}

/// (a) to (d) on one stopped folder. Returns a line for the log.
fn check_stopped(
    stopped: &mut Run,
    interrupted: usize,
    snap: &Path,
    clean_final: &AuditAnchor,
    clean_seq: u64,
    tag: &str,
) {
    let w_id = fixed_identity(BASE + V as u8);
    // (a)
    let opened = open_host(&stopped.w, V, snap, cfg(&stopped.w), 1_000_000);
    let host = match opened {
        Ok((h, _)) => Some(h),
        Err(HostError::NotCreated) if matches!(SCENARIO[interrupted], Step::Create) => None,
        Err(e) => panic!(
            "{tag}: (a) the open failed after a stop in step {interrupted} ({:?}): {e:?}",
            SCENARIO[interrupted]
        ),
    };
    let run = stopped;
    run.root = snap.to_path_buf();
    run.host = host;
    if let Some(h) = run.host.as_ref() {
        // (b) and (c) on the folder as opened
        check_folder(h, run, &w_id, tag, "after the open");
    }
    // (d) the interrupted step re-run, then the rest
    for (i, step) in SCENARIO.iter().enumerate().skip(interrupted) {
        if let Err(e) = run.step(i) {
            panic!("{tag}: (d) re-running step {i} ({step:?}) failed: {e}");
        }
    }
    let h = run.host.as_ref().unwrap();
    check_folder(h, run, &w_id, tag, "after the re-run");
    let m = h.member().unwrap();
    assert_eq!(
        m.own().seq(),
        clean_seq,
        "{tag}: (d) own numbering differs from the run without a stop"
    );
    assert_eq!(
        &m.anchor(),
        clean_final,
        "{tag}: (d) the re-run did not complete the scenario to the same store"
    );
}

fn check_folder(
    h: &AuditHost,
    run: &Run,
    id: &coagent_crypto::identity::DeviceIdentity,
    tag: &str,
    when: &str,
) {
    let segs = h.segment_bundles().unwrap();
    let rels = h.release_bundles().unwrap();
    let export = h.export(id).unwrap();
    for b in &rels {
        verify(b).unwrap_or_else(|e| panic!("{tag}: a release file does not verify {when}: {e:?}"));
    }
    let mut set = segs.clone();
    set.push(export.clone());
    let rep = verify_segments(&set).unwrap_or_else(|e| {
        panic!("{tag}: (c) archive + store do not verify together {when}: {e:?}")
    });
    assert!(
        rep.equivocations.is_empty(),
        "{tag}: (b) the archive and store hold two statements at one number {when}"
    );
    let mut all = segs;
    all.extend(rels);
    let (own, peer) = union(&all, &export).unwrap_or_else(|e| panic!("{tag}: (b) {e} {when}"));
    for (seq, hb) in &run.acked_own {
        assert_eq!(
            own.get(seq),
            Some(hb),
            "{tag}: (b) acknowledged own record {seq} lost or replaced {when}"
        );
    }
    for (a, n) in &run.acked_peer {
        assert!(
            peer.contains(&(*a, *n)),
            "{tag}: (b) acknowledged peer event {n} lost {when}"
        );
    }
}

fn run_with(rule: Rule, root: PathBuf) -> (Run, Option<usize>, crate::fsio::fault::Report) {
    let mut run = Run::new(root);
    fault::arm(rule);
    let mut interrupted = None;
    for (i, step) in SCENARIO.iter().enumerate() {
        let r = run.step(i);
        if fault::stopped() {
            interrupted = Some(i);
            break;
        }
        if let Err(e) = r {
            fault::disarm();
            panic!("step {i} ({step:?}) failed without a stop: {e}");
        }
    }
    run.host = None; // the process is gone: drop the host while every operation still fails
    let rep = fault::disarm();
    (run, interrupted, rep)
}

#[test]
fn qa_stop_anywhere_own_scenario() {
    let base = scratch("qa-stop-anywhere");
    // the run without a stop: count the operations and keep the final anchor
    let (clean, none, rep) = run_with(Rule::None, base.join("clean"));
    assert!(none.is_none());
    let total = rep.ops;
    let (clean_final, clean_seq) = {
        let (h, _) = open_host(&clean.w, V, &base.join("clean"), cfg(&clean.w), 999_999).unwrap();
        let m = h.member().unwrap();
        (m.anchor(), m.own().seq())
    };
    println!(
        "QA stop-anywhere clean run: late events refused {}, release re-runs refused {}, final own seq {}, segment {}",
        clean.late_refused,
        clean.release_rerun_refused,
        clean_seq,
        {
            let (h, _) = open_host(&clean.w, V, &base.join("clean"), cfg(&clean.w), 999_998).unwrap();
            let s = h.member().unwrap().segment();
            s
        }
    );
    println!(
        "QA stop-anywhere: {total} filesystem operations in the scenario ({} steps)",
        SCENARIO.len()
    );
    let only: Option<usize> = std::env::var("QA_STOP_ONLY")
        .ok()
        .and_then(|v| v.parse().ok());
    let (mut points, mut reverted) = (0usize, 0usize);
    for j in 0..total {
        if only.is_some_and(|o| o != j) {
            continue;
        }
        let root = base.join(format!("run-{j}"));
        let (mut run, interrupted, rep) = run_with(Rule::StopAt(j), root.clone());
        let interrupted = interrupted.unwrap_or_else(|| panic!("stop at {j} was never reached"));
        // the disk as it is
        let snap = base.join(format!("snap-{j}"));
        // a stop before the root existed leaves nothing on disk: the snapshot is no folder
        if root.exists() {
            copy_tree(&root, &snap);
        }
        let undo = rep.unsynced.clone();
        let tag = format!("stop {j} (step {interrupted} {:?})", SCENARIO[interrupted]);
        check_stopped(&mut run, interrupted, &snap, &clean_final, clean_seq, &tag);
        points += 1;
        scratch_done_inner(&snap);
        // the disk with the unsynced directory change undone
        if !undo.is_empty() {
            let root2 = base.join(format!("run-{j}-r"));
            let (mut run2, i2, rep2) = run_with(Rule::StopAt(j), root2.clone());
            let snap2 = base.join(format!("snap-{j}-r"));
            if root2.exists() {
                copy_tree(&root2, &snap2);
                revert_unsynced(&root2, &snap2, &rep2.unsynced);
            }
            let tag2 = format!("{tag}, unsynced change undone");
            check_stopped(
                &mut run2,
                i2.unwrap(),
                &snap2,
                &clean_final,
                clean_seq,
                &tag2,
            );
            reverted += 1;
            scratch_done_inner(&snap2);
            scratch_done_inner(&root2);
        }
        scratch_done_inner(&root);
    }
    println!(
        "QA stop-anywhere: {points} stop points reached, {reverted} of them also with the unsynced \
         directory change undone; (a) to (d) held at every one"
    );
    assert!(only.is_some() || points == total);
    scratch_done(&base);
}

fn scratch_done_inner(p: &Path) {
    let _ = std::fs::remove_dir_all(p);
}
