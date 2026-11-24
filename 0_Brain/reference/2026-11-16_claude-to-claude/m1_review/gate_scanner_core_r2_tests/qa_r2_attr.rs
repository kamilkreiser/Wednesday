//! QA-SCANNER-CORE-R2: every text the round turned from flagged to Clean (and every family it lost),
//! attributed by reverting ONE change of the round at a time in a copy of the head:
//!   ansi = the stripped view keeps `ESC [ … final` (item 3 reverted)
//!   lf   = only `\n` ends a line for the line shapes (item 2's line ends reverted)
//!   htp  = the htpasswd letters lower-cased again (item 5 reverted)
//!   m3   = the format list without this round's additions (item 4 reverted)
//!   all4 = all four reverted at once
#[path = "qa/gen.rs"]
mod gen;
#[path = "qa_r2_gen.rs"]
mod r2gen;
#[path = "qa_old/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod old;
#[path = "qa_var_ansi/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod v_ansi;
#[path = "qa_var_lf/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod v_lf;
#[path = "qa_var_htp/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod v_htp;
#[path = "qa_var_m3/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod v_m3;
#[path = "qa_var_all4/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
mod v_all4;
use std::collections::BTreeMap;

macro_rules! kinds { ($m:path, $t:expr) => {{ use $m as m; m::scan($t).findings().iter().map(|f| format!("{:?}", f.kind())).collect::<Vec<String>>() }}; }

fn attribute(t: &str, k: &str) -> String {
    let mut who = vec![];
    if kinds!(v_ansi, t).iter().any(|x| x == k) { who.push("ansi"); }
    if kinds!(v_lf, t).iter().any(|x| x == k) { who.push("lf"); }
    if kinds!(v_htp, t).iter().any(|x| x == k) { who.push("htp"); }
    if kinds!(v_m3, t).iter().any(|x| x == k) { who.push("m3"); }
    if who.is_empty() {
        if kinds!(v_all4, t).iter().any(|x| x == k) { who.push("only-all4"); } else { who.push("UNATTRIBUTED"); }
    }
    who.join("+")
}

fn run(label: &str, n: usize, seed: u64, mk: &dyn Fn(&mut gen::Rng, usize) -> String) {
    let mut r = gen::Rng::new(seed);
    let mut whole_by: BTreeMap<String, usize> = BTreeMap::new();
    let mut fam_by: BTreeMap<String, usize> = BTreeMap::new();
    for i in 0..n {
        let t = mk(&mut r, i);
        let a = kinds!(old, &t);
        if a.is_empty() { continue; }
        let b = kinds!(coagent_scanner, &t);
        let lost: Vec<&String> = a.iter().filter(|k| !b.contains(k)).collect();
        if lost.is_empty() { continue; }
        let mut whys = vec![];
        for k in &lost {
            let why = attribute(&t, k);
            *fam_by.entry(format!("{k} <- {why}")).or_default() += 1;
            if why.contains("UNATTRIBUTED") || why.contains("only-all4") {
                println!("ATTR ODD {label} case {i} | {k} {why} | {t:?}");
            }
            whys.push(format!("{k}:{why}"));
        }
        if b.is_empty() {
            let key = whys.join(",");
            *whole_by.entry(key.clone()).or_default() += 1;
            if !key.split(',').all(|w| w.ends_with(":htp")) {
                println!("ATTR WHOLE {label} case {i} | {key} | {t:?}");
            }
        }
    }
    println!("ATTR {label}: WHOLE by cause {whole_by:?}");
    println!("ATTR {label}: family losses by cause {fam_by:?}");
}

#[test]
fn r2_attribution() {
    run("gen-r1seed", 200_000, 0x0a5c_0ffe_e5ee_d001, &|r, i| gen::text(r, if i % 10 == 0 { 40 } else { 8 }));
    run("gen-r2seed", 100_000, 0x0e2c_0ffe_e5ee_d002, &|r, i| gen::text(r, if i % 10 == 0 { 40 } else { 8 }));
    run("rich", 250_000, 0x0e2c_0ffe_e5ee_d003, &|r, _| r2gen::rich_text(r));
    run("pem-window", 60_000, 0x0e2c_0ffe_e5ee_d004, &|r, _| r2gen::pem_header_text(r));
}

/// each complete `ESC [ … final` replaced by one space (the text as a reader would separate it)
fn space_csi(t: &str) -> String {
    let b = t.as_bytes();
    let mut out = Vec::with_capacity(b.len());
    let mut i = 0;
    while i < b.len() {
        if b[i] == 0x1B && b.get(i + 1) == Some(&b'[') {
            let mut k = i + 2;
            while k < b.len() && (0x30..=0x3F).contains(&b[k]) { k += 1; }
            while k < b.len() && (0x20..=0x2F).contains(&b[k]) { k += 1; }
            if k < b.len() && (0x40..=0x7E).contains(&b[k]) { out.push(b' '); i = k + 1; continue; }
        }
        out.push(b[i]);
        i += 1;
    }
    String::from_utf8(out).unwrap()
}

#[test]
fn r2_ansi_losses_judged() {
    let mut r = gen::Rng::new(0x0e2c_0ffe_e5ee_d003);
    let (mut real, mut artefact, mut no_fmt) = (0, 0, 0);
    let mut real_by: BTreeMap<String, usize> = BTreeMap::new();
    for i in 0..250_000 {
        let t = r2gen::rich_text(&mut r);
        let a = kinds!(old, &t);
        if a.is_empty() { continue; }
        let b = kinds!(coagent_scanner, &t);
        for k in a.iter().filter(|k| !b.contains(k)) {
            if !kinds!(v_ansi, &t).iter().any(|x| x == k) { continue; }
            if !t.chars().any(old::is_format_char) { no_fmt += 1; println!("ANSI NOFMT case {i} {k} | {t:?}"); }
            let sp = space_csi(&t);
            if kinds!(old, &sp).iter().any(|x| x == k) {
                real += 1;
                *real_by.entry(k.clone()).or_default() += 1;
                if real <= 25 { println!("ANSI REAL case {i} {k} | new {:?} | {t:?}", b); }
            } else {
                artefact += 1;
                if artefact <= 8 { println!("ANSI ARTEFACT case {i} {k} | {t:?}"); }
            }
        }
    }
    println!("ANSI JUDGED: family losses from the CSI removal: real shape (old still finds it when each code is a space) {real} {real_by:?}; artefact (old match used the code's own bytes) {artefact}; losses in a text WITHOUT an old-list format character {no_fmt}");
}
