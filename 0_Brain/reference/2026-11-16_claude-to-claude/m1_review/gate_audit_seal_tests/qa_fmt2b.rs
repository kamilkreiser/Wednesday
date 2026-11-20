//! QA gate M3-AUDIT-SEAL: format-2 bytes from FIXED inputs. Events carry random salts, so two
//! scenario runs never give the same bytes; instead every bundle written by the base 36537eb
//! (`qa_fmt2.rs`, $QA_IN) is parsed and re-exported with `export_records` from its own records by
//! the exporter's fixed test identity, on this tree. Re-exports are written to $QA_OUT and must
//! equal the input byte for byte; each input must also verify on this tree.
mod common;

use coagent_audit::bundle::{export_records, verify, Bundle};
use common::*;

#[test]
fn qa_fmt2_reexport_is_byte_identical() {
    let input = std::env::var("QA_IN").expect("QA_IN");
    let out = std::env::var("QA_OUT").expect("QA_OUT");
    let w = World::new(10, 3, 3);
    let mut n = 0;
    for e in std::fs::read_dir(&input).unwrap() {
        let p = e.unwrap().path();
        let name = p.file_name().unwrap().to_string_lossy().to_string();
        let i: usize = name.trim_end_matches(".bin").rsplit('_').next().unwrap().parse().unwrap();
        let bytes = std::fs::read(&p).unwrap();
        let b = Bundle::parse(&bytes).unwrap();
        verify(&b).unwrap_or_else(|e| panic!("qa fmt2b: {name} does not verify here: {e:?}"));
        let mut recs = b.unsealed_records();
        recs.remove(0); // the meta record: export_records makes its own
        let again = export_records(&w.ids[i], b.meta.session_id, recs).unwrap();
        let ab = again.encode().unwrap();
        std::fs::write(format!("{out}/re_{name}"), &ab).unwrap();
        assert!(ab == bytes, "qa fmt2b: {name} re-exported differs ({} vs {} bytes)", ab.len(), bytes.len());
        n += 1;
    }
    eprintln!("qa fmt2b: {n} bundles re-exported byte-identical");
    assert!(n >= 12);
}
