//! QA-SCANNER-NOTES (independent check): two-head differentials, own harness.
//! main = f193620 (scratch module), head = the library at 430dde3, one-item-reverted copies of the head:
//!   r1 = main's lone-CR rule; r2 = main's one stripped view; r2_3v = three views (view 4 dropped);
//!   r3 = forms (a)-(c) off; all3 = r1+r2+r3; none = the head copied unchanged (control).
//! b0835a9 against the head, attributed by copies of the head with the r2 check's causes reverted:
//!   ansi (codes kept), lf (only \n ends a line), htp (htpasswd letters lower-cased), m3 (list additions removed).
//! Generated texts are made up. The texts printed here go to the work-dir log only, never to the verdict.
#[path = "qa/gen.rs"]
mod gen;
#[path = "qa_r2_gen.rs"]
mod r2gen;
macro_rules! m { ($name:ident, $p:literal) => {
    #[path = $p]
    #[allow(dead_code, unused, missing_docs, clippy::all)]
    mod $name;
}; }
m!(main, "qa_main/mod.rs");
m!(old, "qa_old/mod.rs");
m!(old_nonetrc, "qa_old_nonetrc/mod.rs");
m!(v_r1, "qa_v_r1/mod.rs");
m!(v_r2, "qa_v_r2/mod.rs");
m!(v_r2_3v, "qa_v_r2_3v/mod.rs");
m!(v_r3, "qa_v_r3/mod.rs");
m!(v_all3, "qa_v_all3/mod.rs");
m!(v_none, "qa_v_none/mod.rs");
m!(v_ansi, "qa_v_ansi/mod.rs");
m!(v_lf, "qa_v_lf/mod.rs");
m!(v_htp, "qa_v_htp/mod.rs");
m!(v_m3, "qa_v_m3/mod.rs");
use std::collections::BTreeMap;

macro_rules! sig { ($m:path, $t:expr) => {{ use $m as mm; mm::scan($t).findings().iter().map(|f| (format!("{:?}", f.kind()), f.count())).collect::<Vec<(String, u32)>>() }}; }
fn kinds(s: &[(String, u32)]) -> Vec<String> { s.iter().map(|x| x.0.clone()).collect() }
fn has(s: &[(String, u32)], k: &str) -> bool { s.iter().any(|x| x.0 == k) }

fn gen_text(r: &mut gen::Rng, i: usize) -> String { gen::text(r, if i % 10 == 0 { 40 } else { 8 }) }
fn rich_text(r: &mut gen::Rng, _i: usize) -> String { r2gen::rich_text(r) }

/// FR-6 shape: an escaped backslash (two backslashes) right before n/t/r and a `-`
fn fr6_shape(t: &str) -> bool { let b = t.as_bytes(); (3..b.len()).any(|i| b[i] == b'-' && matches!(b[i-1], b'n'|b't'|b'r') && b[i-2] == b'\\' && b[i-3] == b'\\') }

fn two_head(label: &str, n: usize, seed: u64, mk: &dyn Fn(&mut gen::Rng, usize) -> String) {
    let mut r = gen::Rng::new(seed);
    let (mut fm, mut fh, mut whole_loss, mut whole_gain, mut all3_ne, mut none_ne) = (0, 0, 0, 0, 0, 0);
    let mut loss_by: BTreeMap<String, usize> = BTreeMap::new();
    let mut gain_by: BTreeMap<String, usize> = BTreeMap::new();
    let mut gain_whole_by: BTreeMap<String, usize> = BTreeMap::new();
    let mut shown: BTreeMap<String, usize> = BTreeMap::new();
    let (mut fr6_texts, mut fr6_gain) = (0, 0);
    let mut unattributed = 0;
    for i in 0..n {
        let t = mk(&mut r, i);
        let a = sig!(main, &t);
        let b = sig!(coagent_scanner, &t);
        let c = sig!(v_all3, &t);
        if c != a { all3_ne += 1; if all3_ne <= 5 { println!("ALL3!=MAIN {label} case {i} main {a:?} all3 {c:?} | {t:?}"); } }
        if sig!(v_none, &t) != b { none_ne += 1; }
        if !a.is_empty() { fm += 1; }
        if !b.is_empty() { fh += 1; }
        let fr6 = fr6_shape(&t);
        if fr6 { fr6_texts += 1; }
        // losses
        let lost: Vec<String> = kinds(&a).into_iter().filter(|k| !has(&b, k)).collect();
        if !a.is_empty() && b.is_empty() { whole_loss += 1; println!("WHOLE LOSS {label} case {i} | {t:?}"); }
        for k in &lost {
            let mut who = vec![];
            if has(&sig!(v_r1, &t), k) { who.push("r1"); }
            if has(&sig!(v_r2, &t), k) { who.push("r2"); }
            if has(&sig!(v_r3, &t), k) { who.push("r3"); }
            if who.is_empty() { if has(&c, k) { who.push("only-all3"); } else { who.push("UNATTRIBUTED"); unattributed += 1; } }
            let key = format!("{k} <- {}", who.join("+"));
            println!("FAMILY LOSS {label} case {i} | {key} | {t:?}");
            *loss_by.entry(key).or_default() += 1;
        }
        // gains
        let gained: Vec<String> = kinds(&b).into_iter().filter(|k| !has(&a, k)).collect();
        if a.is_empty() && !b.is_empty() { whole_gain += 1; }
        let mut gw = vec![];
        for k in &gained {
            let mut who = vec![];
            if !has(&sig!(v_r1, &t), k) { who.push("r1"); }
            if !has(&sig!(v_r2, &t), k) { who.push("r2"); }
            if !has(&sig!(v_r3, &t), k) { who.push("r3"); }
            let w = if who.is_empty() { "combined".to_string() } else { who.join("+") };
            let key = format!("{k} <- {w}");
            if fr6 && w.contains("r3") { fr6_gain += 1; }
            let e = shown.entry(key.clone()).or_default();
            *e += 1;
            if *e <= 6 { println!("GAIN SAMPLE {label} case {i} | {key} | {t:?}"); }
            *gain_by.entry(key).or_default() += 1;
            gw.push(w);
        }
        if a.is_empty() && !b.is_empty() { gw.sort(); gw.dedup(); *gain_whole_by.entry(gw.join(",")).or_default() += 1; }
    }
    println!("DIFF {label}: {n} texts, seed {seed:#x}; flagged main {fm} -> head {fh}; WHOLE losses {whole_loss}; WHOLE gains {whole_gain}");
    println!("DIFF {label}: family losses by item {loss_by:?}; unattributed {unattributed}");
    println!("DIFF {label}: family gains by item {gain_by:?}");
    println!("DIFF {label}: whole gains by item {gain_whole_by:?}");
    println!("DIFF {label}: all three reverted != main (kinds+counts) on {all3_ne} texts; head copy != library on {none_ne}");
    println!("DIFF {label}: FR-6 shape (escaped backslash before n/t/r then -) in {fr6_texts} texts; PasswordArgument-type gains by r3 in such texts {fr6_gain}");
}

#[test]
fn n_a_gen() {
    two_head("gen", 200_000, 0x0a5c_0ffe_e5ee_d001, &gen_text);
    two_head("gen-own", 200_000, 0x5eed_0a11_c0de_0b07, &gen_text);
}
#[test]
fn n_a_rich() {
    two_head("rich", 250_000, 0x0e2c_0ffe_e5ee_d003, &rich_text);
    two_head("rich-own", 250_000, 0x5eed_0a11_c0de_0b08, &rich_text);
}

/// FRIDAY's answer (1): the losses of the three-view copy against main, each recovered at the head by view 4 alone.
#[test]
fn n_fr2_three_views() {
    for (label, n, seed, mk) in [("gen", 200_000usize, 0x0a5c_0ffe_e5ee_d001u64, &gen_text as &dyn Fn(&mut gen::Rng, usize) -> String),
                                 ("rich", 250_000, 0x0e2c_0ffe_e5ee_d003, &rich_text)] {
        let mut r = gen::Rng::new(seed);
        let (mut fam, mut whole, mut recovered, mut not_rec, mut other_cause) = (0, 0, 0, 0, 0);
        let mut by: BTreeMap<String, usize> = BTreeMap::new();
        for i in 0..n {
            let t = mk(&mut r, i);
            let a = sig!(main, &t);
            if a.is_empty() { continue; }
            let v = sig!(v_r2_3v, &t);
            let lost: Vec<String> = kinds(&a).into_iter().filter(|k| !has(&v, k)).collect();
            if lost.is_empty() { continue; }
            if v.is_empty() { whole += 1; }
            let h = sig!(coagent_scanner, &t);
            // the 3-view copy with r1 and r3 also reverted would isolate item 2; check r1/r3 do not explain it
            for k in &lost {
                fam += 1;
                *by.entry(k.clone()).or_default() += 1;
                if has(&h, k) { recovered += 1; } else { not_rec += 1; }
                if has(&sig!(v_r1, &t), k) && !has(&h, k) { other_cause += 1; }
                println!("FR2 LOSS {label} case {i} | {k} | head {} | {t:?}", if has(&h, k) {"recovered"} else {"NOT RECOVERED"});
            }
        }
        println!("FR2 {label}: three-view copy vs main: family losses {fam} (whole texts {whole}) {by:?}; recovered at head (= by view 4 alone, the only difference) {recovered}; not recovered {not_rec}; other {other_cause}");
    }
}

/// each complete `ESC [ … final` replaced by one space (the r2 check's real-shape method)
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

/// (b) b0835a9 against the head on the rich generator.
#[test]
fn n_b_regressions() {
    for (label, seed) in [("rich", 0x0e2c_0ffe_e5ee_d003u64), ("rich-own", 0x5eed_0a11_c0de_0b08)] {
        let mut r = gen::Rng::new(seed);
        let mut fam_by: BTreeMap<String, usize> = BTreeMap::new();
        let mut whole_by: BTreeMap<String, usize> = BTreeMap::new();
        let (mut lf_b64, mut ansi_real, mut ansi_art, mut lf_pw, mut lf_pw_netrc, mut lf_pw_other) = (0, 0, 0, 0, 0, 0);
        for i in 0..250_000 {
            let t = r2gen::rich_text(&mut r);
            let a = sig!(old, &t);
            if a.is_empty() { continue; }
            let b = sig!(coagent_scanner, &t);
            let lost: Vec<String> = kinds(&a).into_iter().filter(|k| !has(&b, k)).collect();
            if lost.is_empty() { continue; }
            let mut whys = vec![];
            for k in &lost {
                let mut who = vec![];
                for (nm, s) in [("ansi", sig!(v_ansi, &t)), ("lf", sig!(v_lf, &t)), ("htp", sig!(v_htp, &t)), ("m3", sig!(v_m3, &t)),
                                 ("r1", sig!(v_r1, &t)), ("r2", sig!(v_r2, &t)), ("r3", sig!(v_r3, &t))] {
                    if has(&s, k) { who.push(nm); }
                }
                let w = if who.is_empty() { "UNATTRIBUTED".to_string() } else { who.join("+") };
                if w.contains("UNATTRIBUTED") || who.iter().any(|x| x.starts_with('r')) { println!("REG ODD {label} case {i} | {k} <- {w} | {t:?}"); }
                if k == "Base64Lines" && who.contains(&"lf") { lf_b64 += 1; println!("REG LFB64 {label} case {i} | {t:?}"); }
                if who.contains(&"ansi") {
                    if has(&sig!(old, &space_csi(&t)), k) { ansi_real += 1; println!("REG ANSIREAL {label} case {i} {k} | {t:?}"); } else { ansi_art += 1; }
                }
                if k == "PasswordArgument" && who.contains(&"lf") {
                    lf_pw += 1;
                    // own method: b0835a9 without its netrc rule does not name PasswordArgument -> the old flag came from the netrc rule
                    if !has(&sig!(old_nonetrc, &t), k) { lf_pw_netrc += 1; } else { lf_pw_other += 1; println!("REG LFPW-NOT-NETRC {label} case {i} <- {w} | {t:?}"); }
                }
                *fam_by.entry(format!("{k} <- {w}")).or_default() += 1;
                whys.push(format!("{k}:{w}"));
            }
            if b.is_empty() { *whole_by.entry(whys.join(",")).or_default() += 1; }
        }
        println!("REG {label} b0835a9 -> head: WHOLE by cause {whole_by:?}");
        println!("REG {label} b0835a9 -> head: family losses by cause {fam_by:?}");
        println!("REG {label}: lf Base64Lines class {lf_b64}; ansi real-shape class {ansi_real}; ansi artefacts {ansi_art}");
        println!("REG {label}: lf PasswordArgument family losses {lf_pw}: old flag from its netrc rule only (old without netrc Clean for the family) {lf_pw_netrc}; other {lf_pw_other}");
    }
}
