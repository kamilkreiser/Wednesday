//! QA-RELAY-RECONNECT-R2: a copy of the head's `tests/rr_property.rs` (104dd39), changed ONLY in: layer (a)'s seed (the re-checker's own) and layer (b)'s test functions (the re-checker's own seeds 4241-4246). Not part of the branch.
//! RELAY-RECONNECT item 10: the generated property, over the WHOLE input alphabet of the parties
//! this lane touches (the host's own lifecycle and settings, its relay child and guard, the saved
//! file, the guest and its owner's pasted lines, and whatever else answers at the relay's address).
//!
//! (a) FAST, over the pure decision. A model of the host, the disk, the guest and an impostor that
//!     calls the daemon's REAL decision functions (`relay_child::choose_identity`, `file_needed`,
//!     `identity_survives`, `moved_line_accepted`, `RespawnClock`) for every choice, and checks five
//!     invariants after EVERY step against oracles written here from the brief:
//!     I1 the guest is attached only to an endpoint whose pin is its own record's, and that pin
//!        changed only through a `relay.moved` line its owner pasted that names its session;
//!     I2 with the setting off the host writes no identity to disk, ever;
//!     I3 a refused file is left byte-identical and no fresh identity is made while it is there;
//!     I4 within one life of the relay slot every start of the child gets the same identity; and
//!        its converse: after a session END with the setting off, the next session's relay has
//!        another identity;
//!     I5 the host waiting for its relay in an active session always has a deadline armed (R6;
//!        the guest's reconnect deadline is the recovery machine's own V5, `recovery.rs:806-837`).
//!     At least 200,000 sequences of up to 40 steps; fixed seed, printed on failure with the
//!     sequence, the step and the trace; every reach count must be above zero.
//! (b) REAL processes and real TLS: at least 12 seeds of at least 10 executed steps from the same
//!     alphabet (file steps on the real file; the impostor is a second `coagent relay` started on
//!     the freed port, or a TLS listener presenting the saved certificate with another key),
//!     asserting I1 (both statuses and the pins), I2 and I3 (the file and the host's status), and I5
//!     as "connected again within 120 s of the last step once the host runs with the identity the
//!     guest pins" (design 09's V4 figure).
//! I6 (addendum 2, layer (b) only): no relay child this daemon started for an invitation or a
//!    session is stopped because of an EARLIER session's end. Checked when an invitation is made after
//!    an end (its relay still runs several ticks later, then the pair completes) and after that pairing
//!    (the same relay still runs). Layer (a) cannot hold it: the clean-up is the engine's `on_tick`
//!    block, not a pure function, and addendum 2 permits no new place to extract one. Reach counts
//!    (per test, over its seeds): an invitation after a peer end, after an own end, and a pair completed
//!    on such an invitation; every seed's third executed step is a session end (host-ended on even
//!    seeds, guest-ended on odd ones) so both kinds are reached; the other steps are generated.
//!    Addendum 5 (RR-1): a guest's end can also RACE an invitation (the host calls `invite` in a tight
//!    loop while the end is being applied, before the tick); odd seeds race at their third step and
//!    every seed tries once more at its sixth (only while both sides are connected, so the end
//!    reaches the host). Reach (per test): raced invitations, and of them those whose end the invite
//!    itself applied (the host's log line); I6 is checked on each raced invitation as on any other.
//! Red controls: `moved_line_for_another_session_accepted` (I1), `damaged_identity_falls_back_fresh`
//! (I3), `identity_not_erased_at_session_end` (I4's converse), `relay_respawn_no_clock` (I5),
//! `ended_cleanup_repeats` (I6).
mod common;
mod rr_support;

use std::collections::BTreeMap;
use std::time::{Duration, Instant};

use coagent_daemon::relay_child::{
    choose_identity, file_needed, identity_survives, moved_line_accepted, FileFound,
    IdentityChoice, RespawnClock, SlotEvent,
};
use coagent_proto::bytes::SessionId;

/// xorshift64* (no new dependency).
#[derive(Clone)]
struct Rng(u64);
impl Rng {
    fn new(seed: u64) -> Rng {
        Rng(seed.wrapping_mul(0x9E37_79B9_7F4A_7C15) | 1)
    }
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545_F491_4F6C_DD1D)
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
    fn coin(&mut self) -> bool {
        self.next() & 1 == 1
    }
}

// ---------------------------------------------------------------------------------------------
// (a) The model

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Cat {
    Cut,
    Flip,
    Mode,
    Link,
    TooLarge,
}

impl Cat {
    fn text(self) -> &'static str {
        match self {
            Cat::Cut => "the identity is cut short in its key",
            Cat::Flip => "the identity's certificate does not match the hash stored with it",
            Cat::Mode => "mode is not 0600",
            Cat::Link => "not a regular file",
            Cat::TooLarge => "larger than 16 KiB",
        }
    }
    const ALL: [Cat; 5] = [Cat::Cut, Cat::Flip, Cat::Mode, Cat::Link, Cat::TooLarge];
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum Disk {
    Absent,
    Good(u32),
    /// A damaged file (a category) over the good identity it was made from.
    Bad(Cat, u32),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum LineKind {
    Current,
    Stale,
    OtherSession,
    Stranger,
    Garbage,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Line {
    sid: u64,
    pin: u32,
    port: u16,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Step {
    Start { keep: bool },
    StopClean,
    Kill,
    ChildCrash,
    GuardCrash,
    StartFails,
    SessionEnd { by_host: bool },
    NewInvite,
    FileCut,
    FileFlip,
    FileMode,
    FileLink,
    FileOtherValid,
    FileGrow,
    FileMoveAway,
    FilePutBack,
    GuestReconnect,
    Paste(LineKind),
    ImpostorFresh,
    ImpostorCertNoKey,
    ImpostorLeaves,
}

fn gen_step(r: &mut Rng) -> Step {
    match r.below(24) {
        0 | 1 => Step::Start { keep: r.coin() },
        2 => Step::StopClean,
        3 => Step::Kill,
        4 => Step::ChildCrash,
        5 => Step::GuardCrash,
        6 => Step::StartFails,
        7 => Step::SessionEnd { by_host: r.coin() },
        8 => Step::NewInvite,
        9 => Step::FileCut,
        10 => Step::FileFlip,
        11 => Step::FileMode,
        12 => Step::FileLink,
        13 => Step::FileOtherValid,
        14 => Step::FileGrow,
        15 => Step::FileMoveAway,
        16 => Step::FilePutBack,
        17 | 18 => Step::GuestReconnect,
        19 => Step::Paste(match r.below(5) {
            0 => LineKind::Current,
            1 => LineKind::Stale,
            2 => LineKind::OtherSession,
            3 => LineKind::Stranger,
            _ => LineKind::Garbage,
        }),
        20 => Step::ImpostorFresh,
        21 => Step::ImpostorCertNoKey,
        22 => Step::ImpostorLeaves,
        _ => Step::GuestReconnect,
    }
}

#[derive(Clone, Debug)]
struct HostSess {
    sid: u64,
    ended: bool,
    cand: (u32, u16),
    line: Option<Line>,
}

#[derive(Clone, Debug)]
struct GuestSess {
    sid: u64,
    pin: u32,
    port: u16,
    attached: bool,
    ended: bool,
}

#[derive(Clone, Copy, Debug)]
enum Impostor {
    /// Presents a certificate of its own (with its key).
    Fresh(u32),
    /// Presents the given certificate without its key (the handshake signature fails).
    CertNoKey(u32),
}

#[derive(Default, Debug)]
struct Reach {
    heal_child_crash_off: u64,
    heal_restart_on: u64,
    refused: BTreeMap<Cat, u64>,
    heal_after_put_right: u64,
    accepted: BTreeMap<&'static str, u64>,
    refused_lines: BTreeMap<&'static str, u64>,
    impostor_refused: u64,
}

struct World {
    now: Instant,
    rng: Rng,
    next_id: u32,
    next_sid: u64,
    // host
    running: bool,
    keep: bool,
    held: Option<u32>,
    relay: Option<(u32, u16)>,
    clock: RespawnClock,
    start_fails: u8,
    sess: Option<HostSess>,
    lines: Vec<Line>,
    // disk
    disk: Disk,
    owner_good: Option<u32>,
    // guest
    guest: Option<GuestSess>,
    impostor: Option<(u16, Impostor)>,
    // oracle state
    life: Option<u32>,
    life_ended_off: Option<u32>,
    host_wrote: bool,
    fresh_while_refused: bool,
    heal_crash_pending: bool,
    heal_restart_pending: bool,
    put_right_pending: bool,
    refused_since: bool,
    reach: Reach,
}

fn sid_of(n: u64) -> SessionId {
    let mut b = [0u8; 32];
    b[..8].copy_from_slice(&n.to_be_bytes());
    SessionId(b)
}

impl World {
    fn new(seed: u64) -> World {
        World {
            now: Instant::now(),
            rng: Rng::new(seed),
            next_id: 1,
            next_sid: 1,
            running: false,
            keep: false,
            held: None,
            relay: None,
            clock: RespawnClock::new(RespawnClock::MIN, RespawnClock::MAX),
            start_fails: 0,
            sess: None,
            lines: vec![],
            disk: Disk::Absent,
            owner_good: None,
            guest: None,
            impostor: None,
            life: None,
            life_ended_off: None,
            host_wrote: false,
            fresh_while_refused: false,
            heal_crash_pending: false,
            heal_restart_pending: false,
            put_right_pending: false,
            refused_since: false,
            reach: Reach::default(),
        }
    }

    fn fresh(&mut self) -> u32 {
        let i = self.next_id;
        self.next_id += 1;
        i
    }

    fn active(&self) -> bool {
        self.sess.as_ref().map(|s| !s.ended).unwrap_or(false)
    }

    fn new_port(&mut self) -> u16 {
        loop {
            let p = 20_000 + self.rng.below(40_000) as u16;
            if self.impostor.map(|(ip, _)| ip) != Some(p) {
                return p;
            }
        }
    }

    /// The oracle's end of a life (independent of `identity_survives`).
    fn oracle_life_end(&mut self, session_end: bool) {
        if session_end && !self.keep {
            self.life_ended_off = self.life;
        }
        self.life = None;
    }

    /// One start of the own relay child (`engine::relay_identity_for_start` + spawn), through the
    /// REAL decision. `arm`: a failure arms R6's clock (the session path; `invite` does not).
    fn start_child(&mut self, want_port: u16, arm: bool) -> Result<(), String> {
        let held = self.held.is_some();
        let found = if file_needed(self.keep, held) {
            match self.disk {
                Disk::Absent => FileFound::Absent,
                Disk::Good(_) => FileFound::Good,
                Disk::Bad(c, _) => FileFound::Refused(c.text().into()),
            }
        } else {
            FileFound::NotRead
        };
        let refusable = self.keep && matches!(self.disk, Disk::Bad(..));
        let fail = |w: &mut World, why: String| -> Result<(), String> {
            if arm {
                w.clock.failed(w.now);
            }
            Err(why)
        };
        let id = match choose_identity(self.keep, held, &found) {
            IdentityChoice::UseHeld => match self.held {
                Some(i) => i,
                None => return Err("model: UseHeld with nothing held".into()),
            },
            IdentityChoice::UseLoaded => match self.disk {
                Disk::Good(i) => {
                    self.held = Some(i);
                    i
                }
                _ => return Err("model: UseLoaded without a good file".into()),
            },
            IdentityChoice::MakeInMemory => {
                let i = self.fresh();
                if refusable {
                    self.fresh_while_refused = true;
                }
                self.held = Some(i);
                i
            }
            IdentityChoice::MakeAndStore => {
                let i = self.fresh();
                if refusable {
                    self.fresh_while_refused = true;
                }
                if self.disk != Disk::Absent {
                    return fail(self, "exclusive create refused".into());
                }
                self.disk = Disk::Good(i);
                self.host_wrote = true;
                self.owner_good = Some(i);
                self.held = Some(i);
                i
            }
            IdentityChoice::Refuse(c) => {
                let cat = Cat::ALL.iter().find(|k| k.text() == c).copied();
                if let Some(k) = cat {
                    *self.reach.refused.entry(k).or_default() += 1;
                }
                self.refused_since = true;
                return fail(self, c);
            }
        };
        if self.start_fails > 0 {
            self.start_fails -= 1;
            if !identity_survives(SlotEvent::StartFailed) {
                self.held = None;
            }
            return fail(self, "the child did not start".into());
        }
        let port = if want_port == 0 || self.impostor.map(|(p, _)| p) == Some(want_port) {
            self.new_port()
        } else {
            want_port
        };
        // I4: one identity per life.
        match self.life {
            Some(l) if l != id => {
                return Err(format!(
                    "I4 violated: a start within one life of the relay slot got identity {id}, an earlier one got {l}"
                ))
            }
            _ => self.life = Some(id),
        }
        self.relay = Some((id, port));
        self.clock.reset();
        if let Some(s) = self.sess.as_mut() {
            if s.cand != (id, port) {
                let l = Line {
                    sid: s.sid,
                    pin: id,
                    port,
                };
                s.line = Some(l);
                self.lines.push(l);
            }
            s.cand = (id, port);
        }
        Ok(())
    }

    fn ensure(&mut self) -> Result<(), String> {
        if !self.running || self.relay.is_some() || !self.active() {
            return Ok(());
        }
        let port = self.sess.as_ref().map(|s| s.cand.1).unwrap_or(0);
        match self.start_child(port, true) {
            Err(e) if e.starts_with("I4") || e.starts_with("model") => Err(e),
            _ => Ok(()),
        }
    }

    fn child_exit(&mut self) -> Result<(), String> {
        if !self.running || self.relay.is_none() {
            return Ok(());
        }
        self.relay = None;
        if let Some(g) = self.guest.as_mut() {
            g.attached = false;
        }
        if self.active() {
            if !identity_survives(SlotEvent::ExitedInSession) {
                self.held = None;
            }
            if !self.keep {
                self.heal_crash_pending = true;
            }
            self.ensure()
        } else {
            if !identity_survives(SlotEvent::ExitedWithoutSession) {
                self.held = None;
            }
            self.oracle_life_end(false);
            Ok(())
        }
    }

    fn endpoint(&self, port: u16) -> Option<(u32, bool)> {
        if let Some((id, p)) = self.relay {
            if self.running && p == port {
                return Some((id, true));
            }
        }
        match self.impostor {
            Some((p, Impostor::Fresh(i))) if p == port => Some((i, true)),
            Some((p, Impostor::CertNoKey(i))) if p == port => Some((i, false)),
            _ => None,
        }
    }

    fn step(&mut self, st: Step) -> Result<(), String> {
        self.host_wrote = false;
        self.fresh_while_refused = false;
        let pin_before = self.guest.as_ref().map(|g| (g.sid, g.pin));
        let mut legit_pin_change = false;
        let disk_before = self.disk.clone();
        let mut test_touched_disk = false;
        match st {
            Step::Start { keep } => {
                if !self.running {
                    self.running = true;
                    self.keep = keep;
                    self.held = None;
                    self.relay = None;
                    self.clock.reset();
                    self.life = None;
                    if self.active() && keep {
                        self.heal_restart_pending = true;
                    }
                    self.ensure()?;
                }
            }
            Step::StopClean | Step::Kill => {
                if self.running {
                    self.relay = None;
                    // The process ends: nothing held survives (and `Shutdown` erases it anyway).
                    let _ = identity_survives(SlotEvent::Shutdown);
                    self.held = None;
                    self.running = false;
                    self.oracle_life_end(false);
                }
            }
            Step::ChildCrash | Step::GuardCrash => self.child_exit()?,
            Step::StartFails => {
                self.start_fails = 1 + self.rng.below(2) as u8;
                self.child_exit()?;
            }
            Step::SessionEnd { by_host } => {
                if self.active() {
                    let _ = by_host;
                    if let Some(s) = self.sess.as_mut() {
                        s.ended = true;
                    }
                    if let Some(g) = self.guest.as_mut() {
                        g.ended = true;
                        g.attached = false;
                    }
                    if self.running {
                        self.relay = None;
                        if !identity_survives(SlotEvent::SessionEnded) {
                            self.held = None;
                        }
                        self.clock.reset();
                    }
                    self.oracle_life_end(true);
                }
            }
            Step::NewInvite => {
                if self.running && !self.active() && self.relay.is_none() {
                    match self.start_child(0, false) {
                        Ok(()) => {
                            let (id, port) = self.relay.unwrap();
                            if let Some(prev) = self.life_ended_off.take() {
                                if !self.keep && prev == id {
                                    return Err(format!(
                                        "I4 converse violated: after a session end with the setting off the new session's relay has the same identity {id}"
                                    ));
                                }
                            }
                            let sid = self.next_sid;
                            self.next_sid += 1;
                            self.sess = Some(HostSess {
                                sid,
                                ended: false,
                                cand: (id, port),
                                line: None,
                            });
                            // The invitation carries the pin; the guest joins (pairing).
                            self.guest = Some(GuestSess {
                                sid,
                                pin: id,
                                port,
                                attached: true,
                                ended: false,
                            });
                            legit_pin_change = true;
                            self.heal_crash_pending = false;
                            self.heal_restart_pending = false;
                            self.put_right_pending = false;
                            self.refused_since = false;
                        }
                        Err(e) if e.starts_with("I4") || e.starts_with("model") => return Err(e),
                        Err(_) => {}
                    }
                }
            }
            Step::FileCut | Step::FileFlip | Step::FileMode | Step::FileLink | Step::FileGrow => {
                let c = match st {
                    Step::FileCut => Cat::Cut,
                    Step::FileFlip => Cat::Flip,
                    Step::FileMode => Cat::Mode,
                    Step::FileLink => Cat::Link,
                    _ => Cat::TooLarge,
                };
                self.disk = match self.disk {
                    Disk::Absent => Disk::Absent,
                    Disk::Good(i) | Disk::Bad(_, i) => Disk::Bad(c, i),
                };
                test_touched_disk = true;
            }
            Step::FileOtherValid => {
                let i = self.fresh();
                self.disk = Disk::Good(i);
                self.owner_good = Some(i);
                test_touched_disk = true;
            }
            Step::FileMoveAway => {
                if let Disk::Good(i) | Disk::Bad(_, i) = self.disk {
                    self.owner_good = Some(i);
                }
                self.disk = Disk::Absent;
                test_touched_disk = true;
            }
            Step::FilePutBack => {
                if let Some(i) = self.owner_good {
                    if self.refused_since {
                        self.put_right_pending = true;
                    }
                    self.disk = Disk::Good(i);
                    test_touched_disk = true;
                }
            }
            Step::GuestReconnect => {
                let ep = self
                    .guest
                    .as_ref()
                    .filter(|g| !g.ended)
                    .map(|g| (g.port, g.pin));
                if let Some((port, pin)) = ep {
                    let e = self.endpoint(port);
                    let ok = matches!(e, Some((p, true)) if p == pin);
                    if !ok
                        && self.impostor.map(|(p, _)| p) == Some(port)
                        && self.relay.map(|r| r.1) != Some(port)
                    {
                        self.reach.impostor_refused += 1;
                    }
                    let was = self.guest.as_ref().map(|g| g.attached).unwrap_or(false);
                    if let Some(g) = self.guest.as_mut() {
                        g.attached = ok;
                    }
                    if ok && !was {
                        if self.heal_crash_pending {
                            self.reach.heal_child_crash_off += 1;
                            self.heal_crash_pending = false;
                        }
                        if self.heal_restart_pending {
                            self.reach.heal_restart_on += 1;
                            self.heal_restart_pending = false;
                        }
                        if self.put_right_pending {
                            self.reach.heal_after_put_right += 1;
                            self.put_right_pending = false;
                        }
                    }
                }
            }
            Step::Paste(kind) => {
                if let Some(gsid) = self.guest.as_ref().filter(|g| !g.ended).map(|g| g.sid) {
                    let line = match kind {
                        LineKind::Current => self.sess.as_ref().and_then(|s| s.line),
                        LineKind::Stale => self
                            .lines
                            .iter()
                            .rev()
                            .filter(|l| l.sid == gsid)
                            .nth(1)
                            .copied(),
                        LineKind::OtherSession => Some(
                            self.lines
                                .iter()
                                .find(|l| l.sid != gsid)
                                .copied()
                                .unwrap_or(Line {
                                    sid: gsid + 1_000_000,
                                    pin: 0,
                                    port: 9,
                                }),
                        ),
                        LineKind::Stranger => {
                            let pin = self.fresh();
                            Some(Line {
                                sid: gsid,
                                pin,
                                port: 9,
                            })
                        }
                        LineKind::Garbage => None,
                    };
                    let name = match kind {
                        LineKind::Current => "current",
                        LineKind::Stale => "stale",
                        LineKind::OtherSession => "another session's",
                        LineKind::Stranger => "a stranger's with the session id",
                        LineKind::Garbage => "garbage",
                    };
                    let parsed = !matches!(kind, LineKind::Garbage);
                    if let Some(l) = line.filter(|_| parsed) {
                        let accepted = moved_line_accepted(&sid_of(gsid), true, &sid_of(l.sid));
                        let oracle = l.sid == gsid;
                        if accepted {
                            *self.reach.accepted.entry(name).or_default() += 1;
                            if let Some(g) = self.guest.as_mut() {
                                g.pin = l.pin;
                                g.port = l.port;
                                g.attached = false;
                            }
                            legit_pin_change = oracle;
                            self.heal_crash_pending = false;
                            self.heal_restart_pending = false;
                            self.put_right_pending = false;
                        } else {
                            *self.reach.refused_lines.entry(name).or_default() += 1;
                            if oracle {
                                return Err(format!(
                                    "I1 violated: a {name} line that names the guest's session was refused"
                                ));
                            }
                        }
                    } else if kind == LineKind::Garbage {
                        *self.reach.refused_lines.entry(name).or_default() += 1;
                    }
                }
            }
            Step::ImpostorFresh | Step::ImpostorCertNoKey => {
                // Something else answers at the guest's address while the host's relay is not there.
                if let Some((port, pin)) = self.guest.as_ref().map(|g| (g.port, g.pin)) {
                    if self.endpoint(port).is_none() || self.impostor.is_some() {
                        let im = if matches!(st, Step::ImpostorFresh) {
                            Impostor::Fresh(self.fresh())
                        } else {
                            Impostor::CertNoKey(pin)
                        };
                        if self.relay.map(|r| r.1) != Some(port) {
                            self.impostor = Some((port, im));
                            if let Some(g) = self.guest.as_mut() {
                                g.attached = false;
                            }
                        }
                    }
                }
            }
            Step::ImpostorLeaves => self.impostor = None,
        }
        // The guest's link falls when its endpoint goes away.
        let gp = self.guest.as_ref().map(|g| (g.port, g.pin, g.attached));
        if let Some((port, pin, true)) = gp {
            if !matches!(self.endpoint(port), Some((p, true)) if p == pin) {
                if let Some(g) = self.guest.as_mut() {
                    g.attached = false;
                }
            }
        }
        // Time passes; R6's clock fires when due.
        self.now += Duration::from_millis(self.rng.below(90_000));
        while self.running && self.active() && self.relay.is_none() && self.clock.due(self.now) {
            self.ensure()?;
            if self.relay.is_none() && !self.clock.due(self.now) {
                break;
            }
            if self.relay.is_none() {
                break;
            }
        }
        // ---- invariants after the step
        // I1
        if let Some(g) = &self.guest {
            if g.attached {
                match self.endpoint(g.port) {
                    Some((p, true)) if p == g.pin => {}
                    other => {
                        return Err(format!(
                            "I1 violated: the guest is attached to {other:?}, its record pins {}",
                            g.pin
                        ))
                    }
                }
            }
            if let Some((sid, pin)) = pin_before {
                if (sid, pin) != (g.sid, g.pin) && !legit_pin_change {
                    return Err(format!(
                        "I1 violated: the guest's pin changed from {pin} to {} without a line its owner pasted that names its session",
                        g.pin
                    ));
                }
            }
        }
        // I2
        if self.host_wrote && !self.keep {
            return Err(
                "I2 violated: with the setting off the host wrote an identity to disk".into(),
            );
        }
        // I3
        if !test_touched_disk {
            if let Disk::Bad(..) = disk_before {
                if self.disk != disk_before {
                    return Err("I3 violated: a refused file was changed".into());
                }
            }
        }
        if self.fresh_while_refused {
            return Err(
                "I3 violated: a fresh identity was made while the saved one was refused".into(),
            );
        }
        // I5
        if self.running
            && self.active()
            && self.relay.is_none()
            && self.clock.remaining(self.now).is_none()
        {
            return Err(
                "I5 violated: the host waits for its relay in an active session with no deadline armed".into(),
            );
        }
        Ok(())
    }
}

const SEED_A: u64 = 0x0B0B_5EED_2026_1121;
const SEQUENCES: u64 = 200_000;
const MAX_STEPS: u64 = 40;

#[test]
fn rr_property_a_the_pure_decision_holds_i1_to_i5() {
    let mut total = Reach::default();
    let mut steps_run = 0u64;
    for n in 0..SEQUENCES {
        let mut w = World::new(SEED_A ^ n);
        let mut r = Rng::new(SEED_A.wrapping_add(n));
        // Every sequence starts from a running host with an active session (a pairing).
        let keep = r.coin();
        let mut trace = vec![Step::Start { keep }, Step::NewInvite];
        let mut res = w
            .step(Step::Start { keep })
            .and_then(|_| w.step(Step::NewInvite));
        let len = 1 + r.below(MAX_STEPS);
        for _ in 0..len {
            if res.is_err() {
                break;
            }
            let st = gen_step(&mut r);
            trace.push(st);
            res = w.step(st);
            steps_run += 1;
        }
        if let Err(e) = res {
            panic!(
                "{e}\n  seed {SEED_A:#x}, sequence {n}, step {} of the trace:\n  {:?}",
                trace.len() - 1,
                trace
            );
        }
        total.heal_child_crash_off += w.reach.heal_child_crash_off;
        total.heal_restart_on += w.reach.heal_restart_on;
        total.heal_after_put_right += w.reach.heal_after_put_right;
        total.impostor_refused += w.reach.impostor_refused;
        for (k, v) in w.reach.refused {
            *total.refused.entry(k).or_default() += v;
        }
        for (k, v) in w.reach.accepted {
            *total.accepted.entry(k).or_default() += v;
        }
        for (k, v) in w.reach.refused_lines {
            *total.refused_lines.entry(k).or_default() += v;
        }
    }
    eprintln!(
        "rr_property (a): seed {SEED_A:#x}, {SEQUENCES} sequences, {steps_run} generated steps; reach: {total:?}"
    );
    assert!(
        total.heal_child_crash_off > 0,
        "reach: a heal after a child crash (off)"
    );
    assert!(
        total.heal_restart_on > 0,
        "reach: a heal after a daemon restart (on)"
    );
    for c in Cat::ALL {
        assert!(
            total.refused.get(&c).copied().unwrap_or(0) > 0,
            "reach: a refusal of category {c:?}"
        );
    }
    assert!(
        total.heal_after_put_right > 0,
        "reach: a heal after the file was put right"
    );
    for k in ["current", "stale", "a stranger's with the session id"] {
        assert!(
            total.accepted.get(k).copied().unwrap_or(0) > 0,
            "reach: a {k} line accepted"
        );
    }
    for k in ["another session's", "garbage"] {
        assert!(
            total.refused_lines.get(k).copied().unwrap_or(0) > 0,
            "reach: a {k} line refused"
        );
    }
    assert!(total.impostor_refused > 0, "reach: an impostor refused");
}

// ---------------------------------------------------------------------------------------------
// (b) Real processes and real TLS

mod real {
    use super::*;
    use crate::common::*;
    use crate::rr_support::*;
    use serde_json::{json, Value};
    use std::os::unix::fs::PermissionsExt;
    use std::path::{Path, PathBuf};
    use std::process::{Child, Command, Stdio};

    /// The host's log line when a command (not a tick) applied the peer's end first (RR-1).
    const APPLIED_BY_COMMAND: &str = "the peer's end was applied before this command";

    #[derive(Clone, Copy, Debug)]
    enum RStep {
        Restart {
            keep: bool,
            clean: bool,
        },
        ChildCrash,
        GuardCrash,
        StartFails,
        /// `race` (addendum 5, RR-1): the guest ends while the host calls `invite` in a tight
        /// loop, so the invitation can land while the end is being applied (before the tick).
        SessionEnd {
            by_host: bool,
            race: bool,
        },
        FileCut,
        FileFlip,
        FileMode,
        FileLink,
        FileOtherValid,
        FileGrow,
        FileMoveAway,
        FilePutBack,
        GuestWait,
        Paste(LineKind),
        ImpostorRelay,
        ImpostorCertNoKey,
    }

    fn gen(r: &mut Rng) -> RStep {
        match r.below(20) {
            0 | 1 => RStep::Restart {
                keep: r.coin(),
                clean: r.coin(),
            },
            2 => RStep::ChildCrash,
            3 => RStep::GuardCrash,
            4 => RStep::StartFails,
            5 => {
                let by_host = r.coin();
                let race = r.coin();
                RStep::SessionEnd {
                    by_host,
                    race: race && !by_host,
                }
            }
            6 => RStep::FileCut,
            7 => RStep::FileFlip,
            8 => RStep::FileMode,
            9 => RStep::FileLink,
            10 => RStep::FileOtherValid,
            11 => RStep::FileGrow,
            12 => RStep::FileMoveAway,
            13 => RStep::FilePutBack,
            14 => RStep::GuestWait,
            15 => RStep::Paste(match r.below(5) {
                0 => LineKind::Current,
                1 => LineKind::Stale,
                2 => LineKind::OtherSession,
                3 => LineKind::Stranger,
                _ => LineKind::Garbage,
            }),
            16 => RStep::ImpostorRelay,
            17 => RStep::ImpostorCertNoKey,
            _ => RStep::GuestWait,
        }
    }

    struct Seed {
        run: Run,
        a: usize,
        g: InProc,
        keep: bool,
        prog: PathBuf,
        side: PathBuf,
        /// The good saved identity the owner has (the file's bytes when last good).
        good: Option<Vec<u8>>,
        /// What the test last left at the file's name (None = absent); `damaged` = refusable.
        damaged: bool,
        /// The pin the guest's record must hold (changed only by accepted pastes and pairings).
        guest_pin: String,
        guest_sid: String,
        lines: Vec<(String, String)>, // (session id, line)
        rng: Rng,
        log: Vec<String>,
        /// The last session end not yet followed by a pairing: Some(true) = by the host.
        last_end: Option<bool>,
        /// I6 reach: (invitation after a peer end, after an own end, pair completed on one).
        reach: (u64, u64, u64),
        /// RR-1 reach: (raced invitations, of them applied by the invite before the tick).
        race_reach: (u64, u64),
    }

    fn file(s: &Seed) -> PathBuf {
        s.run.dir(s.a).join(ID_FILE)
    }

    fn snap_file(p: &Path) -> Option<(Vec<u8>, u32)> {
        use std::os::unix::fs::MetadataExt;
        let md = std::fs::symlink_metadata(p).ok()?;
        let bytes = if md.file_type().is_file() {
            std::fs::read(p).unwrap_or_default()
        } else if md.file_type().is_symlink() {
            std::fs::read_link(p)
                .map(|t| t.to_string_lossy().as_bytes().to_vec())
                .unwrap_or_default()
        } else {
            b"<not a file>".to_vec()
        };
        Some((bytes, md.mode()))
    }

    fn replace_with(s: &Seed, bytes: &[u8], mode: u32) {
        let tmp = s.side.join("next");
        std::fs::write(&tmp, bytes).unwrap();
        std::fs::set_permissions(&tmp, std::fs::Permissions::from_mode(mode)).unwrap();
        std::fs::rename(&tmp, file(s)).unwrap();
    }

    fn port_of(url: &str) -> u16 {
        url.rsplit_once(':')
            .and_then(|(_, p)| p.split('/').next())
            .and_then(|p| p.parse().ok())
            .unwrap_or(0)
    }

    fn record_line(s: &mut Seed) {
        let st = status_of(&s.run.dir(s.a));
        if let (Some(l), Some(sid)) = (
            st["relay_moved_line"].as_str(),
            st["session"]["session_id"].as_str(),
        ) {
            if !s.lines.iter().any(|(_, x)| x == l) {
                s.lines.push((sid.to_string(), l.to_string()));
            }
        }
    }

    fn restart(s: &mut Seed, keep: bool, clean: bool) {
        let da = s.run.dir(s.a);
        let old = relay_pids_of(&da);
        if clean {
            s.run.stop(s.a);
        } else {
            s.run.crash(s.a);
        }
        wait_gone(&old, "the host's relay and guard gone");
        s.keep = keep;
        s.run.daemons[s.a].extra_args = vec!["--coagent".into(), s.prog.to_string_lossy().into()];
        if keep {
            s.run.daemons[s.a]
                .extra_args
                .push("--keep-relay-identity".into());
        }
        s.run.start(s.a);
        s.run.status(s.a);
    }

    fn guest_status(s: &Seed) -> Value {
        status_of(&s.g.dir)
    }

    /// I1, I2, I3 after a step. `file_before`: the file as the step's start left it (after the
    /// test's own file action).
    fn check(s: &mut Seed, what: &str, file_before: &Option<(Vec<u8>, u32)>, src_before: &str) {
        let da = s.run.dir(s.a);
        // A guest link to a relay that just went away is "attached" until the guest notices: give
        // it 10 s; a guest attached to the wrong certificate would stay so.
        let mismatch = |s: &Seed| {
            let h = status_of(&s.run.dir(s.a));
            let g = guest_status(s);
            g["session"]["attached"] == true
                && g["session"]["ended"] != true
                && (h["relay"].is_null()
                    || h["session"]["relays"][0]["pin"] != g["session"]["relays"][0]["pin"]
                    || h["session"]["relays"][0]["url"] != g["session"]["relays"][0]["url"])
        };
        let t0 = Instant::now();
        while mismatch(s) && t0.elapsed() < Duration::from_secs(10) {
            std::thread::sleep(Duration::from_millis(100));
        }
        let h = status_of(&da);
        let g = guest_status(s);
        // I1: the guest's pin is its record's; attached only to that pin.
        let gpin = g["session"]["relays"][0]["pin"]
            .as_str()
            .unwrap_or_default()
            .to_string();
        let gurl = g["session"]["relays"][0]["url"]
            .as_str()
            .unwrap_or_default()
            .to_string();
        assert_eq!(
            gpin, s.guest_pin,
            "I1 violated after {what}: the guest's pin changed without an accepted line\n{:?}",
            s.log
        );
        if g["session"]["attached"] == true && g["session"]["ended"] != true {
            let hp = h["session"]["relays"][0]["pin"]
                .as_str()
                .unwrap_or_default();
            let hu = h["session"]["relays"][0]["url"]
                .as_str()
                .unwrap_or_default();
            assert!(
                !h["relay"].is_null() && hp == gpin && hu == gurl,
                "I1 violated after {what}: the guest is attached but the relay at its address does not hold its pin\n{:?}",
                s.log
            );
        }
        let now = snap_file(&file(s));
        // I2: with the setting off the host writes nothing.
        if !s.keep {
            assert_eq!(
                &now, file_before,
                "I2 violated after {what}: the file changed while the host ran with the setting off\n{:?}",
                s.log
            );
        }
        // I3: a refused file is byte-identical and no fresh identity was made.
        if s.keep && s.damaged {
            assert_eq!(
                &now, file_before,
                "I3 violated after {what}: a refused file changed\n{:?}",
                s.log
            );
            let src = h["relay_identity"]["source"].as_str().unwrap_or_default();
            assert!(
                src == src_before || (src != "memory" && src != "saved_created"),
                "I3 violated after {what}: a fresh identity ({src}) while the saved one is refused\n{:?}",
                s.log
            );
        }
    }

    fn impostor_relay(s: &mut Seed) {
        let da = s.run.dir(s.a);
        let url = host_url(&da);
        let port = port_of(&url);
        let keep = s.keep;
        let old = relay_pids_of(&da);
        s.run.stop(s.a);
        wait_gone(&old, "the host's relay and guard gone");
        let mut c: Child = Command::new(bin("coagent"))
            .args([
                "relay",
                "--listen",
                &format!("127.0.0.1:{port}"),
                "--status-secs",
                "0",
            ])
            .env_clear()
            .current_dir("/")
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .unwrap();
        std::thread::sleep(Duration::from_secs(3));
        let g = guest_status(s);
        assert_ne!(
            g["session"]["attached"], true,
            "I1 violated: the guest attached to an impostor relay (a fresh identity)"
        );
        let _ = c.kill();
        let _ = c.wait();
        restart_after_stop(s, keep);
    }

    fn restart_after_stop(s: &mut Seed, keep: bool) {
        s.keep = keep;
        s.run.start(s.a);
        s.run.status(s.a);
    }

    /// A TLS listener on the relay's port presenting the saved certificate with ANOTHER key.
    fn impostor_cert_no_key(s: &mut Seed) {
        let Some(good) = s.good.clone() else {
            return impostor_relay(s);
        };
        let da = s.run.dir(s.a);
        let port = port_of(&host_url(&da));
        let keep = s.keep;
        let old = relay_pids_of(&da);
        s.run.stop(s.a);
        wait_gone(&old, "the host's relay and guard gone");
        let cert = {
            let h = 26;
            let cl = u32::from_be_bytes(good[h..h + 4].try_into().unwrap()) as usize;
            good[h + 4..h + 4 + cl].to_vec()
        };
        let stop = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
        let st2 = stop.clone();
        let th = std::thread::spawn(move || {
            let rt = tokio::runtime::Builder::new_current_thread()
                .enable_all()
                .build()
                .unwrap();
            rt.block_on(async move {
                let other = rcgen::KeyPair::generate().unwrap();
                let der = rustls::pki_types::PrivateKeyDer::Pkcs8(
                    rustls::pki_types::PrivatePkcs8KeyDer::from(other.serialize_der()),
                );
                let provider = std::sync::Arc::new(rustls::crypto::ring::default_provider());
                let signer = provider.key_provider.load_private_key(der).unwrap();
                let ck = std::sync::Arc::new(rustls::sign::CertifiedKey::new(
                    vec![rustls::pki_types::CertificateDer::from(cert)],
                    signer,
                ));
                #[derive(Debug)]
                struct Fixed(std::sync::Arc<rustls::sign::CertifiedKey>);
                impl rustls::server::ResolvesServerCert for Fixed {
                    fn resolve(
                        &self,
                        _: rustls::server::ClientHello<'_>,
                    ) -> Option<std::sync::Arc<rustls::sign::CertifiedKey>> {
                        Some(self.0.clone())
                    }
                }
                let cfg = rustls::ServerConfig::builder_with_provider(provider)
                    .with_safe_default_protocol_versions()
                    .unwrap()
                    .with_no_client_auth()
                    .with_cert_resolver(std::sync::Arc::new(Fixed(ck)));
                let acc = tokio_rustls::TlsAcceptor::from(std::sync::Arc::new(cfg));
                let l = tokio::net::TcpListener::bind(("127.0.0.1", port))
                    .await
                    .unwrap();
                while !st2.load(std::sync::atomic::Ordering::SeqCst) {
                    if let Ok(Ok((sock, _))) =
                        tokio::time::timeout(Duration::from_millis(200), l.accept()).await
                    {
                        let acc = acc.clone();
                        tokio::spawn(async move {
                            let _ = tokio::time::timeout(Duration::from_secs(5), acc.accept(sock))
                                .await;
                        });
                    }
                }
            });
        });
        std::thread::sleep(Duration::from_secs(3));
        let g = guest_status(s);
        assert_ne!(
            g["session"]["attached"], true,
            "I1 violated: the guest attached to an endpoint presenting its pinned certificate without the key"
        );
        stop.store(true, std::sync::atomic::Ordering::SeqCst);
        th.join().unwrap();
        restart_after_stop(s, keep);
    }

    fn paste(s: &mut Seed, kind: LineKind) -> bool {
        let gs = guest_status(s);
        if gs["session"].is_null() || gs["session"]["ended"] == true {
            return false;
        }
        record_line(s);
        let gsid = gs["session"]["session_id"]
            .as_str()
            .unwrap_or_default()
            .to_string();
        let line: Option<String> = match kind {
            LineKind::Current => status_of(&s.run.dir(s.a))["relay_moved_line"]
                .as_str()
                .map(str::to_string),
            LineKind::Stale => s
                .lines
                .iter()
                .rev()
                .filter(|(sid, _)| *sid == gsid)
                .nth(1)
                .map(|(_, l)| l.clone()),
            LineKind::OtherSession => s
                .lines
                .iter()
                .find(|(sid, _)| *sid != gsid)
                .map(|(_, l)| l.clone()),
            LineKind::Stranger => {
                let sid = SessionId::from_hex(&gsid).unwrap();
                let rm = coagent_daemon::invite::RelayMoved {
                    session_id: sid,
                    relays: vec![coagent_daemon::store::RelayCandidate {
                        url: "wss://127.0.0.1:9/v1".into(),
                        pin: hex::encode([s.rng.next() as u8; 32]),
                    }],
                };
                Some(coagent_daemon::invite::line(&rm.to_blob().unwrap()).to_string())
            }
            LineKind::Garbage => Some("coagent join zzzz-not-a-blob".into()),
        };
        let Some(line) = line else { return false };
        let r = ctl(&s.g.dir, "join", json!({ "blob": line }));
        let names_session = match kind {
            LineKind::Garbage => false,
            LineKind::Stranger => true,
            _ => {
                s.lines.iter().any(|(sid, l)| *l == line && *sid == gsid)
                    || (kind == LineKind::Current)
            }
        };
        if r["ok"] == true {
            assert!(
                names_session,
                "I1 violated: a {kind:?} line that does not name the guest's session was accepted"
            );
            s.guest_pin = guest_status(s)["session"]["relays"][0]["pin"]
                .as_str()
                .unwrap_or_default()
                .to_string();
        } else {
            assert!(
                !names_session || kind == LineKind::Garbage,
                "a {kind:?} line naming the guest's session was refused: {r}"
            );
        }
        true
    }

    fn one_step(s: &mut Seed, st: RStep) -> bool {
        let da = s.run.dir(s.a);
        let active = status_of(&da)["session"]["ended"] == false;
        match st {
            RStep::Restart { keep, clean } => restart(s, keep, clean),
            RStep::ChildCrash => match relay_pid(&da) {
                Some(p) => {
                    signal(p, "-KILL");
                    std::thread::sleep(Duration::from_millis(1500));
                }
                None => return false,
            },
            RStep::GuardCrash => match (relay_pid(&da), guard_pid(&da)) {
                (Some(_), Some(g)) => {
                    signal(g, "-KILL");
                    std::thread::sleep(Duration::from_millis(2000));
                }
                _ => return false,
            },
            RStep::StartFails => {
                let Some(p) = relay_pid(&da) else {
                    return false;
                };
                let off = s.side.join("cg.off");
                std::fs::rename(&s.prog, &off).unwrap();
                signal(p, "-KILL");
                wait_until("R6's clock armed", Duration::from_secs(30), || {
                    let h = status_of(&da);
                    h["relay"].is_null() && h["relay_identity"]["retry_in_s"].is_u64()
                });
                std::fs::rename(&off, &s.prog).unwrap();
                std::thread::sleep(Duration::from_millis(1500));
            }
            // The race needs the end to reach the host, so both sides connected; otherwise the
            // step is the ordinary end below.
            RStep::SessionEnd {
                by_host: false,
                race: true,
            } if active
                && status_of(&da)["session"]["connected"] == true
                && guest_status(s)["session"]["connected"] == true =>
            {
                // RR-1: the guest's end on another thread; the host's invite in a tight loop.
                let applied_before = host_log(s).matches(APPLIED_BY_COMMAND).count();
                let gdir = s.g.dir.clone();
                let ender = std::thread::spawn(move || {
                    std::thread::sleep(Duration::from_millis(300));
                    ctl(&gdir, "end", json!({}))
                });
                let t0 = Instant::now();
                let inv = loop {
                    let r = ctl(&da, "invite", json!({}));
                    if r["ok"] == true || r["error"]["code"] != "session_active" {
                        break r;
                    }
                    assert!(
                        t0.elapsed() < Duration::from_secs(20),
                        "no invite accepted within 20 s of the guest's end: {r}\n{:?}",
                        s.log
                    );
                };
                assert_eq!(ender.join().unwrap()["ok"], true, "the guest's end");
                s.last_end = Some(false);
                if inv["ok"] != true {
                    // Refused (a refused saved file): the pair stays ended until a later step
                    // puts it right, as after any end.
                    return true;
                }
                s.race_reach.0 += 1;
                if host_log(s).matches(APPLIED_BY_COMMAND).count() > applied_before {
                    s.race_reach.1 += 1;
                }
                joined_session(s, inv);
            }
            RStep::SessionEnd { by_host, .. } => {
                if !active {
                    return false;
                }
                if by_host {
                    ctl(&da, "end", json!({}));
                } else {
                    ctl(&s.g.dir, "end", json!({}));
                }
                s.last_end = Some(by_host);
                // The other side learns it over the link; a side that is detached does not, and its
                // owner ends it (new_session does that for the guest).
                wait_until("the ending side ended", Duration::from_secs(20), || {
                    let h = status_of(&da)["session"]["ended"] == true;
                    let g = guest_status(s)["session"]["ended"] == true;
                    (if by_host { h } else { g }) && (!h || relay_pid(&da).is_none())
                });
                if status_of(&da)["session"]["ended"] != true {
                    std::thread::sleep(Duration::from_secs(2));
                    if status_of(&da)["session"]["ended"] != true {
                        ctl(&da, "end", json!({}));
                        wait_until("the host's session ended", Duration::from_secs(20), || {
                            status_of(&da)["session"]["ended"] == true && relay_pid(&da).is_none()
                        });
                    }
                }
                // A new invitation and pairing (refused while a saved file is refused: then the
                // pair stays ended until a later step puts it right).
                new_session(s);
            }
            RStep::FileCut | RStep::FileFlip | RStep::FileGrow => {
                let Some(good) = s.good.clone() else {
                    return false;
                };
                let mut b = good.clone();
                match st {
                    RStep::FileCut => b.truncate(s.rng.below(good.len() as u64) as usize),
                    RStep::FileFlip => {
                        let p = s.rng.below(good.len() as u64) as usize;
                        b[p] ^= 1 << (p % 8);
                    }
                    _ => b.resize(16 * 1024 + 1, 0),
                }
                replace_with(s, &b, 0o600);
                s.damaged = true;
            }
            RStep::FileMode => {
                if snap_file(&file(s)).is_none() || s.good.is_none() {
                    return false;
                }
                let good = s.good.clone().unwrap();
                replace_with(s, &good, 0o644);
                s.damaged = true;
            }
            RStep::FileLink => {
                let Some(good) = s.good.clone() else {
                    return false;
                };
                let target = s.side.join("good.key");
                let _ = std::fs::remove_file(&target);
                std::fs::write(&target, &good).unwrap();
                std::fs::set_permissions(&target, std::fs::Permissions::from_mode(0o600)).unwrap();
                let tmp = s.side.join("link");
                let _ = std::fs::remove_file(&tmp);
                std::os::unix::fs::symlink(&target, &tmp).unwrap();
                std::fs::rename(&tmp, file(s)).unwrap();
                s.damaged = true;
            }
            RStep::FileOtherValid => {
                use coagent_daemon::datadir::DataDir;
                use coagent_daemon::store::FileStore;
                use std::os::unix::fs::{DirBuilderExt, MetadataExt};
                let d = s.side.join(format!("v{}", s.rng.next() % 1_000_000));
                std::fs::DirBuilder::new().mode(0o700).create(&d).unwrap();
                let uid = std::fs::metadata(&d).unwrap().uid();
                let st = FileStore::new(DataDir::open(&d, uid).unwrap());
                st.create_relay_identity(
                    &coagent_daemon::relay_child::RelayIdentity::generate().unwrap(),
                )
                .unwrap();
                let b = std::fs::read(d.join(ID_FILE)).unwrap();
                replace_with(s, &b, 0o600);
                s.good = Some(b);
                s.damaged = false;
            }
            RStep::FileMoveAway => {
                if snap_file(&file(s)).is_none() {
                    return false;
                }
                let aside = s.side.join(format!("aside{}", s.rng.next() % 1_000_000));
                std::fs::rename(file(s), aside).unwrap();
                s.damaged = false;
            }
            RStep::FilePutBack => {
                let Some(good) = s.good.clone() else {
                    return false;
                };
                replace_with(s, &good, 0o600);
                s.damaged = false;
            }
            RStep::GuestWait => std::thread::sleep(Duration::from_secs(3)),
            RStep::Paste(kind) => return paste(s, kind),
            RStep::ImpostorRelay => {
                if !active {
                    return false;
                }
                impostor_relay(s)
            }
            RStep::ImpostorCertNoKey => {
                if !active {
                    return false;
                }
                impostor_cert_no_key(s)
            }
        }
        true
    }

    fn new_session(s: &mut Seed) {
        let da = s.run.dir(s.a);
        let inv = ctl(&da, "invite", json!({}));
        if inv["ok"] != true {
            return;
        }
        joined_session(s, inv);
    }

    /// The host's stderr (the real process).
    fn host_log(s: &Seed) -> String {
        String::from_utf8_lossy(&std::fs::read(&s.run.daemons[s.a].stderr).unwrap_or_default())
            .to_string()
    }

    /// I6 for an accepted invitation `inv`, then the guest joins it and the pair connects.
    fn joined_session(s: &mut Seed, inv: Value) {
        let da = s.run.dir(s.a);
        // I6: the relay started for this invitation still runs several ticks later.
        let inv_relay = relay_pid(&da);
        std::thread::sleep(Duration::from_millis(600));
        assert!(
            inv_relay.is_some() && relay_pid(&da) == inv_relay && alive(inv_relay.unwrap()),
            "I6 violated: the relay started for this invitation was stopped because of an earlier session's end\n{:?}",
            s.log
        );
        match s.last_end {
            Some(true) => s.reach.1 += 1,
            Some(false) => s.reach.0 += 1,
            None => {}
        }
        let line = inv["result"]["line"].as_str().unwrap().to_string();
        // A guest that never heard the end (it was detached) still holds its session: its owner
        // ends it before joining the new one.
        let gs = guest_status(s);
        if !gs["session"].is_null() && gs["session"]["ended"] != true {
            ctl(&s.g.dir, "end", json!({}));
            wait_until(
                "the guest's old session ended",
                Duration::from_secs(20),
                || guest_status(s)["session"]["ended"] == true,
            );
        }
        let j = ctl(&s.g.dir, "join", json!({ "blob": line }));
        assert_eq!(j["ok"], true, "{j}");
        wait_connected_dirs(&da, &s.g.dir);
        // I6: and the new session's relay (the invitation's) still runs after pairing.
        std::thread::sleep(Duration::from_millis(600));
        assert!(
            relay_pid(&da) == inv_relay,
            "I6 violated: the new session's relay was stopped because of an earlier session's end\n{:?}",
            s.log
        );
        if s.last_end.take().is_some() {
            s.reach.2 += 1;
        }
        let g = guest_status(s);
        s.guest_pin = g["session"]["relays"][0]["pin"]
            .as_str()
            .unwrap()
            .to_string();
        s.guest_sid = g["session"]["session_id"].as_str().unwrap().to_string();
        if s.keep {
            if let Some((b, _)) = snap_file(&file(s)) {
                s.good = Some(b);
            }
        }
    }

    /// I5: bring the host to the identity the guest pins (the good file back, the setting on if the
    /// guest pins the saved one, a pasted current line otherwise, a new session if it ended), then
    /// connected again within 120 s.
    fn settle(s: &mut Seed) {
        let da = s.run.dir(s.a);
        if s.damaged {
            if let Some(good) = s.good.clone() {
                replace_with(s, &good, 0o600);
            }
            s.damaged = false;
        }
        if status_of(&da)["session"]["ended"] == true || guest_status(s)["session"]["ended"] == true
        {
            new_session(s);
        }
        if status_of(&da)["session"]["ended"] == true {
            panic!("I5: no session could be made again: {:?}", s.log);
        }
        // Wait for the host's relay (R6 retries), then compare pins.
        wait_until("the host's relay runs", Duration::from_secs(90), || {
            relay_pid(&da).is_some()
        });
        let hp = host_pin(&da);
        let gp = guest_status(s)["session"]["relays"][0]["pin"]
            .as_str()
            .unwrap_or_default()
            .to_string();
        let hu = host_url(&da);
        let gu = guest_status(s)["session"]["relays"][0]["url"]
            .as_str()
            .unwrap_or_default()
            .to_string();
        if hp != gp || hu != gu {
            match status_of(&da)["relay_moved_line"]
                .as_str()
                .map(str::to_string)
            {
                Some(line) => {
                    let r = ctl(&s.g.dir, "join", json!({ "blob": line }));
                    assert_eq!(r["ok"], true, "{r}");
                    s.guest_pin = hp;
                }
                None => {
                    // The guest followed a line to a relay that is not the host's (a stranger's or
                    // a stale one) and the host's relay never moved: only a new invitation helps.
                    ctl(&da, "end", json!({}));
                    wait_until("ended", Duration::from_secs(20), || {
                        status_of(&da)["session"]["ended"] == true
                    });
                    new_session(s);
                }
            }
        }
        let t0 = Instant::now();
        wait_until(
            "I5: connected again within 120 s of the last step",
            Duration::from_secs(120),
            || {
                status_of(&da)["session"]["connected"] == true
                    && guest_status(s)["session"]["connected"] == true
            },
        );
        s.log.push(format!("settled in {:?}", t0.elapsed()));
    }

    /// Returns (I6 reach, RR-1 race reach).
    pub fn seed(n: u64) -> ((u64, u64, u64), (u64, u64)) {
        let mut rng = Rng::new(0xB0B_2026_1120 ^ n);
        let mut run = Run::new(&format!("rrq{n}"));
        let side = run.root.join("side");
        std::fs::create_dir(&side).unwrap();
        std::fs::set_permissions(&side, std::fs::Permissions::from_mode(0o700)).unwrap();
        let prog = side.join("cg");
        std::os::unix::fs::symlink(bin("coagent"), &prog).unwrap();
        let keep = rng.coin();
        let mut args = vec!["--coagent", prog.to_str().unwrap()];
        if keep {
            args.push("--keep-relay-identity");
        }
        let a = run.daemon("a", &args);
        let g = InProc::start(&mut run, "g", None, |c| {
            c.backoff_min = Duration::from_millis(100);
            c.backoff_max = Duration::from_millis(500);
            c.recovery.bucket_size = 1000;
            c.recovery.bucket_refill = Duration::from_millis(50);
        });
        let mut s = Seed {
            run,
            a,
            g,
            keep,
            prog,
            side,
            good: None,
            damaged: false,
            guest_pin: String::new(),
            guest_sid: String::new(),
            lines: vec![],
            rng,
            log: vec![format!("seed {n}, start keep={keep}")],
            last_end: None,
            reach: (0, 0, 0),
            race_reach: (0, 0),
        };
        new_session(&mut s);
        let mut executed = 0;
        let mut tries = 0;
        let mut race5_tried = false;
        while executed < 10 && tries < 200 {
            tries += 1;
            // The third executed step is a session end (I6's reach); the others are generated.
            let st = if executed == 2 {
                // Odd seeds: the guest ends while the host invites (RR-1's race).
                RStep::SessionEnd {
                    by_host: n.is_multiple_of(2),
                    race: !n.is_multiple_of(2),
                }
            } else if executed == 5 && !race5_tried {
                // Every seed: RR-1's race once more (addendum 5); one try only (no session at
                // that point: the step does not run, and a generated step follows).
                race5_tried = true;
                RStep::SessionEnd {
                    by_host: false,
                    race: true,
                }
            } else {
                gen(&mut s.rng)
            };
            let pre = snap_file(&file(&s));
            let src_before = status_of(&s.run.dir(s.a))["relay_identity"]["source"]
                .as_str()
                .unwrap_or_default()
                .to_string();
            let keep_before = s.keep;
            let done = one_step(&mut s, st);
            if !done {
                continue;
            }
            executed += 1;
            s.log
                .push(format!("{st:?} (keep {keep_before} -> {})", s.keep));
            record_line(&mut s);
            // The file's state right after the test's own action is the reference for I2/I3.
            let reference = match st {
                RStep::FileCut
                | RStep::FileFlip
                | RStep::FileGrow
                | RStep::FileMode
                | RStep::FileLink
                | RStep::FileOtherValid
                | RStep::FileMoveAway
                | RStep::FilePutBack => snap_file(&file(&s)),
                _ => pre,
            };
            // The host creates the saved file when there is none and the setting is on: that is
            // the one allowed write; take it as the new good file.
            if s.keep && reference.is_none() {
                if let Some((b, _)) = snap_file(&file(&s)) {
                    s.good = Some(b);
                    continue;
                }
            }
            let what = format!("{st:?}");
            check(&mut s, &what, &reference, &src_before);
        }
        assert!(executed >= 10, "seed {n}: only {executed} steps executed");
        settle(&mut s);
        eprintln!(
            "rr_property (b): seed {n}: I6 reach {:?}; RR-1 race reach (raced invitations, applied before the tick) {:?}; {:?}",
            s.reach, s.race_reach, s.log
        );
        let reach = (s.reach, s.race_reach);
        let Seed { run, g, .. } = s;
        g.stop();
        run.finish();
        reach
    }

    /// Run seeds and assert I6's reach counts over them.
    pub fn seeds(r: std::ops::Range<u64>) {
        let mut t = (0, 0, 0);
        let mut rt = (0, 0);
        for n in r.clone() {
            let (x, y) = seed(n);
            t = (t.0 + x.0, t.1 + x.1, t.2 + x.2);
            rt = (rt.0 + y.0, rt.1 + y.1);
        }
        eprintln!("rr_property (b): seeds {r:?}: I6 reach (after a peer end, after an own end, paired) = {t:?}; RR-1 race reach (raced invitations, applied before the tick) = {rt:?}");
        assert!(
            rt.0 > 0,
            "reach: an invitation raced against the guest's end"
        );
        assert!(t.0 > 0, "reach: an invitation after a peer end");
        assert!(t.1 > 0, "reach: an invitation after an own end");
        assert!(
            t.2 > 0,
            "reach: a pair completed on an invitation after an end"
        );
    }
}

#[test]
fn qrr2_property_b_my_seeds_4241_to_4243() {
    real::seeds(4241..4244);
}
#[test]
fn qrr2_property_b_my_seeds_4244_to_4246() {
    real::seeds(4244..4247);
}
