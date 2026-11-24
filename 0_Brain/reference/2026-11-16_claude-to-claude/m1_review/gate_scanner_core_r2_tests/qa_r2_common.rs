//! QA-SCANNER-CORE-R2 shared helpers: the scanner at b0835a9 (old) beside the head (new).
#[path = "qa_old/mod.rs"]
#[allow(dead_code, unused, missing_docs)]
pub mod old;

/// family names a scan names, for the old and the new crate, as `Debug` strings
pub fn new_kinds(t: &str) -> Vec<String> {
    coagent_scanner::scan(t).findings().iter().map(|f| format!("{:?}", f.kind())).collect()
}
pub fn old_kinds(t: &str) -> Vec<String> {
    old::scan(t).findings().iter().map(|f| format!("{:?}", f.kind())).collect()
}
#[test]
fn qa_r2_harness_sanity() {
    assert_eq!(old_kinds("`--password hunter22`"), Vec::<String>::new());
    assert_eq!(new_kinds("`--password hunter22`"), vec!["PasswordArgument".to_string()]);
    assert_eq!(old_kinds("htpasswd -B .htpasswd qa"), vec!["PasswordArgument".to_string()]);
    assert!(new_kinds("htpasswd -B .htpasswd qa").is_empty());
}
