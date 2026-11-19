
// =================================================================================================
// QA3 (independent check of M3 AUDIT-FIX3). Appended to a copy of tests/fix_qam1_seat.rs at the
// head under test, compiled as tests/qa_fix3.rs in the checker's work copy only. Reuses that file's
// helpers (World, model, fits, resumed, ...). Fixtures generated here from `common`.
// =================================================================================================

/// Independent reference of every part of one seat (pb, pr), from the arithmetic alone (not the
/// crate's methods): seat, own seat, free part, one allowance, peer pool.
fn qa3_parts(pb: usize, pr: usize) -> [(usize, usize); 5] {
    let own = (pb.saturating_sub(pr), pr);
    let free = (own.0 / 2, own.1 / 2);
    let alw = ((own.0 - free.0) / 7, (own.1 - free.1) / 7);
    [(pb, pr), own, free, alw, (pb * 7, pr * 7)]
}

/// The cap as the brief words it, written here independently of the crate and of `capped`.
fn qa3_expected(l: StoreLimits) -> StoreLimits {
    let d = StoreLimits::default();
    let b = l.bytes.min(d.bytes);
    let r = l.records.min(d.records);
    let (db, dr) = (d.bytes / 8, d.records / 8);
    let (pb, pr) = (b / 8, r / 8);
    if pb.saturating_sub(pr) > db - dr {
        StoreLimits {
            bytes: (db - dr + pr) * 8,
            records: r,
        }
    } else {
        StoreLimits {
            bytes: b,
            records: r,
        }
    }
}

/// Item 1: every offer, boundary and adversarial (records 0, 1, 7, 8, below 8 per seat, bytes near
/// the usize limit, records above the defaults, bytes below records, not multiples of 8, random),
/// on a session with nothing owed: accepted; every part of what is installed at most the defaults'
/// part (by the crate's methods AND by an independent arithmetic); records kept (after the
/// component cap); bytes never raised; when lowered, the own seat's bytes exactly the defaults' (the
/// largest allowed); what is installed equals an independent model of the cap; re-offering what is
/// installed changes nothing (idempotent).
#[test]
fn qa3_every_offer_is_installed_at_or_below_the_defaults_in_every_part() {
    let w = World::new(0xD3, 8, 8);
    let mut v = w.audit(V, every(1_000_000));
    let d = StoreLimits::default();
    let (db, dr) = d.per_peer();
    let own_max = db - dr;
    let dp = qa3_parts(db, dr);
    let mut bytes: Vec<usize> = vec![
        0,
        1,
        7,
        8,
        9,
        15,
        16,
        4_127,
        8 * own_max - 1,
        8 * own_max,
        8 * own_max + 7,
        8 * own_max + 8,
        d.bytes * 2,
        usize::MAX / 8,
        usize::MAX - 7,
        usize::MAX - 1,
        usize::MAX,
    ];
    for k in 0..=17usize {
        bytes.push(d.bytes - k.min(d.bytes));
        bytes.push(d.bytes + k);
    }
    let mut records: Vec<usize> = (0..=17).collect();
    for k in 0..=17usize {
        records.push(d.records - k);
        records.push(d.records + k);
    }
    records.extend([d.records / 2, d.records * 3 / 4, 8 * 516, 8 * 516 - 1, usize::MAX - 1, usize::MAX]);
    let mut offers: Vec<StoreLimits> = Vec::new();
    for &b in &bytes {
        for &r in &records {
            offers.push(StoreLimits { bytes: b, records: r });
        }
    }
    // every record limit per seat, at default bytes and at usize::MAX bytes, both 8r and 8r+7
    for pr in 0..=dr + 1 {
        for b in [d.bytes, usize::MAX] {
            offers.push(StoreLimits { bytes: b, records: 8 * pr });
            offers.push(StoreLimits { bytes: b, records: 8 * pr + 7 });
        }
        // straddle the boundary in bytes for every pr: pb = own_max + pr - 1, +0, +1 (and +7 slack)
        for off in [-1i64, 0, 1] {
            let pb = (own_max + pr) as i64 + off;
            for slack in [0usize, 7] {
                offers.push(StoreLimits {
                    bytes: 8 * pb as usize + slack,
                    records: 8 * pr,
                });
            }
        }
    }
    // random, deterministic LCG
    let mut x: u64 = 0x9E37_79B9_7F4A_7C15;
    let mut next = || {
        x = x.wrapping_mul(6_364_136_223_846_793_005).wrapping_add(1_442_695_040_888_963_407);
        (x >> 11) as usize
    };
    for _ in 0..100_000 {
        let b = next() % (2 * d.bytes + 1);
        let r = next() % (2 * d.records + 1);
        offers.push(StoreLimits { bytes: b, records: r });
    }
    let (mut lowered, mut same, mut bytes_below_records) = (0usize, 0usize, 0usize);
    for l in &offers {
        let tr = v.try_set_limits(*l);
        let got = v.limits();
        assert_eq!(tr, Ok(()), "{l:?} refused with nothing owed");
        let want = qa3_expected(*l);
        assert_eq!(got, want, "QA3: offer {l:?} installed {got:?}, independent model {want:?}");
        if let Some(why) = above_defaults(got) {
            panic!("QA3: offer {l:?} installed {got:?}: {why}");
        }
        let (pb, pr) = (got.bytes / 8, got.records / 8);
        for (i, (p, q)) in qa3_parts(pb, pr).iter().zip(dp.iter()).enumerate() {
            assert!(
                p.0 <= q.0 && p.1 <= q.1,
                "QA3: offer {l:?} installed {got:?}: part {i} {p:?} above the defaults' {q:?}"
            );
        }
        assert_eq!(got.records, l.records.min(d.records), "records not kept: {l:?}");
        assert!(got.bytes <= l.bytes.min(d.bytes), "bytes raised: {l:?} -> {got:?}");
        if got.bytes < l.bytes.min(d.bytes) {
            lowered += 1;
            assert_eq!(got.own_reserved().0, own_max, "lowered below the largest allowed: {l:?}");
            assert_eq!(got.bytes % 8, 0);
        } else {
            same += 1;
        }
        if l.bytes / 8 < l.records / 8 {
            bytes_below_records += 1;
        }
        // idempotent: re-offering what is installed changes nothing
        assert_eq!(v.try_set_limits(got), Ok(()));
        assert_eq!(v.limits(), got, "re-offer of {got:?} changed it");
    }
    eprintln!(
        "qa3 sweep: {} offers, {lowered} lowered, {same} not lowered, {bytes_below_records} with \
         bytes per seat below records per seat; all at or below the defaults in every part",
        offers.len()
    );
}

/// Fill one member's space under limits `l` (records-only lowerings and others) by tiny or large
/// requests from requesters `req` and own events, until refused; then return the session.
fn qa3_fill(w: &World, l: StoreLimits, req: &[usize], big: bool, own_events: bool) -> SessionAudit<MemStore> {
    let mut v = w.audit(V, every(1_000_000));
    assert_eq!(v.try_set_limits(l), Ok(()));
    let mut n = 0u64;
    let s = "q".repeat(3_000);
    if own_events {
        while n < 20_000 && v.record(&w.ids[V], if big { inp(&s) } else { tiny() }, t(n)).is_ok() {
            n += 1;
        }
    }
    for &g in req {
        let mut k = 0;
        while k < 20_000
            && v
                .record_for(&w.ids[V], &w.key(g), if big { inp(&s) } else { tiny() }, t(n))
                .is_ok()
        {
            n += 1;
            k += 1;
        }
        // then tiny ones to fill the remainder
        while k < 40_000 && v.record_for(&w.ids[V], &w.key(g), tiny(), t(n)).is_ok() {
            n += 1;
            k += 1;
        }
    }
    v
}

/// Items 3 and 3's second half: for offers across the record range (default bytes, record limit per
/// seat from 8 to the defaults'), with the allowances (and the free part) filled by tiny and by
/// large requests from one and from several requesters: (a) before any restart the owed checkpoint
/// has room under the limits INSTALLED (the clamp strands nothing); (b) after `resume` and
/// `resume_with_anchor` (defaults) the owed checkpoint is `Ok` and covers the newest own event;
/// (c) on another resumed copy the defaults are accepted, and the original offer is accepted again
/// and installed exactly as before the restart.
#[test]
fn qa3_no_restart_strands_an_owed_checkpoint_after_any_accepted_offer() {
    let d = StoreLimits::default();
    let (_, dr) = d.per_peer();
    let mut lines = Vec::new();
    let mut cases = 0usize;
    let mut owed_cases = 0usize;
    let mut alw_above_def_offered = 0usize;
    for (wi, pr) in [8usize, 9, 15, 16, 64, 516, 515, 2_000, dr / 4, dr / 2, dr * 3 / 4, dr - 1]
        .into_iter()
        .enumerate()
    {
        for (shape, req, big, own) in [
            ("tiny, one requester", vec![4usize], false, false),
            ("large, one requester", vec![4usize], true, false),
            ("tiny, seven requesters + own", vec![0usize, 2, 3, 4, 5, 6, 7], false, true),
        ] {
            // a large-shape fill of a big seat is slow in debug; keep the seven-requester shape to
            // the smaller seats
            if req.len() > 1 && pr > 2_000 {
                continue;
            }
            let w = World::new(0xE0 + wi as u8, 8, 8);
            let l = StoreLimits {
                bytes: d.bytes,
                records: 8 * pr,
            };
            if l.requested_allowance().0 > d.requested_allowance().0 {
                alw_above_def_offered += 1;
            }
            let v = qa3_fill(&w, l, &req, big, own);
            let inst = v.limits();
            let m = model(v.store(), &w.s, v.own().seq());
            cases += 1;
            if m.owing.is_empty() {
                lines.push(format!("pr {pr} {shape}: nothing owed (allowance records {:?})", inst.requested_allowance()));
                continue;
            }
            owed_cases += 1;
            // (a) before a restart, on a copy
            let mut a = resumed(&w, &v, false, every(1_000_000), 9_050_000).unwrap();
            assert_eq!(a.try_set_limits(l), Ok(()));
            assert_eq!(a.limits(), inst);
            let cp_a = a.checkpoint_now(&w.ids[V], t(9_050_001)).map(|h| h.author_seq);
            assert_eq!(cp_a, Ok(a.own().seq()), "QA3 (a): pr {pr} {shape}: stranded under the installed limits");
            for anchor in [false, true] {
                // (b)
                let mut r = resumed(&w, &v, anchor, every(1_000_000), 9_060_000).unwrap();
                assert_eq!(r.limits(), d);
                let cp = r.checkpoint_now(&w.ids[V], t(9_060_001)).map(|h| h.author_seq);
                assert_eq!(
                    cp,
                    Ok(r.own().seq()),
                    "QA3 (b): pr {pr} {shape} anchor {anchor}: owed {:?}, allowances {:?}, installed {inst:?}",
                    m.owing,
                    m.allow
                );
                // (c)
                let mut r2 = resumed(&w, &v, anchor, every(1_000_000), 9_070_000).unwrap();
                assert_eq!(r2.try_set_limits(d), Ok(()), "QA3 (c): defaults refused, pr {pr} {shape}");
                assert_eq!(r2.try_set_limits(l), Ok(()), "QA3 (c): own offer refused after resume, pr {pr} {shape}");
                assert_eq!(r2.limits(), inst);
                let cp2 = r2.checkpoint_now(&w.ids[V], t(9_070_001)).map(|h| h.author_seq);
                assert_eq!(cp2, Ok(r2.own().seq()));
            }
            lines.push(format!(
                "pr {pr} {shape}: installed {inst:?}, owing {:?}, payer usage {:?} of {:?} (defaults' {:?}); before-restart cp Ok; after resume/anchor cp Ok, defaults Ok, own offer Ok",
                m.owing,
                m.owing.iter().next().and_then(|s| m.allow.get(s)),
                inst.requested_allowance(),
                d.requested_allowance()
            ));
        }
    }
    for l in &lines {
        eprintln!("qa3 restart: {l}");
    }
    eprintln!("qa3 restart: {cases} cases, {owed_cases} with a checkpoint owed, {alw_above_def_offered} offers whose OFFERED allowance is above the defaults'");
    assert!(owed_cases > 10 && alw_above_def_offered > 10);
}

/// Item 3, the clamp itself: an allowance filled under the defaults to its last checkpoint's room,
/// then an offer with fewer records (installed lowered): accepted only if the owed checkpoint keeps
/// room under what is INSTALLED, and then it is stored; a refusal changes nothing.
#[test]
fn qa3_an_offer_installed_lower_than_offered_never_strands_the_payer_or_the_seat() {
    let d = StoreLimits::default();
    let (_, dr) = d.per_peer();
    let w = World::new(0xEE, 8, 8);
    let v0 = qa3_fill(&w, d, &[4], false, false);
    let mut out = Vec::new();
    for pr in [8usize, 515, 516, 2_000, dr / 2, dr - 1] {
        let mut v = resumed(&w, &v0, false, every(1_000_000), 9_080_000).unwrap();
        let l = StoreLimits { bytes: d.bytes, records: 8 * pr };
        let before = v.limits();
        let tr = v.try_set_limits(l);
        let inst = v.limits();
        if tr.is_err() {
            assert_eq!(inst, before, "a refusal changed the limits");
        } else {
            assert_eq!(inst, qa3_expected(l));
        }
        let cp = v.checkpoint_now(&w.ids[V], t(9_080_001)).map(|h| h.author_seq);
        assert_eq!(cp, Ok(v.own().seq()), "QA3: pr {pr}: {tr:?}, installed {inst:?}, checkpoint {cp:?}");
        out.push(format!("pr {pr}: {tr:?} installed {inst:?} checkpoint {cp:?}"));
    }
    eprintln!("qa3 clamp strand: {}", out.join("; "));
}
