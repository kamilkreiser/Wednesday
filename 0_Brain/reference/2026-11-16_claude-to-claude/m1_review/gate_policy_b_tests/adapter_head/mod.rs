//! QA-POLICY-B adapter, HEAD tree (cd7b6fd): scan B's own figures through the head's public `shell::scan_free_text`.
pub const HEAD: bool = true;
pub fn scan_b(windows: &[(String, bool)], a: &[String]) -> Option<(Vec<String>, u64, bool)> {
    let b = coagent_policy::shell::scan_free_text(
        windows,
        a,
        coagent_policy::action::MAX_FREE_PIECES,
        coagent_policy::action::MAX_FREE_WORK,
    );
    Some((b.pieces, b.work, b.over))
}
