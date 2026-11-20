//! QA-POLICY-MODE-R2: every probe of zz_r2_inc/cases.rs decided three ways (mode absent via decide_with_mode(None) and
//! checked equal to decide; mode live with the shell NOT verified; mode live with the shell verified). Compiles at
//! fc7acfc and the head. With QA_ASSERT=1 (the head): an "M1" or "N3" probe must never be a mode allow.
use coagent_policy::*;
include!("zz_r2_inc/cases.rs");

fn mode(sh: bool) -> BypassView {
    BypassView {
        consent_set_id: "cs-r2".into(),
        expires_at: Timestamp(NOW.0 + 3600),
        bound_sessions: [S.to_string()].into_iter().collect(),
        shell_verified: sh,
    }
}

#[test]
fn qa_r2_probes() {
    let f = fx();
    let states = [state(&f, &[]), state(&f, &["**/.env*"])];
    let assert_on = std::env::var("QA_ASSERT").is_ok();
    let mut out = String::new();
    let mut bad = Vec::new();
    let mut counts = std::collections::BTreeMap::<String, usize>::new();
    for (name, si, h, class) in cases(&f) {
        *counts.entry(class.to_string()).or_default() += 1;
        let line = match HookInput::parse(&h.to_string()) {
            Err(e) => format!("PARSE-ERR {e:?} (never reaches the policy)"),
            Ok(hi) => {
                let a = classify(&hi, HostOs::Posix, &Env { home: f.home.clone() }, &PosixNormaliser);
                let st = &states[si];
                let plain = decide(&a, st, Surface::Console, NOW);
                let none = decide_with_mode(&a, st, None, Surface::Console, NOW);
                assert_eq!(plain, none, "decide != decide_with_mode(None) for {name}");
                let mut cols = vec![short(&plain)];
                for sh in [false, true] {
                    for surface in [Surface::Console, Surface::TerminalPrompt, Surface::None] {
                        let d = decide_with_mode(&a, st, Some(&mode(sh)), surface, NOW);
                        if (class == "M1" || class == "N3") && matches!(d, Decision::Allow { .. }) {
                            bad.push(format!("{name} (shell verified {sh}, {surface:?}): {}", short(&d)));
                        }
                        if surface == Surface::Console {
                            cols.push(short(&d));
                        }
                    }
                }
                cols.join(" || ")
            }
        };
        out.push_str(&format!("{class} | {name} | {line}\n"));
    }
    let p = std::env::var("QA_OUT").expect("QA_OUT");
    std::fs::write(&p, &out).unwrap();
    eprintln!("QA-R2-PROBES {counts:?}; mode allows on M1/N3 probes: {}", bad.len());
    for b in &bad {
        eprintln!("QA-R2-BAD {b}");
    }
    if assert_on {
        assert!(bad.is_empty(), "QA-R2: {} M1/N3 probes were mode-allowed", bad.len());
    }
}
