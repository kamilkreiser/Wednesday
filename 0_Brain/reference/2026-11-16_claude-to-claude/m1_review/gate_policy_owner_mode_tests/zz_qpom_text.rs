//! QA-POLICY-OWNER-MODE item 8: the two owner texts byte for byte as ruled, display-safe, and the both-agree texts as
//! at the base, for every refused class (head 59de2d3).
use coagent_policy::*;

#[test]
fn qpom_texts() {
    let allow = AllowWhy::OwnerChoseAllow.text();
    assert_eq!(allow.as_bytes(), b"allowed: the owner chose ALLOW for this session");
    assert_eq!(coagent_policy::text::visible(&allow), allow);
    let mut lines = vec![format!("ALLOW {allow:?} len {}", allow.len())];
    for c in RefusedClass::ALL {
        let t = DenyReason::RefusedInAllow { reason: c.text() }.text();
        assert_eq!(t, format!("coagent: not allowed even in ALLOW mode: {}", c.text()));
        assert!(t.starts_with("coagent: not allowed even in ALLOW mode: "));
        assert_eq!(coagent_policy::text::visible(&t), t, "display-safe");
        for bad in ["both agree", "consent set", "approvals off"] {
            assert!(!t.contains(bad) && !allow.contains(bad));
        }
        let b = DenyReason::BypassRefused { reason: c.text() }.text();
        assert_eq!(b, format!("coagent: not allowed even with approvals off: {}", c.text()));
        lines.push(format!("{c:?} | {t} | {b}"));
    }
    let ba = AllowWhy::Bypass { consent_set_id: "cs-1".into() }.text();
    assert_eq!(ba, "allowed with approvals off (both agree; consent set cs-1)");
    lines.push(format!("BOTH-AGREE ALLOW {ba:?}"));
    std::fs::write(std::env::var("QPOM_TEXTS").unwrap(), lines.join("\n") + "\n").unwrap();
}
