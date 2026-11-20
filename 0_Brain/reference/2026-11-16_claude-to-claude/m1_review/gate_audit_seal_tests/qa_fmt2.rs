//! QA gate M3-AUDIT-SEAL (independent check): format-2 bundles byte for byte. Runs unchanged at the
//! base 36537eb and at the head 841c445; writes each export's bytes to $QA_OUT so the two trees can
//! be compared with shasum. Test code only; fixed test identities, in-memory stores.
mod common;

use common::*;

#[test]
fn qa_fmt2_exports_written() {
    let out = std::env::var("QA_OUT").expect("QA_OUT");
    for n_a in [1u64, 4, 7, 12] {
        let (w, audits) = scenario(n_a);
        for i in 0..3 {
            let b = export(&w, &audits, i);
            assert_eq!(b.meta.format, 2, "qa fmt2: a plain store exports format 2");
            let bytes = b.encode().unwrap();
            std::fs::write(format!("{out}/fmt2_{n_a}_{i}.bin"), &bytes).unwrap();
            coagent_audit::bundle::verify(&b).unwrap();
        }
    }
}
