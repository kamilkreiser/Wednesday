//! QA-AUDIT-WIRE task 1 / task 2: the checker's OWN alphabet of audit-host answers, run through the
//! head's public `act_on_record`, `act_on_seal`, `drive_seal`. Scratch copy only; not part of the lane.
//! Values: built from public fields, plus a REAL host (temp folder) for SignedHead / SegmentInfo / Bundle.
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
use coagent_daemon::audit::{act_on_record, act_on_seal, drive_seal, Action, Around};
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
    let root: PathBuf = PathBuf::from(format!("/private/tmp/claude-501/qaw/h/{}-{}", std::process::id(), N.fetch_add(1, std::sync::atomic::Ordering::SeqCst)));
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

fn line(call: &str, label: &str, around: &Around, a: &Action) -> String {
    format!(
        "{call}\t{label}\tseg_before={} closed_after={}\trow={}\tdone={}\treopen={}\tread_segment={}\tcall_again={}\tlimits={}\ttext={}",
        around.segment_before, around.closed_after, a.row, a.done, a.reopen, a.read_segment, a.call_again, a.limits.is_some(), a.text
    )
}

#[test]
fn qa_alphabet_table() {
    let r = real();
    let seg = 1u64;
    let mut out = vec![];
    let arounds = [
        Around { segment_before: seg, closed_after: false },
        Around { segment_before: seg, closed_after: true },
    ];
    // ---- seal answers
    let mut seal_answers: Vec<(String, Result<SealReport, HostError>)> = vec![];
    seal_answers.push(("Ok(SealReport{limits:None})".into(), Ok(r.report.clone())));
    seal_answers.push(("Ok(SealReport{limits:Some})".into(), Ok(SealReport { limits: Some(lim(true)), ..r.report.clone() })));
    for (n, e) in errors(seg) {
        seal_answers.push((format!("Err({n})"), Err(e)));
    }
    // LimitsChanged wrapping every Outcome and every error (one level), and two levels
    for (n, o) in outcomes(&r) {
        seal_answers.push((format!("Err(LimitsChanged{{Ok({n})}})"), Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Ok(o)) })));
    }
    for (n, e) in errors(seg) {
        seal_answers.push((format!("Err(LimitsChanged{{Err({n})}})"), Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Err(e)) })));
    }
    seal_answers.push((
        "Err(LimitsChanged{Err(LimitsChanged{Ok(Checkpoint)})})".into(),
        Err(HostError::LimitsChanged {
            limits: lim(true),
            answer: Box::new(Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Ok(Outcome::Checkpoint(r.head.clone()))) })),
        }),
    ));
    let mut fails = vec![];
    for (n, ans) in &seal_answers {
        for ar in &arounds {
            let a = act_on_seal(ans, *ar);
            out.push(line("seal", n, ar, &a));
            // the checker's rules (task 1 / task 2):
            if a.call_again {
                fails.push(format!("seal {n}: call_again"));
            }
            let is_ok = ans.is_ok();
            let moved_commit = n.contains("SealCommitFailed{moved}");
            let only_ok_or_moved = is_ok || moved_commit;
            if a.done && !only_ok_or_moved {
                fails.push(format!("seal {n}: done although not Ok and no moved commit"));
            }
            if !a.done && only_ok_or_moved && !n.contains("LimitsChanged{Ok") {
                fails.push(format!("seal {n}: a landed seal not reported done"));
            }
            if n.starts_with("Err(LimitsChanged{Ok") && a.done {
                fails.push(format!("seal {n}: m-2 read as done"));
            }
            if (n.contains("LandedUnknown") || n.contains("Closed")) && !a.reopen {
                fails.push(format!("seal {n}: no reopen"));
            }
            if n.contains("NothingToSeal") && (a.done || a.call_again) {
                fails.push(format!("seal {n}: NothingToSeal retried or done"));
            }
            if n.starts_with("Err(LimitsChanged") && a.limits.is_none() {
                fails.push(format!("seal {n}: limits report dropped"));
            }
        }
    }
    // ---- record answers
    let mut rec_answers: Vec<(String, Result<Outcome, HostError>)> = vec![];
    for (n, o) in outcomes(&r) {
        rec_answers.push((format!("Ok({n})"), Ok(o)));
    }
    for (n, e) in errors(seg) {
        rec_answers.push((format!("Err({n})"), Err(e)));
    }
    for (n, o) in outcomes(&r) {
        rec_answers.push((format!("Err(LimitsChanged{{Ok({n})}})"), Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Ok(o)) })));
    }
    for (n, e) in errors(seg) {
        rec_answers.push((format!("Err(LimitsChanged{{Err({n})}})"), Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Err(e)) })));
    }
    for (n, ans) in &rec_answers {
        for ar in &arounds {
            let a = act_on_record(ans, *ar);
            out.push(line("record", n, ar, &a));
            let landed = n == "Ok(Recorded(7))" || n == "Err(LimitsChanged{Ok(Recorded(7))})";
            if a.done != landed {
                fails.push(format!("record {n}: done={} but landed={landed}", a.done));
            }
            if a.call_again {
                fails.push(format!("record {n}: call_again"));
            }
            if landed && a.recorded != Some(7) {
                fails.push(format!("record {n}: number lost"));
            }
            if (n.contains("LandedUnknown") || n.ends_with("(Closed)")) && !a.reopen {
                fails.push(format!("record {n}: no reopen"));
            }
        }
    }
    // ---- task 1 (iii): the segment read before the call fell back to 0 (status() failed), host at 2,
    // the commit did NOT land (segment_now = 2 = the real segment before)
    let hazard = act_on_seal(
        &Err(HostError::SealCommitFailed { cause: AuditError::Store(StoreError::Unavailable("x")), segment_now: 2 }),
        Around { segment_before: 0, closed_after: false },
    );
    out.push(line("seal", "HAZARD SealCommitFailed{segment_now:2} with segment_before fallen back to 0 (real 2: NOT landed)", &Around { segment_before: 0, closed_after: false }, &hazard));
    let hazard2 = act_on_seal(
        &Err(HostError::SealCommitFailed { cause: AuditError::Store(StoreError::Unavailable("x")), segment_now: 2 }),
        Around { segment_before: 2, closed_after: false },
    );
    out.push(line("seal", "CONTROL SealCommitFailed{segment_now:2} with segment_before 2 (NOT landed)", &Around { segment_before: 2, closed_after: false }, &hazard2));
    let p = "/private/tmp/claude-501/qaw/out_alpha.tsv";
    std::fs::write(p, out.join("\n") + "\n").unwrap();
    println!("QA alphabet: {} seal answers, {} record answers, {} lines -> {p}", seal_answers.len(), rec_answers.len(), out.len());
    println!("QA hazard (iii): done={} row={} text={}", hazard.done, hazard.row, hazard.text);
    println!("QA control (iii): done={} row={} text={}", hazard2.done, hazard2.row, hazard2.text);
    for f in &fails {
        println!("QA RULE BROKEN: {f}");
    }
    assert!(fails.is_empty(), "{} rule(s) broken", fails.len());
}

/// Task 2: N owner commands through `drive_seal`, each answered from the alphabet (every failing
/// answer and Ok, in turn): exactly N calls of `seal`.
#[test]
fn qa_n_commands_n_calls() {
    let r = real();
    let mut answers: Vec<Result<SealReport, HostError>> = vec![Ok(r.report.clone())];
    for (_, e) in errors(1) {
        answers.push(Err(e.clone()));
        answers.push(Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Err(e)) }));
    }
    answers.push(Err(HostError::LimitsChanged { limits: lim(true), answer: Box::new(Ok(Outcome::Checkpoint(r.head.clone()))) }));
    let n_cmds = 3 * answers.len() + 7; // over 100
    let mut calls_total = 0u64;
    let mut i = 0usize;
    for _ in 0..n_cmds {
        let (_a, calls, _) = drive_seal(|| {
            calls_total += 1;
            let ans = answers[i % answers.len()].clone();
            i += 1;
            (ans, Around { segment_before: 1, closed_after: false })
        });
        assert_eq!(calls, 1, "a command made {calls} calls");
    }
    println!("QA drive_seal: {n_cmds} owner commands, {calls_total} seal calls, alphabet {}", answers.len());
    assert_eq!(calls_total, n_cmds as u64);
}
