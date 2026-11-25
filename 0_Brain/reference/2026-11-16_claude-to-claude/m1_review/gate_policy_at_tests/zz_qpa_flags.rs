//! QA-POLICY-AT item 7 (n-5): the check's own instrumented copy. The SAME file in a tree at the base and one at the
//! head; each uses ITS OWN `owner_common::generated_actions` (t26's seed and count) and `corpus`. Writes, per generated
//! item, its tool, cwd and sandbox-flag value, and the action's Debug with the flag, the input hash and
//! `sandbox_disabled` masked (so two draws are comparable); then t26's case -> item mapping for chosen cases (t26's own
//! loop: `ai, si, vi, fi` drawn from `Gen(SEED)` in that order).
#![cfg(unix)]
mod bypass_common;
mod common;
mod owner_common;
use bypass_common::*;
use coagent_policy::*;
use owner_common::*;
use std::io::Write;

#[test]
fn qpa_flags() {
    let out = std::env::var("QPA_FLAGS_OUT").expect("QPA_FLAGS_OUT");
    let fx = mode_fixture("qpa-flags");
    let root = fx.root.to_str().unwrap().to_string();
    let corpus_len = corpus(&fx).len();
    let items = generated_actions(&fx, 0x0A11_0E0E_2026_1123, 4_000);
    let mut f = std::io::BufWriter::new(std::fs::File::create(&out).unwrap());
    writeln!(f, "CORPUS {corpus_len}").unwrap();
    let flag_re = |s: &str| -> String {
        // mask the flag's value inside the debug text of the raw input
        let mut s = s.to_string();
        for v in ["true", "false", "\\\"true\\\"", "\\\"false\\\"", "1", "0", "null", "{}"] {
            s = s.replace(&format!("\\\"dangerouslyDisableSandbox\\\":{v}"), "\\\"dangerouslyDisableSandbox\\\":<F>");
        }
        s
    };
    for (i, it) in items.iter().enumerate() {
        let (cwd, flag) = it.hook_raw.as_ref().unwrap();
        let a = &it.action;
        // the DRAW signature: only what comes straight from the generated hook (no scan-derived target)
        let sig: Vec<String> = a
            .targets
            .iter()
            .filter_map(|t| match t {
                Target::Command { text, shell, .. } => Some(format!("Command({shell:?}): {text}")),
                Target::Raw { input } => Some(format!("Raw: {input}")),
                Target::Query { text } => Some(format!("Query: {text}")),
                Target::Url { url, .. } => Some(format!("Url: {url}")),
                Target::Tool { server, tool } => Some(format!("Tool: {server:?} {tool}")),
                Target::Path { role, path } if !matches!(role, PathRole::Mentioned | PathRole::InText) => {
                    Some(format!("Path({role:?}): {path:?}"))
                }
                _ => None,
            })
            .collect();
        let sig = flag_re(&format!(
            "{} | {} | {:?} | {:?} | {:?} | {:?}",
            a.tool_name, cwd, a.kind, sig, a.share_flagged, a.origin
        ))
        .replace(&root, "<root>");
        writeln!(
            f,
            "ITEM\t{i}\t{}\t{}\t{}\t{}",
            a.tool_name.replace('\t', " "),
            cwd.replace(&root, "<root>"),
            flag.as_ref().map(|v| v.to_string()).unwrap_or_else(|| "absent".into()),
            sig.replace('\n', "\\n").replace('\t', "\\t")
        )
        .unwrap();
    }
    // t26's case -> item mapping (its loop draws ai, si, vi, fi from Gen(SEED) for every case, in this order)
    let n_items = corpus_len + items.len();
    let mut g = Gen(0x0A11_0E0E_2026_1123);
    let want = [15usize, 30, 45, 207, 298, 374, 575, 685];
    for i in 0..=685usize {
        let ai = g.below(n_items);
        let si = g.below(owner_common::states(&fx).len());
        let vi = g.below(5);
        let fi = g.below(3);
        if want.contains(&i) {
            let gi = ai.checked_sub(corpus_len);
            writeln!(f, "CASE\t{i}\tai={ai}\tsi={si}\tvi={vi}\tfi={fi}\tgenerated_index={gi:?}").unwrap();
        }
    }
    f.flush().unwrap();
}
