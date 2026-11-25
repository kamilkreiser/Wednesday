//! QA-POLICY-NOTES D-A (independent check): MODE ABSENT equals main. A differential of `decide` (full Debug, every
//! text incl. card reason texts and option labels), `would_have_been` (Debug and reason texts) and `decide_with_mode`
//! under five both-agree views, between main `f193620` and the head `b6af26c`. Generator: `qpn_gen` (the owner-mode
//! check's, widened with every POLICY-NOTES input shape). Uses only API present at main, so the SAME file is compiled
//! in both trees. Every call in catch_unwind. Env: QA_SEED, QA_N, QA_OUT, QA_FX.
mod qpn_gen;
use coagent_policy::*;
use qpn_gen::*;
use std::io::Write;

fn views() -> Vec<(&'static str, BypassView)> {
    let v = |e: Timestamp, s: &[&str], sh: bool| BypassView {
        consent_set_id: "cs-qpn".into(),
        expires_at: e,
        bound_sessions: s.iter().map(|x| x.to_string()).collect(),
        shell_verified: sh,
    };
    vec![
        ("live", v(Timestamp(NOW.0 + 3600), &[SESSION], false)),
        ("live_shell", v(Timestamp(NOW.0 + 3600), &[SESSION, "x"], true)),
        ("expired", v(NOW, &[SESSION], true)),
        ("unbound", v(Timestamp(NOW.0 + 3600), &["sess-other"], true)),
        ("nobody", v(Timestamp(NOW.0 + 86_400 * 3), &[], true)),
    ]
}

fn kind(d: &Decision) -> String {
    match d {
        Decision::Allow { why } => format!("allow {:?}", why).split([' ', '{', '(']).take(2).collect::<Vec<_>>().join(" "),
        Decision::Ask { card } => format!("ask {:?}", card.tier),
        Decision::Deny { reason } => format!("deny {:?}", reason).split([' ', '{', '(']).take(2).collect::<Vec<_>>().join(" "),
    }
}

#[test]
fn qpn_da() {
    let (seed, n, out_path) = seed_n_out();
    let fx = fixture();
    let paths = path_pool(&fx);
    let tools = tools();
    let sts = states(&fx);
    let vs = views();
    let mut r = R(seed);
    let mut f = std::io::BufWriter::new(std::fs::File::create(&out_path).unwrap());
    let (mut cases, mut parse_err, mut mode_calls, mut panics) = (0usize, 0usize, 0usize, 0usize);
    let mut dist: std::collections::BTreeMap<String, usize> = Default::default();
    let mut mdist: std::collections::BTreeMap<String, usize> = Default::default();
    writeln!(f, "seed {seed:#x} n {n} states {} paths {} tools {}", sts.len(), paths.len(), tools.len()).unwrap();
    for (i, (name, _)) in sts.iter().enumerate() {
        writeln!(f, "S{i} {name}").unwrap();
    }
    for i in 0..n {
        let Some((_, _, a)) = hook_and_action(&mut r, &fx, &paths, &tools) else {
            parse_err += 1;
            writeln!(f, "A{i} PARSE-ERR").unwrap();
            continue;
        };
        writeln!(f, "A{i} {a:?}").unwrap();
        for _ in 0..5 {
            let si = r.below(sts.len());
            let mut st = sts[si].1.clone();
            with_approvals(&mut r, &mut st, &a, &fx);
            let surface = SURFACES[r.below(3)];
            let now = NOWS[r.below(NOWS.len())];
            let res = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| decide(&a, &st, surface, now)));
            let wh = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| would_have_been(&a, &st)));
            cases += 1;
            let plain = match res {
                Ok(d) => {
                    *dist.entry(kind(&d)).or_default() += 1;
                    let s = format!("{d:?}");
                    writeln!(
                        f,
                        " s{si} {surface:?} {} {s} TEXT {:?} WHB {:?} {:?}",
                        now.0,
                        dtext(&d),
                        wh.as_ref().ok(),
                        wh.as_ref().ok().map(|(_, rs)| rs.iter().map(|r| r.text()).collect::<Vec<_>>())
                    )
                    .unwrap();
                    Some(s)
                }
                Err(_) => {
                    panics += 1;
                    writeln!(f, " s{si} {surface:?} {} PANIC", now.0).unwrap();
                    None
                }
            };
            for (vn, v) in &vs {
                mode_calls += 1;
                let m = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| decide_with_mode(&a, &st, Some(v), surface, now)));
                match m {
                    Ok(m) => {
                        let s = format!("{m:?}");
                        if Some(&s) == plain.as_ref() {
                            writeln!(f, "  {vn} =").unwrap();
                        } else {
                            *mdist.entry(format!("{vn} {}", kind(&m))).or_default() += 1;
                            writeln!(f, "  {vn} {s} TEXT {:?}", dtext(&m)).unwrap();
                        }
                    }
                    Err(_) => {
                        panics += 1;
                        writeln!(f, "  {vn} PANIC").unwrap();
                    }
                }
            }
        }
    }
    for (k, v) in &dist {
        writeln!(f, "DIST decide {k} {v}").unwrap();
    }
    for (k, v) in &mdist {
        writeln!(f, "DIST mode-differs-from-decide {k} {v}").unwrap();
    }
    writeln!(f, "cases {cases} mode_calls {mode_calls} parse_err {parse_err} panic {panics}").unwrap();
    eprintln!("QPN-DA seed {seed:#x}: decide {cases} mode {mode_calls} parse_err {parse_err} panic {panics}");
    for (k, v) in &dist {
        eprintln!("DIST decide {k} {v}");
    }
    for (k, v) in &mdist {
        eprintln!("DIST mode-differs-from-decide {k} {v}");
    }
}
