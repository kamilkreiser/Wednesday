//! QA-AUDIT-NEXT-A (b2), (b3) S-1, (c) S-3, S-4: the checker's OWN ENUMERATED harness over the head's
//! public `owner_seal_steps`. The alphabet builders are the r2 check's `qa_alpha2.rs` (its own, not the
//! lane's), path changed. Scratch copy only; never in a tree whose whole suite is run.
#![allow(dead_code)]
use std::cell::RefCell;
use std::collections::BTreeMap;
use std::path::PathBuf;

use coagent_audit::checkpoint::CheckpointPolicy;
use coagent_audit::redact::{PatternRedactor, Redactor};
use coagent_audit::session::StoreLimits;
use coagent_audit::store::StoreError;
use coagent_audit::time::AuditTime;
use coagent_audit::AuditError;
use coagent_audit_host::{
    AuditHost, Causer, DirError, HostConfig, HostError, Input, LimitsReport, Outcome, OwnedInput,
    SealReport, SealTrigger,
};
use coagent_crypto::identity::DeviceIdentity;
use coagent_daemon::audit::{owner_seal_steps, segment_unknown, Figures};
use coagent_proto::bytes::{Digest32, SessionId};
use coagent_roster::{sign, Member, Role, RosterBody, CAP};

fn t(ms: u64) -> AuditTime {
    AuditTime::from_unix_ms(1_794_884_645_000 + ms)
}

struct Real {
    head: coagent_audit::checkpoint::SignedHead,
    report: SealReport,
    bundle: coagent_audit::bundle::Bundle,
}

static N: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);

fn real() -> Real {
    let a = DeviceIdentity::generate().unwrap();
    let b = DeviceIdentity::generate().unwrap();
    let sid = SessionId([0x5a; 32]);
    let m = |d: &DeviceIdentity, slot: u8| {
        Member::new(&d.public_keys(), d.key_id(), Role::Guest, slot, 1, "2026-11-26T01:00:00Z")
    };
    let r1 = sign(
        &a,
        RosterBody {
            session_id: sid,
            version: 1,
            prev_hash: Digest32([0; 32]),
            convener: a.key_id(),
            cap: CAP,
            members: vec![m(&a, 0), m(&b, 1)],
            removed: vec![],
        },
    )
    .unwrap();
    let root: PathBuf = PathBuf::from(format!("/private/tmp/claude-501/qana/hr/{}-{}", std::process::id(), N.fetch_add(1, std::sync::atomic::Ordering::SeqCst)));
    std::fs::create_dir_all(root.parent().unwrap()).unwrap();
    let (mut h, _) = AuditHost::create(
        &root,
        HostConfig::new(sid, CheckpointPolicy::default()),
        &a,
        &a.verified(),
        &r1,
        Box::new(|| Box::new(PatternRedactor) as Box<dyn Redactor>),
        t(0),
    )
    .unwrap();
    for i in 0..3 {
        let o = h
            .apply(
                &a,
                Input::Record {
                    causer: Causer::LocalHuman,
                    input: OwnedInput { kind: "chat".into(), summary: None, full: Some(format!("qa {i}")) },
                },
                t(1 + i),
            )
            .unwrap();
        assert!(matches!(o, Outcome::Recorded(_)));
    }
    let head = match h.apply(&a, Input::Checkpoint, t(10)).unwrap() {
        Outcome::Checkpoint(hd) => hd,
        o => panic!("checkpoint answered {o:?}"),
    };
    h.apply(
        &a,
        Input::Record {
            causer: Causer::LocalHuman,
            input: OwnedInput { kind: "chat".into(), summary: None, full: Some("qa 4".into()) },
        },
        t(11),
    )
    .unwrap();
    let report = h.seal(&a, SealTrigger::OwnerCommand, t(20)).unwrap();
    let bundle = h.export(&a).unwrap();
    Real { head, report, bundle }
}

fn lim(differs: bool) -> LimitsReport {
    let d = StoreLimits::default();
    LimitsReport {
        before: Some(d),
        offered: d,
        in_force: if differs { StoreLimits { records: d.records.saturating_sub(1), ..d } } else { d },
        refused: Some(AuditError::LogFull),
    }
}

fn dirs() -> Vec<(&'static str, DirError)> {
    vec![
        ("Dir(Unsupported)", DirError::Unsupported("x")),
        (
            "Dir(Io anchors sync)",
            DirError::Io { what: "sync the directory", name: "anchors".into(), kind: std::io::ErrorKind::PermissionDenied },
        ),
        (
            "Dir(Io anchors/limits)",
            DirError::Io { what: "write a file", name: "anchors/limits".into(), kind: std::io::ErrorKind::StorageFull },
        ),
        (
            "Dir(Io archive list)",
            DirError::Io { what: "list the archive", name: "archive".into(), kind: std::io::ErrorKind::PermissionDenied },
        ),
        ("Dir(NotADirectory)", DirError::NotADirectory("archive".into())),
        ("Dir(Symlink)", DirError::Symlink("anchors".into())),
        ("Dir(Rights)", DirError::Rights { name: "store".into(), mode: 0o755 }),
        ("Dir(NotOwned)", DirError::NotOwned("store".into())),
        ("Dir(HardLink)", DirError::HardLink("anchors/current".into())),
        ("Dir(UnknownFile)", DirError::UnknownFile("archive/x".into())),
        ("Dir(Unreadable)", DirError::Unreadable { name: "archive/seg".into(), why: "not a bundle" }),
        ("Dir(TooManyLeftovers)", DirError::TooManyLeftovers(65)),
        ("Dir(InUse)", DirError::InUse),
        ("Dir(Poisoned)", DirError::Poisoned),
        ("Dir(Bounds)", DirError::Bounds("archive attempts for one segment")),
    ]
}

/// Every HostError variant (with sub-values), labelled. `seg` = the segment before the seal.
fn errors(seg: u64) -> Vec<(String, HostError)> {
    let mut v: Vec<(String, HostError)> = vec![];
    for (n, d) in dirs() {
        v.push((n.into(), HostError::Dir(d)));
    }
    for (n, a) in [
        ("Audit(NothingToSeal)", AuditError::NothingToSeal),
        ("Audit(LogFull)", AuditError::LogFull),
        ("Audit(ExportTooLarge)", AuditError::ExportTooLarge),
        ("Audit(Store)", AuditError::Store(StoreError::Unavailable("x"))),
        ("Audit(SealStale)", AuditError::SealStale),
        ("Audit(FieldLimit)", AuditError::FieldLimit("kind")),
        ("Audit(TooLarge)", AuditError::TooLarge("event")),
    ] {
        v.push((n.into(), HostError::Audit(a)));
    }
    v.push(("Anchor".into(), HostError::Anchor { pending: None, current: None }));
    v.push(("NotCreated".into(), HostError::NotCreated));
    v.push(("AlreadyCreated".into(), HostError::AlreadyCreated));
    v.push(("Closed".into(), HostError::Closed));
    v.push(("Busy".into(), HostError::Busy { queued: 1, bytes: 1 }));
    v.push(("SealInProgress".into(), HostError::SealInProgress));
    v.push(("NoSealInProgress".into(), HostError::NoSealInProgress));
    v.push(("TriggerOff".into(), HostError::TriggerOff(SealTrigger::Timer)));
    v.push(("NotDue".into(), HostError::NotDue(SealTrigger::Timer)));
    v.push(("Settings".into(), HostError::Settings("x".into())));
    v.push(("AnchorNotSaved".into(), HostError::AnchorNotSaved));
    v.push(("Reopened{landed:false}".into(), HostError::Reopened { cause: AuditError::Store(StoreError::Unavailable("x")), landed: false }));
    v.push(("Reopened{landed:true}".into(), HostError::Reopened { cause: AuditError::Store(StoreError::Unavailable("x")), landed: true }));
    v.push((
        "LandedUnknown".into(),
        HostError::LandedUnknown { cause: AuditError::Store(StoreError::Unavailable("x")), reopen: Box::new(HostError::Dir(DirError::InUse)) },
    ));
    v.push(("SealStaleTwice".into(), HostError::SealStaleTwice));
    v.push((
        "SealCommitFailed{not moved}".into(),
        HostError::SealCommitFailed { cause: AuditError::Store(StoreError::Unavailable("x")), segment_now: seg },
    ));
    v.push((
        "SealCommitFailed{moved}".into(),
        HostError::SealCommitFailed { cause: AuditError::Store(StoreError::Unavailable("x")), segment_now: seg + 1 },
    ));
    v.push(("ArchiveMismatch".into(), HostError::ArchiveMismatch("archive/seg-x".into())));
    v
}

fn outcomes(r: &Real) -> Vec<(String, Outcome)> {
    vec![
        ("Recorded(7)".into(), Outcome::Recorded(7)),
        ("Checkpoint".into(), Outcome::Checkpoint(r.head.clone())),
        ("Evidence([])".into(), Outcome::Evidence(vec![])),
        ("Released".into(), Outcome::Released(Box::new(r.bundle.clone()))),
        ("Kept".into(), Outcome::Kept),
        ("Queued(1)".into(), Outcome::Queued(1)),
    ]
}

/// Every seal answer of the alphabet, built around segment `seg` (row 7's commit errors at seg-1,
/// seg, seg+1, seg+2 where they exist), bare, inside one and two `LimitsChanged`, and the Oks.
fn seal_alphabet(r: &Real, seg: u64) -> Vec<(String, Result<SealReport, HostError>)> {
    let mut v: Vec<(String, Result<SealReport, HostError>)> = vec![];
    v.push(("Ok(SealReport{limits:None})".into(), Ok(r.report.clone())));
    v.push(("Ok(SealReport{limits:Some})".into(), Ok(SealReport { limits: Some(lim(true)), ..r.report.clone() })));
    let mut errs = errors(seg);
    for now in [seg.wrapping_sub(1), seg + 2] {
        if now != u64::MAX {
            errs.push((format!("SealCommitFailed{{segment_now:{now}}}"), HostError::SealCommitFailed { cause: AuditError::Store(StoreError::Unavailable("x")), segment_now: now }));
        }
    }
    for (n, e) in &errs {
        v.push((format!("Err({n})"), Err(e.clone())));
    }
    for (n, o) in outcomes(r) {
        v.push((format!("Err(LimitsChanged{{Ok({n})}})"), Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Ok(o)) })));
    }
    for (n, e) in &errs {
        v.push((format!("Err(LimitsChanged{{Err({n})}})"), Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Err(e.clone())) })));
        v.push((format!("Err(LimitsChanged{{Err(LimitsChanged{{Err({n})}})}})"), Err(HostError::LimitsChanged { limits: lim(false), answer: Box::new(Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Err(e.clone())) })) })));
    }
    v
}

fn commit_now(ans: &Result<SealReport, HostError>) -> Option<u64> {
    let mut e = match ans { Err(e) => e, Ok(_) => return None };
    loop {
        match e {
            HostError::SealCommitFailed { segment_now, .. } => return Some(*segment_now),
            HostError::LimitsChanged { answer, .. } => match answer.as_ref() { Err(x) => e = x, Ok(_) => return None },
            _ => return None,
        }
    }
}

/// R2 task 1: the segment before UNKNOWN (None) for every seal answer, host open and closed after:
/// 0 reported sealed, 0 seal calls. Then KNOWN segments 0, 1, 3: done only for Ok or a commit

const T_NOTHING: &str = "not sealed: nothing could be filed (nothing new since the last filed point, or the log could not write)";
const T_UNWRITTEN: &str = "not sealed: the log could not write its checkpoint; fix the cause (see status.audit), then give the command again";
const T_NEW: &str = "not sealed: nothing new since the last filed point";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Ev { Read(bool), Reopen(bool), Seal, Limits }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum After { K, K1, NoMember }

#[derive(Debug, Clone)]
struct Case {
    k: u64,
    label: String,
    answer: Result<SealReport, HostError>,
    member_at_start: bool,
    reopen_before_ok: bool,
    reopen_after_ok: bool,
    closed_after: bool,
    after: After,
    own_seq: u64,
    own_cp: u64,
}

struct M {
    c: Case,
    /// the host has its member ("no member" and "segment unknown" are ONE state, as in production)
    member: bool,
    seg: u64,
    reopens: u32,
    sealed_yet: bool,
    ev: RefCell<Vec<Ev>>,
}

fn run(c: &Case) -> (coagent_daemon::audit::Action, u32, bool, Vec<Ev>, u32) {
    let mut m = M { c: c.clone(), member: c.member_at_start, seg: c.k, reopens: 0, sealed_yet: false, ev: RefCell::new(vec![]) };
    let mut seal_calls = 0u32;
    let (a, calls, was_err) = {
        let sc = &mut seal_calls;
        owner_seal_steps(
            &mut m,
            |m: &M| {
                let f = m.member.then_some(Figures { segment: m.seg, own_seq: m.c.own_seq, own_checkpoint: m.c.own_cp });
                m.ev.borrow_mut().push(Ev::Read(f.is_some()));
                f
            },
            |m: &mut M| {
                let ok = if m.sealed_yet { m.c.reopen_after_ok } else { m.c.reopen_before_ok };
                m.reopens += 1;
                m.ev.borrow_mut().push(Ev::Reopen(ok));
                if ok {
                    if m.sealed_yet {
                        match m.c.after {
                            After::K => { m.member = true; m.seg = m.c.k; }
                            After::K1 => { m.member = true; m.seg = m.c.k + 1; }
                            // a re-open that says ok but leaves no member (production cannot: kept to probe)
                            After::NoMember => m.member = false,
                        }
                    } else {
                        m.member = true;
                        m.seg = m.c.k;
                    }
                } else {
                    m.member = false;
                }
                ok
            },
            |m: &mut M| {
                *sc += 1;
                m.ev.borrow_mut().push(Ev::Seal);
                m.sealed_yet = true;
                if m.c.closed_after { m.member = false; }
                (m.c.answer.clone(), m.c.closed_after)
            },
            |m: &mut M, _l: &LimitsReport| m.ev.borrow_mut().push(Ev::Limits),
        )
    };
    let ev = m.ev.into_inner();
    (a, calls, was_err, ev, seal_calls)
}

fn core(a: &Result<SealReport, HostError>) -> Result<(), &HostError> {
    fn peel(e: &HostError) -> &HostError {
        match e {
            HostError::LimitsChanged { answer, .. } => match answer.as_ref() { Err(i) => peel(i), Ok(_) => e },
            _ => e,
        }
    }
    match a { Ok(_) => Ok(()), Err(e) => Err(peel(e)) }
}

fn is_nothing(a: &Result<SealReport, HostError>) -> bool {
    matches!(core(a), Err(HostError::Audit(AuditError::NothingToSeal)))
}

fn check(c: &Case, counts: &mut BTreeMap<String, u64>) -> Vec<String> {
    let (a, calls, _w, ev, seal_calls) = run(c);
    let mut bad = vec![];
    let mut hit = |k: &str| *counts.entry(k.to_string()).or_default() += 1;
    let seal_at = ev.iter().position(|e| *e == Ev::Seal);
    let pre = &ev[..seal_at.unwrap_or(ev.len())];
    let post: &[Ev] = match seal_at { Some(i) => &ev[i + 1..], None => &[] };
    let reopens_before = pre.iter().filter(|e| matches!(e, Ev::Reopen(_))).count();
    let last_after = post.iter().rev().find_map(|e| match e { Ev::Reopen(ok) => Some(*ok), _ => None });
    // A1/A2: re-open words
    let failed_w = a.text.contains("could not be opened again");
    let opened_w = a.text.contains("opened again") && !failed_w;
    if opened_w { hit("A1 says opened again"); if last_after != Some(true) { bad.push("A1 says opened again without a successful re-open after the answer".into()); } }
    if failed_w { hit("A2 says could not be opened again"); if last_after != Some(false) { bad.push("A2 says could not be opened again without a failed re-open".into()); } }
    // A3: sealed
    if a.done != a.text.starts_with("sealed:") { bad.push("A3 sealed flag and text disagree".into()); }
    if a.done {
        hit("A3 sealed: true");
        let before_known = pre.contains(&Ev::Read(true));
        let ok = match core(&c.answer) {
            Ok(()) => true,
            Err(HostError::SealCommitFailed { segment_now, .. }) => before_known && *segment_now != c.k,
            Err(HostError::LandedUnknown { .. }) => before_known && last_after == Some(true) && c.after == After::K1,
            _ => false,
        };
        if !ok { bad.push("A3 sealed without an Ok answer or a moved segment against a known one".into()); }
    }
    // A4: re-open before the seal
    if !c.member_at_start {
        hit("A4 member-less at start");
        if reopens_before != 1 { bad.push(format!("A4 member-less host opened {reopens_before} times before the seal")); }
        let r = pre.iter().position(|e| matches!(e, Ev::Reopen(_)));
        let first_ok = pre.iter().position(|e| *e == Ev::Read(true));
        if let (Some(r), Some(f)) = (r, first_ok) { if f < r { bad.push("A4 a figure read before the re-open".into()); } }
    } else {
        hit("A4 member at start");
        if reopens_before != 0 { bad.push("A4 a host with its member opened before the seal".into()); }
    }
    // A5: calls
    hit(&format!("A5 calls {calls}"));
    if calls != seal_calls { bad.push(format!("A5 calls {calls} but {seal_calls} seal_once calls")); }
    if calls > 1 { bad.push("A5 more than one seal".into()); }
    if a.row == segment_unknown().row {
        hit("A5 segment_unknown");
        if seal_calls != 0 { bad.push("A5 segment_unknown made a seal".into()); }
        if c.member_at_start || c.reopen_before_ok { bad.push("A5 segment_unknown with a readable segment".into()); }
    }
    // A6 (S-4): limits after the answer, before any re-open after it
    if let Some(li) = ev.iter().position(|e| *e == Ev::Limits) {
        hit("A6 limits reported");
        let s = seal_at.unwrap_or(usize::MAX);
        let first_reopen_after = ev.iter().enumerate().skip(s.saturating_add(1)).find(|(_, e)| matches!(e, Ev::Reopen(_))).map(|(i, _)| i);
        if li < s || first_reopen_after.is_some_and(|r| r < li) { bad.push(format!("A6 limits out of order {ev:?}")); }
        if ev.iter().filter(|e| **e == Ev::Limits).count() != 1 { bad.push("A6 limits twice".into()); }
    } else if a.limits.is_some() { bad.push("A6 an action with limits not reported".into()); }
    // A7: NothingToSeal texts (S-1 included: own seq below the checkpoint)
    if is_nothing(&c.answer) && seal_calls == 1 {
        let want = if c.own_seq > c.own_cp { T_UNWRITTEN } else if c.own_seq == c.own_cp { T_NEW } else { T_NOTHING };
        hit(&format!("A7 NothingToSeal {}", if c.own_seq > c.own_cp { "seq>cp" } else if c.own_seq == c.own_cp { "seq=cp" } else { "seq<cp (S-1)" }));
        if a.text != want { bad.push(format!("A7 NothingToSeal text {:?} want {want:?}", a.text)); }
    }
    // reach
    if c.after == After::NoMember && c.reopen_after_ok && a.reopen { hit("R reopen-ok-but-no-member after (not producible)"); }
    if !c.member_at_start && c.reopen_before_ok && !c.reopen_after_ok && seal_calls == 1 && a.reopen { hit("R S-5 member-less, opened before, failed after"); }
    if (a.row == "11" || a.row == "12 and 11") && last_after == Some(false) { hit("R row 11/12+11 re-open failed"); }
    if a.row == "4" && last_after == Some(true) { hit(&format!("R row 4 re-open ok after {:?}", c.after)); }
    if a.row == "4" && last_after == Some(false) { hit("R row 4 re-open failed"); }
    bad.into_iter().map(|b| format!("{b}: {} k={} member={} rb={} ra={} closed={} after={:?} seq={} cp={} -> row={} done={} text={:?} calls={} ev={ev:?}", c.label, c.k, c.member_at_start, c.reopen_before_ok, c.reopen_after_ok, c.closed_after, c.after, c.own_seq, c.own_cp, a.row, a.done, a.text, calls)).collect()
}

#[test]
fn qa_owner_seal_steps_enumerated() {
    let r = real();
    let mut counts: BTreeMap<String, u64> = BTreeMap::new();
    let mut bad: Vec<String> = vec![];
    let mut texts: BTreeMap<String, u64> = BTreeMap::new();
    let mut n = 0u64;
    let mut alpha_n = 0;
    for k in [0u64, 1, 5] {
        let alpha = seal_alphabet(&r, k);
        alpha_n = alpha_n.max(alpha.len());
        for (label, answer) in &alpha {
            for member_at_start in [true, false] {
                for reopen_before_ok in [true, false] {
                    for reopen_after_ok in [true, false] {
                        for closed_after in [false, true] {
                            for after in [After::K, After::K1, After::NoMember] {
                                for (own_seq, own_cp) in [(3u64, 3u64), (4, 3), (2, 3), (0, 0)] {
                                    let c = Case { k, label: label.clone(), answer: answer.clone(), member_at_start, reopen_before_ok, reopen_after_ok, closed_after, after, own_seq, own_cp };
                                    n += 1;
                                    let b = check(&c, &mut counts);
                                    let (a, ..) = run(&c);
                                    *texts.entry(format!("{} | {}", a.row, a.text)).or_default() += 1;
                                    bad.extend(b);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    println!("QA steps: {n} cases (alphabet up to {alpha_n} answers x k in 0,1,5 x member 2 x reopen-before 2 x reopen-after 2 x closed 2 x after 3 x figures 4)");
    for (k, v) in &counts { println!("QA count\t{k}\t{v}"); }
    for (k, v) in &texts { println!("QA text\t{v}\t{k}"); }
    println!("QA failures: {}", bad.len());
    let mut kinds: BTreeMap<String, u64> = BTreeMap::new();
    for b in &bad { *kinds.entry(b.split(':').next().unwrap().to_string()).or_default() += 1; }
    for (k, v) in &kinds { println!("QA failure kind\t{k}\t{v}"); }
    for b in bad.iter().take(12) { println!("QA FAIL {b}"); }
    assert!(bad.is_empty(), "{} failures", bad.len());
}

/// S-3: the fake `Closed` that `owner_seal`'s `seal_once` answers with no host, driven as it would be.
#[test]
fn qa_s3_fake_closed() {
    for reopen_ok in [true, false] {
        let mut st = (0u32, reopen_ok);
        let (a, calls, was_err) = owner_seal_steps(
            &mut st,
            |_s: &(u32, bool)| Some(Figures { segment: 1, own_seq: 1, own_checkpoint: 1 }),
            |s: &mut (u32, bool)| s.1,
            |s: &mut (u32, bool)| { s.0 += 1; (Err(HostError::Closed), true) },
            |_s: &mut (u32, bool), _l: &LimitsReport| {},
        );
        println!("QA S-3 reopen_ok={reopen_ok}: row={:?} done={} text={:?} calls={calls} real seals=0 was_err={was_err}", a.row, a.done, a.text);
    }
}
