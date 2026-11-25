//! QA-POLICY-NOTES D-B (independent check): the OWNER origin, main `f193620` against the head `b6af26c` (and the old
//! item-1 head `535b017` as the control). Same generator as D-A (`qpn_gen`). Per action: the hook JSON and the scan
//! words (the action is D-A-identical, so its scan words are the same in every tree); per decision: `decide`'s Debug,
//! then five owner columns: no view, `StillAsk` bound, `Allowed` bound, `Allowed` bound elsewhere (`sess-other`),
//! `Allowed` bound to nobody; "=" when the column's Debug equals `decide`'s, else its Debug and text. The ONLY
//! per-tree difference is `qpn_adapter/mod.rs` (the entry point's signature). The comparator `cmp_db.py` computes every
//! item predicate itself from the hook JSON, the scan words and the state names printed here.
mod qpn_adapter;
mod qpn_gen;
use coagent_policy::*;
use qpn_gen::*;
use std::collections::BTreeSet;
use std::io::Write;

fn cols() -> Vec<(&'static str, Option<OwnerAllow>)> {
    let o = |s: &[&str], t: TerminalCommands| OwnerAllow {
        bound_sessions: s.iter().map(|x| x.to_string()).collect::<BTreeSet<_>>(),
        terminal: t,
    };
    vec![
        ("none", None),
        ("still", Some(o(&[SESSION], TerminalCommands::StillAsk))),
        ("allowed", Some(o(&[SESSION], TerminalCommands::Allowed))),
        ("elsewhere", Some(o(&["sess-other"], TerminalCommands::Allowed))),
        ("nobody", Some(o(&[], TerminalCommands::Allowed))),
    ]
}

#[test]
fn qpn_db() {
    let (seed, n, out_path) = seed_n_out();
    let fx = fixture();
    let paths = path_pool(&fx);
    let tools = tools();
    let sts = states(&fx);
    let cs = cols();
    let mut r = R(seed);
    let mut f = std::io::BufWriter::new(std::fs::File::create(&out_path).unwrap());
    let (mut cases, mut parse_err, mut owner_calls, mut panics) = (0usize, 0usize, 0usize, 0usize);
    writeln!(f, "seed {seed:#x} n {n} states {} paths {} tools {}", sts.len(), paths.len(), tools.len()).unwrap();
    for (i, (name, _)) in sts.iter().enumerate() {
        writeln!(f, "S{i} {name}").unwrap();
    }
    for i in 0..n {
        let Some((text, hi, a)) = hook_and_action(&mut r, &fx, &paths, &tools) else {
            parse_err += 1;
            writeln!(f, "A{i} PARSE-ERR").unwrap();
            continue;
        };
        writeln!(f, "A{i} HOOK {text}").unwrap();
        writeln!(f, "W {}", serde_json::to_string(&scan_words(&a)).unwrap()).unwrap();
        for _ in 0..5 {
            let si = r.below(sts.len());
            let mut st = sts[si].1.clone();
            with_approvals(&mut r, &mut st, &a, &fx);
            let surface = SURFACES[r.below(3)];
            let now = NOWS[r.below(NOWS.len())];
            cases += 1;
            let plain = match std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| decide(&a, &st, surface, now))) {
                Ok(d) => {
                    let s = format!("{d:?}");
                    writeln!(f, " s{si} {surface:?} {} D {s} TEXT {:?}", now.0, dtext(&d)).unwrap();
                    Some(s)
                }
                Err(_) => {
                    panics += 1;
                    writeln!(f, " s{si} {surface:?} {} D PANIC", now.0).unwrap();
                    None
                }
            };
            for (cn, m) in &cs {
                owner_calls += 1;
                let d = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                    qpn_adapter::owner(&a, &hi, &st, m.as_ref(), surface, now)
                }));
                match d {
                    Ok(d) => {
                        let s = format!("{d:?}");
                        if Some(&s) == plain.as_ref() {
                            writeln!(f, "  {cn} =").unwrap();
                        } else {
                            writeln!(f, "  {cn} {s} TEXT {:?}", dtext(&d)).unwrap();
                        }
                    }
                    Err(_) => {
                        panics += 1;
                        writeln!(f, "  {cn} PANIC").unwrap();
                    }
                }
            }
        }
    }
    writeln!(f, "cases {cases} owner_calls {owner_calls} parse_err {parse_err} panic {panics}").unwrap();
    eprintln!("QPN-DB seed {seed:#x}: decide {cases} owner {owner_calls} parse_err {parse_err} panic {panics}");
}
