//! QA-SCANNER-NEXT (independent check), item 3: every NEW pin judged at the base and the head by my
//! own probe, the families of each over-flag, the "upper-case forms also flag through the assignment
//! family" claim (two copies of the head with the flag rule loosened), and two variants of my own per
//! form. Every value is made up.
macro_rules! m { ($name:ident, $p:literal) => {
    #[path = $p]
    #[allow(dead_code, unused, missing_docs, clippy::all)]
    mod $name;
}; }
m!(base, "qa_base/mod.rs");
m!(loose_case, "qa_loose_case/mod.rs");
m!(loose_b, "qa_loose_b/mod.rs");
#[path = "qa_t03_base.rs"]
#[allow(dead_code)]
mod t03b;
#[path = "t03_known_overflag.rs"]
#[allow(dead_code)]
mod t03h;

macro_rules! sig { ($m:path, $t:expr) => {{ use $m as mm; mm::scan($t).findings().iter().map(|f| (format!("{:?}", f.kind()), f.count())).collect::<Vec<(String, u32)>>() }}; }

fn new_of<'a>(head: &'a [(&'a str, &'a str)], base: &[(&str, &str)]) -> Vec<&'a (&'a str, &'a str)> {
    head.iter().filter(|h| !base.contains(h)).collect()
}

#[test]
fn p_new_pins() {
    // existing entries unchanged and in order: the base list is a prefix of the head list
    assert_eq!(&t03h::KNOWN_OVERFLAGS[..t03b::KNOWN_OVERFLAGS.len()], t03b::KNOWN_OVERFLAGS, "an existing over-flag pin changed");
    assert_eq!(&t03h::KNOWN_MISSES[..t03b::KNOWN_MISSES.len()], t03b::KNOWN_MISSES, "an existing miss pin changed");
    println!("PREFIX: base KNOWN_OVERFLAGS ({}) and KNOWN_MISSES ({}) are exact prefixes of the head lists", t03b::KNOWN_OVERFLAGS.len(), t03b::KNOWN_MISSES.len());
    let misses = new_of(t03h::KNOWN_MISSES, t03b::KNOWN_MISSES);
    let over = new_of(t03h::KNOWN_OVERFLAGS, t03b::KNOWN_OVERFLAGS);
    println!("NEW misses {} over-flags {}", misses.len(), over.len());
    let mut bad = 0;
    for (what, ex) in &misses {
        let (b, h) = (sig!(base, ex), sig!(coagent_scanner, ex));
        if !b.is_empty() || !h.is_empty() { bad += 1; }
        println!("MISS {what:<62} | {ex:?} | base {b:?} | head {h:?}");
    }
    for (what, ex) in &over {
        let (b, h) = (sig!(base, ex), sig!(coagent_scanner, ex));
        if b.is_empty() || h.is_empty() { bad += 1; }
        println!("OVER {what:<62} | {ex:?} | base {b:?} | head {h:?} | flag rule case-sensitive {:?} | form (b) off {:?}", sig!(loose_case, ex), sig!(loose_b, ex));
    }
    assert_eq!(bad, 0, "a new pin is not what its list says");
}

#[test]
fn p_docs_examples_and_variants() {
    // the docs' own examples (§4 bullet, §5 row) and two variants of mine per form
    let rows: &[(&str, &str, &str)] = &[
        // (form, expected per the docs, text)
        ("M(i) docs", "Clean", "[\"--password\",\n\"x\"]"),
        ("M(i) var: other flag, value", "Clean", "[\"--token\",\n  \"qatk0002\"]"),
        ("M(i) var: -u with colon, tab indent", "Clean", "[\"-u\",\n\t\"qa:zz0002\"]"),
        ("M(ii) docs", "Clean", "[\"--password\",\r\n\"x\"]"),
        ("M(ii) var: --secret", "Clean", "[\"--secret\",\r\n  \"qase0003\"]"),
        ("M(ii) var: CR alone after comma", "Clean", "[\"--password\",\r\"qapw0002\"]"),
        ("M(iii) docs", "Clean", "'--password' 'x'"),
        ("M(iii) var: double quotes, --token", "Clean", "\"--token\" \"qatk0002\""),
        ("M(iii) var: quoted flag, bare value", "Clean", "'--password' qapw0002"),
        ("M(iii) ctl: bare flag, quoted value (spaced rule)", "Flagged", "--password 'qapw0002'"),
        ("M(iv) docs", "Clean", "[\"mysql\", \"-p\", \"x\"]"),
        ("M(iv) var: mariadb", "Clean", "[\"mariadb\", \"-p\", \"qapw0002\"]"),
        ("M(iv) var: sshpass", "Clean", "[\"sshpass\", \"-p\", \"qapw0003\", \"ssh\"]"),
        ("M(iv) ctl: glued -p in argv", "?", "[\"mysql\", \"-pqapw0002\"]"),
        ("M(v) docs", "Clean", "\\\"--password\\\", \\\"x\\\""),
        ("M(v) var: --token", "Clean", "{\"a\": \"[\\\"--token\\\", \\\"qatk0002\\\"]\"}"),
        ("M(v) var: -u colon", "Clean", "{\"a\": \"[\\\"-u\\\", \\\"qa:zz0002\\\"]\"}"),
        ("M(vi) docs", "Clean", "--user= qa:x"),
        ("M(vi) var: -u= blank", "Clean", "-u= qa:zz0002"),
        ("M(vi) var: tab after =", "Clean", "--user=\tqa:qapw0002"),
        ("M(vii) docs", "Clean", "\"a\\u000a--password x\""),
        ("M(vii) var: \\u0009 and --token", "Clean", "{\"cmd\": \"a\\u0009--token qatk0002\"}"),
        ("M(vii) var: \\u000d and -u", "Clean", "{\"cmd\": \"a\\u000d-u qa:zz0002\"}"),
        ("O(i) docs", "Flagged", "--user=:"),
        ("O(i) var: -u=:", "Flagged", "-u=:"),
        ("O(i) var: --user=\":\"", "Flagged", "--user=\":\""),
        ("O(ii) docs -U=", "Flagged", "-U=qa:x"),
        ("O(ii) docs --USER=", "Flagged", "--USER=qa:x"),
        ("O(ii) var: -U=root:wheel", "Flagged", "-U=root:wheel"),
        ("O(ii) var: --User= mixed case", "Flagged", "--User=1000:1000"),
        ("O(ii) var: psql -U=", "Flagged", "psql -U=qa:zz0002 -h db"),
        ("O(iii) docs", "Flagged", "C:\\tools\\n-u qa:x"),
        ("O(iii) var: \\t folder, root:wheel", "Flagged", "C:\\t-u root:wheel"),
        ("O(iii) var: \\r folder, --password", "Flagged", "D:\\work\\r--password qapw0002"),
        ("O(iii) ctl: folder name longer", "?", "C:\\tools\\nightly-u qa:x"),
    ];
    let mut wrong = 0;
    for (form, want, t) in rows {
        let (b, h) = (sig!(base, t), sig!(coagent_scanner, t));
        let got = if h.is_empty() { "Clean" } else { "Flagged" };
        let ok = *want == "?" || *want == got;
        if !ok { wrong += 1; }
        println!("VAR {form:<44} | {t:?} | base {b:?} | head {h:?} | {}", if *want == "?" { "recorded" } else if ok { "as expected" } else { "NOT AS EXPECTED" });
        assert_eq!(b, h, "base and head differ on {t:?}");
    }
    println!("VARIANTS: {} rows, {wrong} not as expected", rows.len());
}

/// For the owner's card: what a loosened flag rule would also clear (made-up values).
#[test]
fn p_owner_card() {
    for t in ["curl -U qa:qapw0001 -x http://p:3128 https://h", "curl --proxy-user qa:qapw0001 https://h", "-U=qa:qapw0001", "--User=qa:qapw0001",
              "C:\\tools\\n--key-file id_rsa", "C:\\tools\\n-u root:wheel", "--user=:", "curl --user=qa:qapw0001 https://h"] {
        println!("CARD {:<52} | head {:?} | flag rule case-sensitive {:?} | form (b) off {:?}", format!("{t:?}"), sig!(coagent_scanner, t), sig!(loose_case, t), sig!(loose_b, t));
    }
}
