fn depends_on_policy(manifest: &str) -> bool {
    const NAME: &str = "coagent-policy";
    let unquote = |k: &str| -> String {
        let k = k.trim();
        for q in ['"', '\''] {
            if k.len() >= 2 && k.starts_with(q) && k.ends_with(q) {
                return k[1..k.len() - 1].to_string();
            }
        }
        k.to_string()
    };
    // a table header's keys, split at dots outside quotes
    let keys = |h: &str| -> Vec<String> {
        let (mut out, mut cur, mut quote) = (Vec::new(), String::new(), None::<char>);
        let mut esc = false;
        for c in h.chars() {
            if esc {
                esc = false;
                cur.push(c);
                continue;
            }
            match (quote, c) {
                (Some('"'), '\\') => {
                    esc = true;
                    cur.push(c);
                }
                (None, '.') => out.push(unquote(&std::mem::take(&mut cur))),
                (None, '"' | '\'') => {
                    quote = Some(c);
                    cur.push(c);
                }
                (Some(q), _) if c == q => {
                    quote = None;
                    cur.push(c);
                }
                _ => cur.push(c),
            }
        }
        out.push(unquote(&cur));
        out
    };
    let dep_table = |k: &str| {
        matches!(
            k,
            "dependencies"
                | "dev-dependencies"
                | "build-dependencies"
                | "dev_dependencies"
                | "build_dependencies"
        )
    };
    let after_blanks_is = |rest: &str, c: char| rest.trim_start().starts_with(c);
    // the text before the first `stop` outside quotes (a basic string's `\"` does not end it), if there is one
    let until_outside_quotes = |t: &str, stop: char| -> Option<String> {
        let (mut quote, mut esc) = (None::<char>, false);
        for (i, c) in t.char_indices() {
            if esc {
                esc = false;
                continue;
            }
            match (quote, c) {
                (Some('"'), '\\') => esc = true,
                (Some(q), _) if c == q => quote = None,
                (None, '"' | '\'') => quote = Some(c),
                (None, _) if c == stop => return Some(t[..i].to_string()),
                _ => {}
            }
        }
        None
    };
    // a dependency key path: `<table>.coagent-policy…` or `target.<x>.<table>.coagent-policy…`
    let dep_path = |k: &[String]| {
        (k.len() >= 2 && dep_table(&k[0]) && k[1] == NAME)
            || (k.len() >= 4 && k[0] == "target" && dep_table(&k[2]) && k[3] == NAME)
    };
    let first_header = manifest
        .lines()
        .position(|l| l.trim_start().starts_with('['))
        .unwrap_or(usize::MAX);
    manifest.lines().enumerate().any(|(line_no, l)| {
        let t = l.trim_start();
        // the old disjunct, unchanged
        if t.starts_with(NAME) {
            return true;
        }
        if t.starts_with('#') {
            return false;
        }
        // a table header (its closing `]` found outside quotes)
        if let Some(h) = t
            .strip_prefix('[')
            .and_then(|h| until_outside_quotes(h, ']'))
        {
            let h = h.as_str();
            if !t.starts_with("[[") {
                let k = keys(h);
                let n = k.len();
                if n >= 2
                    && k[n - 1] == NAME
                    && dep_table(&k[n - 2])
                    && (n == 2 || (n == 4 && k[0] == "target"))
                {
                    return true;
                }
            }
        }
        // a top-level dotted key, before any header
        if line_no < first_header {
            if let Some(k) = until_outside_quotes(t, '=') {
                if dep_path(&keys(&k)) {
                    return true;
                }
            }
        }
        // a quoted key
        for q in ["\"coagent-policy\"", "'coagent-policy'"] {
            if let Some(rest) = t.strip_prefix(q) {
                if after_blanks_is(rest, '=') || after_blanks_is(rest, '.') {
                    return true;
                }
            }
        }
        // package = "coagent-policy"
        let mut from = 0;
        while let Some(i) = t[from..].find("package") {
            let at = from + i;
            let before_ok = t[..at]
                .chars()
                .last()
                .is_none_or(|c| !(c.is_ascii_alphanumeric() || c == '_' || c == '-'));
            let mut rest = t[at + "package".len()..].trim_start();
            // a quoted key `"package"` / `'package'`: skip its closing quote
            if let Some(q @ ('"' | '\'')) = t[..at].chars().last() {
                if let Some(r) = t[at + "package".len()..].strip_prefix(q) {
                    rest = r.trim_start();
                }
            }
            if before_ok {
                if let Some(v) = rest.strip_prefix('=') {
                    let v = v.trim_start();
                    if v.starts_with("\"coagent-policy\"")
                        || v.starts_with("'coagent-policy'")
                        || v.starts_with("\"\"\"coagent-policy\"\"\"")
                        || v.starts_with("'''coagent-policy'''")
                    {
                        return true;
                    }
                }
            }
            from = at + "package".len();
        }
        false
    })
}

fn main() { let mut s = String::new(); std::io::Read::read_to_string(&mut std::io::stdin(), &mut s).unwrap(); println!("{}", depends_on_policy(&s)); }
