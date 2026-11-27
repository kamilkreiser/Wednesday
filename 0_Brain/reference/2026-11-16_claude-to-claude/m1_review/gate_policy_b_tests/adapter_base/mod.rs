//! QA-POLICY-B adapter, BASE tree (5cab5e4): there is no scan B at the base.
pub const HEAD: bool = false;
pub fn scan_b(_windows: &[(String, bool)], _a: &[String]) -> Option<(Vec<String>, u64, bool)> {
    None
}
