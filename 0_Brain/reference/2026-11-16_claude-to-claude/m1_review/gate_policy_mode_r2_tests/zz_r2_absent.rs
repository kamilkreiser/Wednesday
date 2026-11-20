//! QA-POLICY-MODE-R2: every probe of zz_r2_inc/cases.rs decided with the mode ABSENT through `decide` only (API present
//! at main), so this one file compiles at main, fc7acfc and the head; the outputs must be byte-identical.
use coagent_policy::*;
include!("zz_r2_inc/cases.rs");

#[test]
fn qa_r2_absent() {
    let f = fx();
    let states = [state(&f, &[]), state(&f, &["**/.env*"])];
    let mut out = String::new();
    for (name, si, h, class) in cases(&f) {
        let line = match HookInput::parse(&h.to_string()) {
            Err(e) => format!("PARSE-ERR {e:?}"),
            Ok(hi) => {
                let a = classify(&hi, HostOs::Posix, &Env { home: f.home.clone() }, &PosixNormaliser);
                short(&decide(&a, &states[si], Surface::Console, NOW))
            }
        };
        out.push_str(&format!("{class} | {name} | {line}\n"));
    }
    let p = std::env::var("QA_OUT").expect("QA_OUT");
    std::fs::write(&p, &out).unwrap();
    eprintln!("QA-R2-ABSENT {} probes -> {p}", out.lines().count());
}
