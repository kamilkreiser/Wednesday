// QA-POLICY-NEXT item 7: the header condition before (74dc861, nested ifs) and after (7677162, one `&&` chain), as
// written, over every case n = 0..=5 x last key NAME or not x second-last a dependency table or not x first "target" or not.
const NAME: &str = "coagent-policy";
fn dep_table(k: &str) -> bool { matches!(k, "dependencies" | "dev-dependencies" | "build-dependencies" | "dev_dependencies" | "build_dependencies") }
fn before(k: &[String]) -> bool {
    let n = k.len();
    if n >= 2 && k[n - 1] == NAME && dep_table(&k[n - 2]) {
        if n == 2 || (n == 4 && k[0] == "target") {
            return true;
        }
    }
    false
}
fn after(k: &[String]) -> bool {
    let n = k.len();
    if n >= 2
        && k[n - 1] == NAME
        && dep_table(&k[n - 2])
        && (n == 2 || (n == 4 && k[0] == "target"))
    {
        return true;
    }
    false
}
fn main() {
    let mut seen = std::collections::BTreeSet::new();
    let (mut total, mut same, mut trues) = (0, 0, 0);
    for n in 0..=5usize {
        for last in [true, false] { for second in [true, false] { for first in [true, false] {
            let mut k: Vec<String> = vec!["mid".to_string(); n];
            if n >= 1 { k[0] = if first { "target".into() } else { "x".into() }; }
            if n >= 2 { k[n - 2] = if second { "dependencies".into() } else { "y".into() }; }
            if n >= 1 { k[n - 1] = if last { NAME.into() } else { "other".into() }; }
            if !seen.insert(k.clone()) { continue; }
            let b = std::panic::catch_unwind(|| before(&k));
            let a = std::panic::catch_unwind(|| after(&k));
            total += 1;
            let (b, a) = (b.expect("before panicked"), a.expect("after panicked"));
            if a == b { same += 1; }
            if a { trues += 1; }
            println!("n={n} keys={k:?} before={b} after={a}");
        }}}
    }
    println!("DISTINCT CASES {total}; SAME {same}; true in {trues}; no panic in either");
}
