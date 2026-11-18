
// QA CHECK ADD-ON (independent check of M3 AUDIT-FIX2; not part of the tree): the recogniser on
// the state where N1 and the resume-defaults state hold TOGETHER. Conditions (i) and (ii) hold,
// (iii) does not (the limits before the restart are refused: N1), so the property would FAIL here
// (correctly: the carve-out is not wider), and the docs' caller remedy does not end the state.
#[test]
fn qa_check_recogniser_on_n1_plus_resume_defaults() {
    let mut w = World::new(0xC1, 10, 6);
    let pol = every(1_000_000);
    let mut v = w.audit(V, pol);
    let d = StoreLimits::default();
    let (bd, _) = d.per_peer();
    let l = small(bd - 20_000, 2_000);
    assert_eq!(v.try_set_limits(l), Ok(()));
    for i in 0..3u64 {
        v.record(&w.ids[V], inp("own"), t(i)).unwrap();
    }
    let h = w.key(3);
    let mut n = 10u64;
    for size in [4_000usize, 2_000, 1_000, 300, 100, 30, 10, 1] {
        let f = "f".repeat(size);
        while v.record_for(&w.ids[V], &h, inp(&f), t(n)).is_ok() {
            n += 1;
        }
    }
    let mut x = AuthorChain::new(&w.ids[2], w.s, pol, Box::new(PatternRedactor), t(0));
    let mut xi = 0u64;
    'x: for size in [40_000usize, 10_000, 3_000] {
        loop {
            let f = "x".repeat(size);
            if x.append(&w.ids[2], input("x", "s", &f), t(100 + xi)).is_err() {
                continue 'x;
            }
            xi += 1;
            if v.receive(&w.ids[V], x.event(xi).unwrap(), t(100 + xi)).is_err() {
                break 'x;
            }
        }
    }
    for ro in [w.remove(2), w.remove(V), w.add(V, 2)] {
        v.apply_roster(&ro).unwrap();
    }
    let r = resumed(&w, &v, false, pol, 6_000).unwrap();
    let at_cp = resume_defaults_state(&w, &r, d, Some(l), Refusal::Checkpoint(3), pol, 6_001);
    let at_lim = resume_defaults_state(&w, &r, d, Some(l), Refusal::LimitsAfterResume, pol, 6_001);
    eprintln!("qa check recogniser on N1 + resume-defaults: checkpoint {at_cp:?}; limits {at_lim:?}");
    assert!(matches!(&at_cp, Err(e) if e.starts_with("(iii)")));
    assert!(matches!(&at_lim, Err(e) if e.starts_with("(iii)")));
}
