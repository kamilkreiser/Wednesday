//! QA-AUDIT-HOST-FIX (the independent check of branch `audit-host-fix`, head 5b3a395): my own fault
//! schedules through the crate's fault injector. Written by the checker, not by the builder; lives
//! only in the checker's clone (one `mod qahf;` line added there to `src/tests/mod.rs`).
//!
//! For each operation (a local record, a member-requested record, an own checkpoint, a peer's event,
//! a release with and without a tombstone, a whole seal) it fails filesystem operations of that call
//! and of its re-open BY INDEX (every single index; every pair; then a generated run of random sets
//! and persistent "disk full" rules), and after each call compares the answer with what a FRESH open
//! of a copy of the folder shows. Then it applies the caller's rule of `docs/AUDIT-HOST.md` §3 (the
//! P-4 answer table) mechanically and checks that the change is in the store exactly once.
//! Every disagreement is collected; the test prints a class table and fails if any was found.
//!
//! QA-AUDIT-HOST-NOTES (independent check of branch `audit-host-notes`): copied UNCOMMITTED into the
//! checker's own trees at 9145840 and 52ad858; added only a per-case line (`QAHN CASE`), a kind
//! filter (`QAHN_ONLY`, for the ablation run; schedules are drawn identically), and at 52ad858 only
//! the seal's new `limits` field printed apart (`QAHN SEALLIMITS`).

thread_local! {
    static QAHN_RUN: std::cell::Cell<&'static str> = const { std::cell::Cell::new("-") };
    static QAHN_SEALS: RefCell<Vec<String>> = const { RefCell::new(Vec::new()) };
}

fn qahn_only(k: K) -> bool {
    match std::env::var("QAHN_ONLY") {
        Ok(v) if !v.is_empty() => format!("{k:?}") == v,
        _ => true,
    }
}

fn qahn_t(s: &Snap) -> String {
    format!("({},{},{},{},{},{})", s.seq, s.cps, s.seg, s.p3, s.p2, s.logical)
}

fn qahn_detail(a: &Ans) -> String {
    let s = match a {
        Ans::O(Ok(o)) => format!("Ok({o:?})"),
        Ans::S(Ok(seg)) => format!("Ok(seg {seg})"),
        Ans::O(Err(e)) | Ans::S(Err(e)) => format!("Err({e:?})"),
    };
    s.replace('\n', " ")
}

use std::cell::RefCell;
use std::collections::BTreeMap;
use std::path::PathBuf;
use std::rc::Rc;

use coagent_audit::anchor::AuditAnchor;
use coagent_audit::chain::AuditEvent;

use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::{AuditHost, Causer, HostError, Input, Outcome, SealTrigger};

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum K {
    Record,
    RecordFor,
    Checkpoint,
    Receive,
    Release,
    ReleaseTomb,
    Seal,
}

const KINDS: [K; 7] = [
    K::Record,
    K::RecordFor,
    K::Checkpoint,
    K::Receive,
    K::Release,
    K::ReleaseTomb,
    K::Seal,
];

struct Tmpl {
    w: World,
    dir: PathBuf,
    root: PathBuf,
    ev2: AuditEvent,
    /// The store's logical record count after a CLEAN release of peer 3 (calibrated on a copy).
    rel_post: usize,
}

/// V=1, members 0..3; three own records, peer 3's three events (and, with `tomb`, its checkpoint
/// countersigned), peer 3 removed; an event of peer 2 made but NOT yet delivered (for `Receive`).
fn template(b: u8, tomb: bool) -> Tmpl {
    let mut w = World::new(b, 4, 4);
    let dir = scratch(&format!("qahf-tmpl-{b}"));
    let root = dir.join("host");
    let mut h = create_host(&w, 1, &root, cfg(&w));
    let mut p3 = mem_member(&w, 3);
    for n in 0..3u64 {
        host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
        let s = p3.record(&w.ids[3], bare("p"), t(n + 1)).unwrap();
        let e = p3
            .outgoing(s)
            .into_iter()
            .find(|(to, _)| *to == w.key(1))
            .unwrap()
            .1;
        h.apply(&w.ids[1], Input::Receive(e), t(n + 1)).unwrap();
    }
    if tomb {
        let hd = p3.checkpoint_now(&w.ids[3], t(5)).unwrap();
        match h.apply(&w.ids[1], Input::ReceiveHead(hd), t(5)) {
            Ok(Outcome::Countersigned(_)) => {}
            o => panic!("template: peer 3's checkpoint not taken: {o:?}"),
        }
    }
    let r = w.remove(3);
    h.apply(&w.ids[1], Input::Roster(r), t(10)).unwrap();
    let mut p2 = mem_member(&w, 2);
    let s2 = p2.record(&w.ids[2], bare("p2"), t(11)).unwrap();
    let ev2 = p2
        .outgoing(s2)
        .into_iter()
        .find(|(to, _)| *to == w.key(1))
        .unwrap()
        .1;
    drop(h);
    // calibrate: a clean release on a copy
    let cal = dir.join("cal");
    copy_tree(&root, &cal);
    let (mut hc, _) = open_host(&w, 1, &cal, cfg(&w), 40).unwrap();
    match hc.apply(&w.ids[1], Input::Release(w.key(3)), t(41)) {
        Ok(Outcome::Released(_)) => {}
        o => panic!("template: clean release failed: {o:?}"),
    }
    let rel_post = hc.status().unwrap().logical_records;
    drop(hc);
    std::fs::rename(&cal, dir.join("cal-done")).unwrap();
    Tmpl { w, dir, root, ev2, rel_post }
}

#[derive(Clone, Debug, PartialEq)]
struct Snap {
    seq: u64,
    cps: usize,
    seg: u64,
    p3: bool,
    p2: u64,
    logical: usize,
    anchor: AuditAnchor,
}

fn snap_of(h: &AuditHost, w: &World) -> Snap {
    let m = h.member().unwrap();
    Snap {
        seq: m.own().seq(),
        cps: m.own().checkpoints().len(),
        seg: m.segment(),
        p3: m.peer(&w.key(3)).is_some(),
        p2: m.peer(&w.key(2)).map(|c| c.next_seq()).unwrap_or(0),
        logical: h.status().map(|s| s.logical_records).unwrap_or(usize::MAX),
        anchor: m.anchor(),
    }
}

enum Ans {
    O(Result<Outcome, HostError>),
    S(Result<u64, HostError>),
}

impl Ans {
    fn err(&self) -> Option<&HostError> {
        match self {
            Ans::O(Err(e)) | Ans::S(Err(e)) => Some(e),
            _ => None,
        }
    }
    fn short(&self) -> String {
        fn e_short(e: &HostError) -> String {
            match e {
                HostError::Reopened { landed, .. } => format!("Err(Reopened{{landed:{landed}}})"),
                HostError::LandedUnknown { .. } => "Err(LandedUnknown)".into(),
                HostError::LimitsChanged { answer, .. } => match &**answer {
                    Ok(_) => "Err(LimitsChanged{Ok})".into(),
                    Err(e) => format!("Err(LimitsChanged{{{}}})", e_short(e)),
                },
                HostError::SealCommitFailed { segment_now, .. } => {
                    format!("Err(SealCommitFailed{{segment_now:{segment_now}}})")
                }
                HostError::Dir(d) => {
                    let s = format!("{d:?}");
                    format!("Err(Dir({}))", s.split([' ', '(']).next().unwrap_or(""))
                }
                HostError::Audit(a) => {
                    let s = format!("{a:?}");
                    format!("Err(Audit({}))", s.split([' ', '(']).next().unwrap_or(""))
                }
                other => {
                    let s = format!("{other:?}");
                    format!("Err({})", s.split([' ', '(', '{']).next().unwrap_or(""))
                }
            }
        }
        match self {
            Ans::O(Ok(o)) => {
                let s = format!("{o:?}");
                format!("Ok({})", s.split(['(', ' ']).next().unwrap_or(""))
            }
            Ans::S(Ok(seg)) => format!("Ok(SealReport seg {seg})"),
            Ans::O(Err(e)) | Ans::S(Err(e)) => e_short(e),
        }
    }
}

fn act(h: &mut AuditHost, tm: &Tmpl, k: K, now: u64) -> Ans {
    let id = &tm.w.ids[1];
    let rec = |c: Causer| Input::Record {
        causer: c,
        input: owned("qahf.ev", Some("qa"), None),
    };
    match k {
        K::Record => Ans::O(h.apply(id, rec(Causer::LocalHuman), t(now))),
        K::RecordFor => Ans::O(h.apply(id, rec(Causer::Member(tm.w.key(2))), t(now))),
        K::Checkpoint => Ans::O(h.apply(id, Input::Checkpoint, t(now))),
        K::Receive => Ans::O(h.apply(id, Input::Receive(tm.ev2.clone()), t(now))),
        K::Release | K::ReleaseTomb => Ans::O(h.apply(id, Input::Release(tm.w.key(3)), t(now))),
        K::Seal => Ans::S(
            h.seal(id, SealTrigger::OwnerCommand, t(now))
                .map(|r| r.info.segment),
        ),
    }
}

/// Is the change of kind `k` in `s` (a fresh open), measured against `b` (before the call)?
fn landed(k: K, b: &Snap, s: &Snap, rel_post: usize) -> bool {
    match k {
        K::Record | K::RecordFor => s.seq == b.seq + 1,
        K::Checkpoint => s.cps == b.cps + 1,
        // a peer chain's next_seq: 0 = none; after its first event (seq 1) it is 2
        K::Receive => s.p2 >= 2 && s.p2 > b.p2,
        K::Release | K::ReleaseTomb => s.logical == rel_post && b.logical != rel_post,
        K::Seal => s.seg == b.seg + 1,
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Say {
    Landed,
    NotLanded,
    Unknown,
}

fn say_err(b: &Snap, e: &HostError) -> Say {
    match e {
        HostError::Reopened { landed, .. } => {
            if *landed {
                Say::Landed
            } else {
                Say::NotLanded
            }
        }
        HostError::LandedUnknown { .. } => Say::Unknown,
        HostError::LimitsChanged { answer, .. } => match &**answer {
            Ok(_) => Say::Landed,
            Err(e2) => say_err(b, e2),
        },
        HostError::SealCommitFailed { segment_now, .. } => {
            if *segment_now == b.seg + 1 {
                Say::Landed
            } else {
                Say::NotLanded
            }
        }
        _ => Say::NotLanded,
    }
}

fn say(b: &Snap, a: &Ans) -> Say {
    match a.err() {
        None => Say::Landed,
        Some(e) => say_err(b, e),
    }
}

fn short_name(dir: &str, name: &str) -> String {
    let mut out = String::new();
    let mut digit = false;
    for c in name.chars() {
        if c.is_ascii_digit() {
            if !digit {
                out.push('#');
            }
            digit = true;
        } else {
            out.push(c);
            digit = false;
        }
    }
    if out.len() > 18 {
        out.truncate(18);
    }
    format!("{dir}/{out}")
}

/// A fault schedule: which operations of the call fail.
#[derive(Clone, Debug)]
enum Sched {
    /// Fail exactly the operations with these indices (0-based, counted over the whole call).
    Idx(Vec<usize>),
    /// From index `from` on, fail EVERY operation of this kind in this directory ("disk full").
    From(usize, Op, &'static str),
}

struct Outcome1 {
    class: String,
    problems: Vec<String>,
}

/// Count the operations a clean call of kind `k` makes.
fn count_ops(tm: &Tmpl, k: K, case: &str) -> (usize, Vec<String>) {
    let base = scratch(&format!("qahf-count-{case}"));
    let root = base.join("host");
    copy_tree(&tm.root, &root);
    let (mut h, _) = open_host(&tm.w, 1, &root, cfg(&tm.w), 50).unwrap();
    fault::arm(Rule::None);
    let _ = act(&mut h, tm, k, 60);
    let rep = fault::disarm();
    drop(h);
    scratch_done(&base);
    let names = rep
        .log
        .iter()
        .map(|(op, d, n)| format!("{op:?}:{}", short_name(d, n)))
        .collect();
    (rep.ops, names)
}

fn run_case(tm: &Tmpl, k: K, sched: &Sched, case: &str) -> Outcome1 {
    let w = &tm.w;
    let base = scratch(&format!("qahf-{case}"));
    let root = base.join("host");
    copy_tree(&tm.root, &root);
    let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
    let before = snap_of(&h, w);
    QAHN_SEALS.with(|v| v.borrow_mut().clear());
    let mut qahn_final = String::from("?");
    let mut qahn_dirty_next = String::from("-");
    let failed: Rc<RefCell<Vec<String>>> = Rc::new(RefCell::new(Vec::new()));
    let f2 = failed.clone();
    let mut i = 0usize;
    let s2 = sched.clone();
    fault::arm(Rule::FailEvery(Box::new(move |c| {
        let n = i;
        i += 1;
        let hit = match &s2 {
            Sched::Idx(v) => v.contains(&n),
            Sched::From(from, op, dir) => n >= *from && c.op == *op && c.dir == *dir,
        };
        if hit {
            f2.borrow_mut()
                .push(format!("{:?}:{}", c.op, short_name(c.dir, c.name)));
        }
        hit
    })));
    let ans = act(&mut h, tm, k, 60);
    fault::disarm();
    let mut problems = Vec::new();
    let said = say(&before, &ans);
    let has_member = h.member().is_ok();
    let host_snap = has_member.then(|| snap_of(&h, w));
    // a fresh open of a copy of the folder, now
    let copy = base.join("copy");
    copy_tree(&root, &copy);
    let fresh = open_host(w, 1, &copy, cfg(w), 70);
    let (fresh_snap, fresh_limits_before) = match &fresh {
        Ok((h2, r)) => (Some(snap_of(h2, w)), r.limits.before),
        Err(e) => {
            problems.push(format!("a fresh open REFUSED the folder: {e:?}"));
            (None, None)
        }
    };
    drop(fresh);
    let is_landed = fresh_snap.as_ref().map(|s| landed(k, &before, s, tm.rel_post));
    // the answer against the fresh open
    match (said, is_landed) {
        (Say::Landed, Some(false)) => problems.push(format!(
            "answered LANDED ({}) but a fresh open shows it NOT in the store",
            ans.short()
        )),
        (Say::NotLanded, Some(true)) => problems.push(format!(
            "answered NOT landed ({}) but a fresh open shows it IN the store",
            ans.short()
        )),
        _ => {}
    }
    // a record answered Ok must carry the number it got
    if let (Ans::O(Ok(Outcome::Recorded(n))), Some(s)) = (&ans, &fresh_snap) {
        if *n != s.seq {
            problems.push(format!("Recorded({n}) but fresh own seq {}", s.seq));
        }
    }
    if let (Ans::S(Ok(seg)), Some(s)) = (&ans, &fresh_snap) {
        if *seg != s.seg {
            problems.push(format!("seal Ok segment {seg} but fresh segment {}", s.seg));
        }
    }
    // "landed unknown" only when the host could not know (no member); an ordinary failure never
    // when the host is closed
    match (said, has_member) {
        (Say::Unknown, true) => problems.push(format!(
            "LandedUnknown although the host has a member ({})",
            ans.short()
        )),
        (Say::NotLanded, false) if !matches!(ans.err(), Some(HostError::Closed)) => problems.push(
            format!("an ordinary failure ({}) while the host is closed", ans.short()),
        ),
        _ => {}
    }
    // a restart agrees with the host
    if let (Some(hs), Some(fs)) = (&host_snap, &fresh_snap) {
        let stub = hs.anchor == fs.anchor
            && (hs.seq, hs.cps, hs.seg, hs.p3, hs.logical) == (fs.seq, fs.cps, fs.seg, fs.p3, fs.logical)
            && hs.p2 == 1
            && fs.p2 == 0;
        if stub {
            problems.push(
                "NOTE-STUB: host holds an empty peer-2 chain (next_seq 1) a restart does not (0); anchors EQUAL"
                    .into(),
            );
        } else if hs != fs {
            problems.push(format!(
                "a restart DISAGREES with the host (anchors equal {}): host {:?} fresh {:?}",
                hs.anchor == fs.anchor,
                (hs.seq, hs.cps, hs.seg, hs.p3, hs.p2, hs.logical),
                (fs.seq, fs.cps, fs.seg, fs.p3, fs.p2, fs.logical)
            ));
        }
    }
    // the dirty flags tell the truth about the disk
    let mut dirty = false;
    if has_member {
        let m_limits = h.member().unwrap().limits();
        let m_anchor = h.member().unwrap().anchor();
        if h.limits_dirty() {
            dirty = true;
        } else if fresh_snap.is_some() && fresh_limits_before != Some(m_limits) {
            problems.push(format!(
                "limits not dirty but anchors/limits holds {fresh_limits_before:?}, in force {m_limits:?}"
            ));
        }
        match h.status() {
            Ok(st) if !st.anchor_saved => dirty = true,
            Ok(_) => {
                let cur =
                    crate::host::read_anchor_file(&root.join("anchors").join("current")).ok();
                if cur != Some(Some(m_anchor)) {
                    problems.push("anchor_saved but anchors/current is not the member's".into());
                }
            }
            Err(e) => problems.push(format!("status() fails after the call: {e:?}")),
        }
        if h.pending_held() {
            problems.push("pending_held set after the call returned".into());
        }
        if let Err(e) = h.export(&w.ids[1]) {
            problems.push(format!("export() fails after the call: {e:?}"));
        }
    }
    // the dirty-state rule: while the failed write still fails, the next change is refused
    if dirty {
        let pre = snap_of(&h, w);
        fault::arm(Rule::FailEvery(Box::new(|c| {
            c.dir == "anchors" && c.op == Op::CreateTemp
        })));
        let r = act(&mut h, tm, K::Record, 61);
        fault::disarm();
        let post = h.member().ok().map(|_| snap_of(&h, w));
        qahn_dirty_next = r.short();
        if r.err().is_none() || post.as_ref().map(|p| p.seq) != Some(pre.seq) {
            problems.push(format!(
                "DIRTY RULE: a next change was accepted while the failed write still fails ({})",
                r.short()
            ));
        }
    }
    // the caller's rule (docs §3 table), applied mechanically
    let retry = match said {
        Say::Landed => false,
        Say::NotLanded => true,
        Say::Unknown => {
            // open the host again, read what is there, then decide
            drop(h);
            match open_host(w, 1, &root, cfg(w), 80) {
                Ok((h2, _)) => {
                    let s = snap_of(&h2, w);
                    h = h2;
                    !landed(k, &before, &s, tm.rel_post)
                }
                Err(e) => {
                    problems.push(format!("after LandedUnknown the host cannot be opened: {e:?}"));
                    scratch_done(&base);
                    return Outcome1 {
                        class: format!("{}|unknown|{:?}", ans.short(), is_landed),
                        problems,
                    };
                }
            }
        }
    };
    // a host closed by an ordinary answer would make the caller open it again too
    if h.member().is_err() {
        drop(h);
        h = match open_host(w, 1, &root, cfg(w), 81) {
            Ok((h2, _)) => h2,
            Err(e) => {
                problems.push(format!("the closed host cannot be opened again: {e:?}"));
                scratch_done(&base);
                return Outcome1 {
                    class: format!("{}|closed|{:?}", ans.short(), is_landed),
                    problems,
                };
            }
        };
    }
    let mut retry_ans = String::from("-");
    if retry {
        let r = act(&mut h, tm, k, 90);
        retry_ans = r.short();
        if let Some(e) = r.err() {
            problems.push(format!("the caller's retry failed: {e:?}"));
        }
    }
    // the host is not stuck refusing: a clean record goes through
    let extra = act(&mut h, tm, K::Record, 95);
    if extra.err().is_some() {
        problems.push(format!(
            "HOST STUCK: a clean record after the writes succeed is refused ({})",
            extra.short()
        ));
    }
    let extra_n = u64::from(extra.err().is_none());
    drop(h);
    match open_host(w, 1, &root, cfg(w), 99) {
        Ok((h3, _)) => {
            let f = snap_of(&h3, w);
            qahn_final = qahn_t(&f);
            let rec_n = u64::from(matches!(k, K::Record | K::RecordFor));
            let ok = match k {
                K::Record | K::RecordFor => f.seq == before.seq + 1 + extra_n,
                K::Checkpoint => f.cps == before.cps + 1 && f.seq == before.seq + extra_n,
                K::Receive => f.p2 == 2 && f.seq == before.seq + extra_n,
                K::Release | K::ReleaseTomb => f.logical == tm.rel_post + extra_n as usize && f.seq == before.seq + extra_n,
                K::Seal => f.seg == before.seg + 1 && f.seq == before.seq + extra_n,
            };
            if !ok {
                problems.push(format!(
                    "CALLER RULE: the change is not in the store EXACTLY once: before {:?} final {:?} (record kind {rec_n}, extra {extra_n})",
                    (before.seq, before.cps, before.seg, before.p3, before.p2, before.logical),
                    (f.seq, f.cps, f.seg, f.p3, f.p2, f.logical)
                ));
            }
        }
        Err(e) => problems.push(format!("final open refused: {e:?}")),
    }
    scratch_done(&base);
    let fl = failed.borrow().join("+");
    println!(
        "QAHN CASE {} {case} {k:?} {sched:?} | {} | member {has_member} | fresh {} | dirty {dirty} next {qahn_dirty_next} | retry {retry_ans} | final {qahn_final} | before {} | extra {extra_n} | failed {fl} | problems {} | detail {}",
        QAHN_RUN.with(|r| r.get()),
        ans.short(),
        fresh_snap.as_ref().map_or("REFUSED".into(), qahn_t),
        qahn_t(&before),
        problems.iter().filter(|p| !p.starts_with("NOTE-STUB")).count(),
        qahn_detail(&ans)
    );
    QAHN_SEALS.with(|v| {
        let v = v.borrow();
        if !v.is_empty() {
            println!("QAHN SEALLIMITS {} {case} {sched:?} | {}", QAHN_RUN.with(|r| r.get()), v.join(" ; "));
        }
    });
    Outcome1 {
        class: format!(
            "{fl}|{}|member {}|fresh landed {}|retry {}",
            ans.short(),
            has_member,
            is_landed.map_or("?".into(), |b| b.to_string()),
            retry_ans
        ),
        problems,
    }
}

#[derive(Default)]
struct Tally {
    cases: usize,
    classes: BTreeMap<(K, String), usize>,
    bad: Vec<String>,
    total: usize,
    per_kind: BTreeMap<K, usize>,
    notes: BTreeMap<K, usize>,
}

impl Tally {
    fn add(&mut self, k: K, sched: &Sched, o: Outcome1) {
        self.cases += 1;
        // the class without the failed-operation names for the generated run (kept for exhaustive)
        *self.classes.entry((k, o.class.clone())).or_default() += 1;
        for p in o.problems {
            if p.starts_with("NOTE-STUB") {
                *self.notes.entry(k).or_default() += 1;
                continue;
            }
            self.total += 1;
            let per = self.per_kind.entry(k).or_default();
            *per += 1;
            if *per <= 40 {
                self.bad.push(format!("{k:?} {sched:?} [{}]: {p}", o.class));
            }
        }
    }
    fn print(&self, title: &str) {
        println!(
            "QAHF {title}: {} cases, {} problems (per kind {:?}); empty-peer-chain stubs (not a problem, see verdict) {:?}",
            self.cases, self.total, self.per_kind, self.notes
        );
        for ((k, c), n) in &self.classes {
            println!("QAHF CLASS {k:?} | {c} | x{n}");
        }
        for b in &self.bad {
            println!("QAHF PROBLEM {b}");
        }
    }
}

fn template_for(k: K) -> Tmpl {
    match k {
        K::ReleaseTomb => template(150, true),
        _ => template(140, false),
    }
}

/// Every single failed operation, then every PAIR, for each kind of call.
#[test]
fn qahf_exhaustive_singles_and_pairs() {
    QAHN_RUN.with(|r| r.set("exh"));
    let mut tally = Tally::default();
    for k in KINDS {
        if !qahn_only(k) {
            continue;
        }
        let tm = template_for(k);
        let (n, names) = count_ops(&tm, k, &format!("{k:?}"));
        println!("QAHF OPS {k:?}: {n} operations in a clean call: {}", names.join(", "));
        // singles; each also says how many operations its run made, for the pairs
        for i in 0..n {
            let s = Sched::Idx(vec![i]);
            let o = run_case(&tm, k, &s, &format!("{k:?}-s{i}"));
            tally.add(k, &s, o);
        }
        // pairs: the second index runs over the operations a single failure's run can reach
        // (a re-open adds operations, so up to n + 24)
        for i in 0..n {
            for j in (i + 1)..(n + 24) {
                let s = Sched::Idx(vec![i, j]);
                let o = run_case(&tm, k, &s, &format!("{k:?}-p{i}-{j}"));
                tally.add(k, &s, o);
            }
        }
        scratch_done(&tm.dir);
    }
    tally.print("exhaustive");
    assert!(tally.total == 0, "{} problems", tally.total);
}

/// Persistent failures ("disk full" from operation i on, of one kind in one directory), each kind.
#[test]
fn qahf_persistent_rules() {
    let mut tally = Tally::default();
    let rules: [(Op, &'static str); 10] = [
        (Op::CreateTemp, "anchors"),
        (Op::SyncDir, "anchors"),
        (Op::SyncDir, "store"),
        (Op::CreateTemp, "store"),
        (Op::Rename, "store"),
        (Op::Unlink, "store"),
        (Op::SyncFile, "anchors"),
        (Op::Rename, "anchors"),
        (Op::Link, "archive"),
        (Op::Unlink, "anchors"),
    ];
    QAHN_RUN.with(|r| r.set("per"));
    for k in KINDS {
        if !qahn_only(k) {
            continue;
        }
        let tm = template_for(k);
        let (n, _) = count_ops(&tm, k, &format!("p{k:?}"));
        for (op, dir) in rules {
            for from in 0..n {
                let s = Sched::From(from, op, dir);
                let o = run_case(&tm, k, &s, &format!("{k:?}-f{from}"));
                tally.add(k, &s, o);
            }
        }
        scratch_done(&tm.dir);
    }
    tally.print("persistent");
    assert!(tally.total == 0, "{} problems", tally.total);
}

/// A generated run: QAHF_CASES (default 2,400) random schedules, my own seed (QAHF_SEED, hex;
/// default 0x9a7fc0de5eed0b1e): a kind, then 1 to 4 random indices, or a persistent rule.
#[test]
fn qahf_generated() {
    let cases: usize = std::env::var("QAHF_CASES")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(2_400);
    let mut x: u64 = std::env::var("QAHF_SEED")
        .ok()
        .and_then(|v| u64::from_str_radix(v.trim_start_matches("0x"), 16).ok())
        .unwrap_or(0x9a7f_c0de_5eed_0b1e);
    println!("QAHF generated: seed {x:#018x}, {cases} cases");
    QAHN_RUN.with(|r| r.set("gen"));
    let mut next = move || {
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        x
    };
    let tmpls = [template(160, false), template(165, true)];
    let mut counts = BTreeMap::new();
    for k in KINDS {
        let tm = &tmpls[usize::from(k == K::ReleaseTomb)];
        counts.insert(k, count_ops(tm, k, &format!("g{k:?}")).0);
    }
    let mut tally = Tally::default();
    let ops = [
        Op::CreateTemp,
        Op::Write,
        Op::SyncFile,
        Op::Rename,
        Op::Link,
        Op::Unlink,
        Op::SyncDir,
    ];
    let dirs = ["store", "anchors", "archive"];
    for c in 0..cases {
        let k = KINDS[(next() % KINDS.len() as u64) as usize];
        let tm = &tmpls[usize::from(k == K::ReleaseTomb)];
        let n = counts[&k] + 24;
        let s = if next() % 5 == 0 {
            Sched::From(
                (next() % counts[&k] as u64) as usize,
                ops[(next() % ops.len() as u64) as usize],
                dirs[(next() % dirs.len() as u64) as usize],
            )
        } else {
            let m = 1 + (next() % 4) as usize;
            let mut v: Vec<usize> = (0..m).map(|_| (next() % n as u64) as usize).collect();
            v.sort_unstable();
            v.dedup();
            Sched::Idx(v)
        };
        if !qahn_only(k) {
            continue;
        }
        let mut o = run_case(tm, k, &s, &format!("g{c}"));
        // group the generated run's classes by answer and fresh state only
        o.class = o.class.split_once('|').map(|x| x.1.to_string()).unwrap_or(o.class);
        tally.add(k, &s, o);
    }
    for tm in &tmpls {
        scratch_done(&tm.dir);
    }
    tally.print("generated");
    assert!(tally.total == 0, "{} problems", tally.total);
}


// ------------------------------------------------------------------------------------------------
// Targeted tests: N-3 at each step of the collection, N-r2-2 on every path of `release`, N-4 at a
// re-open, the dirty-state rule inside a seal.
// ------------------------------------------------------------------------------------------------

/// N-3: a seal; each store operation AFTER the commit put's directory sync (the collection, then
/// step 4) failed once, and then every one of them at once. When the host keeps a member, `status()`
/// and `export()` answer, and a restart agrees with the host.
#[test]
fn qahf_n3_each_collection_step() {
    let tm = template(170, false);
    let w = &tm.w;
    // the operations of a clean seal, to find those after the commit put
    let (n, _) = count_ops(&tm, K::Seal, "n3count");
    let mut lines = Vec::new();
    let mut bad = Vec::new();
    // which index is the commit put's directory sync: the one whose name holds F07 (the Segment)
    let commit_idx = {
        let base = scratch("qahf-n3-find");
        let root = base.join("host");
        copy_tree(&tm.root, &root);
        let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
        let found = Rc::new(RefCell::new(None));
        let f2 = found.clone();
        let mut i = 0usize;
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            if c.op == Op::SyncDir && c.dir == "store" && c.name.contains(".F07.") {
                f2.borrow_mut().get_or_insert(i);
            }
            i += 1;
            false
        })));
        let _ = act(&mut h, &tm, K::Seal, 60);
        fault::disarm();
        drop(h);
        scratch_done(&base);
        let v = *found.borrow();
        v.expect("no commit put sync found")
    };
    let mut scheds: Vec<Sched> = ((commit_idx + 1)..n).map(|i| Sched::Idx(vec![i])).collect();
    scheds.push(Sched::Idx(((commit_idx + 1)..n).collect()));
    for s in scheds {
        let base = scratch("qahf-n3");
        let root = base.join("host");
        copy_tree(&tm.root, &root);
        let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
        let mut i = 0usize;
        let s2 = s.clone();
        let failed: Rc<RefCell<Vec<String>>> = Rc::new(RefCell::new(Vec::new()));
        let f2 = failed.clone();
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            let k = i;
            i += 1;
            let hit = matches!(&s2, Sched::Idx(v) if v.contains(&k));
            if hit {
                f2.borrow_mut().push(format!("{:?}:{}", c.op, c.dir));
            }
            hit
        })));
        let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(60));
        fault::disarm();
        let member = h.member().is_ok();
        let st = h.status().map(|s| s.segment);
        let ex = h.export(&w.ids[1]).map(|_| ());
        let copy = base.join("copy");
        copy_tree(&root, &copy);
        let fresh = open_host(w, 1, &copy, cfg(w), 70).map(|(h2, _)| snap_of(&h2, w));
        let agree = match (&fresh, member) {
            (Ok(f), true) => *f == snap_of(&h, w),
            (Ok(_), false) => true,
            (Err(_), _) => false,
        };
        lines.push(format!(
            "{s:?} failed [{}]: seal {:?}; member {member}; status {:?}; export {:?}; restart agrees {agree}",
            failed.borrow().join("+"),
            r.as_ref().map(|x| x.info.segment).map_err(|e| format!("{e:?}").chars().take(80).collect::<String>()),
            st.as_ref().map_err(|_| "ERR"),
            ex.as_ref().map_err(|_| "ERR"),
        ));
        if member && (st.is_err() || ex.is_err()) {
            bad.push(format!("N-3: {s:?}: a read call failed after the seal"));
        }
        if !agree {
            bad.push(format!("N-3: {s:?}: restart disagrees or refuses ({fresh:?})"));
        }
        if r.is_ok() && fresh.as_ref().map(|f| f.seg) != Ok(1) {
            bad.push(format!("N-3: {s:?}: seal Ok but fresh segment {fresh:?}"));
        }
        drop(h);
        scratch_done(&base);
    }
    println!(
        "QAHF N-3 (commit sync at index {commit_idx} of {n}):\n  {}",
        lines.join("\n  ")
    );
    scratch_done(&tm.dir);
    assert!(bad.is_empty(), "{bad:#?}");
}

/// N-r2-2: `pending_held` is clear after EVERY return of `release` I can reach: refused before
/// (anchor unsaved; a peer still a member); the first file's write failing at each operation; the
/// pending anchor's write failing; the release's own store operations failing (each); the hook's
/// second file failing at each operation; current's save failing after a landed release.
#[test]
fn qahf_nr22_every_path() {
    let tm = template(175, true);
    let w = &tm.w;
    let mut lines = Vec::new();
    let mut bad = Vec::new();
    let mut case = |label: String,
                    hook: bool,
                    key: usize,
                    rule: Option<Box<dyn FnMut(&fault::Ctx) -> bool>>| {
        let base = scratch("qahf-nr22");
        let root = base.join("host");
        copy_tree(&tm.root, &root);
        let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
        if hook {
            crate::host::test_hooks::release_differs_next();
        }
        if let Some(f) = rule {
            fault::arm(Rule::FailEvery(f));
        }
        let r = h.apply(&w.ids[1], Input::Release(w.key(key)), t(60));
        fault::disarm();
        // a hook not consumed must not leak into the next case
        let _ = crate::host::test_hooks::take_release_differs();
        let held = h.pending_held();
        let member = h.member().is_ok();
        lines.push(format!(
            "{label}: answer {}; member {member}; pending_held {held}",
            Ans::O(r).short()
        ));
        if held {
            bad.push(label.clone());
        }
        drop(h);
        scratch_done(&base);
    };
    case("clean".into(), false, 3, None);
    case("peer 2 still a member (dry run refuses)".into(), false, 2, None);
    for op in [
        Op::CreateTemp,
        Op::Write,
        Op::SyncFile,
        Op::Link,
        Op::SyncDir,
    ] {
        case(
            format!("first file {op:?} fails"),
            false,
            3,
            Some(Box::new(move |c| c.dir == "archive" && c.op == op)),
        );
    }
    for op in [Op::CreateTemp, Op::Write, Op::SyncFile, Op::Rename, Op::SyncDir] {
        case(
            format!("pending write {op:?} fails"),
            false,
            3,
            Some(Box::new(move |c| {
                c.dir == "anchors" && c.name == "pending" && c.op == op
            })),
        );
    }
    for k in 0..8 {
        let mut i = 0;
        case(
            format!("release store op #{k} fails"),
            false,
            3,
            Some(Box::new(move |c| {
                if c.dir != "store" {
                    return false;
                }
                let hit = i == k;
                i += 1;
                hit
            })),
        );
    }
    for op in [
        Op::CreateTemp,
        Op::Write,
        Op::SyncFile,
        Op::Link,
        Op::SyncDir,
    ] {
        let mut n = 0;
        case(
            format!("hook: second file {op:?} fails"),
            true,
            3,
            Some(Box::new(move |c| {
                if c.dir == "archive" && c.op == op {
                    n += 1;
                    return n == 2;
                }
                false
            })),
        );
    }
    case("hook: second file ok".into(), true, 3, None);
    case(
        "current save fails after the release".into(),
        false,
        3,
        Some(Box::new(|c| c.dir == "anchors" && c.name == "current")),
    );
    case(
        "hook: second file fails AND current save fails".into(),
        true,
        3,
        Some(Box::new({
            let mut n = 0;
            move |c| {
                if c.dir == "archive" && c.op == Op::CreateTemp {
                    n += 1;
                    return n == 2;
                }
                c.dir == "anchors" && c.name == "current"
            }
        })),
    );
    println!("QAHF N-r2-2:\n  {}", lines.join("\n  "));
    scratch_done(&tm.dir);
    assert!(bad.is_empty(), "pending_held left set: {bad:?}");
}

/// N-4 at a RE-OPEN: the live host's `anchors/current` (then `anchors/pending`) damaged on disk,
/// the owner's unanchored setting ON, then a record whose store sync fails (P-4): the re-open must
/// refuse the damaged anchor (LandedUnknown), never resume as if it were absent.
#[test]
fn qahf_n4_damaged_anchor_at_reopen() {
    let tm = template(180, false);
    let w = &tm.w;
    let mut lines = Vec::new();
    let mut bad = Vec::new();
    for file in ["current", "pending"] {
        let base = scratch("qahf-n4r");
        let root = base.join("host");
        copy_tree(&tm.root, &root);
        let mut c = cfg(w);
        c.allow_unanchored = true;
        let (mut h, _) = open_host(w, 1, &root, c, 50).unwrap();
        let p = root.join("anchors").join(file);
        let good = std::fs::read(root.join("anchors").join("current")).unwrap();
        let mut badb = good.clone();
        badb[0] ^= 0xff;
        std::fs::write(&p, &badb).unwrap();
        std::fs::set_permissions(&p, std::os::unix::fs::PermissionsExt::from_mode(0o600))
            .unwrap();
        fault::arm(Rule::FailWhen(Box::new(|c| {
            c.op == Op::SyncDir && c.dir == "store"
        })));
        let r = act(&mut h, &tm, K::Record, 60);
        fault::disarm();
        let s = r.short();
        let reopen_err = match r.err() {
            Some(HostError::LandedUnknown { reopen, .. }) => format!("{reopen:?}"),
            _ => String::new(),
        };
        lines.push(format!("{file} damaged at a re-open: {s} {reopen_err}"));
        if !matches!(r.err(), Some(HostError::LandedUnknown { .. })) {
            bad.push(format!("{file}: {s}"));
        }
        drop(h);
        scratch_done(&base);
    }
    println!("QAHF N-4 at re-open:\n  {}", lines.join("\n  "));
    scratch_done(&tm.dir);
    assert!(bad.is_empty(), "{bad:?}");
}

/// The dirty-state rule inside a seal: step 0's own checkpoint lands through a P-4 re-open whose
/// `anchors/limits` write fails and KEEPS failing. Does the seal go on (plan, file, commit) while
/// `anchors/limits` is unwritten? Measured, and the limits file and a restart compared.
#[test]
fn qahf_dirty_inside_a_seal() {
    let tm = template(185, false);
    let w = &tm.w;
    let base = scratch("qahf-dirtyseal");
    let root = base.join("host");
    copy_tree(&tm.root, &root);
    let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
    let before = snap_of(&h, w);
    let mut first = false;
    fault::arm(Rule::FailEvery(Box::new(move |c| {
        if !first && c.op == Op::SyncDir && c.dir == "store" {
            first = true;
            return true;
        }
        first && c.dir == "anchors" && c.name == "limits"
    })));
    let r = h.seal(&w.ids[1], SealTrigger::OwnerCommand, t(60));
    let still_dirty = h.limits_dirty();
    // a next ordinary change while the limits write still fails
    let next = act(&mut h, &tm, K::Record, 61);
    fault::disarm();
    let after = snap_of(&h, w);
    drop(h);
    let fresh = open_host(w, 1, &root, cfg(w), 70);
    println!(
        "QAHF dirty inside a seal: seal {:?}; limits still dirty {still_dirty}; segment {} -> {}; cps {} -> {}; next change while still failing {}; fresh open {:?}",
        r.as_ref().map(|x| x.info.segment).map_err(|e| format!("{e:?}")),
        before.seg,
        after.seg,
        before.cps,
        after.cps,
        next.short(),
        fresh.as_ref().map(|(h2, rep)| (h2.member().unwrap().segment(), rep.limits.before, rep.limits.in_force))
    );
    assert!(next.err().is_some(), "an ordinary change went through while dirty");
    scratch_done(&base);
    scratch_done(&tm.dir);
}

/// Baseline: a CLEAN receive of peer 2's event (no fault), then a fresh open: what does the fresh
/// member say about peer 2? (Calibrates the `Receive` measure of the schedules.)
#[test]
fn qahf_receive_baseline() {
    let tm = template(190, false);
    let w = &tm.w;
    let base = scratch("qahf-rb");
    let root = base.join("host");
    copy_tree(&tm.root, &root);
    let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
    let b = snap_of(&h, w);
    let r = act(&mut h, &tm, K::Receive, 60);
    let a = snap_of(&h, w);
    let st = h.status().unwrap();
    drop(h);
    let (h2, _) = open_host(w, 1, &root, cfg(w), 70).unwrap();
    let f = snap_of(&h2, w);
    let st2 = h2.status().unwrap();
    let r2 = {
        let mut h2 = h2;
        let x = act(&mut h2, &tm, K::Receive, 80).short();
        (x, snap_of(&h2, w).p2)
    };
    println!(
        "QAHF receive baseline: answer {}; p2 before {} host {} fresh {}; logical records host {} fresh {}; anchors equal {}; a second offer after restart -> {:?}",
        r.short(), b.p2, a.p2, f.p2, st.logical_records, st2.logical_records, a.anchor == f.anchor, r2
    );
    scratch_done(&base);
    scratch_done(&tm.dir);
}

/// Builder's interpretation 3 (N-r2-2 answer): a release that LANDED but whose second archive
/// file failed is answered `Err(Dir(..))`, a shape the docs' table does not list. A caller that
/// retries on it: what happens (a second release? a second file? own seq?), and a restart.
#[test]
fn qahf_retry_after_a_landed_release_with_a_failed_second_file() {
    for tomb in [false, true] {
        let tm = template(if tomb { 196 } else { 195 }, tomb);
        let w = &tm.w;
        let base = scratch("qahf-rr");
        let root = base.join("host");
        copy_tree(&tm.root, &root);
        let (mut h, _) = open_host(w, 1, &root, cfg(w), 50).unwrap();
        let b = snap_of(&h, w);
        let files0 = h.release_bundles().unwrap().len();
        crate::host::test_hooks::release_differs_next();
        let mut n = 0;
        fault::arm(Rule::FailEvery(Box::new(move |c| {
            if c.dir == "archive" && c.op == Op::CreateTemp {
                n += 1;
                return n == 2;
            }
            false
        })));
        let r = h.apply(&w.ids[1], Input::Release(w.key(3)), t(60));
        fault::disarm();
        let a = snap_of(&h, w);
        let files1 = h.release_bundles().unwrap().len();
        let retry = h.apply(&w.ids[1], Input::Release(w.key(3)), t(61));
        let c = snap_of(&h, w);
        let bl = h.release_bundles().unwrap();
        let files2 = bl.len();
        let enc: Vec<Vec<u8>> = bl.iter().map(|b| b.encode().unwrap()).collect();
        println!(
            "QAHF release files (tomb {tomb}): sizes {:?}; first == second {}",
            enc.iter().map(Vec::len).collect::<Vec<_>>(),
            enc.len() == 2 && enc[0] == enc[1]
        );
        // a CLEAN second release of a peer already released (no fault at all): the base behaviour
        let again = h.apply(&w.ids[1], Input::Release(w.key(3)), t(62));
        println!(
            "QAHF a third release, clean: {}; release files now {}",
            Ans::O(again).short(),
            h.release_bundles().unwrap().len()
        );
        drop(h);
        let (h2, _) = open_host(w, 1, &root, cfg(w), 70).unwrap();
        let f = snap_of(&h2, w);
        println!(
            "QAHF retry after a landed release (tomb {tomb}): answer {}; peer 3 present {} -> {}; own seq {} -> {}; release files {files0} -> {files1}; RETRY -> {} ({:?}); own seq then {}; files then {files2}; restart: peer 3 present {}, own seq {}, anchor = host {}",
            Ans::O(r).short(), b.p3, a.p3, b.seq, a.seq,
            Ans::O(retry.clone()).short(), retry.as_ref().err(), c.seq, f.p3, f.seq, f.anchor == c.anchor
        );
        assert!(a.logical == tm.rel_post && c.logical == tm.rel_post && a.seq == b.seq && c.seq == b.seq && f.seq == c.seq);
        drop(h2);
        scratch_done(&base);
        scratch_done(&tm.dir);
    }
}
